from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

client = Elasticsearch(hosts = "http://@localhost:9200")

with open("hotel_1.json", "r") as f:
    resp = client.bulk(body=[f.read()])
    print(resp)


