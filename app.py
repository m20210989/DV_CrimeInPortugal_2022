import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import urllib.request, json

from pandas import DataFrame, Series
from pandas.core.generic import NDFrame

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Dataset Processing

with open('NUTS_2.geojson', encoding='utf-8') as json_file:
    NUTS2 = json.load(json_file)

with open('NUTS_3.geojson', encoding='utf-8') as json_file:
    NUTS3 = json.load(json_file)

with open('NUTS_1.geojson', encoding='utf-8') as json_file:
    NUTS1 = json.load(json_file)

df = pd.read_excel('DS_DV_Final_12_04_22.xlsx', sheet_name='Folha1')
df1 = pd.read_excel('DS_DV_onlycrime_Final.xlsx')
df2 = pd.read_excel('DS_DV_Final_12_04_22.xlsx', sheet_name='scatterplot')


region_options = [
    dict(label=region, value=region)
    for region in df['Location'].unique()]

selections = set()
selections2 = set()

crime_options = [
    {'label': 'Overall', 'value': 'Crimes Overall total (‰)'},
    {'label': 'Assault', 'value': 'Crimes of assault (‰)'},
    {'label': 'Theft/purse', 'value': 'Theft/purse snatching (‰)'},
    {'label': 'Theft in motor vehicles', 'value': 'Theft of and from motor vehicles (‰)'},
    {'label': 'Drunk driving', 'value': 'Driving with a blood alcohol equal or above 1,2 g/l (‰)'},
    {'label': 'No license driving', 'value': 'Driving without legal documentation (‰)'},
    {'label': 'Against Patrimony', 'value': 'Crimes against patrimony (‰)'}
]

# Requirements for the dash core components

slider_year = dcc.Slider(
        id='year_slider',
        min=2016,
        max=2020,
        value=2016,
        marks={str(year): str(year) for year in df['Year'].unique()},
        included=False,
        step=1
    )

dropdown_crime = dcc.Dropdown(
        id='crime_options',
        options=crime_options,
        value='Crimes Overall total (‰)'
    )

dropdown_tabs = dcc.Tabs(id="tabs_NUTS", value='I', children=[
                dcc.Tab(label='NUTS I', value='I'),
                dcc.Tab(label='NUTS II', value='II'),
                dcc.Tab(label='NUTS III', value='III'),
    ])

# STYLES

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '30%',
    'padding': '20px 10px',
    'background-color': '#69140f'
}

CONTENT_STYLE = {
    'margin-left': '35%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#333333'
}

# App

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server

sidebar = html.Div(
    [
        html.H3('Choose the crime category, year and region you want to explore...', style={'margin': '5px', 'color': '#ffffff', 'font-size': '30px', 'text-align': 'center'}),
        html.Br(),
        html.Label('Crime categories', style={"font-weight": "bold", 'color': '#ffffff'}),
        dropdown_crime,
        html.Br(),
        html.Label('Year', style={"font-weight": "bold", 'color': '#ffffff'}),
        slider_year,
        html.Br(),
        dropdown_tabs,
        # MAP
        dcc.Graph(id='Portugal Crime',
                  # click data
                  clickData={'points': [{'hovertext': 'Continente'}]}
                  ),
    ],
    style=SIDEBAR_STYLE
)

content_first_row = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Maximum", className="card-title"),
                    html.P(
                        "Maximum region",
                        className="card-text",
                        id='card_1',
                    ),
                    html.P(
                        "Maximum value",
                        className="card-text",
                        id='card_2',
                    ),
                ]
            ), className='card_style', style={"width": "25rem", 'text-align': 'center'},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("National Crime Rate", className="card-title"),
                    html.P(
                        "Portugal crime rate",
                        className="card-text",
                        id='card_3',
                    ),
                ]
            ), className='card_style', style={"width": "25rem", 'text-align': 'center'},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Minimum", className="card-title"),
                    html.P(
                        "Minimum region",
                        className="card-text",
                        id='card_4',
                    ),
                    html.P(
                        "Minimum crime rate",
                        id='card_5',
                        className="card-text",
                    ),
                ]
            ), className='card_style', style={"width": "25rem", 'text-align': 'center'},
        ),
    ], id='1th row', style={'display': 'flex', 'justify-content': 'center'}
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1', className='graph_1'), md=12
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_2'), md=12
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_3'), md=12
        )
    ]
)

content_fifth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12
        )
    ]
)

content = html.Div(
    [
        html.H1('Crime in Portugal: uphill or downhill?'),
        html.Br(),
        dbc.Row(content_first_row),
        html.Hr(),
        dbc.Row(content_second_row),
        html.Br(),
        dbc.Row(content_third_row),
        html.Br(),
        dbc.Row(content_fourth_row),
        html.Br(),
        dbc.Row(content_fifth_row),
        html.Br(),
        html.H6(['Authors: Carolina Rodrigues(20211298), Elena Nozal(20210989), Elsa Camuamba(20210992) and Manuel Pedro(20210999)', html.Br(), 'Source: Instituto Nacional de Estatística (INE)'], style={'font-size': '15px'}),
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([sidebar, content])

# Callbacks

##MAP##
@app.callback(
    Output(component_id='Portugal Crime', component_property='figure')
    ,
    [
        Input(component_id='year_slider', component_property='value'),
        Input(component_id="crime_options", component_property='value'),
        Input(component_id="tabs_NUTS", component_property='value'),
        Input(component_id='Portugal Crime', component_property='clickData')
    ]
)
def update_map(year, crime, tab, clickData):
    print(clickData['points'][0]['hovertext'])


    ds = df.copy()
    ds = ds[ds['Year'] == year]

    if tab == "I":
        choropleth = px.choropleth_mapbox(ds[ds['NUTS'] == "I"], geojson=NUTS1, locations='ID', color=crime,
                                          color_continuous_scale="RdBu",
                                          # range_color=(20, 60),
                                          mapbox_style="white-bg",
                                          zoom=4, center={"lat": 39.6505, "lon": -8.13022}, opacity=0.5,
                                          hover_name=ds[ds['NUTS'] == "I"]['Location'],
                                          hover_data=[crime,
                                                      'Median value per m2 of dwellings sales (€)'
                                                      ],
                                          labels={'Crimes Overall total (‰)': 'Rate',
                                                  'Crimes of assault (‰)': 'Rate',
                                                  'Theft/purse snatching (‰)': 'Rate',
                                                  'Theft of and from motor vehicles (‰)': 'Rate',
                                                  'Driving a motor vehicle with a blood alcohol equal or above 1,2 g/l (‰)': 'Rate',
                                                  'Driving without legal documentation (‰)': 'Rate',
                                                  'Crimes against patrimony (‰)': 'Rate',
                                                  'Median value per m2 of dwellings sales (€)':
                                                      'Median house value per ㎡ (€)'})
    elif tab == "II":
        choropleth = px.choropleth_mapbox(ds[ds['NUTS'] == "II"], geojson=NUTS2, locations='ID', color=crime,
                                          color_continuous_scale="RdBu",
                                          # range_color=(20, 60),
                                          mapbox_style="white-bg", zoom=4, center={"lat": 39.6505, "lon": -8.13022},
                                          opacity=0.5, hover_name=ds[ds['NUTS'] == "II"]['Location'],
                                          hover_data=[crime,
                                                      'Median value per m2 of dwellings sales (€)'
                                                      ],
                                          labels={'Crimes Overall total (‰)': 'Rate',
                                                  'Crimes of assault (‰)': 'Rate',
                                                  'Theft/purse snatching (‰)': 'Rate',
                                                  'Theft of and from motor vehicles (‰)': 'Rate',
                                                  'Driving a motor vehicle with a blood alcohol equal or above 1,2 g/l (‰)': 'Rate',
                                                  'Driving without legal documentation (‰)': 'Rate',
                                                  'Crimes against patrimony (‰)': 'Rate',
                                                  'Median value per m2 of dwellings sales (€)':
                                                      'Median house value per ㎡ (€)'})
    elif tab == "III":
        choropleth = px.choropleth_mapbox(ds[ds['NUTS'] == "III"], geojson=NUTS3, locations='ID', color=crime,
                                          color_continuous_scale="RdBu",
                                          # range_color=(20, 60),
                                          mapbox_style="white-bg", zoom=4, center={"lat": 39.6505, "lon": -8.13022},
                                          opacity=0.5, hover_name=ds[ds['NUTS'] == "III"]['Location'],
                                          hover_data=[crime,
                                                      'Median value per m2 of dwellings sales (€)'
                                                      ],
                                          labels={'Crimes Overall total (‰)': 'Rate',
                                                  'Crimes of assault (‰)': 'Rate',
                                                  'Theft/purse snatching (‰)': 'Rate',
                                                  'Theft of and from motor vehicles (‰)': 'Rate',
                                                  'Driving a motor vehicle with a blood alcohol equal or above 1,2 g/l (‰)': 'Rate',
                                                  'Driving without legal documentation (‰)': 'Rate',
                                                  'Crimes against patrimony (‰)': 'Rate',
                                                  'Median value per m2 of dwellings sales (€)':
                                                      'Median house value per ㎡ (€)'})

    choropleth.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                             clickmode='event')
    return choropleth


## TIMESERIES ##
@app.callback(
    Output('graph_1', 'figure'),
    [
        Input(component_id='Portugal Crime', component_property='clickData'),
        Input(component_id="crime_options", component_property='value'),
    ]
)
def update_graph1(clickData, crime):
    filtered_by_year_df = df[(df['Year'] >= 2011) & (df['Year'] <= 2020)]

    scatter_data = []

    if clickData is not None:
        location = clickData['points'][0]['hovertext']

        if location not in selections2:
            selections2.add(location)
        else:
            selections2.remove(location)

    for i in selections2:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['Location'] == i]

        temp_data = dict(
            type='scatter',
            y=filtered_by_year_and_country_df[crime],
            x=filtered_by_year_and_country_df['Year'],
            name=i
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title=crime),
                          title='How have crime rates evolved along the years?<br><sup> - select a crime category and/or a region to learn more! </sup>',
                          plot_bgcolor='rgba(0,0,0,0)'
    )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)
    fig.update_xaxes(showline=True, linewidth=1, gridcolor='#f6f5f5')
    fig.update_yaxes(showline=True, linewidth=1, gridcolor='#f6f5f5')

    return fig

## BAR PLOT ##
@app.callback(
    Output('graph_2', 'figure'),
    [
        Input(component_id="year_slider", component_property='value'),
        Input(component_id='Portugal Crime', component_property='clickData'),
    ]
)
def update_graph2(year, clickData):
    dff = df1.loc[(df1['Year'] >= year-2) & (df1['Year'] <= year)]
    dff1 = dff.loc[dff['Location'] == clickData['points'][0]['hovertext']]
    dff1 = dff1.astype({"Year": object})

    barchart = px.bar(
        data_frame=dff1,
        x="Category",
        y="Value",
        color='Year',
        text='Value',
        labels={'Value': 'Crime Rate (‰)'},
        color_discrete_sequence=['#5e2121','#852e2e','#ac3a3a'],
        barmode='group',
        title='In which year and region was the ‘no license driving’ rate the lowest?<br><sup> - select a region or a year to find out! </sup>',
        )
    barchart.update_layout(xaxis={'categoryorder': 'total descending'},
                           plot_bgcolor='rgba(0,0,0,0)')
    barchart.update_traces(textposition='outside')

    return barchart

## SCATTER PLOT ## (filtered by years)
@app.callback(
    Output('graph_3', 'figure'),
    [
        Input(component_id="year_slider", component_property='value'),
        Input(component_id="crime_options", component_property='value'),
    ]
)
def update_graph3(year, crime):
    graph3_filter = df2.loc[df2['Year'] == year]

    scatterplot = px.scatter(
        data_frame=graph3_filter,
        x='Median value per m2 of dwellings sales (€)',
        y=graph3_filter[crime],
        hover_data=['Location'],
        color='NUTS II',
        title='Is there a relationship between a given crime category and house prices?<br><sup> - select a crime category and/or a year to find out! </sup>'
        )

    scatterplot.update_xaxes(showline=True, linewidth=2, gridcolor='#f6f5f5')
    scatterplot.update_yaxes(showline=True, linewidth=2, gridcolor='#f6f5f5')
    scatterplot.update_traces(marker_size=9)
    scatterplot.update_layout(yaxis=dict(title=crime), plot_bgcolor='rgba(0,0,0,0)')

    return scatterplot

## SUNBURST ##
@app.callback(
    Output('graph_4', 'figure'),
    [
        Input(component_id="year_slider", component_property='value'),
    ]
)
def update_graph4(selected_year):
    sunburst_data = df.loc[df['Year'] == selected_year].dropna(subset='NUTS I')
    fig = px.sunburst(sunburst_data, path=['NUTS I', 'NUTS II', 'NUTS III'],
                          values='Crimes Overall total (‰)', color='Median value per m2 of dwellings sales (€)',
                          hover_data=['Year', 'NUTS I', 'NUTS II', 'Crimes Overall total (‰)',
                                  'Median value per m2 of dwellings sales (€)'],
                          labels={'Median value per m2 of dwellings sales (€)': 'Median house value per ㎡ (€)'},
                          color_continuous_scale='RdBu', color_continuous_midpoint=np.average(sunburst_data['Median value per m2 of dwellings sales (€)'], weights=sunburst_data['Crimes Overall total (‰)']))
    fig.update_traces(
        go.Sunburst(
            hovertemplate="""Year: %{customdata[0]} <br>NUTS I: %{customdata[1]} 
    <br>NUTS II: %{customdata[2]} <br>Crimes Rate total (‰)': %{customdata[3]} <br>Median house value per ㎡ (€): %{customdata[4]}""",
            insidetextorientation="radial"
        )
    )
    fig.update_layout(dict(title=dict(text='Are high house prices synonymous with low crime regions?<br><sup> - select a year and click on the figure to learn more! </sup>'),
                           margin=dict(t=90, l=0, r=0, b=0),
                           uniformtext=dict(minsize=6, mode='hide'),
                           )
                      )
    return fig


# Card callbacks
@app.callback(
    [
        Output("card_1", "children"),
        Output("card_2", "children"),
        Output("card_3", "children"),
        Output("card_4", "children"),
        Output("card_5", "children")
    ],
    [
        Input(component_id="year_slider", component_property='value'),
        Input(component_id="crime_options", component_property='value'),
        Input(component_id="tabs_NUTS", component_property='value'),
    ]
)
def update_card_text(year, crime, tab):

    if tab == "III":
        dff = df.loc[df['Year'] == year]
        dff0 = dff.loc[dff['NUTS']=="III"]

        value_1 = round(max(dff0[crime]), 2)
        label_1 = dff0.loc[dff0[crime] == value_1, 'Location'].iloc[0]
        value_2 = round(min(dff0[crime]), 2)
        label_2 = dff0.loc[dff0[crime] == value_2, 'Location'].iloc[0]
        dff1= dff.loc[dff['Location'] == 'Portugal']
        value_3 = round(dff1[crime].iloc[0], 2)


    elif tab == "II":
        dff = df.loc[df['Year'] == year]
        dff0 = dff.loc[dff['NUTS']=="II"]

        value_1 = round(max(dff0[crime]), 2)
        label_1 = dff0.loc[dff0[crime] == value_1, 'Location'].iloc[0]
        value_2 = round(min(dff0[crime]), 2)
        label_2 = dff0.loc[dff0[crime] == value_2, 'Location'].iloc[0]
        dff1= dff.loc[dff['Location'] == 'Portugal']
        value_3 = round(dff1[crime].iloc[0], 2)

    elif tab == "I":
        dff = df.loc[df['Year'] == year]
        dff0 = dff.loc[dff['NUTS']=="I"]

        value_1 = round(max(dff0[crime]), 2)
        label_1 = dff0.loc[dff0[crime] == value_1, 'Location'].iloc[0]
        value_2 = round(min(dff0[crime]), 2)
        label_2 = dff0.loc[dff0[crime] == value_2, 'Location'].iloc[0]
        dff1= dff.loc[dff['Location'] == 'Portugal']
        value_3 = round(dff1[crime].iloc[0], 2)



    return label_1, str(value_1)+'‰', str(value_3)+'‰', label_2, str(value_2)+'‰'


if __name__ == '__main__':
    app.run_server(debug=True)