# -*- coding: utf-8 -*-
"""

This script builds a Dash web application for finding maximum module Voc.

Todd Karin

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# import dash_table
import plotly.colors
import plotly.graph_objs as go
# import plotly.plotly as py
from flask_caching import Cache
from dash.dependencies import Input, Output, State
import vocmaxlib
import numpy as np
import pvlib
import nsrdbtools
import pandas as pd
# import uuid
import os
import flask
import json
import time
import datetime
import io
import pvtoolslib


from app import app

# mapbox_access_token = 'pk.eyJ1IjoidG9kZGthcmluIiwiYSI6Ik1aSndibmcifQ.hwkbjcZevafx2ApulodXaw'

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# session_id = str(uuid.uuid4())

layout = dbc.Container([
    html.Hr(),
    html.Div([
        html.H1("Photovoltaic Maximum Open Circuit Voltage"),
    ], style={
        # 'background-color': 'lightblue',
        'width': '100%',
        'padding-left': '10px',
        'padding-right': '10px',
        'textAlign': 'center'}),
    html.Hr(),
    # html.Div(str(uuid.uuid4()), id='session-id', style={'display': 'none'}),
    html.Div(id='click-data', style={'display': 'none'}),
    html.H2('Overview'),
    # html.H1(
    #     children='Photovoltaic String Length Based on Historical Weather',
    #     style={
    #         'textAlign': 'left'
    #     }
    # ),
    html.P("""The maximum open circuit voltage (Voc) is a key design 
    parameter for solar power plants. This application provides an 
    industry-standard method for calculating the maximum open circuit voltage 
    given weather data and module parameters. Weather data is sourced from the 
    national solar radiation database (NSRDB) [1]. The open circuit voltage 
    is calculated using the Sandia PV models [2] as implemented in the open 
    source python library PVLIB [3]. This work is funded by the Duramat 
    consortium [4]. 

    """),
    html.H2('Methods'),
    html.P("""The national electric code 2017 lists three different methods 
    for determining the maximum string length in Article 690.7:

    """),
    html.Ol([
        html.Li("""690.7(A)(1) Instruction in listing or labeling of module: 
        The sum of the PV module-rated open-circuit voltage of the 
        series-connected modules corrected for the lowest expected ambient 
        temperature using the open-circuit voltage temperature coefficients 
        in accordance with the instructions included in the listing or 
        labeling of the module. 

        """),
        html.Li("""690.7(A)(2) Crystalline and multicrystalline modules: For 
        crystalline and multicrystalline silicon modules, the sum of the PV 
        module-rated open-circuit voltage of the series-connected modules 
        corrected for the lowest expected ambient temperature using the 
        correction factor provided in Table 690.7(A). 

        """),
        html.Li("""690.7(A)(3) PV systems of 100 kW or larger: For PV systems 
        with a generating capcity of 100 kW or greater, a documented and 
        stamped PV system design, using an industry standard method and 
        provided by a licensed professional electrical engineer, shall be 
        permitted. 

        """)

    ], style={'marginLeft': 50}),

    html.P("""This tool provides information for methods 690.7(A)(1) and 
    690.7(A)(3). For method 690.7(A)(1), The lowest expected ambient 
    temperature is calculated by finding the minimum temperature during 
    daylight hours, defined as GHI>150 W/m^2. 

    """),
    html.P("""For method 690.7(A)(3), a full PVLIB model is run using weather 
    data from the selected location and module parameters. Module parameters 
    are either taken from database values or entered manually.

    """),

    # html.H2('Simulation Input'),
    html.H2('Weather'),

    html.P(
        'Enter Latitude and longitude to set target point for weather data.'),
    html.Table([
        html.Tr([
            html.Td([
                html.P('Latitude'),
                dbc.Input(id='lat', value='37.88', type='text')
            ]),
            html.Td([
                html.P('Longitude'),
                dbc.Input(id='lon', value='-122.25', type='text')
            ]),
            html.Td([
                html.P('Get Data'),
                dbc.Button(id='get-weather', n_clicks=0,
                           children='Show Map')
            ])
        ])
    ]),
    # html.Label('Latitude (degrees)'),
    # dbc.Input(id='lat', value=37.88, type='number'),
    # html.Label('Longitude (degrees)'),
    # dbc.Input(id='lon', value=-122.25, type='number'),
    # html.Div(
    #     'Press button to get closest weather data to target point'),
    # dbc.Button(id='get-weather', n_clicks=0,
    #             children='Get Weather Data'),
    html.Div(id='closest-message',
             children='Closest point shown on map'),
    html.Div(id='location-map', children=[
        dcc.Graph(id='map')
    ],
             style={'align': 'left'}),
    html.H2('Simulation Parameters'),

    html.Label('Choose module to get library values for simulation'),
    dcc.Dropdown(
        id='module_name',
        options=vocmaxlib.get_sandia_module_dropdown_list(),
        value=vocmaxlib.get_sandia_module_dropdown_list()[0]['value'],
        style={'max-width': 500}
    ),
    html.Label('Choose racking model to get library values for simulation'),
    dcc.Dropdown(
        id='racking_model',
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

    html.Label('Choose fixed tilt or single axis tracker'),
    dbc.Tabs([
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [dbc.Label('Surface Tilt (degrees)'),
                     dbc.Input(id='surface_tilt', value='30', type='text',
                               style={'max-width': 200}),

                     dbc.Label('Surface Azimuth (degrees)'),
                     dbc.Input(id='surface_azimuth', value='180', type='text',
                               style={'max-width': 200})],
                    dbc.FormText("""For module face oriented due South use 180. 
                For module face oreinted due East use 90"""),
                )
            )
        ], tab_id='fixed_tilt', label='Fixed Tilt'),
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [dbc.Label('Axis Tilt (degrees)'),
                     dbc.Input(id='axis_tilt', value='0', type='text',
                               style={'max-width': 200}),
                     dbc.FormText("""The tilt of the axis of rotation (i.e, 
                the y-axis defined by axis_azimuth) with respect to 
                horizontal, in decimal degrees."""),
                     dbc.Label('Axis Azimuth (degrees)'),
                     dbc.Input(id='axis_azimuth', value='0', type='text',
                               style={'max-width': 200}),
                     dbc.FormText("""A value denoting the compass direction along 
                which the axis of rotation lies. Measured in decimal degrees 
                East of North."""),
                     dbc.Label('Max Angle (degrees)'),
                     dbc.Input(id='max_angle', value='90', type='text',
                               style={'max-width': 200}),
                     dbc.FormText("""A value denoting the maximum rotation angle, 
                in decimal degrees, of the one-axis tracker from its 
                horizontal position (horizontal if axis_tilt = 0). A 
                max_angle of 90 degrees allows the tracker to rotate to a 
                vertical position to point the panel towards a horizon. 
                max_angle of 180 degrees allows for full rotation."""),
                     dbc.Label('Backtrack'),
                     dbc.FormText("""Controls whether the tracker has the 
                 capability to ''backtrack'' to avoid row-to-row shading. False 
                 denotes no backtrack capability. True denotes backtrack 
                 capability."""),
                     dbc.RadioItems(
                         options=[
                             {"label": "True", "value": True},
                             {"label": "False", "value": False},
                         ],
                         value=True,
                         id="backtrack",
                     ),
                     dbc.Label('Ground Coverage Ratio'),
                     dbc.Input(id='ground_coverage_ratio', value='0.286',
                               type='text',
                               style={'max-width': 200}),
                     dbc.FormText("""A value denoting the ground coverage ratio 
                 of a tracker system which utilizes backtracking; i.e. the 
                 ratio between the PV array surface area to total ground 
                 area. A tracker system with modules 2 meters wide, centered 
                 on the tracking axis, with 6 meters between the tracking 
                 axes has a gcr of 2/6=0.333. If gcr is not provided, 
                 a gcr of 2/7 is default. gcr must be <=1"""),
                     ]
                )
            )
        ], tab_id='single_axis_tracker', label='Single Axis Tracker')
    ], id='mount_type', active_tab='fixed_tilt'),

    dbc.Label('Max string voltage (V)'),
    dbc.Input(id='max_string_voltage',
              value=1500,
              type='number',
              style={'max-width': 200}),
    dbc.FormText('Maximum string voltage for calculating string length'),

    html.Details([
        html.Summary('Modify/view model Parameters'),
        html.Div([
            html.P(
                'Module and racking model (above) are used to populate fields '
                'below. Changing the fields below will use these modified '
                'parameters in the model.'),

            dbc.Label(
                'Voco: Open circuit module voltage at standard test conditions (V)'),
            dbc.Input(id='Voco', value='60', type='text',
                      style={'max-width': 200}),
            dbc.Label('Num_cells: Cells in series.'),
            dbc.Input(id='Cells_in_Series', value='96', type='text',
                      style={'max-width': 200}),
            dbc.Label(
                'Bvoco: Temperature coefficient for module open-circuit-voltage (V/C)'),
            dbc.Input(id='Bvoco', value='-0.21696', type='text',
                      style={'max-width': 200}),
            dbc.Label(
                'Mbvoc: Coefficient providing the irradiance dependence for the Voc temperature coefficient, typically assumed to be zero (V/C)'),
            dbc.Input(id='Mbvoc', value='0', type='text',
                      style={'max-width': 200}),
            dbc.Label('n: Diode ideality factor'),
            dbc.Input(id='diode_ideality_factor', value='1.4032', type='text',
                      style={'max-width': 200}),
            dbc.Label('FD: Fraction of diffuse irradiance used'),
            dbc.Input(id='FD', value='1', type='text',
                      style={'max-width': 200}),
            dbc.Label('Air mass coefficients'),
            # dbc.Form([
            #     dbc.FormGroup([
            #         dbc.Label('A0'),
            #         dbc.Input(id='A0',type='number')
            #     ])
            # ],inlne=True),


            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("A0"),
                                dbc.Input(id="A0",value='0.9281',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("A1"),
                                dbc.Input(id="A1",value='0.06615',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("A2"),
                                dbc.Input(id="A2",value='-0.01384',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("A3"),
                                dbc.Input(id="A3",value='0.001298',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("A4"),
                                dbc.Input(id="A4",value='-4.6e-05',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                ],
                form=True,
            ),
            dbc.Label('AOI coefficients'),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B0"),
                                dbc.Input(id="B0",value='1',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B1"),
                                dbc.Input(id="B1",value='-0.002438', type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B2"),
                                dbc.Input(id="B2",value='0.0003103', type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B3"),
                                dbc.Input(id="B3",value='-1.246e-05', type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B4"),
                                dbc.Input(id="B4",value='2.11e-07',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("B5"),
                                dbc.Input(id="B5",value='-1.36e-09',type="text"),
                            ]
                        ),
                        width=2,
                    ),
                ],
                form=True,
            ),
            dbc.Label(
                'a: Empirically-determined coefficient establishing the upper limit for module temperature at low wind speeds and high solar irradiance'),
            dbc.Input(id='a', value=-3.47, type='number',
                      style={'max-width': 200}),
            dbc.Label(
                'b: Empirically-determined coefficient establishing the rate at which module temperature drops as wind speed increases (s/m)'),
            dbc.Input(id='b', value=-0.0594, type='number',
                      style={'max-width': 200}),
            dbc.Label(
                'DT: temperature difference between cell and module at reference irradiance (C)'),
            dbc.Input(id='DT', value=3, type='number', style={'max-width': 200})
        ], style={'marginLeft': 50})
    ]),

    html.H3('Calculate Voc'),
    html.P('Press "Calculate" to run Voc calculation (~5 seconds)'),
    dbc.Button(id='submit-button', n_clicks=0, children='Calculate',
               color="secondary"),
    # html.P(' '),
    # html.A(dbc.Button(id='submit-button-with-download',
    #                   n_clicks=0,
    #                   children='Calculate and download data as csv'),
    #        href="/download_simulation_data/"),
    # html.P(
    #     'Select whether to generate csv for downloading data (summary csv is always generated):'),
    # dbc.Checklist(id='generate-datafile',
    #               options=[
    #                   {'label': 'Generate Download Datafile',
    #                    'value': 'generate-datafile'},
    #               ],
    #               values=[]
    #               ),
    html.H2('Results'),
    html.Div(id='load'),
    html.Div(id='graphs', style={'display': 'none'}),
    dcc.Store(id='results-store',storage_type='memory'),
    # dbc.Button('Download results as csv',id='download_csv',n_clicks=0),
    # html.Div(id='graphs'),

    # html.Div([html.Div('Calculating...')], id='graphs'),
    # html.A('Download data as csv file', id='download-data',style={'display':None}),
    # dcc.Slider(
    #     min=0,
    #     max=9,
    #     marks={i: '{}'.format(i) for i in range(9)},
    #     value=5,
    # ),
    html.Div(id='voc_list'),
    html.H2('Frequently Asked Questions'),
    html.Details([
        html.Summary(
            'Why is there a spike in the temperature histogram at 0 C?'),
        html.Div("""In the NSRDB database, the temperature values are 
        interpolated from the NASA MERRA-2 dataset using a standard 
        temperature lapse rate [1]. The temperature data are then truncated 
        to an integer value, meaning all temperatures between -0.999 and 
        0.999 become 0 in the stored data. This only affects the calculation 
        result if the max Voc values occur at a temperature of 0 C. So, 
        for most locations, this rounding error has no effect on max Voc, 
        but in the worst case the rounding error results in a fractional 
        error in Voc of Bvoco*(1 C)/Voco, on the order of 0.3%. 

        """, style={'marginLeft': 50}),
    ]),
    html.Details([
        html.Summary(
            'Can I get the source code for this website?'),
        html.Div([
            html.Label(["Of Course! Please visit us on github: ",
                        html.A("https://github.com/toddkarin/pvtools",
                               href="https://github.com/toddkarin/pvtools")])
        ],
            style={'marginLeft': 50})
    ]),
    html.H2('References'),
    html.P("""
        [1]  M. Sengupta, Y. Xie, A. Lopez, A. Habte, G. Maclaurin, and J. 
        Shelby, “The national solar radiation data base (NSRDB),” Renewable 
        and Sustainable Energy Reviews, vol. 89, pp. 51–60, 2018. 
        """),
    html.P("""
    [2] D. King, W. Boyson, and J. Kratochvill, “Photovoltaic array 
    performance model,” SAND2004-3535, 2004. 
    """),
    html.P("""[3] W. F. Holmgren, C. W. Hansen, and M. A. Mikofski, “pvlib 
    python: a python package for modeling solar energy systems,” Journal of 
    Open Source Software, vol. 3, no. 29, p. 884, 2018"""),
    html.H2('About'),
    html.P("""Funding was primarily provided as part of the Durable Modules 
    Consortium (DuraMAT), an Energy Materials Network Consortium funded by 
    the U.S. Department of Energy, Office of Energy Efficiency and Renewable 
    Energy, Solar Energy Technologies Office. Lawrence Berkeley National 
    Laboratory is funded by the DOE under award DE-AC02-05CH11231 """),
    html.P('VOCMAX-DASH V-0.1'),
    html.P('Author: Todd Karin')
],
    style={'columnCount': 1,
           'maxWidth': 1000,
           'align': 'center'})


# app.layout = layout


# Callback for finding closest lat/lon in database.
@app.callback(
    Output('closest-message', 'children'),
    [Input('lat', 'value'),
     Input('lon', 'value')]
)
def update_output_div(lat, lon):
    filedata = vocmaxlib.filedata
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)

    closest_lat = np.array(filedata_closest['lat'])[0]
    closest_lon = np.array(filedata_closest['lon'])[0]
    return 'Closest position in database is {:.3f} latitude, {:.3f} longitude'.format(
        closest_lat, closest_lon)
    # return str(n_clicks)


# @app.callback(
#     Output('map', 'figure'),
#     [Input('session-id', 'children'),
#      Input('lat', 'value'),
#      Input('lon', 'value')])
@app.callback(
    Output('map', 'figure'),
    [Input('get-weather', 'n_clicks')],
    [State('lat', 'value'),
     State('lon', 'value')])
def update_map_callback(n_clicks, lat, lon):
    filedata = pvtoolslib.get_s3_filename_df()

    print(filedata)
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)

    closest_lat = np.array(filedata_closest['lat'])[0]
    closest_lon = np.array(filedata_closest['lon'])[0]
    return {
        'data': [
            go.Scattermapbox(
                lat=filedata['lat'],
                lon=filedata['lon'],
                mode='markers',
                marker=dict(
                    size=4
                ),
                text=[''],
                name='Database location'
            ),
            go.Scattermapbox(
                lat=[float(lat)],
                lon=[float(lon)],
                mode='markers',
                marker=dict(
                    size=14
                ),
                text=['Target location'],
                name='Target location'
            ),
            go.Scattermapbox(
                lat=[closest_lat],
                lon=[closest_lon],
                mode='markers',
                marker=dict(
                    size=14
                ),
                text=['Closest datapoint'],
                name='Closest datapoint'
            )

        ],
        'layout': go.Layout(
            autosize=False,
            width=1000,
            height=600,
            margin={'l': 10, 'b': 10, 't': 0, 'r': 0},
            hovermode='closest',
            mapbox=dict(
                accesstoken='pk.eyJ1IjoidG9kZGthcmluIiwiYSI6Ik1aSndibmcifQ.hwkbjcZevafx2ApulodXaw',
                bearing=0,
                center=dict(
                    lat=float(lat),
                    lon=float(lon)
                ),
                pitch=0,
                zoom=5,
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


# @app.callback(
#     Output('click-data', 'children'),
#     [Input('map', 'clickData')])
# def display_click_data(clickData):
#
#     # If no type given, do not change lat or lon
#     if type(clickData)==type(None):
#         d = {'lat':37.88, 'lon':-122.25}
#     else:
#         click_dict = eval(str(clickData))
#         d = click_dict['points'][0]
#         print(d)
#
#     # update_map(d['lat'],d['lon'])
#
#     return str(d)


# @app.callback(
#     Output('lon', 'value'),
#     [Input('click-data', 'children')])
# def set_lat(click_data):
#     print(click_data)
#     d = eval(click_data)
#     return d['lon']
# #
#

# @app.callback(
#     Output('lat', 'value'),
#     [Input('click-data', 'children')])
# def set_lat(click_data):
#     print(click_data)
#     d = eval(click_data)
#     return d['lat']
# #


# @app.callback(
#     Output('lon', 'value'),
#     [Input('click-data', 'children')])
# def set_lat(click_data):
#     d = eval(click_data)
#     return d['lon']


#
#
# @app.callback(
#     Output('get-weather', 'n_clicks'),
#     [Input('click-data', 'children')],
#     [State('get-weather', 'n_clicks')])
# def display_click_data(click_data, n_clicks):
#     return n_clicks+1
#     # return json.dumps(clickData, indent=2)
#
#


# Update values when changing the module name.
@app.callback(Output('Voco', 'value'), [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['Voco'])


@app.callback(Output('Bvoco', 'value'), [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['Bvoco'])


@app.callback(Output('Mbvoc', 'value'), [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['Mbvoc'])


@app.callback(Output('Cells_in_Series', 'value'),
              [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['Cells_in_Series'])


@app.callback(Output('diode_ideality_factor', 'value'),
              [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['N'])


@app.callback(Output('FD', 'value'), [Input('module_name', 'value')])
def update_Voco(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['FD'])

@app.callback(Output('A0', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['A0'])

@app.callback(Output('A1', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['A1'])

@app.callback(Output('A2', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['A2'])

@app.callback(Output('A3', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['A3'])

@app.callback(Output('A4', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['A4'])

@app.callback(Output('B0', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B0'])

@app.callback(Output('B1', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B1'])

@app.callback(Output('B2', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B2'])

@app.callback(Output('B3', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B3'])

@app.callback(Output('B4', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B4'])

@app.callback(Output('B5', 'value'), [Input('module_name', 'value')])
def update(module_name):
    return str(pvtoolslib.sandia_modules[module_name]['B5'])

@app.callback(Output('a', 'value'), [Input('racking_model', 'value')])
def update_Voco(racking_model):
    return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][0]


@app.callback(Output('b', 'value'), [Input('racking_model', 'value')])
def update_Voco(racking_model):
    return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][1]


@app.callback(Output('DT', 'value'), [Input('racking_model', 'value')])
def update(racking_model):
    return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][2]


#
# @app.callback(Output('download-data', 'href'),
#     [Input('session-id', 'children')])
# def update_download_link(session_id):
#     # dff = filter_data(filter_value)
#     # csv_string = dff.to_csv(index=False, encoding='utf-8')
#     # csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)
#
#     csv_string = 'hello'
#     return csv_string
#
#


@app.callback(Output('load', 'children'),
              [Input('submit-button', 'n_clicks')
               ])
def prepare_data(categ):
    if categ:
        return html.Div([
            dbc.Alert("Calculating...",
                                   color="primary")
                ],
            id='graphs')


#
@app.callback([Output('graphs', 'children'),
               Output('results-store','children')
               ],
              [Input('submit-button', 'n_clicks')
               ],
              [State('module_name', 'value'),
               State('racking_model', 'value'),
               State('surface_tilt', 'value'),
               State('surface_azimuth', 'value'),
               State('lat', 'value'),
               State('lon', 'value'),
               State('Voco', 'value'),
               State('Bvoco', 'value'),
               State('Mbvoc', 'value'),
               State('Cells_in_Series', 'value'),
               State('diode_ideality_factor', 'value'),
               State('FD', 'value'),
               State('A0', 'value'),
               State('A1', 'value'),
               State('A2', 'value'),
               State('A3', 'value'),
               State('A4', 'value'),
               State('B0', 'value'),
               State('B1', 'value'),
               State('B2', 'value'),
               State('B3', 'value'),
               State('B4', 'value'),
               State('B5', 'value'),
               State('a', 'value'),
               State('b', 'value'),
               State('DT', 'value'),
               State('max_string_voltage', 'value'),
               State('mount_type', 'active_tab'),
               State('axis_tilt', 'value'),
               State('axis_azimuth', 'value'),
               State('max_angle', 'value'),
               State('backtrack', 'value'),
               State('ground_coverage_ratio', 'value'),
               ]
              )
def update_graph(n_clicks, module_name, racking_model,
                 surface_tilt, surface_azimuth, lat, lon, Voco, Bvoco, Mbvoc,
                 Cells_in_Series,
                 diode_ideality_factor, FD,
                 A0,A1,A2,A3,A4,B0,B1,B2,B3,B4,B5,
                 a, b, DT,
                 max_string_voltage,
                 mount_type, axis_tilt, axis_azimuth, max_angle, backtrack,
                 ground_coverage_ratio):
    system_parameters = {
        'racking_model': {'a': a, 'b': b, 'deltaT': DT},
        # 'racking_model': racking_model,
        'surface_tilt': float(surface_tilt),
        'surface_azimuth': float(surface_azimuth),
        'mount_type': mount_type,
        'axis_tilt': float(axis_tilt),
        'axis_azimuth': float(axis_azimuth),
        'max_angle': float(max_angle),
        'backtrack': float(backtrack),
        'ground_coverage_ratio': float(ground_coverage_ratio)}


    print('Number clicks: ' + str(n_clicks))
    if n_clicks<1:
        print('Not running simulation.')
        return [], ''

    print(system_parameters)
    module_parameters = pvtoolslib.sandia_modules[module_name]

    # Overwrite provided module parameters.
    module_parameters['Voco'] = float(Voco)
    module_parameters['Bvoco'] = float(Bvoco)
    module_parameters['Mbvoc'] = float(Mbvoc)
    module_parameters['Cells_in_Series'] = float(Cells_in_Series)
    module_parameters['diode_ideality_factor'] = float(diode_ideality_factor)
    module_parameters['FD'] = float(FD)

    module_parameters['A0'] = float(A0)
    module_parameters['A1'] = float(A1)
    module_parameters['A2'] = float(A2)
    module_parameters['A3'] = float(A3)
    module_parameters['A4'] = float(A4)
    module_parameters['B0'] = float(B0)
    module_parameters['B1'] = float(B1)
    module_parameters['B2'] = float(B2)
    module_parameters['B3'] = float(B3)
    module_parameters['B4'] = float(B4)
    module_parameters['B5'] = float(B5)


    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)


    # filedata = vocmaxlib.filedata
    # filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
    #                                                      filedata)





    print('Getting weather data...')
    weather, info = pvtoolslib.get_s3_weather_data(filedata_closest['filename'].iloc[0])
    print('done.')
    # print(info.keys())

    # Get weather data
    # weather_fullpath = filedata_closest['weather_fullpath'].to_list()[0]
    # info_fullpath = filedata_closest['info_fullpath'].to_list()[0]

    # weather = nsrdbtools.import_weather_pickle(weather_fullpath)
    # info = pd.read_pickle(info_fullpath)

    print('done')

    # weather, info = get_weather_data(session_id)

    print('Simulating system...')
    (df, mc) = vocmaxlib.calculate_max_voc(weather, info,
                                           module_parameters=module_parameters,
                                           system_parameters=system_parameters)

    # print(weather['temp_cell'])

    print('done')
    y, c = np.histogram(df.v_oc,
                        bins=np.linspace(df.v_oc.max() * 0.75,
                                         df.v_oc.max() + 1, 500))

    years = list(set(weather.index.year))
    yearly_min_temp = []
    yearly_min_daytime_temp = []
    for j in years:
        yearly_min_temp.append(
            weather[weather.index.year == j]['temp_air'].min())
        yearly_min_daytime_temp.append(
            weather[weather.index.year == j]['temp_air'][
                weather[weather.index.year == j]['ghi'] > 150].min()
        )
    mean_yearly_min_ambient_temp = np.mean(yearly_min_temp)
    mean_yearly_min_daytime_ambient_temp = np.mean(yearly_min_daytime_temp)

    # min_daytime_temp = df['temp_air'][df['ghi']>150].min()

    voc_1sun_min_temp = mc.system.sapm(1, mean_yearly_min_ambient_temp)['v_oc']
    voc_1sun_min_daytime_temp = \
    mc.system.sapm(1, mean_yearly_min_daytime_ambient_temp)['v_oc']

    voc_dni_cell_temp = \
    mc.system.sapm((df['dni'] + df['dhi']) / 1000, df['temp_cell'])[
        'v_oc'].max()
    voc_P99p5 = np.percentile(
        df['v_oc'][np.logical_not(np.isnan(df['v_oc']))],
        99.5)
    voc_P99 = np.percentile(df['v_oc'][np.logical_not(np.isnan(df['v_oc']))],
                            99)

    results_dict = {
        'Source': info['source'],
        'Location ID': info['location_id'],
        'Elevation': info['elevation'],
        'Latitude': info['lat'],
        'Longitude': info['lon'],
        # 'DHI Units': info['DHI Units'][0],
        # 'DNI Units': info['DNI Units'][0],
        # 'GHI Units': info['GHI Units'][0],
        # 'V_oc Units': 'V',
        # 'Wind Speed Units': info['Wind Speed'][0],
        'interval_in_hours': info['interval_in_hours'],
        'timedelta_in_years': info['timedelta_in_years'],
        'NSRDB Version': info['version'],
        'PVLIB Version': pvlib._version.get_versions()['version'],
        'PVTools Version': '0.0.1',
        'Date Created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    info_df = pd.DataFrame(results_dict, index=[0])

    summary = [
        'Latitude: {:0.4f}'.format(info['lat']),
        'Longitude: {:0.4f}'.format(info['lon']),
        'Maximum Design String Voltage: {:0.2f} V'.format(max_string_voltage),
        'Historical Max Voc: {:0.3f} V'.format(df.v_oc.max()),
        'P99.5 Voc: {:0.3f} V'.format(voc_P99p5),
        'P99.5 Max String length: {:0.0f} modules'.format(
            np.floor(max_string_voltage / voc_P99p5)),
        'Traditional max Voc: {:0.3f} V'.format(voc_1sun_min_temp),
        'Traditional Max String length: {:0.0f} modules'.format(
            np.floor(max_string_voltage / voc_1sun_min_temp)),
        'Yearly mean minimum ambient temperature: {:0.3f} C'.format(mean_yearly_min_ambient_temp),
        'Weather data source: {}'.format(info['source']),
        'Location ID: {}'.format(info['location_id']),
        'Weather data start date: {}'.format(
            df.index[0].strftime("%Y-%m-%d %H:%M:%S")),
        'Weather data end date: {}'.format(
            df.index[-1].strftime("%Y-%m-%d %H:%M:%S")),

    ]

    # summary.append('Sandia Module parameters')
    # for p in list(module_parameters.keys()):
    #     summary.append( p + ': {:0.3f}'.format(module_parameters[p]))


              # + \
              # 'Location ID, {}\n'.format(info['location_id']) + \
              # 'Weather data start date, {}\n'.format(
              #     df.index[0].strftime("%Y-%m-%d %H:%M:%S")) + \
              # 'Weather data end date, {}\n'.format(
              #     df.index[-1].strftime("%Y-%m-%d %H:%M:%S")) + \
              # 'Latitude, {:0.4f}\n'.format(info.Latitude[0]) + \
              # 'Longitude, {:0.4f}\n'.format(info.Longitude[0]) + \
              # 'P99 Voc (V), {:0.3f}\n'.format(np.percentile(df.v_oc, 99)) + \
              # 'Max Historical Voc (V), {:0.3f}\n'.format(df.v_oc.max()) + \
              # 'P01 Air Temp (C), {:0.2f}\n'.format(
              #     np.percentile(df['temp_air'], 1)) + \
              # 'Min Historical Air Temp (C), {:0.3f}\n'.format(
              #     df['temp_air'].min()) + \
              # 'P01 Cell Temp (C), {:0.2f}\n'.format(
              #     np.percentile(df['temp_cell'], 1)) + \
              # 'Min Historical Cell Temp (C), {:0.2f}\n'.format(
              #     df['temp_cell'].min())

    # print(info_df)

    # # Make a directory for saving session files.
    # if not os.path.isdir(os.path.join('downloads',session_id)):
    #     os.mkdir(os.path.join('downloads',session_id))
    # save_filename = os.path.join('downloads',session_id,'maxvoc_data.csv')
    # info_filename = os.path.join('downloads',session_id,'maxvoc_info.csv')
    # temp_filename = os.path.join('downloads', session_id, 'maxvoc_temp.pkl')
    # print('Saving data as ' + str(save_filename) + '...')
    # with open(save_filename,'w') as f:
    #     f.write(info_df.to_csv(index=False))
    #     if len(generate_datafile)>0:
    #         f.write(df.to_csv(float_format='%.2f'))
    #
    # with open(info_filename,'w') as f:
    #     # f.write('hello')
    #     # f.write(info_df.to_csv(index=False))
    #     f.write(summary)
    # print('done')

    # Make histograms
    def scale_to_hours_per_year(y):
        return y / info['timedelta_in_years'] * info['interval_in_hours']

    y_scale = scale_to_hours_per_year(y)
    voc_hist_y = y_scale[1:]
    voc_hist_x = c[1:-1]

    temp_bins = np.arange(
        -4 + np.floor(np.min([df['temp_cell'].min(), df['temp_air'].min()])),
        1 + np.floor(np.max([df['temp_cell'].max(), df['temp_air'].max()]))
    )

    temp_cell_hist, temp_cell_hist_bin = np.histogram(df['temp_cell'],
                                                      bins=temp_bins)
    temp_cell_hist = scale_to_hours_per_year(temp_cell_hist)

    temp_air_hist, temp_air_hist_bin = np.histogram(df['temp_air'],
                                                    bins=temp_bins)
    temp_air_hist = scale_to_hours_per_year(temp_air_hist)

    temp_cell_hist_x = temp_cell_hist_bin[1:-1]
    temp_air_hist_x = temp_air_hist[1:-1]
    temp_cell_hist_y = temp_cell_hist[1:]
    temp_air_hist_y = temp_air_hist[1:]

    max_pos = np.argmax(np.array(df.v_oc))
    plot_min_index = np.max([0, max_pos - 1500])
    plot_max_index = np.min([len(df.v_oc), max_pos + 1500])

    colors = plotly.colors.DEFAULT_PLOTLY_COLORS

    voc_poi = pd.DataFrame.from_dict(
        {
            # 'P99':
            #     ['P99',
            #      'P99 Voc: {:.3f} V<br>'
            #      'Maximum String length: {:.0f}<br>'.format(
            #          voc_P99,
            #          np.floor(max_string_voltage / voc_P99)
            #      ),
            #      voc_P99,
            #      'rgb(0, 0, 0)'
            #      ],
            'P99.5':
                ['P99.5',
                 'P99.5 Voc: {:.3f} V<br>'
                 'Maximum String length: {:.0f}<br>'
                 'Recommended 690.7(A)(3) value'.format(
                     voc_P99p5,
                     np.floor(max_string_voltage / voc_P99p5)
                 ),
                 voc_P99p5,
                 colors[2]
                 ],
            'Max':
                ['Hist',
                 'Historical Maximum Voc: {:.3f} V<br>'
                 'Maximum String length: {:.0f}<br>'
                 'Conservative 690.7(A)(3) value'.format(
                     df.v_oc.max(),
                     np.floor(max_string_voltage / df.v_oc.max())
                 ),
                 df.v_oc.max(),
                 colors[3]
                 ],
            'Trad':
                ['Trad',
                 'Traditional Maximum Voc: {:.3f} V<br>'
                 'Maximum String length: {:.0f}<br>'
                 'Calculated using 1 sun and mean yearly min ambient temp of {:.1f} C<br>Conservative 690.7(A)(1) value'.format(
                     voc_1sun_min_temp,
                     np.floor(max_string_voltage / voc_1sun_min_temp),
                     mean_yearly_min_ambient_temp,
                 ),
                 voc_1sun_min_temp,
                 colors[4]
                 ],
            'Tradday':
                ['Day',
                 'Traditional Maximum Daytime Voc: {:.3f} V<br>'
                 'Maximum String length: {:.0f}<br>'
                 'Calculated using 1 sun and mean yearly min daytime (GHI>150) temp of {:.1f} C<br>'
                 'Recommended 690.7(A)(1) value'.format(
                     voc_1sun_min_daytime_temp,
                     np.floor(max_string_voltage / voc_1sun_min_daytime_temp),
                     mean_yearly_min_daytime_ambient_temp),
                 voc_1sun_min_daytime_temp,
                 colors[5]
                 ],
            'dni':
                ['Normal',
                 'Max Voc using DNI+DHI (simple calculation): {:.3f} V<br>'
                 'Maximum String length: {:.0f}<br>'.format(
                     voc_dni_cell_temp,
                     np.floor(max_string_voltage / voc_dni_cell_temp)),
                 voc_dni_cell_temp,
                 colors[6]
                 ],

        },
        orient='index',
        columns=['short_label', 'hover_label', 'value', 'color']
    ).transpose()

    temperature_poi = pd.DataFrame.from_dict(
        {
            'P1 Air':
                ['P1',
                 '1 Percentile Air Temperature: {:.1f} C'.format(
                     np.percentile(df['temp_air'], 1)),
                 np.percentile(df['temp_air'], 1),
                 'rgb(0, 0, 0)'
                 ],
            # 'P4 Air':
            #  ['P4',
            #   'P4 Air Temperature: {:.1f} C'.format(np.percentile(df['temp_air'], 4)),
            #   np.percentile(df['temp_air'], 4),
            #   'rgb(0, 0, 0)'
            #   ],
            'Hist':
                ['HA',
                 'Historical Minimum Ambient Temperature: {:.1f} C'
                 '<br>Conservative 690.7(A)(1) value'.format(
                     df['temp_air'].min()),
                 df['temp_air'].min(),
                 'rgb(0, 0, 0)'
                 ],
            'Hist2':
                ['Day',
                 'Historical Minimum Daytime Ambient Temperature: {:.1f} C'
                 '<br>Recommended 690.7(A)(1) value'.format(
                     df['temp_air'][df['ghi'] > 150].min()),
                 df['temp_air'][df['ghi'] > 150].min(),
                 'rgb(0, 0, 0)'
                 ],
            # 'Hist2':
            #     ['HC',
            #      'Historical Minimum Cell Temperature: {:.1f} C'.format(
            #      df['temp_cell'].min()),
            #      df['temp_cell'].min(),
            #      'rgb(0, 0, 0)'
            #      ],
            'TM':
                ['Max',
                 'Cell Temperature when max Voc was reached: {:.1f} C'.format(
                     df['temp_cell'][max_pos]),
                 df['temp_cell'][max_pos],
                 'rgb(0, 0, 0)'
                 ],
        },
        orient='index',
        columns=['short_label', 'hover_label', 'value', 'color']
    ).transpose()

    #
    #
    # voc_poi = pd.DataFrame.from_dict(
    #     {
    #         'P99':
    #          ['P99',
    #           'P99 Voc ',
    #           909
    #           ]
    #      },
    #     orient='index',
    #     columns = ['short_label','hover_label','value']
    # ).transpose()

    #
    # voc_poi = {'P99 Voc': np.percentile(df.v_oc, 99),
    #            'P99.9 Voc (Recommended)': np.percentile(df.v_oc, 99.9),
    #            'Historical Max Voc (Conservative)': df.v_oc.max(),
    #            '1 sun, historical min temp (Traditional)': voc_1sun_min_temp
    #            }

    print('making output graphs...')

    return_layout = [
        html.P('Simulation results for maximum Voc.'),
        dcc.Graph(
            id='Voc-histogram',
            figure={
                'data': [
                    {'x': voc_hist_x, 'y': voc_hist_y, 'type': 'line',
                     'name': 'Voc'}
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Voc (Volts)'},
                    yaxis={'title': 'hours/year'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    annotations=[
                        dict(
                            dict(
                                x=voc_poi[s]['value'],
                                y=voc_hist_y[np.argmin(
                                    np.abs(voc_poi[s]['value'] - voc_hist_x))],
                                xref='x',
                                yref='y',
                                xanchor='center',
                                text=voc_poi[s]['short_label'],
                                hovertext=voc_poi[s]['hover_label'],
                                textangle=0,
                                font=dict(
                                    color=voc_poi[s]['color']
                                ),
                                arrowcolor=voc_poi[s]['color'],
                                showarrow=True,
                                align='left',
                                standoff=2,
                                arrowhead=4,
                                ax=0,
                                ay=-40
                            ),
                            align='left'
                        )
                        for s in voc_poi]
                )
            }
        ),
        dcc.Graph(
            id='temperature-histogram',
            figure={
                'data': [
                    {'x': temp_cell_hist_bin[1:-1], 'y': temp_cell_hist[1:],
                     'type': 'line', 'name': 'Cell Temperature'},
                    {'x': temp_air_hist_bin[1:-1], 'y': temp_air_hist[1:],
                     'type': 'line', 'name': 'Air Temperature'}
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Temperature (C)'},
                    yaxis={'title': 'hours/year'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    annotations=[
                        dict(
                            dict(
                                x=temperature_poi[s]['value'],
                                y=temp_cell_hist_y[np.argmin(
                                    np.abs(temperature_poi[s][
                                               'value'] - temp_cell_hist_x))],
                                xref='x',
                                yref='y',
                                xanchor='center',
                                text=temperature_poi[s]['short_label'],
                                hovertext=temperature_poi[s]['hover_label'],
                                textangle=0,
                                font=dict(
                                    color=temperature_poi[s]['color']
                                ),
                                arrowcolor=temperature_poi[s]['color'],
                                showarrow=True,
                                align='left',
                                standoff=2,
                                arrowhead=4,
                                ax=0,
                                ay=-40
                            ),
                            align='left'
                        )
                        for s in temperature_poi]
                )
            }
        ),
        html.Div(
            'Calculation performed for {:.1f} years, showing position of maximum Voc'.format(
                info['timedelta_in_years'])),
        dcc.Graph(
            id='temperature-PLOT',
            figure={
                'data': [
                    {'x': weather.index[plot_min_index:plot_max_index],
                     'y': df['temp_cell'][plot_min_index:plot_max_index],
                     'type': 'line', 'name': 'Cell Temperature'},
                    {'x': weather.index[plot_min_index:plot_max_index],
                     'y': df['temp_air'][plot_min_index:plot_max_index],
                     'type': 'line', 'name': 'Air Temperature'}
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Temperature (C)'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    annotations=[
                        dict(
                            dict(
                                x=weather.index[max_pos],
                                y=df['temp_cell'][max_pos],
                                xref='x',
                                yref='y',
                                xanchor='center',
                                text='Hist',
                                hovertext='Historical max Voc: {:.2f} V<br>'
                                          'Air temperature: {:.0f} C<br>'
                                          'Cell temperature: {:.0f} C<br>'
                                          'GHI: {:.0f} W/m^2'.format(
                                    df['v_oc'][max_pos],
                                    df['temp_air'][max_pos],
                                    df['temp_cell'][max_pos],
                                    df['ghi'][max_pos]),
                                textangle=0,
                                showarrow=True,
                                standoff=2,
                                arrowhead=4,
                                borderwidth=2,
                                borderpad=4,
                                opacity=0.8,
                                bgcolor='#ffffff',
                                ax=0,
                                ay=-40
                            ),
                            align='center'
                        )]
                )
            }
        ),
        # html.A(html.Button('Download results as csv'),href='download_simulation_data'),
        # dbc.Button('Download results as csv',id='download_csv',n_clicks=0),
        html.H4('Results summary'),
        # html.Details([
            # html.Summary('View text summary'),
        html.Div([html.P(s) for s in summary],
                 style={'marginLeft': 10})
        # ]),
        # html.P(
        #     html.A('Download data as csv file', id='download-data',href=save_filename)
        # ),
        # html.A('Download summary as csv file', id='download-summary',
        #        href=info_filename),
        # html.Button(id='download-summary', children='Download Summary'),
        # html.Button(id='download-data', children='Download Data as CSV')
    ]



    print('converting to json...')
    weather_json = weather.to_json()
    print('done')

    print('** Calculation done.')
    return return_layout, weather_json
#
#
# @app.callback([],
#               [Input('download_csv','n_clicks')]
#               [State('results-store', 'children')])
# def update_Voco(n_clicks,results):
#     print(results)


#
#
#
# @app.server.route('/download_simulation_data/',
#                   [State('results-store','children')
#                    ])
# def download_simulation_data(x):
#     #Create DF
#     d = {'col1': [1, 2], 'col2': [3, 4]}
#     df = pd.DataFrame(data=d)
#
#     #Convert DF
#     str_io = io.StringIO()
#     df.to_csv(str_io, sep=",")
#
#     mem = io.BytesIO()
#     mem.write(str_io.getvalue().encode('utf-8'))
#     mem.seek(0)
#     str_io.close()
#
#
#
#     # excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
#     # df.to_excel(excel_writer, sheet_name="sheet1")
#     # excel_writer.save()
#     # excel_data = strIO.getvalue()
#     # stream.seek(0)
#
#     return flask.send_file(mem,
# 					   mimetype='text/csv',
# 					   attachment_filename='downloadFile.csv',
# 					   as_attachment=True)
# @app.server.route('/downloads/<path:path>')
# def serve_static(path):
#     root_dir = os.getcwd()
#     return flask.send_from_directory(
#         os.path.join(root_dir, 'downloads'), path
#     )


#
# if __name__ == '__main__':
#     app.run_server(debug=True)