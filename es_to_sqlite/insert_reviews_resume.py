import sqlite3
from sqlite3 import Error
import itertools
# pip3 install gensim==3.6.0
import yake
from gensim.summarization.summarizer import summarize
import re

# keywords lib
kw_extractor = yake.KeywordExtractor()
text = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
language = "fr"
max_ngram_size = 3
deduplication_threshold = 0.2 # avoid the repetition
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)


# connexion db
db_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/es_to_sqlite/project.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

params = [("text_sat", ">"), ("text_unsat", "<")]

for p in params:

    # sql
    cur.execute("""
        SELECT company_id, review_text 
        FROM review 
        WHERE rating {operator} 3 
        AND company_id NOT IN (select company_id from review_resume where resume_type = '{sat_type}')
        ORDER BY company_id
        """.format(operator=p[1], sat_type=p[0]))

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

