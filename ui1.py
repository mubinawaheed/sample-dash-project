import pandas as pd
import numpy as np
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html, dash_table, State
from dash.dependencies import Input, Output
import plotly_express as px
import pandas_datareader.data as web
import datetime

# start = datetime.datetime(2020, 1, 1)
# end = datetime.datetime(2020, 12, 3)
# df = web.DataReader(["AMZN", "GOOGL", "FB", "PFE", "BNTX", "MRNA"], "stooq", start=start, end=end)
# df=df.stack().reset_index()
# df.to_csv('stock_Data.csv', index=False)

df = pd.read_csv('stock_Data.csv')

display_Data = df.head(8)
symbols = df['Symbols'].unique()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{
                    'name': 'viewport',
                    'content': 'width=device-width, initial-scale:1.0'}])

# layout session
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Stock Market Prediction",
                className='text-center my-3 text-primary'), width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdwn', multi=False, value='AMZN',
                         options=[{'label': k, 'value': k} for k in sorted(symbols)]),
            # offset adds an empty column to the left and shifts your component to the left. It is used to create
            # empty spaces on sides, order specifies the order of component in a column
            dcc.Graph(id='line-figure', figure={})
        ],
            # width={'size':6, 'order':1 },

            # included for different screen sicd ze 12 and 5 are no of columns thats why we comment out wiidth line
            xs=12, sm=12, md=12, lg=6, xl=6),

        dbc.Col([
            dcc.Dropdown(id='my-dpdwn2', multi=True, value=['PFE', 'BNTX'],
                         options=[{'label': i, 'value': i} for i in sorted(symbols)]),
            dcc.Graph(id='line-figure2', figure={}),
            html.Div([
                dbc.Button(
                    "Open collapse", id="collapse-button", className="mx-3 my-2", color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(
                        dash_table.DataTable(
                            id='table',
                            columns=[{'name': t, "id": t} for t in df.columns],
                            data=display_Data.to_dict('records'),
                            style_table={
                                'maxHeight': '300px', 'overflowY': 'scroll', 'overflowX': 'scroll'},
                            style_cell={
                                'padding': '0px', 'font_size': '12px', 'textAlign': 'center'},
                        ),
                    ),
                    id="collapse-div",
                    is_open=False,
                ), ], style={'width': '75%'})
        ],
            # width={'size':6, 'order':2},
            xs=12, sm=12, md=12, lg=6, xl=6),

    ], justify='around'),
    dbc.Row([
        dbc.Col([
            html.P("Select any company stock:", style={
                   "textDecoration": "underline"}),

            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': j, 'value': j} for j in sorted(df['Symbols'].unique())], labelClassName='mr-5 text-success',
                style={'justify-content': 'space-evenly', 'display': 'flex'}),

            dcc.Graph(id='my-hist', figure={}, className='text-center')
        ], xs=12, sm=12, md=12, lg=5, xl=5,
            #  width={'offset':1},
        ),

        dbc.Col([
            dbc.Card(
                [dbc.CardBody(
                    html.P(
                        "We're better together. Help each other out!",
                        className="card-text")
                ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
        ],
            # width={'size':5},
            xs=12, sm=12, md=12, lg=5, xl=5)
    ], align='center')

], fluid=True)

# code for callbacks

@app.callback(
    # they both take 2 arguments component id and component property i.e value
    # jis property ka naam arguments me lkhty hain wohi update hoti ha bs call backs pr. if you want more than one component properties to be altered then specify thier names in the arguments
    # we can have more than 1 outputs as well like this # Output('line-figure', 'figure'), for updating more than one components
    Output('line-figure', 'figure'),
    Input('my-dpdwn', 'value')
)
# the function argument comes from the component property of input i.e. "value"
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln = px.line(dff, x='level_0', y='High')
    # the returned objects are assigned to the component property of Output
    return figln

@app.callback(
    Output("collapse-div", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse-div", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('table', 'data'),
    Input('my-dpdwn2', 'value')
)
def datadisplay(value):
    df_data = df[df['Symbols'].isin(value)]
    df_data = df_data.to_dict('records')
    return df_data

# Line chart - multiple
@app.callback(
    Output('line-figure2', 'figure'),
    Input('my-dpdwn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='level_0', y='Open', color='Symbols')
    # figln2.update_yaxes(showline=True, linewidth=2, linecolor='black')
    # figln2.update_xaxes(showline=True, linewidth=2, linecolor='black')

    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['level_0'] == '2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    fighist.update_yaxes(showline=True, linewidth=2, linecolor='black')
    fighist.update_xaxes(showline=True, linewidth=2, linecolor='black')

    return fighist


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
