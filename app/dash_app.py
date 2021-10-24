# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.html.P import P
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import date

from utils import *

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

prediction_card = dbc.Card([
    dbc.CardHeader('Traffic Prediction'),
    dbc.CardBody(
        [
            html.H5('Select date and time of travel'),
            dbc.Label('Date:', html_for='date-input', width=1),
            dcc.DatePickerSingle(
                id='date-input',
                min_date_allowed=date(2019, 1, 1),
                max_date_allowed=date(2025, 1, 1),
                initial_visible_month=date(2021, 11, 1),
                display_format='D.M.Y',
                first_day_of_week=1,
                date=date(2021, 11, 1)
            ),
            html.Br(),
            html.Br(),
            html.P('Hour of the day:'),
            dcc.Slider(
                id='hour-input',
                min=0,
                max=23,
                step=None,
                marks={
                    0: '0',
                    1: '1',
                    2: '2',
                    3: '3',
                    4: '4',
                    5: '5',
                    6: '6',
                    7: '7',
                    8: '8',
                    9: '9',
                    10: '10',
                    11: '11',
                    12: '12',
                    13: '13',
                    14: '14',
                    15: '15',
                    16: '16',
                    17: '17',
                    18: '18',
                    19: '19',
                    20: '20',
                    21: '21',
                    22: '22',
                    23: '23'
                },
                value=16
            ),
            html.Br(),
            dbc.Label("Direction:", html_for='direction-input', width=2),
            dbc.Col(
                dbc.RadioItems(
                    id='direction-input',
                    options=[
                        {"label": "Towards city centre", "value": 0},
                        {"label": "Towards outskirts", "value": 1}
                    ],
                ),
                width=5,
            ),
            html.Hr(),
            html.H5('Predicted number of cars on the road'),
            html.P('Output of model:'),
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ]
    )
])

card_transportation_means = dbc.Card(
    [
        dbc.CardHeader('Travel time estimation based on historic records'),
        dbc.CardBody(
            [
                dbc.Tabs(id="tabs-transportation-means", active_tab='tab-1-example-graph', children=[
                    dbc.Tab(label='Car', tab_id='car-map'),
                    dbc.Tab(label='Public transport', tab_id='public-transport-map'),
                    dbc.Tab(label='Bike', tab_id='bike-map'),
                    dbc.Tab(label='On foot', tab_id='walk-map'),
                ]),
                html.Div(id='tabs-content-example-graph')
            ]
        )
    ]
)

app.layout = dbc.Container(children=[
    html.H1(children='Helsinki Traffic monitoring with Machine Learning'),
    html.Hr(),
    html.H4(children='HTML: A web application to support your transportation needs'),
    html.Br(),
    dbc.Row([
        dbc.Col(prediction_card, width=5),
        dbc.Col(card_transportation_means, width=7)
        ])
    # dcc.RadioItems(
    #     options=[
    #         {'label': 'Car', 'value': 'Car'},
    #         {'label': 'Public transport', 'value': 'Public'},
    #         {'label': 'Bike', 'value': 'bike'},
    #         {'label': 'On foot', 'value': 'walk'}
    #     ],
    #     value='transport',
    #     labelStyle={'display': 'block'},
    #     id='my-input'
    # ),
    # dbc.Tabs(id="tabs-transportation-means", active_tab='tab-1-example-graph', children=[
    #     dbc.Tab(label='Car', tab_id='car-map'),
    #     dbc.Tab(label='Public transport', tab_id='public-transport-map'),
    #     dbc.Tab(label='Bike', tab_id='bike-map'),
    #     dbc.Tab(label='On foot', tab_id='walk-map'),
    # ]),
    # html.Div(id='tabs-content-example-graph'),
    # html.Div(id='my-output'),
    # html.Iframe(src=f"assets\Car_travel_time_to_5986753.html",
    #         style={"height": "600px", "width": "50%"}),
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-transportation-means', 'active_tab'))
def render_content(tab):
    if tab == 'car-map':
        return html.Iframe(src="assets\Car_travel_time_to_5986753.html",
            style={"height": "500px", "width": "100%"})
    elif tab == 'public-transport-map':
        return html.Iframe(src=f"assets\Public_travel_time_to_5986753.html",
            style={"height": "500px", "width": "100%"})
    else:
        return html.Iframe(src="assets\Car_travel_time_to_5986753.html",
            style={"height": "500px", "width": "100%"})

if __name__ == '__main__':
    app.run_server(debug=True)