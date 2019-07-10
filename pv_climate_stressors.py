# -*- coding: utf-8 -*-
"""

Example page template for the pvtools site

toddkarin

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
import plotly.colors
import plotly.graph_objs as go
# import plotly.plotly as py
# from flask_caching import Cache
from dash.dependencies import Input, Output, State
import vocmaxlib
import numpy as np
import pvlib
import nsrdbtools
import pandas as pd
# import uuid
# import os
import flask
# import json
# import time
import datetime
import io
import pvtoolslib
import urllib

import pvcz

from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# session_id = str(uuid.uuid4())

layout = dbc.Container([
    html.Hr(),
    html.Div([
        html.H1("Photovoltaic Climate Stressors and Zones"),
    ], style={
        # 'background-color': 'lightblue',
        'width': '100%',
        'padding-left': '10px',
        'padding-right': '10px',
        'textAlign': 'center'}),
    html.Hr(),
    html.H2('Overview'),
    dcc.Markdown("""This is a test deployment of a map showing the 
    photovoltaic climate zones. 

    **We would highly appreciate any feedback** (praise, bug reports, 
    suggestions, etc.). Please contact us at pvtools.lbl@gmail.com. 

    """.replace('    ', '')
                 ),

    dbc.Row([
        dbc.Col([
            dbc.Button("Show me more details",
                       id="pvcz-details-button",
                       color='light',
                       n_clicks=0,
                       className="mb-3"),
        ], width=3)

    ], justify='start'),

    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            dcc.Markdown("""

            ### Summary


            ### Who we are

            We are a collection of national lab researchers funded under the 
            [Durable module materials consortium (DuraMAT)](https://www.duramat.org/). 

            """.format(pvtoolslib.contact_email).replace('    ', '')
                         ),

            dbc.Row([
                dbc.Col(
                    html.Img(
                        src=app.get_asset_url('duramat_logo.png'),
                        style={'height': 50})
                ),
                dbc.Col(
                    html.Img(
                        src=app.get_asset_url('pvlib_logo_horiz.png'),
                        style={'height': 50})
                ),
                dbc.Col(
                    html.Img(
                        src=app.get_asset_url(
                            'LBL_Masterbrand_logo_with_Tagline-01.jpg'),
                        style={'height': 50})
                )
            ], justify='center'
            )
        ])), id="pvcz-details-collapse"
    ),

    # html.H2('Simulation Input'),
    html.P(''),
    html.H2('Photovoltaic climate data points'),
    dcc.Graph(id='pvcz-map',
              figure={
                  'data': [
                      go.Scattermapbox(
                          lat=pvcz.get_pvcz_data()['lat'],
                          lon=pvcz.get_pvcz_data()['lon'],
                          mode='markers',
                          marker=dict(
                              color=pvcz.get_pvcz_data()['T_equiv_rack'],
                              colorscale=[
                                  [0, "rgb(150,0,90)"],
                                  [0.125, "rgb(0, 0, 200)"],
                                  [0.25, "rgb(0, 25, 255)"],
                                  [0.375, "rgb(0, 152, 255)"],
                                  [0.5, "rgb(44, 255, 150)"],
                                  [0.625, "rgb(151, 255, 0)"],
                                  [0.75, "rgb(255, 234, 0)"],
                                  [0.875, "rgb(255, 111, 0)"],
                                  [1, "rgb(255, 0, 0)"]
                              ],
                              size=6
                          ),
                          text='T_equiv_rack: ' + pvcz.get_pvcz_data()[
                              'T_equiv_rack'].astype(str) + ' C',
                          name='Database location'
                      ),
                  ],
                  'layout': go.Layout(
                      # autosize=True,
                      width=1000,
                      height=700,
                      margin={'l': 10, 'b': 10, 't': 0, 'r': 0},
                      hovermode='closest',
                      mapbox=dict(
                          accesstoken='pk.eyJ1IjoidG9kZGthcmluIiwiYSI6Ik1aSndibmcifQ.hwkbjcZevafx2ApulodXaw',
                          bearing=0,
                          center=dict(
                              lat=float(40),
                              lon=float(-100)
                          ),
                          pitch=0,
                          zoom=2,
                          style='light'
                      ),
                      legend=dict(
                          x=0,
                          y=1,
                          traceorder='normal',
                          font=dict(
                              family='sans-serif',
                              size=12,
                              color='#000'
                          ),
                          bgcolor='#E2E2E2',
                          bordercolor='#FFFFFF',
                          borderwidth=2
                      )
                  )}

              )

])

# app.layout = layout


@app.callback(
    Output("pvcz-details-collapse", "is_open"),
    [Input("pvcz-details-button", "n_clicks")],
    [State("pvcz-details-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#
# if __name__ == '__main__':
#     app.run_server(debug=True)