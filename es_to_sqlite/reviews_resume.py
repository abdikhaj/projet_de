import sqlite3
from sqlite3 import Error
import itertools
# pip3 install gensim==3.6.0
import yake


# connexion
db_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/es_to_sqlite/project.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
    SELECT company_id, review_text 
    FROM review 
    WHERE rating > 3 
    AND company_id NOT IN (select company_id from review_resume where resume_type = 'text_sat')
    ORDER BY company_id
    """)

# keywords lib
kw_extractor = yake.KeywordExtractor()
text = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
language = "fr"
max_ngram_size = 3
deduplication_threshold = 0.2 # avoid the repetition
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)


# fetch data
rows = cur.fetchall()
list_sat = []
for l in [list(g) for k, g in itertools.groupby(rows, lambda x: x[0])]:
    concat_text = ""
    for t in l:
        concat_text += t[1] + '. '
    keywords = custom_kw_extractor.extract_keywords(concat_text)
    concat_kw = [kw[0] for kw in keywords]
        
    list_sat.append((t[0], concat_text, concat_kw))

print(list_sat)