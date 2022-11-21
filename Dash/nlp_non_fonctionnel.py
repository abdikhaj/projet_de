import spacy
import pandas as pd
import sqlite3
# Charge le petit pipeline français
nlp = spacy.load("fr_core_news_sm")
############################# SQL ########################################

conn = sqlite3.connect('project.db')  
print('Connexion SQLite est ouvert')
#Créer un cursor  

#récupérer le tableau du review

review_text= pd.read_sql('SELECT review_text FROM review ', conn) # table review

conn.close()
print("Connexion SQLite est fermee")

############################# spacy  ########################
# Traite le texte

def nlp_review(text_a):
    doc = nlp(text_a)
    token_head_text = []   
    #token_pos = []
   # token_text = []
    # Itère sur les tokens
    for token in doc:
        # token.head.text : L'attribut .head retourne le token de tête syntaxique ou noyau.
        # Tu peux le voir comme le token parent auquel le mot considéré se rattache.
        # token_pos : la position de la phrase dans les discours
        # token_text
        #token_text.append(token.text.split()) 
        #token_pos.append(token.pos_.split())  
        token_head_text =  (token.head.text.split())
         
      # resume =  pd.DataFrame(list(token_text,token_pos,token_head_text))
    print(f"{ token_head_text }")
a = review_text.head(20)
nlp_review(a)

