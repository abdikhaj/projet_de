import requests
import re
import os
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from custom_vars_db import create_connection, insert_data_perm, insert_data_temp, delete_data
import sqlite3
import itertools
# pip3 install gensim==3.6.0
import yake
from gensim.summarization.summarizer import summarize

def vars(var):
    if var == "db_path":
        return "/home/utilisateur/Documents/datascientest/projet_data/projet_de/src/2_from_es_to_sqlite/project.db"
    if var == "file_path_push_to_es":
        return "/home/utilisateur/Documents/datascientest/projet_data/projet_de/src/3_from_sqlite_to_sqlite/files_to_import_to_es"

def update_reviews(website_name):

    json_name = "reviews_update"

    # delete the review file if exsts
    if os.path.exists("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es"))):
        os.remove("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")))

    # loop on companies and append the result to the review file
    html_all_rev = ""
    for comp_name in tqdm(website_name):

        # get the last num html page to loop on page
        urlRevLast = 'https://fr.trustpilot.com/review/{website}'.format(website=comp_name)
        html_respRevLast = requests.get(url=urlRevLast)
        m = re.search('"totalPages"\:(\d+)', html_respRevLast.text)
        if m:
            html_last_num_page = int(m.group(1))

        # loop on page
        for num_page in tqdm(range(1,html_last_num_page), leave=False):
            if num_page == 1:
                suffix = ""
            else:
                suffix = "?page=" + str(num_page)

            doc_name = comp_name + "_" + str(num_page)
            urlRev = 'https://fr.trustpilot.com/review/{comp_name}{suffix}'.format(comp_name=comp_name, suffix=suffix)
            html_respRev = requests.get(url=urlRev, allow_redirects=False)
            if html_respRev.status_code == 200:
                html_substr_rev1 = re.findall('"reviews"\:.+\}\]\,"products"', html_respRev.text)[0]
                html_substr_rev = re.findall('"businessUnit"\:\{"id"\:"\w+"', html_respRev.text)[0] + '},' + html_substr_rev1
                html_rev = r'{"create":{"_index":"rev_1","_id":' + '"{doc_name}"}}\n'.format(doc_name=doc_name) +'{' + html_substr_rev[:-11] + '}\n'
                html_all_rev += html_rev
            else:
                break

    with open("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")), "a", encoding='utf-8') as file:
        file.write(html_all_rev)

    
    #bulk default companies 
    client = Elasticsearch(hosts = "http://@localhost:9200")
    with open("{file_path}/reviews_update.json".format(file_path=vars("file_path_push_to_es")), "r") as f:
        resp = client.bulk(body=[f.read()])
        #client.transport.close()

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

    print(len(listRev), " lines imported from Elasticsearch")

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
    conn = create_connection(vars("db_path"))

    # insert tables
    if conn is not None:
        delete_data(conn, sql_delete_temp_review_table)
        insert_data_temp(conn, sql_insert_temp_review_table, listRev)
        print(len(listRev), " rows inserted into review temp table")
        insert_data_perm(conn, sql_insert_review_table)

    else:
        print("Error! cannot create the database connection.")


def update_reviews_resume(list_company_website):

    # keywords lib
    kw_extractor = yake.KeywordExtractor()
    text = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
    language = "fr"
    max_ngram_size = 3
    deduplication_threshold = 0.2 # avoid the repetition
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

    # params
    params = [("text_sat", ">"), ("text_unsat", "<")]

    # convert list to str -> from ["aaaa", "bbbb"] to '"aaaa","bbbb"'
    list_company_website = str(list_company_website).strip("[]")

    # connexion db
    conn = sqlite3.connect(vars("db_path"))
    cur = conn.cursor()

    for p in tqdm(params):

        # sql delete
        cur.execute("""
            DELETE 
            FROM review_resume
            WHERE company_id in (select id from company where website in ({website}))
            AND resume_type = '{sat_type}'
        """.format(website=list_company_website, sat_type=p[0]))

        # sql insert
        cur.execute("""
            SELECT company_id, review_text 
            FROM review 
            WHERE rating {operator} 3 
            AND company_id IN (select id from company where website in ({website}))
            ORDER BY company_id
            """.format(operator=p[1], website=list_company_website))

        # fetch data
        rows = cur.fetchall()
        list_sat = []
        for l in [list(g) for k, g in itertools.groupby(rows, lambda x: x[0])]:
            concat_text = ""
            for t in l:
                concat_text += t[1] + '. '

            # use gensim lib to resume text
            summarize_text = summarize(concat_text, word_count=100)
            # before to extract keywords delete all special caracters
            summarize_text_clean = re.sub("[^a-zéèàôîïöçA-Z]", ' ', summarize_text)
            summarize_text_clean = re.sub("\s+", ' ', summarize_text_clean)
            # use yake lib to extract keywords from text resume
            keywords = custom_kw_extractor.extract_keywords(summarize_text_clean)
            keyword_extracted = [kw[0] for kw in keywords]
                

            list_sat.append((t[0], "{sat_type}".format(sat_type=p[0]), summarize_text, str(keyword_extracted)))

        cur.executemany("""
        INSERT INTO review_resume (company_id, resume_type, resume_text, resume_keywords)
        VALUES (?, ?, ?, ?)""", list_sat)


    conn.commit()
    conn.close()