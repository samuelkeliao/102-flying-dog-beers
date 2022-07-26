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


fig_map1.update_layout(clickmode='event+select')

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
    )

])


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_merged.to_csv, "ABS_QLD_LGA.csv")

@app.callback(
    Output('graph', 'figure'),
    Input('map', 'selectedData'), prevent_initial_call=True)
def display_selected_data(selectedData):
    if selectedData is None:
        return fig_bar
    else:
        #print(selectedData)
        #sel = selectedData['points'][0]['location']
        sel = []
        for item in selectedData['points']:
            sel.append(item['location'])
        dff = df_merged[df_merged['LGA_CODE_2021_x'].isin(sel)]
        fig_bar_sel = px.bar(dff, y="LGA_NAME20", x="NATIVE_CHINESE_SPEAKERS_RATE", title='Population: Chinese Speakers, LGA', orientation='h', text='label')
        fig_bar_sel.update_traces(
                    marker_color='#592c82',
                    textposition='inside',
                    hovertemplate=None,
                    hoverinfo='skip'
                     )
        fig_bar_sel.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
        fig_bar_sel.update_yaxes(title=None)
        fig_bar_sel.update_xaxes(title='% Chinese-spoken population')
        return fig_bar_sel

@app.callback(
    Output('gender', 'figure'),
    Input('map', 'selectedData'), prevent_initial_call=True)
def generate_gender_donut(selectedData):
    if selectedData is None:
        return fig_sex
    else:
        sel = []
        for item in selectedData['points']:
            sel.append(item['location'])
        dff = df_merged[df_merged['LGA_CODE_2021_x'].isin(sel)]
        df_sel = pd.DataFrame({"names": ['Male', 'Female'],
                   "values": [dff['Estimated resident population - males (no.)'].sum(), dff['Estimated resident population - females (no.)'].sum()]})
        df_sel['values'] = df_sel['values'].astype('int')
        fig_sex_sel = px.pie(df_sel,
                            values=df_sel['values'],
                            names=df_sel['names'],
                            hole=.3,
                            title='Gender breakdown, LGA',
                            color=df_sel['names'],
                            color_discrete_map={'Female':'#592c82',
                                                   'Male':'#dbcbee'})
        return fig_sex_sel

@app.callback(
    Output('donut', 'figure'),
    Input('map', 'selectedData'), prevent_initial_call=True)
def generate_donut(selectedData):
    if selectedData is None:
        return fig_donut
    else:
        sel = []
        for item in selectedData['points']:
            sel.append(item['location'])
        dff = df_merged[df_merged['LGA_CODE_2021_x'].isin(sel)]
        df_sel = pd.DataFrame({"names": ['Age 5-19', 'Age 20-64', 'Age 64 +'],
                   "values": [dff['Age 5-19'].sum(), dff['Age 20-64'].sum(), dff['Age 64 +'].sum()]})
        df_sel['values'] = df_sel['values'].astype('int')
        fig_donut_sel = px.pie(df_sel,
                           values=df_sel['values'],
                           names=df_sel['names'],
                           hole=.3,
                           title='Age breakdown, LGA',
                           color=df_sel['names'],
                           color_discrete_map={'Age 5-19':'#592c82',
                                       'Age 20-64':'#8e7cc3ff',
                                       'Age 64 +':'#dbcbee'})
        return fig_donut_sel

@app.callback(
    Output('indicator', 'figure'),
    Input('map', 'selectedData'), prevent_initial_call=True)
def generate_indicator(selectedData):
    if selectedData is None:
        return fig_indicator
    else:
        sel = []
        for item in selectedData['points']:
            sel.append(item['location'])
        dff = df_merged[df_merged['LGA_CODE_2021_x'].isin(sel)]
        fig_indicator_sel = go.Figure()
#        fig_indicator_sel.add_trace(go.Indicator(
#            mode = "number",
#            value = dff['Estimated resident population  (no.)'].sum(),
#            title = {"text": "Population: Overall, LGA<br><span style='font-size:0.8em;color:gray'>"},
#            domain = {'row': 0, 'column': 1}))



        fig_indicator_sel.add_trace(go.Indicator(
            mode = "number",
            value = dff['NATIVE_CHINESE_SPEAKERS'].sum(),
            title = {"text": "(Population: Chinese Speakers, LGA)"},
            #delta = {'reference': total_population, 'relative': True},
            domain = {'x': [0, 1], 'y': [0, 0.2]}
        ))

        #fig_indicator.update_traces(delta_decreasing_symbol=None, selector=dict(type='indicator'))
        #fig_indicator.update_traces(delta_decreasing_color='purple', selector=dict(type='indicator'))

        fig_indicator_sel.add_trace(go.Indicator(
            mode = "number",
            value = dff['Estimated resident population  (no.)'].sum(),
            title = {"text": "Population: Overall, LGA<br><span style='font-size:0.8em;color:gray'>"},
            domain = {'x': [0, 1], 'y': [0.5, 0.8]}
        ))




        return fig_indicator_sel

#app.run_server(debug=True, port=8080, use_reloader=False)
app.run_server()
#application.run(debug=True, port=8080)

