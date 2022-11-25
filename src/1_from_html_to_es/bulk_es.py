from elasticsearch import Elasticsearch
from custom_vars import vars

#bulk categories
client = Elasticsearch(hosts = "http://@localhost:9200")
with open("{file_path}/categories.json".format(file_path=vars("file_path_push_to_es")), "r") as f:
    resp = client.bulk(body=[f.read()]) 
    client.close()

#bulk default companies 
client = Elasticsearch(hosts = "http://@localhost:9200")
with open("{file_path}/companies_default.json".format(file_path=vars("file_path_push_to_es")), "r") as f:
    resp = client.bulk(body=[f.read()])
    client.close()

    """
    with open("{file_path}/reviews_1.json".format(file_path=vars("file_path_push_to_es")), "r") as f:
        resp = client.bulk(body=[f.read()])
    """
