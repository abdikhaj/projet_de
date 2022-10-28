#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv, json
from pprint import pprint

# Connexion au cluster
es = Elasticsearch(hosts = "http://@localhost:9200")

# Décommenter cette commande si vous utilisez l'installation sécurisée avec 3 nodes

#es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200",
#                  ca_certs="./ca/ca.crt")

with open('hotel_1.json', "r") as f:
    reader = json.load(f)
    helpers.bulk(es, reader, index='hotel_test')
