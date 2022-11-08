from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

client = Elasticsearch(hosts = "http://@localhost:9200")
s = Search(using=client, index="companies_2")

a = str([hit.to_dict() for hit in s.scan()])
#df = pd.DataFrame(a)

with open("result_es","w") as f:
    f.write(a)



