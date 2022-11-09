import sqlite3
from sqlite3 import Error
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch(hosts = "http://@localhost:9200")
s = Search(using=client, index="cat_1")

scanListCat = [hit.to_dict() for hit in s.scan()][0]["topCategories"]
listCat = str([(x["categoryId"], x["displayName"]) for x in scanListCat]).strip("[]")

scanDictSubCat = [hit.to_dict() for hit in s.scan()][0]["SubCategories"]
listSubCat = []
for key, value in scanDictSubCat.items():
    for d in value:
        listSubCat.append((d["parentId"], d["categoryId"], d["displayName"]))
strSubCat = str(listSubCat).strip("[]")



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


def insert_data(conn, insert_sql):
    """ insert date from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(insert_sql)
    except Error as e:
        print(e)


def main():
    database = r"/home/ubuntu/sqlite/project.db"

    sql_insert_cat_table = """
    INSERT INTO sector (label_name, display_name)
    SELECT * FROM
    (
        VALUES {}
    ) t1
    LEFT JOIN sector t2 ON t1.{} = t2.label_name
    WHERE t2.label_name is null
    ;""".format(listCat, scanListCat[0]["categoryId"])

    sql_insert_subCat_table = """
    INSERT INTO subSectorLevel1 (sector_id, label_name, display_name)
    SELECT t3.id, {}, {} FROM
    (
        VALUES {}
    ) t1
    LEFT JOIN subSectorLevel1 t2 on t2.label_name = t1.{}
    LEFT JOIN sector t3 ON t3.label_name = t1.{}
    WHERE t2.label_name is null
    ;""".format(listSubCat[0][1], listSubCat[0][2], strSubCat, listSubCat[0][0], listSubCat[0][0])


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # insert into cat table
        insert_data(conn, sql_insert_cat_table)

        # insert into subCat table
        insert_data(conn, sql_insert_subCat_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()