from dash import Dash, html, dcc, Output, Input, dash_table, callback 
import dash_core_components as dcc
#import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Output,Input
import plotly.express as px
import plotly.graph_objs as go
import sqlite3  
import pandas as pd

# mise en place le type du CSS et le dash
app = Dash( __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
   

############################# SQL ########################################

conn = sqlite3.connect('project.db')  
print('Connexion SQLite est ouvert')
#Créer un cursor  

#Récupérer la table dans la base de données 
df_sec = pd.read_sql('SELECT * FROM sectors ', conn)  # table sectors
df_link = pd.read_sql('SELECT * FROM link_company_sectors', conn) # table link_company_sectors
df_com = pd.read_sql('SELECT * FROM company ', conn) # table company
df_rev = pd.read_sql('SELECT * FROM review ', conn) # table review

conn.close()
print("Connexion SQLite est fermee")

######################## Dash  ###################################


app.layout = dbc.Container([
  dbc.Row([
        dbc.Col([
            html.Span([
                " In all simplicity, you can analyze the comments of a company  ",
                html.I(className="fa-solid fa-magnifying-glass")], className='h2')
    ], width=13)
    ], justify='center', className='my-2', style={'textAlign': 'center', 'font-weight': 900}),
    
    dbc.Row([
        dbc.Col([
            html.Label('Sector name'),
            dcc.Dropdown(options= df_sec['child_label_name'].unique(),value= '', id='page-1-dropdown'),
            html.Label('Subsector name'),
            dcc.Dropdown( id='page-1-dropdown2'),
            html.H1(id=''),
            html.Label('Sompany name'),
            dcc.Dropdown( id='page-1-dropdown3'),
            html.Label('Rating'),
            dcc.Slider(1, 5, 1, value=3, id='page-1-slider')
            
        ],width=3)

], style = {'background' : 'beige', 'font-weight': 'bold'}),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='page-1-graph')
        ], width=13)
    ])
], style = {'background' : 'Snow'})

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

    # On renomme la colonne 'id' en 'company_id' pour faire la fusion
    company = df_com.rename(columns = {'id':'company_id'})
    company.head()    
    #jointure de la fusion sec et company 
    fusion_com = company.merge(right = fusion_sec, on = 'company_id', how = 'left')
    # filtrer les 'company' selon le 'subsector' 
    filtre_company = fusion_com[fusion_com['subchild_label_name'] == c ]
    d = filtre_company['display_name'].unique()
    return d
################### review ##############



'''@app.callback(Output(component_id='page-1-graph', component_property='figure'),
            [Input(component_id='page-1-dropdown', component_property='value')])
def Filtrer_Rating(r):
    dff = df_com[df_com["company_id"] == r]
    count = dff['rating'].value_counts()
    data = go.Bar(x=count.index,
                  y=count.values)
    layout = go.Layout(title='Notes')
    fig = go.Figure(data=data, layout=layout)
    return fig'''



if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")
