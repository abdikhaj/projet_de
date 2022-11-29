from dash import Dash, html, dcc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Output,Input
import plotly.express as px
import sqlite3  
import dash_table as dt
from plotly.offline import init_notebook_mode, iplot
import pandas as pd
#from word_rev import countwords
#from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go

# mise en place le type du CSS et le dash
app = Dash( __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP,  dbc.icons.FONT_AWESOME])


############################# SQL ########################################

conn = sqlite3.connect('project.db')   ## <--------------  modifier le chemin en fonction de l'emplacement 'project.db'
print('Connexion SQLite est ouvert')
#Récupérer la table dans la base de données 
df_sec = pd.read_sql('SELECT * FROM sectors ', conn)  # table sectors
df_link = pd.read_sql('SELECT * FROM link_company_sectors', conn) # table link_company_sectors
df_com = pd.read_sql('SELECT id as company_id, display_name FROM company ', conn) # table company
df_rev = pd.read_sql('SELECT company_id, review_text FROM review ', conn) # table review
#df_resume = pd.read_sql('SELECT company_id, resume_keywords FROM review_resume ', conn) # table resum
df_1 = pd.read_sql('SELECT display_name, score, postal_address as address, postal_city as ville, postal_country as pays FROM company', conn)
df_2 = pd.read_sql('SELECT display_name,contact_website as site,contact_email as email,contact_phone as telephone FROM company', conn)
df_4 = pd.read_sql('SELECT display_name ,resume_text,resume_type,resume_keywords FROM review_resume JOIN company ON review_resume.company_id = company.id ', conn)
#df_res = pd.read_sql('SELECT  company_id, review_text FROM review', conn) # table review
#df_moins_3 = pd.read_sql('SELECT id, company_id, review_text FROM review where rating < 3 or rating = 3', conn) # table review
conn.close()
print("Connexion SQLite est fermee")


######################## Dash  ###################################


app.layout = html.Div([
            dbc.Row([
                    dbc.Col([
                        html.Span([
                            "Résumé les avis pour chaque entreprise",
                            html.I(className="fa-solid fa-magnifying-glass")], className='h2')
                ], width=13)
                ], justify='center', align="start" ,style={'textAlign': 'center', 'color': 'Black', 'font-size': 'x-large' }),


  
            dbc.Row([
                    dbc.Col([
                        html.Label('Catégorie'),
                        dcc.Dropdown(options= df_sec['child_label_name'].unique(),value= '', id='page-1-dropdown',  style={'width': '40%'}),
                        html.Label('Sous-catégorie'),
                        dcc.Dropdown(id='page-1-dropdown2', style={'width': '40%'}),
                        html.Label('Entreprise'),
                        dcc.Dropdown(id='page-1-dropdown3', style={'width': '40%'})
                        
                        ],style = {'display': 'flex'})
                        ],align="center", style = {'background' : 'beige', 'font-weight': 'bold'}),

             dbc.Row([
                    dbc.Col([   
                        html.Div(id='content1'),
                        html.Div(id='content2') ], style = {'display': 'flex'}),]),
            dbc.Row([    
                    dbc.Col([
                        html.Label("Contacter l'entreprise"),   
                        html.Div(id ='table2'),
                        html.Label("Information de l'entreprise"),   
                        html.Div(id ='table1')])
                    ],  align="end")
         
   
 ], style = { 'background' : 'snow', 'textAlign': 'center' , 'font-weight': 'bold'})
######### drapdown subsector  ########
@app.callback(Output('page-1-dropdown2','options'),
            [Input('page-1-dropdown', 'value')])

def fil_subsector(a):
    sec = df_sec[df_sec['child_label_name'] == a]
    b = sec['subchild_label_name'].unique()
    return b
######### drapdown company  ########
@app.callback(Output('page-1-dropdown3','options'),
            [Input('page-1-dropdown2', 'value')])
###jointure des tables 
def filt_company(c):
    # On renomme la colonne 'id' en 'sector_id' pour faire la fusion
    sectors = df_sec.rename(columns = {'id':'sectors_id'})
    # Jointure à gauche avec la table sectors et link_company_sectors
    fusion_sec = df_link.merge(right = sectors , on = 'sectors_id', how = 'left')
       
    #jointure de la fusion sec et company 
    fusion_com = df_com.merge(right = fusion_sec, on = 'company_id', how = 'left')
    # filtrer les 'company' selon le 'subsector' 
    filtre_company = fusion_com[fusion_com['subchild_label_name'] == c ]
    d = filtre_company['display_name'].unique()
    return d


############### table 
#info
@app.callback(Output("table1","children"), [Input("page-1-dropdown3", "value")])

def table(n):
    df_filtr = df_1[df_1['display_name'] == n ]
    df = df_filtr[['score','address','ville', 'pays']]
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, size = 'sm')
#contact
@app.callback(Output("table2","children"), [Input("page-1-dropdown3", "value")])

def table(n):
    df_filtr = df_2[df_2['display_name'] == n ]
    df = df_filtr[['site','email','telephone']]
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, size = 'sm')

##################  card  ################
#sat
@app.callback(Output("content1", "children"), [Input("page-1-dropdown3", "value")])

def create_card(val):
    df_filtr = df_4[df_4['display_name'] == val ]
    df_sat = df_filtr[df_filtr['resume_type']=='text_sat']
    if not None:
        return dbc.Card(
            dbc.CardBody([
                html.H4("La synthèse de commentaires des clients satisfaisants", className="card-title"),
                html.P(df_sat['resume_keywords'] , className="card-text" ),
                html.P(df_sat['resume_text'] , className="card-text" ),
                ], style={"width": "60rem"}) )
    else:
        return "No hover"
    
#unsat
@app.callback(Output("content2", "children"), [Input("page-1-dropdown3", "value")])

def create_card(val):
    df_filtr = df_4[df_4['display_name'] == val ]
    df_unsa = df_filtr[df_filtr['resume_type']=='text_unsat']
    
    if not None:
        return dbc.Card(
            dbc.CardBody([
                html.H4("La synthèse de commentaires des clients insatisfaisants", className="card-title"),
                html.P(df_unsa['resume_keywords'], className="card-text" ),
                html.P(df_unsa['resume_text'] , className="card-text" ),
                ], style={"width": "60rem"})
            )

    else:
        return "No hover"



    
    
if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")


