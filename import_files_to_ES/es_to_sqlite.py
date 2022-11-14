from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

client = Elasticsearch(hosts = "http://@localhost:9200")
s = Search(using=client, index="companies_2")

scanListCat = [hit.to_dict() for hit in s.scan()][0]["topCategories"]
listCat = [(x["categoryId"], x["displayName"]) for x in scanListCat]

#df = pd.DataFrame(a)

with open("result_es","w") as f:
    f.write(a)



