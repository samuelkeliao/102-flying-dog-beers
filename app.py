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






#Bar chart
df_merged['PERCENT_NATIVE_CHINESE_SPEAKERS'] = (round(df_merged['NATIVE_CHINESE_SPEAKERS_RATE'], 2)*100).astype('str') + '%'
df_merged['NATIVE_CHINESE_SPEAKERS'] = df_merged['NATIVE_CHINESE_SPEAKERS'].fillna(0).astype('int')
df_merged['label'] = df_merged['NATIVE_CHINESE_SPEAKERS'].astype('str') + ' (' + df_merged['PERCENT_NATIVE_CHINESE_SPEAKERS'] + ')'
tmp = df_merged[df_merged['NATIVE_CHINESE_SPEAKERS'] >= 500]
df_top_5 = tmp.sort_values('NATIVE_CHINESE_SPEAKERS_RATE', ascending = False).head(5)

fig_bar = px.bar(
    df_top_5,
    y="LGA_NAME20",
    x="NATIVE_CHINESE_SPEAKERS_RATE",
    title='Population: Chinese Speakers, LGA',
    orientation='h',
    text='label'
)
fig_bar.update_traces(marker_color='#592c82',
                      textposition='inside',
                      hovertemplate=None,
                      hoverinfo='skip'
                     )
fig_bar.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig_bar.update_yaxes(title=None)
fig_bar.update_xaxes(title='Chinese-spoken rate')

#Age Pie chart
df = pd.DataFrame({"names": ['Age 5-19', 'Age 20-64', 'Age 64 +'],
                   "values": [df_top_5['Age 5-19'].sum(), df_top_5['Age 20-64'].sum(), df_top_5['Age 64 +'].sum()]})
df['values'] = df['values'].astype('int')
fig_donut = px.pie(df,
                   values=df['values'],
                   names=df['names'],
                   hole=.3,
                   title='Age breakdown, LGA',
                   color=df['names'],
                   color_discrete_map={'Age 5-19':'#592c82',
                                       'Age 20-64':'#8e7cc3ff',
                                       'Age 64 +':'#dbcbee'})

#Gender pie chart
df = pd.DataFrame({"names": ['Male', 'Female'],
                   "values": [df_top_5['Estimated resident population - males (no.)'].sum(), df_top_5['Estimated resident population - females (no.)'].sum()]})
df['values'] = df['values'].astype('int')
fig_sex = px.pie(df,
                values=df['values'],
                names=df['names'],
                hole=.3,
                title='Gender breakdown, LGA',
                color=df['names'],
                color_discrete_map={'Female':'#592c82',
                                       'Male':'#dbcbee'})


#Indicator
df_merged['NATIVE_CHINESE_SPEAKERS'] = df_merged['NATIVE_CHINESE_SPEAKERS'].astype('int')

cnt_chn_speaker = df_merged['NATIVE_CHINESE_SPEAKERS'].sum()
total_population = df_merged['Estimated resident population  (no.)'].sum()

fig_indicator = go.Figure()

fig_indicator.add_trace(go.Indicator(
    mode = "number",
    value = cnt_chn_speaker,
    title = {"text": "(Population: Chinese Speakers, LGA)"},
    #delta = {'reference': total_population, 'relative': True},
    domain = {'x': [0, 1], 'y': [0, 0.2]}))

#fig_indicator.update_traces(delta_decreasing_symbol=None, selector=dict(type='indicator'))
#fig_indicator.update_traces(delta_decreasing_color='purple', selector=dict(type='indicator'))

fig_indicator.add_trace(go.Indicator(
    mode = "number",
    value = df_merged['Estimated resident population  (no.)'].sum(),
    title = {"text": "Population: Overall, LGA<br><span style='font-size:0.8em;color:gray'>"},
    domain = {'x': [0, 1], 'y': [0.5, 0.8]}
))






#Build dash


#app = JupyterDash(__name__)
app = dash.Dash(__name__)
server=app.server
#application = app.server

map_style = {'width': '50%', 'height': '800px', 'float': 'left', 'marginTop': '5%', "verticalAlign": "bottom"}
bar_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}
indicator_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}
graph_style = {'width': '25%', 'height': '400px', 'float': 'left', "verticalAlign": "bottom"}




app.layout = html.Div([
        html.Div(children=[

            html.Div([dcc.Graph(
                            id='indicator',
                            figure=fig_indicator,
                            style=indicator_style
                        )
                     ]),
            html.Div([dcc.Graph(
                            id='graph',
                            figure=fig_bar,
                            style=bar_style
                        )
                      ]),

            html.Div([dcc.Graph(
                            id='gender',
                            figure=fig_sex,
                            style=graph_style
                        )
                      ]),
            html.Div([dcc.Graph(
                            id='donut',
                            figure=fig_donut,
                            style=graph_style
                        )
                      ]),
        ])

])




#app.run_server(debug=True, port=8080, use_reloader=False)
app.run_server(debug=True)
#application.run(debug=True, port=8080)
