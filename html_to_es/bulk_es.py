from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

client = Elasticsearch(hosts = "http://@localhost:9200")
file_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/html_to_es/files_to_import_to_es"


with open("{}/hotel_1.json".format(file_path), "r") as f:
    resp = client.bulk(body=[f.read()])
    print(resp)

with open("{}/categories.json".format(file_path), "r") as f:
    resp = client.bulk(body=[f.read()])
    print(resp)

with open("{}/reviews_1.json".format(file_path), "r") as f:
    resp = client.bulk(body=[f.read()])
    print(resp)


