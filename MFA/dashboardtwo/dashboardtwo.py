from typing import Any
from flask import Flask, request, session, redirect, url_for, abort, make_response
from dash import Dash, html, dcc,dash
import plotly.graph_objs as go


def dashboardtwo(flask_server):
    app = Dash(server=flask_server, url_base_pathname='/dash2/')

    app.layout = html.Div([
        html.H1('Stock Tickers'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Tesla', 'value': 'TSLA'},
                {'label': 'Apple', 'value': 'AAPL'},
                {'label': 'Coke', 'value': 'COKE'}
            ],
            value='TSLA'
        ),
        dcc.Graph(id='my-graph')
    ], className="container")

    return app