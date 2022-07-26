#import geopandas as gpd

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
#from dash import Dash, dcc, html, Input, Output
#from dash import Dash, Input, Output
import dash_core_components as dcc
import dash_html_components as html
#from plotly.subplots import make_subplots
#from PIL import Image
#import dash_bootstrap_components as dbc
#from shapely import wkt
import os
#import json

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'raw.csv')
df_merged = pd.read_csv(file_path)

df_merged = df_merged.set_index('LGA_CODE20')






########### Set up the layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
            This is Dash running on Elastic Beanstalk.
        '''),
    dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': ['left', 'center', 'right'], 'y': [3,7,6], 'type': 'bar', 'name': 'category 1'},
                    {'x': ['left', 'center', 'right'], 'y': [4,2,5], 'type': 'bar', 'name': 'category 2'},
                ],
                'layout': {
                    'plot_bgcolor': 'lightgray',
                    'title': 'Graph Title',
                    'xaxis':{'title':'x-axis label'},
                    'yaxis':{'title':'y-axis label'},
                },
            }
        )
])



#app.run_server(debug=True, port=8080, use_reloader=False)
app.run_server(debug=True)
#application.run(debug=True, port=8080)
