# projet_de
Établir une base de données fondée sur la satisfaction de la clientèle.

Ce lien vous donne accès à un document de description de notre projet :

https://docs.google.com/document/d/1vqq-mXVUuiHR_ijIjdI69I5Q9ZI3lWZGQKPnaKg5yiU/edit?usp=sharing


Dans le dossier **src**, executer le projet dans l'ordre suivant:

1) dossier 1_from_html_to_es

    1) scraping_trustpilot.py

        - **création de 2 fichiers json, categories.json et companies.json au format [bulk](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)** ("create index"), 1 fichier pour extraire les catégories, 1 fichier pour extrair la liste des entreprises

        - dans le fichier companies.json généré, le format bulk se lit de cette manière, nous allons retrouver sur la:
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

2) dossier 2_from_es_to_sqlite

    1) create_db.py -> création de la db project.db

    2) create_tables.py -> création des tables

        - sectors -> liste toutes les categories et sous catégories des entreprise. A noter qu'une entreprise peut appartenir à plusieurs sous categories (voir UML)
        - company -> liste toutes les entreprises
        - link_company_sectors -> permet de faire le lien entre la table sectors et company
        - review -> liste tous les avis
        - review_resume -> table agrégée par entreprise et type de résumé qui recense les résumés des avis et les mots-cles des résumés des avis
        - ztemp_[nom de la table] -> ce sont des tables temporaires, qui sont tronquées avant insertion de nouvelles données. Ces tables sont des tables intermediaires qui permettent d'alimenter les tables citées au-dessus.

    3) insert_data.py -> insert les données dans les tables suivantes par ordre chronologique:
        - ztemp_sectors
        - ztemp_company
        - ztemp_lk_company_sectors
        - sectors
        - company
        - link_comany_sectors

3) dossier 3_from_sqlite_to_sqlite

    1) update_reviews.py -> insert les données dans les tables:
        - review

        via la fonction **update_reviews()** qui prend une liste d'entreprise en parametre, ce sript permet d'alimenter la table review (scrape les données des avis, puis importe les donneés dans Elasticsearch, puis alimente la table review) en **insérant uniquement le delta des avis** (review) qui ne sont pas déjà insérés.

        - review_resume

        via la fonction **update_reviews_resume()** qui prend une liste d'entreprise en parametre. Cette fonction  résume les avis et créé une liste de mots cles des avis, ces données sont agrégées par entreprise et par type de résumé.

        Les types de résumé sont:
     
          - text_sat: résume les avis des utilisateurs satisfaits (score de 4/5 et 5/5)
          - text_unsat: résume les avis des utilisateurs non satisfaits (score de 1/5 et 2/5)

        Les étapes pour résumer les avis et extraire les mots-clés sont détaillées ci-dessous:
        
          1) extraction des données de la table review, le score 3/5 n'est pas pris en compte
          2) concaténation des avis par entreprise

               - on obtient une 1ere liste des avis positifs et une 2eme liste des avis négatifs de la forme suivante:
                [("entreprise 1", "text_1. text_2."), ("entreprise 2", "text_1. text_2. ect.")]
          3) résumé des avis en utilisant la librairie [gensim.summarization.summarizer](https://radimrehurek.com/gensim_3.8.3/summarization/summariser.html)

               - on obtient une liste de la forme  suivante:
                [("entreprise 1", "text_1. text_2. text_3.", "resumé du champ précédent"), ("entreprise 2", "text_1. text_2. ect.", ""resumé du champ précédent")]
          4) génération de la liste des mots clés en utilisant la fonction KeywordExtractor de la librairie [yake](https://pypi.org/project/yake/) sur le résumé des textes.

               - on obtient une liste de la forme suivante:
                [("entreprise 1", "text_1. text_2. text_3.", "resumé du champ précédent", "mots-cles du résumé"), ("entreprise 2", "text_1. text_2. ect.", ""resumé du champ précédent", mots-clés du résumé)]

4) Dossier Dash :

 - Préciser l’emplacement actuelle de BDD (project.db) :
        conn = sqlite3.connect('C:…./projet_de/src/2_from_es_to_sqlite/project.db') 
 - Lancer le scripte :
        Sélectionner le lien pour accéder au Dashboard 
        Sélection dans l’ordre suivant :
                      Catégorie
                      Sous-catégorie 
                      Entreprise (selon l’entreprise les informations présentes dans base de données, sont afficher en dessous )
