import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import dash_table
import sidetable as stb
import datetime
from datetime import datetime, timedelta
from datetime import date
import geopandas as gpd
import flask
import os

baseju= pd.read_csv("https://raw.githubusercontent.com/Aeelen/Juana/main/mapaJuana.csv")
baseju

from urllib.request import urlopen
import json

with urlopen('https://www.gits.igg.unam.mx/repositoriodecapas/geojson/u_territorial_municipios_mgn_inegi_2013.json') as response:
    counties = json.load(response)
counties["features"][0]
# Creacion de geodataframe
geo_df = gpd.GeoDataFrame.from_features(counties["features"])

geo_df['cvegeomuni'] = [s.lstrip("0") for s in geo_df.cvegeomuni]

geo_df['cvegeomuni'] = geo_df['cvegeomuni'].astype(int)

union = geo_df.merge(baseju, left_on= "cvegeomuni", right_on= "CVEGEO", 
                       how= "inner")


# Selección de columnas 
concat2 = union[
    ['geometry',
    'nom_mun',
        'CVEGEO', 'SEMANA 1', 'SEMANA 2', 'SEMANA 3', 'SEMANA 4', 'SEMANA 5',
       'SEMANA 6', 'SEMANA 7', 'SEMANA 8', 'SEMANA 9', 'SEMANA 10',
       'SEMANA 11', 'SEMANA 12', 'SEMANA 13', 'SEMANA 14', 'SEMANA 15',
       'SEMANA 16', 'SEMANA 17', 'SEMANA 18', 'SEMANA 19', 'SEMANA 20'
    ]]

############################################## lista de semanas 

listameses = [ 'SEMANA 1', 'SEMANA 2', 'SEMANA 3', 'SEMANA 4', 'SEMANA 5',
       'SEMANA 6', 'SEMANA 7', 'SEMANA 8', 'SEMANA 9', 'SEMANA 10',
       'SEMANA 11', 'SEMANA 12', 'SEMANA 13', 'SEMANA 14', 'SEMANA 15',
       'SEMANA 16', 'SEMANA 17', 'SEMANA 18', 'SEMANA 19', 'SEMANA 20'
    ]

#lista de las semanas 
fnameDict = listameses
names = list(fnameDict)
# A P P
####################################




server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
    
       html.Br(),
    
   
   dbc.Row([
            
            
           dbc.Col(html.H6(" INEGI," 
                          ),
                  style={'size': 3, 'offset': 0, "text-align": "center",}),
               ], justify="start",),
            
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),

# Title
      html.Br(),
        dbc.Row(
           [
            dbc.Col(html.P("Mapa Juana"),
                  style={
                         #'offset' : 3, 
                         'color' : 'danger',
                          "font-size": "70px", "text-align": "center",
                              "text-shadow": "10px 20px 30px black"
                        }), 
                

            ],justify="start"),
  
    html.Br(),
    html.Br(),
    html.Br(),
#insertar en app al final de aquí.... 
    
           dbc.Col(html.H1("Mapa con acumulados semanales por municipios"), 
                width={'size' : "auto",'offset' : 2 }),
                #style={'text-align': 'left'}
    
    
           dbc.Col(dcc.Dropdown(
           id="slct_year",
           options=[{'label':name, 'value':name}
                 for name in names],
           value = list(fnameDict)[0]),
                width={'size' : 8,'offset' :2 },
                  style={'text-size': 38}),


        #style={'width': '70%', 'display': 'inline-block'},
        #),
       html.Div(id='output_container', children=[]),
       html.Br(),
        
           dcc.Graph(id='my_bee_map', figure={},
                      style={'width': '100%', 'display': 'inline-block',
                            'align': 'center'}),
         
    ],style={
            #'margin-top': '0px',
            #'margin-left': '10px',
            'width': '1800px',
           # 'height': '1413px',
      #'backgroundColor': 'lightgray'
         })

  
    
    
        # Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
    )
def update_graph(option_slctd):
    
    #print(option_slctd)
    print(type(option_slctd))
        
    container = "______________semana seleccionada:     {}".format(option_slctd) 
        
        
    semnalgraph =  px.choropleth_mapbox(concat2[(option_slctd)],
                                   geojson=concat2.geometry,
                                   locations=concat2.index,
                                   color= (option_slctd),
                                   range_color=[100, 1500],     
                                   center={"lat": 23.88234, "lon": -102.28259},
                                   mapbox_style="carto-positron",
                                   zoom= 4.5,
                                   opacity=.6,
                                   color_continuous_scale=px.colors.sequential.Oranges,
      
                                       )     

    
    semnalgraph.update_layout(
        margin={"r":0,"t":0,"l":100,"b":0},
        autosize=False,
        width=1200,
        height=700,
        showlegend = False
            )
    
    return container, semnalgraph
        
  
  
  
  
  
  
#])
app.layout = html.Div([body],
                              style={'width': '1900px',
                                    "background-color": "white"})

#from application.dash import app
#from settings import config

if __name__ == "__main__":
    app.run_server()
