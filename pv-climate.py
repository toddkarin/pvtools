
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
# import flask
# import json
# import time
import datetime
import io
import pvtoolslib
import urllib


from app import app

# app = dash.Dash()
layout = html.Div(children=[
    html.A("download csv", href="/download_csv/"),
    dbc.Button("Download csv",id='download-button',n_clicks=0),
    dbc.Input(id='an_input', value=12345, type='number',
              style={'max-width': 200}),

dcc.Dropdown(
        id='racking_model_xx',
        options=[
            {'label': 'open rack cell glassback',
             'value': 'open_rack_cell_glassback'},
            {'label': 'roof mount cell glassback',
             'value': 'roof_mount_cell_glassback'},
            {'label': 'insulated back polymerback',
             'value': 'insulated_back_polymerback'},
            {'label': 'open rack polymer thinfilm steel',
             'value': 'open_rack_polymer_thinfilm_steel'},
            {'label': '22x concentrator tracker',
             'value': '22x_concentrator_tracker'}
        ],
        value='open_rack_cell_glassback',
        style={'max-width': 500}
    ),
    # dcc.Dropdown(
    #     id='dropdown_unique',
    #     options=pvtoolslib.cec_module_dropdown_list,
    #     value=pvtoolslib.cec_module_dropdown_list[0]['value'],
    #     style={'max-width': 500}
    # ),
])


@app.callback([Output('an_input', 'value')
               ],
              [Input('racking_model_xx', 'value')])
def update_Voco(racking_model):
    print('Racking model changed')
    return 5

#
#
# @app.callback([Output('an_input', 'value')
#                ],
#               [Input('dropdown_unique', 'value')])
# def update_this_div(module):
#     print('Racking model changed')
#     return 5

#
# @app.callback(
#
# @app.callback([],
#               [Input('download-button','n_clicks')])
# def update_Voco(n_clicks,results):
#     print(results)


@app.server.route('/download_csv/')
def download_excel():
    #Create DF
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    #Convert DF
    str_io = io.StringIO()
    df.to_csv(str_io, sep=",")

    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()



    # excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    # df.to_excel(excel_writer, sheet_name="sheet1")
    # excel_writer.save()
    # excel_data = strIO.getvalue()
    # stream.seek(0)

    return flask.send_file(mem,
					   mimetype='text/csv',
					   attachment_filename='downloadFile.csv',
					   as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)