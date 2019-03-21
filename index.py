

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# # import dash_table
# import plotly.colors
# import plotly.graph_objs as go
# # import plotly.plotly as py
# from flask_caching import Cache
from dash.dependencies import Input, Output, State
# import vocmaxlib
# import numpy as np
# import pvlib
# import nsrdbtools
# import pandas as pd
# import uuid
# import os
# import flask
# import json
# import time
# import datetime

from app import app

# Line is important for Heroku.
server = app.server


# session_id = str(uuid.uuid4())
# mapbox_access_token = 'pk.eyJ1IjoidG9kZGthcmluIiwiYSI6Ik1aSndibmcifQ.hwkbjcZevafx2ApulodXaw'


# import home, string_length_calculator
import home, pvcz

# # Cache for saving local files.
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'redis',
#     # Note that filesystem cache doesn't work on systems with ephemeral
#     # filesystems like Heroku.
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory',
#
#     # should be equal to maximum number of users on the app at a single time
#     # higher numbers will store more data in the filesystem / redis cache
#     'CACHE_THRESHOLD': 200
# })
#
#

# NSRDB_pickle_database = '/Users/toddkarin/Documents/NSRDB_pickle/'




app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',children=[home.layout])
])


header = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(
                src=app.get_asset_url('LBL_Masterbrand_logo_with_Tagline-01.jpg'),
                style={'height': 50})
            ],width=4),
        dbc.Col([
            html.Img(
                src=app.get_asset_url('duramat_logo.png'),
                style={'height': 50})
            ],width=4)

        ],justify='between')
])

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Tools",
            children=[
                dbc.DropdownMenuItem("String Length Calculator",href='/string-length-calculator'),
                dbc.DropdownMenuItem("Photovoltaic Climate Zones"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Documentation"),
            ],
        ),
        dbc.NavItem(dbc.NavLink("Contact", href="#")),
    ],
    brand="PVTOOLS",
    brand_href="/",
    sticky="top",
)





@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/string-length-calculator':
        body = pvcz.layout
        # body = string_length_calculator.layout
    elif pathname == 'PVCZ':
        body = pvcz.layout
    elif pathname == '/home':
        body = home.layout
    elif pathname == '/':
        body = home.layout
    else:
        body = '404'

    return [header, navbar, body]

if __name__ == '__main__':
    app.run_server(debug=True)