from elasticsearch import Elasticsearch
from custom_vars import vars
from custom_es_vars import es_vars
from elasticsearch import client

conn = client.IndicesClient(Elasticsearch(hosts = "http://@localhost:9200"))

mapping_category = eval(es_vars("mapping_cat").replace("/n", "").replace(" ", ""))
mapping_company = eval(es_vars("mapping_comp").replace("/n", "").replace(" ", ""))
mapping_review = eval(es_vars("mapping_rev").replace("/n", "").replace(" ", ""))

resp = conn.create(index="cat_1", mappings=mapping_category)
print(resp)

resp = conn.create(index="comp_1", mappings=mapping_company)
print(resp)

resp = conn.create(index="rev_1", mappings=mapping_review)
print(resp)