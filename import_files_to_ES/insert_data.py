import sqlite3
from sqlite3 import Error
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch(hosts = "http://@localhost:9200")
sCat = Search(using=client, index="cat_1")
sComp = Search(using=client, index="comp_1")
sRev = Search(using=client, index="rev_1")


scanListCat = [hit.to_dict() for hit in sCat.scan()][0]["topCategories"]
listCat = [(x["categoryId"], x["displayName"]) for x in scanListCat]

scanDictSubCat = [hit.to_dict() for hit in sCat.scan()][0]["subCategories"]
listSubCat = []
for key, value in scanDictSubCat.items():
    for d in value:
        listSubCat.append((d["parentId"], d["categoryId"], d["displayName"]))

scanListComp = [hit.to_dict() for hit in sComp.scan()][0]["businesses"]
listComp = [(
    x["businessUnitId"], x["identifyingName"], x["displayName"],
    x["trustScore"], x["logoUrl"], x["location"]["address"],
    x["location"]["city"], x["location"]["zipCode"], x["location"]["country"],
    x["contact"]["website"], x["contact"]["email"], x["contact"]["phone"]
    ) for x in scanListComp]

scanListRev = [hit.to_dict() for hit in sRev.scan()][0]
listRev = [(
    x["businessUnit"]["id"], x["reviews"]["id"], x["reviews"]["title"], x["reviews"]["text"],
    x["reviews"]["dates"]["experiencedDate"], x["reviews"]["dates"]["publishedDate"], x["reviews"]["text"],
    x["reviews"]["rating"], x["reviews"]["verification"]["isVerified"], x["reviews"]["consumer"]["id"],
    x["reviews"]["consumer"]["displayName"], x["reviews"]["consumer"]["numberOfReviews"],
    x["reviews"]["consumer"]["countryCode"], x["reviews"]["reply"]["message"], x["reviews"]["reply"]["publishedDate"]
    ) for x in scanListRev]





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
    except Error as e:
        print(e)

def insert_data_perm(conn, insert_sql):
    """ insert data from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        d = conn.cursor()
        d.execute(insert_sql)
    except Error as e:
        print(e)


def main():
    database = r"/home/ubuntu/sqlite/project.db"

    sql_insert_temp_cat_table = """
    INSERT INTO ztemp_sector (label_name, display_name)
    VALUES (?, ?)
    ;"""

    sql_insert_cat_table = """
    INSERT INTO sector (label_name, display_name)
    SELECT label_name, display_name from ztemp_sector
    WHERE label_name not in (select label_name from sector)
    ;"""

    sql_insert_temp_subCat_table = """
    INSERT INTO ztemp_subSectorLevel1 (sector_label_name, label_name, display_name)
    VALUES (?, ?, ?)
    ;"""

    sql_insert_subCat_table = """
    INSERT INTO subSectorLevel1 (sector_id, label_name, display_name)

    SELECT t2.sector_id, t1.label_name, t1.display_name 
    FROM ztemp_subSectorLevel1 t1
    LEFT JOIN sector t2 ON t2.label_name = t1.sector_label_name
    WHERE t1.label_name NOT IN
    (
        select label_name from subSectorLevel1
    )
    ;"""

    sql_insert_temp_company_table = """
    INSERT INTO ztemp_company (
    subSector1_label_name, businessUnitId, website, display_name,
    score, logoUrl, postal_address, postal_city, postal_zipCode, 
    postal_country, contact_website, contact_email, contact_phone
    )
    VALUES (?, ?, ?)
    ;"""

    sql_insert_company_table = """
    INSERT INTO company (
    subSectorLevel1_id, businessUnitId, website, display_name,
    score, logoUrl, postal_address, postal_city, postal_zipCode, 
    postal_country, contact_website, contact_email, contact_phone
    )
    SELECT
    t2.id, businessUnitId, website, display_name,
    score, logoUrl, postal_address, postal_city, postal_zipCode, 
    postal_country, contact_website, contact_email, contact_phone

    FROM ztemp_company t1
    LEFT JOIN subSectorLevel1 t2 ON t2.label_name = t1.subSector1_label_name

    WHERE t1.businessUnitId NOT IN (select businessUnitId from company)
    ;"""

    sql_insert_temp_review_table = """
    INSERT INTO ztemp_review (
    businessUnitId, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date
    )
    VALUES (?, ?, ?)
    ;"""
    
    sql_insert_review_table = """
    INSERT INTO review (
    company_id, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date
    )
    SELECT
    t2.id, reviewUnitId, review_title, review_text,
    experience_date, publish_date, rating, isVerified, user_id, 
    user_name, user_nbOfReviews, user_country, response_company,
    response_company_date

    FROM ztemp_review t1
    LEFT JOIN company t2 ON t2.label_name = t1.company_label_name

    WHERE t1.reviewUnitId NOT IN (select reviewUnitId from review)
    ;"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:

        # insert into temp cat table
        insert_data_temp(conn, sql_insert_temp_cat_table, listCat)

        # insert into cat table
        insert_data_perm(conn, sql_insert_cat_table)

        # insert into temp subCat table
        insert_data_temp(conn, sql_insert_temp_subCat_table, listSubCat)

        # insert into subCat table
        insert_data_perm(conn, sql_insert_subCat_table)

        # insert into temp company table
        insert_data_temp(sql_insert_temp_company_table, listComp)

        # insert into company table
        insert_data_perm(sql_insert_company_table)

        # insert into temp review table
        insert_data_temp(sql_insert_temp_review_table, listRev)

        # insert into review table
        insert_data_perm(sql_insert_review_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()