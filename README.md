# projet_de
Établir une base de données fondée sur la satisfaction de la clientèle.

Ce lien vous donne accès à un document de description de notre projet :

https://docs.google.com/document/d/1vqq-mXVUuiHR_ijIjdI69I5Q9ZI3lWZGQKPnaKg5yiU/edit?usp=sharing


Executer le projet dans l'order suivant:

1) dossier html_to_es
    1) scraping_trustpilot.py

        - **création de 2 fichiers json, categories.json et companies.json au format bulk** ("create index"), 1 fichier pour lister les catégories, 1 fichier pour lister les entreprises

        - dans le fichier companies.json nous allons retrouver sur la:
            - 1ere ligne -> l'entete du bulk de la 1ere page à scrapper (nom de l'index à créer = comp_1, nom du document = nom de la catégorie + numero de la page=1)
            - 2eme ligne -> les données de la 1ere page à scrapper (liste des entreprises et leurs details)
            - 3e ligne -> l'entete du bulk de la 2e page à scrapper (nom de l'index à créer = comp_1, nom du document = nom de la catégorie + numero de la page=2)
            - 4e ligne -> les données de la 2e page à scrapper (liste des entreprises et leurs details)
            - etc.
    2) put_mapping_es.py 
        - création de 3 mappings dans elasticsearch, cat_1, comp_1, rev_1
            - cat_1 -> nom de l'index contenant la liste des catégories d'entreprise, dans le mapping il été introduit uniquement des types "flatenned" pour contourner le probleme cité [ici](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings).
            En effet il y a trop de champ a indexer ce qui provoque une erreur de mémoire dans elasticsearch si nous mettons tous les champs en type "keyword"
    3) bulk_es.py
        - importe les 2 fichies présents dans le point 1 dans elasticsearch via la méthode bulk

2) dossier es_to_sqlite
    1) create_db.py -> création de la db project.db
    2) create_tables.py -> création des tables
    3) insert_data.py -> insert les données suivant dans sqlite:
        - liste des categories -> table category
        - lites des entreprises -> table company

3) dossier html_to_es
    1) update_reviews.py
        - création d'une fonction update_reviews(liste_entreprise) permettant d'inserer des données dans la table review

4) dossier es_to_sqlite
    1) insert_reviews_resume.py -> insert les résumés et les mot-cles des avis agrégés par entreprise