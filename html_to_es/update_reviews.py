import requests
import re
from custom_vars import vars
import os
from tqdm import tqdm
from elasticsearch import Elasticsearch
from custom_vars import vars

import sqlite3
from sqlite3 import Error
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

site_name = ["grandluxuryhotels.com", "hofesh.fr"]
list_status_code = []
database = "{db_path}".format(db_path=vars("db_path"))

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

def updateReviews(website_name):

    json_name = "reviews_update"

    # delete the review file if exsts
    if os.path.exists("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es"))):
        os.remove("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")))

    # append the review file
    for comp_name in tqdm(website_name):
        for num_page in tqdm(range(1,4), leave=False):
            if num_page == 1:
                suffix = ""
            else:
                suffix = "?page=" + str(num_page)

            doc_name = comp_name + "_" + str(num_page)
            urlRev = 'https://fr.trustpilot.com/review/{comp_name}{suffix}'.format(comp_name=comp_name, suffix=suffix)
            html_respRev = requests.get(url=urlRev, allow_redirects=False)
            list_status_code.append(html_respRev.status_code)
            if html_respRev.status_code == 200:
                html_substr_rev1 = re.findall('"reviews"\:.+\}\]\,"products"', html_respRev.text)[0]
                html_substr_rev = re.findall('"businessUnit"\:\{"id"\:"\w+"', html_respRev.text)[0] + '},' + html_substr_rev1
                html_rev = r'{"create":{"_index":"rev_1","_id":' + '"{doc_name}"}}\n'.format(doc_name=doc_name) +'{' + html_substr_rev[:-11] + '}\n'

                with open("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")), "a", encoding='utf-8') as file:
                    file.write(html_rev)
            else:
                break

    
    #bulk default companies 
    client = Elasticsearch(hosts = "http://@localhost:9200")
    with open("{file_path}/reviews_update.json".format(file_path=vars("file_path_push_to_es")), "r") as f:
        resp = client.bulk(body=[f.read()])
        client.transport.close

    # insert into db
    sRev = Search(using=client, index="rev_1")

    listRev = []
    for hit in sRev.scan():
        for l in hit.to_dict()["reviews"]:
            listRev.append((
                hit.to_dict()["businessUnit"]["id"],
                l["id"],
                l["title"],
                l["text"],
                l["dates"]["experiencedDate"],
                l["dates"]["publishedDate"],
                l["rating"],
                l["labels"]["verification"]["isVerified"],
                l["consumer"]["id"],
                l["consumer"]["displayName"],
                l["consumer"]["numberOfReviews"],
                l["consumer"]["countryCode"],
                None if l["reply"] is None else l["reply"]["message"],
                None if l["reply"] is None else l["reply"]["publishedDate"]
                )
            )

    sql_delete_temp_review_table = """DELETE FROM ztemp_review;"""

    sql_insert_temp_review_table = """
        INSERT INTO ztemp_review (
        businessUnitId, reviewUnitId, review_title, review_text,
        experience_date, publish_date, rating, isVerified, user_id, 
        user_name, user_nbOfReviews, user_country, response_company,
        response_company_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ;"""

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

    # insert tables
    if conn is not None:
        delete_data(conn, sql_delete_temp_review_table)
        insert_data_temp(conn, sql_insert_temp_review_table, listRev)
        insert_data_perm(conn, sql_insert_review_table)

    else:
        print("Error! cannot create the database connection.")


updateReviews(website_name=site_name)
