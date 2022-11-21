import sqlite3
from sqlite3 import Error
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch(hosts = "http://@localhost:9200")
sCat = Search(using=client, index="cat_1")
sComp = Search(using=client, index="comp_1")
#sRev = Search(using=client, index="rev_1")

db_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/es_to_sqlite/project.db"


##### list for sectors ######
scanCat = [hit.to_dict() for hit in sCat.scan()]
listCat = []
for d in scanCat:
    for d2 in d.values():
        for l in d2.values():
            for d3 in l:
                parent_lname = d3["parentId"]
                child_lname = d3["categoryId"]
                child_dname = d3["displayName"]
                for subchild_lname in d3["childrenCategories"]:
                    listCat.append((parent_lname, child_lname, child_dname, subchild_lname))

##### list for companies ######
listComp = []
listLinkCompSectors = []
for hit in sComp.scan():
    for d in hit.to_dict()["businesses"]:
        listComp.append((
            d["businessUnitId"],
            d["identifyingName"],
            d["displayName"],
            d["trustScore"],
            d["logoUrl"],
            d["location"]["address"],
            d["location"]["city"],
            d["location"]["zipCode"],
            d["location"]["country"],
            d["contact"]["website"],
            d["contact"]["email"],
            d["contact"]["phone"]
            ))
        ######## list for link sectors_company ######
        for dd in d["categories"]:
            listLinkCompSectors.append((d["businessUnitId"], dd["categoryId"]))

####### list for reviews #########
"""
scanDictRev = [hit.to_dict() for hit in sRev.scan()][0]
listRev = [(
    scanDictRev["businessUnit"]["id"], x["id"], x["title"], x["text"],
    x["dates"]["experiencedDate"], x["dates"]["publishedDate"],
    x["rating"], x["labels"]["verification"]["isVerified"], x["consumer"]["id"],
    x["consumer"]["displayName"], x["consumer"]["numberOfReviews"],
    x["consumer"]["countryCode"],
    None if x["reply"] is None else x["reply"]["message"],
    None if x["reply"] is None else x["reply"]["publishedDate"]
    ) for x in scanDictRev["reviews"]]
"""




def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def insert_data_temp(conn, insert_sql, list_to_insert):
    """ insert data from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        c = conn.cursor()
        c.executemany(insert_sql, list_to_insert)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

def insert_data_perm(conn, insert_sql):
    """ insert data from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(insert_sql)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

def delete_data(conn, delete_sql):
    """ delete data from the delete_sql statement
    :param conn: Connection object
    :param delete_sql: a DELETE FROM statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(delete_sql)
        conn.commit()
    except Error as e:
        print(e)


def main():
    database = r"{}".format(db_path)

    ################# DELETE TEMP TABLES ######################
    sql_delete_temp_cat_table = """DELETE FROM ztemp_sectors;"""
    sql_delete_temp_company_table = """DELETE FROM ztemp_company;"""
    sql_delete_temp_review_table = """DELETE FROM ztemp_review;"""
    sql_delete_temp_lk_company_sectors_table = """DELETE FROM ztemp_lk_company_sectors"""

    ################# INSERT TEMP TABLES ######################
    sql_insert_temp_cat_table = """
    INSERT INTO ztemp_sectors (parent_label_name, child_label_name, child_display_name, subchild_label_name)
    VALUES (?, ?, ?, ?)
    ;"""

    sql_insert_temp_company_table = """
    INSERT INTO ztemp_company (
    businessUnitId, website, display_name,
    score, logoUrl, postal_address, postal_city, postal_zipCode, 
    postal_country, contact_website, contact_email, contact_phone
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ;"""

    sql_insert_temp_company_sectors_table = """
    INSERT INTO ztemp_lk_company_sectors (company_businessUnitId, subchild_label_name)
    VALUES (?, ?)
    ;"""

    sql_insert_temp_review_table = """
    INSERT INTO ztemp_review (
    businessUnitId, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ;"""

    ################# INSERT PERM TABLES ######################
    sql_insert_cat_table = """
    INSERT INTO sectors (parent_label_name, child_label_name, child_display_name, subchild_label_name)
    SELECT DISTINCT parent_label_name, child_label_name, child_display_name, subchild_label_name
    FROM ztemp_sectors
    WHERE (parent_label_name, child_label_name, child_display_name, subchild_label_name) 
        not in (select parent_label_name, child_label_name, child_display_name, subchild_label_name from sectors)
    ;"""

    sql_insert_company_table = """
    INSERT INTO company (
    businessUnitId, website, display_name,
    score, logoUrl, postal_address, postal_city, postal_zipCode, 
    postal_country, contact_website, contact_email, contact_phone
    )
    SELECT DISTINCT
    t1.businessUnitId, t1.website, t1.display_name,
    t1.score, t1.logoUrl, t1.postal_address, t1.postal_city, t1.postal_zipCode, 
    t1.postal_country, t1.contact_website, t1.contact_email, t1.contact_phone

    FROM ztemp_company t1

    WHERE t1.businessUnitId NOT IN (select businessUnitId from company)
    ;"""

    sql_insert_lk_company_sectors_table = """
    INSERT INTO link_company_sectors (company_id, sectors_id)
    SELECT c.id, s.id
    FROM ztemp_lk_company_sectors t
    LEFT JOIN company c on c.businessUnitId = t.company_businessUnitId
    LEFT JOIN sectors s on s.subchild_label_name = t.subchild_label_name
    LEFT JOIN link_company_sectors l on l.company_id = c.id and l.sectors_id = s.id
    WHERE (l.company_id is null or l.sectors_id is null)
    GROUP BY c.id, s.id
    """
    
    sql_insert_review_table = """
    INSERT INTO review (
    company_id, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date
    )
    SELECT DISTINCT
    t2.id, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date

    FROM ztemp_review t1
    LEFT JOIN company t2 ON t2.businessUnitId = t1.businessUnitId

    WHERE t1.reviewUnitId NOT IN (select reviewUnitId from review)
    ;"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:

        # delete temp tables
        delete_data(conn, sql_delete_temp_cat_table)
        delete_data(conn, sql_delete_temp_lk_company_sectors_table)
        delete_data(conn, sql_delete_temp_company_table)
        #delete_data(conn, sql_delete_temp_review_table)

        # insert temp tables
        insert_data_temp(conn, sql_insert_temp_cat_table, listCat)
        insert_data_temp(conn, sql_insert_temp_company_table, listComp)
        insert_data_temp(conn, sql_insert_temp_company_sectors_table, listLinkCompSectors)
        #insert_data_temp(conn, sql_insert_temp_review_table, listRev)

        # insert perm tables
        insert_data_perm(conn, sql_insert_cat_table)
        insert_data_perm(conn, sql_insert_company_table)    
        insert_data_perm(conn, sql_insert_lk_company_sectors_table)
        #insert_data_perm(conn, sql_insert_review_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()