#import geopandas as gpd

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
#from dash import Dash, dcc, html, Input, Output
from dash import Dash, Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
from PIL import Image
import dash_bootstrap_components as dbc
#from shapely import wkt
import os
import json

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'raw.csv')
df_merged = pd.read_csv(file_path)

df_merged = df_merged.set_index('LGA_CODE20')


json_path = os.path.join(script_dir, 'data.json')
with open(json_path) as json_file:
    lga_json = json.load(json_file)




#################Build Map###################################

zmin = df_merged['NATIVE_CHINESE_SPEAKERS_RATE'].min()
zmax = df_merged['NATIVE_CHINESE_SPEAKERS_RATE'].max()

fig_map1 = go.Figure(go.Choroplethmapbox(geojson=lga_json,
                                    locations=df_merged.index,
                                    z=df_merged.NATIVE_CHINESE_SPEAKERS_RATE,
                                    colorscale='Viridis',
                                    text=df_merged.LGA_NAME20,
                                    zmin=zmin,
                                    zmax=zmax,
                                    marker_line_width=1,
                                    hovertemplate = "<b>%{text}</b><br>" +
                                                    "%{z:.2%}<br>" +
                                                    "<extra></extra>"))

fig_map1.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=4,
                      mapbox_center = {"lat": -21.6, "lon": 145.2},
                      title = {'text': f"Percentage of Population: Chinese Speakers, QLD",
                                'font': {'size':24}})
fig_map1.update_layout(margin={"r":0,"t":40,"l":0,"b":0})



#Add logo
image_path = os.path.join(script_dir, 'logo.png')
html.Img(src=image_path)

pil_img = Image.open(image_path)



#Build dash


#app = JupyterDash(__name__)
app = dash.Dash(__name__)
server=app.server
#application = app.server

map_style = {'width': '50%', 'height': '800px', 'float': 'left', 'marginTop': '5%', "verticalAlign": "bottom"}
bar_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}
indicator_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}
graph_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}


#fig_map1.update_layout(clickmode='event+select')

app.layout = html.Div([
    dbc.Row(
        html.Div(children=[
            html.Div([
                html.Button("Download CSV", id="btn_csv", style={'marginLeft': '1%'}),
                dcc.Download(id="download-dataframe-csv"),
                ]),
            html.Img(src=pil_img, style={'height':'5%', 'width':'5%', 'float': 'right', 'marginRight': '1%'}),
        ])
    ),
    dbc.Row(
        html.Div(children=[
            html.Div([dcc.Graph(id='map', figure=fig_map1, style=map_style)]),
            html.Div([dcc.Graph(
                            id='indicator',
                            figure=fig_indicator,
                            style=indicator_style
                        )]),
                      ]),
        ])
    )

])



#app.run_server(debug=True, port=8080, use_reloader=False)
app.run_server()
#application.run(debug=True, port=8080)

