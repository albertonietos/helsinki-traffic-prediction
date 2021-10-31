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
import joblib

from utils import *

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

# Clean traffic data set
data = pd.read_csv('clean_traffic.csv')
model = joblib.load('./model/forest_model_compressed.pkl')

prediction_card = dbc.Card([
    dbc.CardHeader('Traffic Prediction'),
    dbc.CardBody(
        [
            html.H5('Select date, time and direction of travel'),
            dbc.Label('Date:', html_for='date-input', width=2),
            dcc.DatePickerSingle(
                id='date-input',
                min_date_allowed=date(2019, 1, 1),
                max_date_allowed=date(2025, 1, 1),
                initial_visible_month=date(2021, 12, 12),
                display_format='D.M.Y',
                first_day_of_week=1,
                date=date(2021, 12, 12)
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
                    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
                    9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
                    16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'
                },
                value=16
            ),
            html.Br(),
            dbc.Label("Direction:", html_for='direction-input', width=4),
            dbc.Col(
                dbc.RadioItems(
                    id='direction-input',
                    options=[
                        {"label": "Towards city centre", "value": 1},
                        {"label": "Towards outskirts", "value": 2}
                    ],
                    value=1,
                ),
                width=7,
            ),
            html.Hr(),
            html.P(id='result'),
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

car_plot_card = dbc.Card(
    [
        dbc.CardHeader('Historic records of cars on the road'),
        dbc.CardBody(
            [
                dcc.Graph(
                id='cars-graph',
            )
            ]
        )
    ]
)

app.layout = dbc.Container(children=[
    html.H1(children='Helsinki Traffic monitoring with Machine Learning'),
    html.Hr(),
    html.H4(children='HTML: A web application to support your transportation needs'),
    html.P(children='A pilot study for the Munkkiniemi neighbourhood in Helsinki'),
    html.Br(),
    dbc.Row([
        dbc.Col([prediction_card], width=5),
        dbc.Col(card_transportation_means, width=7)
        ]),
    car_plot_card
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-transportation-means', 'active_tab'))
def render_content(tab):
    if tab == 'car-map':
        return html.Iframe(src="assets\Car_travel_time_to_5986740.html",
            style={"height": "500px", "width": "100%"})
    elif tab == 'public-transport-map':
        return html.Iframe(src=f"assets\Public_travel_time_to_5986740.html",
            style={"height": "500px", "width": "100%"})
    elif tab == 'bike-map':
        return html.Iframe(src=f"assets\Bike_travel_time_to_5986740.html",
            style={"height": "500px", "width": "100%"})
    elif tab == 'walk-map':
        return html.Iframe(src=f"assets\Walk_travel_time_to_5986740.html",
            style={"height": "500px", "width": "100%"})
    else:
        return html.Iframe(src="assets\Car_travel_time_to_5986740.html",
            style={"height": "500px", "width": "100%"})

@app.callback(
    Output(component_id='result', component_property='children'),
    Input(component_id='date-input', component_property='date'),
    Input(component_id='hour-input', component_property='value'),
    Input(component_id='direction-input', component_property='value'))
def update_model_output(date_input, hour_input, direction_input):
    try:
        input = preprocess_input(date_input, hour_input, direction_input)
        output = int(model.predict(input)[0])
        lower_bound = np.maximum(output - 155, 0) # can not be less than zero
        upper_bound = output + 155
        prediction = f'The predicted number of cars on the road is {output}.'
        confidence_interval = f'The 97.5% confidence interval is [{lower_bound},{upper_bound}].'
        interpretation = 'This means that there is a 97.5% probability that the true value is within those bounds.'
        return (html.H6(prediction), html.H6(confidence_interval), html.P(interpretation))
    except ValueError:
        return 'Error in prediction'

@app.callback(
    Output('cars-graph', 'figure'),
    Input(component_id='date-input', component_property='date'),
    Input(component_id='hour-input', component_property='value')
)
def update_graph(date_input, hour_input):
    timestamp = pd.to_datetime(date_input)

    date_data = data[(data.month == timestamp.month) & (data.day == timestamp.day)].copy()
    date_data.direction.replace([1, 2], ['Centre', 'Outskirts'], inplace=True)

    fig = px.line(date_data, x='hour', y='value', color='year', facet_col="direction", #line_dash='direction',
                  labels={"year": "Year", "direction": "Direction", "hour": "Hour"},
                  line_shape='spline')
    fig.add_vline(x=hour_input, line_width=2, line_dash="dash", line_color="grey")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      yaxis_title="Number of cars")

    return fig

if __name__ == '__main__':
    model = joblib.load('./model/forest_model_compressed.pkl')
    app.run_server(debug=True)