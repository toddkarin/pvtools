# -*- coding: utf-8 -*-
"""

This script builds a Dash web application for finding maximum module Voc.
Specifically, it builds the layout that is called by index.py

Todd Karin

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
# import flask
# import json
# import time
import datetime
import io
import pvtoolslib
import urllib


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

    # html.H2('Methods'),
    html.H2('Background: National Electric Code'),
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
    html.H2('Calculation methods'),
    dcc.Markdown("""The simulation first acquires weather data from the 
    National Solar Radiation Database (NSRDB) [1]. The data was sampled 
    across the continental US at approximately a 0.125 degree grid. If a 
    different weather data source is desired, it is necessary to use the open 
    source associated python package [vocmax]( 
    https://github.com/toddkarin/vocmax), which performs the same calculation 
    as this web tool. If the particular weather data point is not on the map, 
    please contact us and we will try to provide it. 
    
    """),

    dcc.Markdown("""The string voltage calculator uses the open source [ 
    PVLIB](https://pvlib-python.readthedocs.io/en/latest/) library to perform 
    the calculation using the single diode model and the CEC 
    parameterization. Module parameters are either taken from a standard 
    database or entered manually. The calculation conservatively assumes that 
    all diffuse irradiance is used and that there are no reflection losses 
    from the top cell. These two assumptions cause a small increase in the 
    Voc and make the simulation more conservative. Other specific details of 
    the calculations are explained in [vocmax]( 
    https://github.com/toddkarin/vocmax). 

    """),

    html.P("""This tool provides standard values for methods 690.7(A)(1) and 
    690.7(A)(3). For method 690.7(A)(1), The lowest expected ambient 
    temperature is calculated by finding the minimum temperature during 
    daylight hours, defined as GHI>150 W/m^2. For method 690.7(A)(3), the full 
    PVLIB model is run using weather data from the selected location and 
    module parameters.

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
    dbc.Label("""Either select module name from data base or manually enter 
    parameters for the  California Energy Commission (CEC) 6-paramater model 
    [4,5]. 
    
    """),
    dbc.Tabs([
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Label("""Module Name (from CEC database). This 
                        method uses 'no_loss' AOI model and fraction of 
                        diffuse irradiance 'FD' equal to 1. 
                        
                        """),
                        dcc.Dropdown(
                            id='module_name',
                            options=pvtoolslib.cec_module_dropdown_list,
                            value=pvtoolslib.cec_module_dropdown_list[0]['value'],
                            style={'max-width': 500}
                        ),
                     ],
                )
            )
        ], tab_id='lookup', label='Library Lookup'),
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.P("""Manually set module parameters.
                        
                        """),
                        dbc.Label("""Module name 

                                    """),
                        dbc.Input(id='module_name_manual',
                                  value='Custom Module',
                                  type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""alpha_sc: The short-circuit current 
                        temperature coefficient of the module in units of A/C 

                                    """),
                        dbc.Input(id='alpha_sc', value='0.007997', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""a_ref: The product of the usual diode 
                        ideality factor (n, unitless), number of cells in 
                        series (Ns), and cell thermal voltage at reference 
                        conditions, in units of V. 

                                    """),
                        dbc.Input(id='a_ref', value='1.6413', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""I_L_ref: The light-generated current (or 
                        photocurrent) at reference conditions, in amperes. 

                                    """),
                        dbc.Input(id='I_L_ref', value='7.843', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""I_o_ref: The dark or diode reverse 
                        saturation current at reference conditions, in amperes. 

                                    """),
                        dbc.Input(id='I_o_ref', value='1.936e-09', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""R_sh_ref: The shunt resistance at 
                        reference conditions, in ohms. 

                                    """),
                        dbc.Input(id='R_sh_ref', value='839.4', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""R_s: The series resistance at reference 
                        conditions, in ohms. 

                                    """),
                        dbc.Input(id='R_s', value='0.359', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""Adjust: The adjustment to the 
                        temperature coefficient for short circuit current, 
                        in percent. 

                                    """),
                        dbc.Input(id='Adjust', value='16.5', type='text',
                                  style={'max-width': 200}),
                        dbc.Label("""FD: Fraction of diffuse irradiance

                                    """),
                        dbc.Input(id='FD', value='1', type='text',
                                  style={'max-width': 200}),
                        # dbc.Label("""AOI model. Loss model for
                        # angle-of-incidence losses. These occur due to
                        # reflection from surfaces above the cell.
                        #
                        #             """),
                        # dcc.Dropdown(
                        #     id='aoi_model',
                        #     options=[
                        #         {'label': 'ashrae',
                        #          'value': 'ashrae'},
                        #         {'label': 'no_loss',
                        #          'value': 'no_loss'},
                        #     ],
                        #     value='ashrae',
                        #     style={'max-width': 500}
                        # ),
                        # dbc.Label("""Ashrae IAM coefficient. 'b' coefficient
                        # describing incidence angle modifier losses. Typical
                        # value is 0.05.
                        #
                        #             """),
                        # dbc.Input(id='ashrae_iam_param', value='0.05',
                        #           type='text',
                        #           style={'max-width': 200}),
                     ]
                )
            )
        ], tab_id='manual', label='Manual Entry')
    ], id='module_parameter_input_type', active_tab='lookup'),


    html.Label('Choose thermal racking model'),

    dbc.Tabs([
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [dbc.Label('Surface Tilt (degrees)'),
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
                     ],

                )
            )
        ], tab_id='lookup', label='Default models'),
        dbc.Tab([
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Label("""a: Empirically-determined coefficient 
                        establishing the upper limit for module temperature 
                        at low wind speeds and high solar irradiance 
                        
                        """),
                        dbc.Input(id='a', value=-3.47, type='number',
                                  style={'max-width': 200}),
                        dbc.Label("""b: Empirically-determined coefficient 
                        establishing the rate at which module temperature 
                        drops as wind speed increases (s/m) 
                        
                        """),
                        dbc.Input(id='b', value=-0.0594, type='number',
                                  style={'max-width': 200}),
                        dbc.Label("""DT: temperature difference between cell 
                        and module at reference irradiance (C) 
                        
                        """),
                        dbc.Input(id='DT', value=3, type='number',
                                  style={'max-width': 200})
                     ]
                )
            )
        ], tab_id='manual', label='Manual Entry')
    ], id='thermal_model_input_type', active_tab='lookup'),

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
                               style={'max-width': 200}),
                     dbc.FormText("""For module face oriented due South use 180. 
                     For module face oreinted due East use 90"""),

                     ],

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

    html.H3('Calculate Voc'),
    html.P('Press "Calculate" to run Voc calculation (~10 seconds)'),
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
            "Can I run the code myself?"),
        html.Div(
            dcc.Markdown("""Yes! We have an example for running this 
            calculation in python. Visit the [github page for vocmax](
            https://github.com/toddkarin/vocmax) 
 

    """), style={'marginLeft': 50}),
    ]),
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
            dcc.Markdown("Of Course! Please visit us on [github](https://github.com/toddkarin/pvtools)")
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
    html.P("""[4] A. Dobos, “An Improved Coefficient Calculator for the 
    California Energy Commission 6 Parameter Photovoltaic Module Model”, 
    Journal of Solar Energy Engineering, vol 134, 2012. 
    
    """),
    html.P("""[5] W. De Soto et al., “Improvement and validation of a model 
    for photovoltaic array performance”, Solar Energy, vol 80, pp. 78-88, 2006. 
    
    """),
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





# Callback for finding closest lat/lon in database.
@app.callback(
    Output('closest-message', 'children'),
    [Input('get-weather', 'n_clicks')],
    [State('lat', 'value'),
     State('lon', 'value')]
)
def update_output_div(n_clicks, lat, lon):
    # print('Finding database location')
    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)

    closest_lat = np.array(filedata_closest['lat'])[0]
    closest_lon = np.array(filedata_closest['lon'])[0]
    return 'Closest position in database is {:.3f} latitude, {:.3f} longitude'.format(
        closest_lat, closest_lon)
    # return str(n_clicks)

#
# @app.callback(
#     Output('map','config'),
#     [Input('map','figure')]
# )
# def forcezoom(f):
#     return(dict(scrollZoom = True))

# @app.callback(
#     Output('map', 'figure'),
#     [Input('session-id', 'children'),
#      Input('lat', 'value'),
#      Input('lon', 'value')])
@app.callback(
    [Output('map','figure'),
     Output('map','config')
     ],
    [Input('get-weather', 'n_clicks')],
    [State('lat', 'value'),
     State('lon', 'value')])
def update_map_callback(n_clicks, lat, lon):
    # print('Updating the map')
    filedata = pvtoolslib.get_s3_filename_df()

    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)

    closest_lat = np.array(filedata_closest['lat'])[0]
    closest_lon = np.array(filedata_closest['lon'])[0]
    map_figure = {
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
    return map_figure, dict(scrollZoom = True)



# @app.callback([Output('alpha_sc', 'value')
#                ],
#               [Input('modrop', 'value')
#                ])
# def update_module_paramaters_please(module_name):
#     print('hello')
#     # print(module_name)
#     # print('{:0.6f}'.format(pvtoolslib.cec_modules[module_name]['alpha_sc']))
#     return 5
#


#
@app.callback([Output('a', 'value'),
                Output('b', 'value'),
                Output('DT', 'value')
               ],
              [Input('racking_model', 'value')])
def update_Voco(racking_model):
    # print('Racking model changed')
    return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][0], \
        pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][1], \
        pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][2]

#
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


# @app.callback(
#     Output('get-weather', 'n_clicks'),
#     [Input('click-data', 'children')],
#     [State('get-weather', 'n_clicks')])
# def display_click_data(click_data, n_clicks):
#     return n_clicks+1
#     # return json.dumps(clickData, indent=2)
#
#

#
# # Update values when changing the module name.
# @app.callback(Output('alpha_sc', 'value'), [Input('module_name', 'value')])
# def update_alpha_sc(module_name):
#     print(module_name)
#     print('{:0.6f}'.format(pvtoolslib.cec_modules[module_name]['alpha_sc']))
#     return 'heello'


# @app.callback(Output('Bvoco', 'value'), [Input('module_name', 'value')])
# def update_Voco(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['Bvoco'])
#
#
# @app.callback(Output('Mbvoc', 'value'), [Input('module_name', 'value')])
# def update_Voco(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['Mbvoc'])
#
#
# @app.callback(Output('Cells_in_Series', 'value'),
#               [Input('module_name', 'value')])
# def update_Voco(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['Cells_in_Series'])
#
#
# @app.callback(Output('diode_ideality_factor', 'value'),
#               [Input('module_name', 'value')])
# def update_Voco(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['N'])
#
#
# @app.callback(Output('FD', 'value'), [Input('module_name', 'value')])
# def update_Voco(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['FD'])
#
# @app.callback(Output('A0', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['A0'])
#
# @app.callback(Output('A1', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['A1'])
#
# @app.callback(Output('A2', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['A2'])
#
# @app.callback(Output('A3', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['A3'])
#
# @app.callback(Output('A4', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['A4'])
#
# @app.callback(Output('B0', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B0'])
#
# @app.callback(Output('B1', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B1'])
#
# @app.callback(Output('B2', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B2'])
#
# @app.callback(Output('B3', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B3'])
#
# @app.callback(Output('B4', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B4'])
#
# @app.callback(Output('B5', 'value'), [Input('module_name', 'value')])
# def update(module_name):
#     return str(pvtoolslib.sandia_modules[module_name]['B5'])
# #
# @app.callback(Output('a', 'value'), [Input('racking_model', 'value')])
# def update_Voco(racking_model):
#     return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][0]
#
#
# @app.callback(Output('b', 'value'), [Input('racking_model', 'value')])
# def update_Voco(racking_model):
#     return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][1]
#
#
# @app.callback(Output('DT', 'value'), [Input('racking_model', 'value')])
# def update(racking_model):
#     return pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][2]


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
# @app.callback(Output('graphs', 'children'),
#               [Input('submit-button', 'n_clicks')
#                ],
#               [State('lat', 'value'),
#                 State('lon', 'value'),
#                 State('module_parameter_input_type','active_tab'),
#                 State('module_name','value'),
#                 State('module_name_manual','value'),
#                 State('alpha_sc','value'),
#                 State('a_ref','value'),
#                 # State('I_L_ref','value'),
#                 # State('I_o_ref','value'),
#                 # State('R_sh_ref','value'),
#                 # State('R_s','value'),
#                 # State('Adjust','value'),
#                 # State('FD','value'),
#                ]
#               )
# def run_simulation(n_clicks,lat,lon,module_parameter_input_type,module_name,
#                    module_name_manual,
#                     alpha_sc,
#                    a_ref
#                    # I_L_ref, I_o_ref, R_sh_ref, R_s, Adjust, FD):
#     ):
#     print('Run simulation!!')
#     return [dbc.Label('All done')]




#
@app.callback(Output('graphs', 'children'),
              [Input('submit-button', 'n_clicks')
               ],
              [State('lat', 'value'),
                State('lon', 'value'),
                State('module_parameter_input_type','active_tab'),
                State('module_name','value'),
                State('module_name_manual','value'),
                State('alpha_sc','value'),
                State('a_ref','value'),
                State('I_L_ref','value'),
                State('I_o_ref','value'),
                State('R_sh_ref','value'),
                State('R_s','value'),
                State('Adjust','value'),
                State('FD','value'),
                State('thermal_model_input_type', 'active_tab'),
                State('racking_model', 'value'),
                State('a', 'value'),
                State('b', 'value'),
                State('DT', 'value'),
                State('mount_type', 'active_tab'),
                State('surface_tilt', 'value'),
                State('surface_azimuth', 'value'),
                State('axis_tilt', 'value'),
                State('axis_azimuth', 'value'),
                State('max_angle', 'value'),
                State('backtrack', 'value'),
                State('ground_coverage_ratio', 'value'),
                State('max_string_voltage', 'value'),
               ]
              )
def run_simulation(n_clicks, lat, lon,  module_parameter_input_type, module_name, module_name_manual,
                 alpha_sc, a_ref, I_L_ref, I_o_ref, R_sh_ref, R_s, Adjust, FD,
                 thermal_model_input_type, racking_model, a, b, DT,
                 mount_type, surface_tilt, surface_azimuth,
                 axis_tilt, axis_azimuth, max_angle, backtrack, ground_coverate_ratio,
                 max_string_voltage):
# def run_simulation(*argv):

    # print('Run simulation!!')
    if n_clicks<1:
        # print('Not running simulation.')
        return []


    # Get weather

    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)


    print('Getting weather data...')
    weather, info = pvtoolslib.get_s3_weather_data(
        filedata_closest['filename'].iloc[0])

    print(pd.Series(info))


    if module_parameter_input_type=='lookup':
        module_parameters = pvtoolslib.cec_modules[module_name].to_dict()
        module_parameters['FD'] = 1
        module_parameters['name'] = module_name
        module_parameters['aoi_model'] = 'no_loss'
    elif module_parameter_input_type=='manual':
        module_parameters = {
            'name': module_name_manual,
            'alpha_sc': float(alpha_sc),
            'a_ref': float(a_ref),
            'I_L_ref': float(I_L_ref),
            'I_o_ref': float(I_o_ref),
            'R_sh_ref': float(R_sh_ref),
            'R_s': float(R_s),
            'Adjust': float(Adjust),
            'FD': float(FD)
        }
    else:
        print('input type not understood.')

    if thermal_model_input_type=='lookup':
        thermal_model = racking_model
    elif thermal_model_input_type=='manual':
        thermal_model = {
            'a':float(a),
            'b':float(b),
            'deltaT':float(DT)
        }
    else:
        print('Racking model not understood')

    if mount_type=='fixed_tilt':
        racking_parameters = {
            'racking_type': 'fixed_tilt',
            'surface_tilt': float(surface_tilt),
            'surface_azimuth': float(surface_azimuth)
        }
    elif mount_type=='single_axis_tracker':
        racking_parameters = {
            'racking_type': 'single_axis',
            'axis_tilt': float(axis_tilt),
            'axis_azimuth': float(axis_azimuth),
            'max_angle': float(max_angle),
            'backtrack': backtrack,
            'gcr': float(ground_coverate_ratio)
        }
    else:
        print('error getting racking type')

    max_string_voltage = float(max_string_voltage)

    df = vocmaxlib.simulate_system(weather, info,module_parameters,
                                   racking_parameters, thermal_model)

    voc_summary = vocmaxlib.make_voc_summary(df, module_parameters,
                                   max_string_voltage=max_string_voltage)

    summary_text = vocmaxlib.make_simulation_summary(df, info,
                                                 module_parameters,
                                                 racking_parameters,
                                                 thermal_model,
                                                 max_string_voltage)

    summary_text_for_download = "data:text/csv;charset=utf-8," + summary_text

    # df_temp = pd.DataFrame(info,index=[0])
    df_temp = df.copy()
    df_temp['wind_speed'] = df_temp['wind_speed'].map(lambda x: '%2.1f' % x)
    df_temp['v_oc'] = df_temp['v_oc'].map(lambda x: '%3.2f' % x)
    df_temp['temp_cell'] = df_temp['temp_cell'].map(lambda x: '%2.1f' % x)
    df_temp['aoi'] = df_temp['aoi'].map(lambda x: '%3.0f' % x)

    # This works for creating a downloadable csv, but it takes an extra 7 seconds to transfer the data.
    # csv_string_one_year = "data:text/csv;charset=utf-8," + \
    #     urllib.parse.quote(
    #         pd.DataFrame(info,index=[0]).to_csv(index=False,
    #                                 encoding='utf-8',
    #                                 float_format='%.3f')
    #             ) + \
    #     urllib.parse.quote(
    #         df_temp[0:17520].to_csv(index=False,
    #                                 encoding='utf-8',
    #                                 float_format='%.3f')
    #     )

    colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    plot_color = {}
    pc = 1
    for s in list(voc_summary.index):
        plot_color[s] = colors[pc]
        pc = pc+1
    # voc_summary['plot_color'] = colors[0:len(voc_summary)]


    # Make histograms
    def scale_to_hours_per_year(y):
        return y / info['timedelta_in_years'] * info['interval_in_hours']


    # Voc histogram
    voc_hist_y_raw, voc_hist_x_raw = np.histogram(df['v_oc'],
                        bins=np.linspace(df['v_oc'].max() * 0.4,
                                         df['v_oc'].max() + 1, 500))

    voc_hist_y = scale_to_hours_per_year(voc_hist_y_raw)[1:]
    voc_hist_x = voc_hist_x_raw[1:-1]

    # Temperature histogram
    temp_bins = np.arange(
        -4 + np.floor(np.min([df['temp_cell'].min(), df['temp_air'].min()])),
        1 + np.floor(np.max([df['temp_cell'].max(), df['temp_air'].max()]))
    )
    temp_air_hist_y_raw, temp_air_hist_x_raw = np.histogram(df['temp_air'],
                        bins=temp_bins)
    temp_air_hist_y = scale_to_hours_per_year(temp_air_hist_y_raw)[1:]
    temp_air_hist_x = temp_air_hist_x_raw[1:-1]


    temp_cell_hist_y_raw, temp_cell_hist_x_raw = np.histogram(df['temp_cell'],
                                                            bins=temp_bins)
    temp_cell_hist_y = scale_to_hours_per_year(temp_cell_hist_y_raw)[1:]
    temp_cell_hist_x = temp_cell_hist_x_raw[1:-1]

    # Plotting
    max_pos = np.argmax(np.array(df['v_oc']))
    plot_min_index = np.max([0, max_pos - 1000])
    plot_max_index = np.min([len(df), max_pos + 1000])




    print('making the layout')
    return_layout = [
        html.P("""Using the weather data and the module parameters, the open 
        circuit voltage is simulated using the single diode model. Figure 1 
        shows a histogram of open circuit voltage (Voc) values, with the y 
        axis scaled to the number of hours per year spent at this open 
        circuit voltage. Note that this voltage value would only be reached 
        for a system in open circuit conditions. Typically PV arrays operate 
        at the maximum power point, with a voltage approximately 20% lower 
        than the open circuit voltage. 

        """),
        html.P("""The string voltage calculation provides several standard 
        values for designing string lengths. The values are: 

        """),
        html.Div([
            html.Ul([
                html.Li(
                    dcc.Markdown(
                    """**P99.5** is the 99.5 percentile Voc value over the 
                    simulation time. Statistically Voc will exceed this value 
                    only 0.5% of the year. Suppose that open circuit 
                    conditions occur 1% of the time randomly. In this case 
                    the probability that the weather and system design 
                    maintain the system voltage under the standard limit is 
                    99.995%, i.e. max system voltage would statistically be 
                    exceeded for 26 minutes per year. 

                    """
                    )),
                html.Li(
                    dcc.Markdown(
                        """**Hist** is the historical maximum Voc over the {:.0f} 
                        years of simulation. 
                    
                        """.format(info['timedelta_in_years'])
                    )),
                html.Li(
                    dcc.Markdown(
                        """**Norm_P99.5** is the 99.5 percentile Voc value 
                        when assuming that the PV array is always oriented 
                        normal to the sun. This value can be easily computed 
                        given weather data (DNI + DHI) and the module 
                        parameters since angle-of-incidence calculations are 
                        avoided. This would also be the value to use in the 
                        case of two-axis trackers. 
                    
                        """.format(info['timedelta_in_years'])
                    )),
                html.Li(
                    dcc.Markdown(
                    """**Trad** is the traditional value used for maximum 
                    Voc. This is found using the mean minimum yearly dry bulb 
                    temperature (i.e. find the minimum temperature in each 
                    year and take the mean of those values). The Voc is 
                    calculated assuming 1 sun irradiance (1000 W/m^2), 
                    the mean minimum yearly dry bulb temperature and the 
                    module paramaeters. 
                
                    """
                    )),
                html.Li(
                    dcc.Markdown(
                        """**Day** is similar to the trad value, except the 
                        mean minimum yearly daytime dry bulb temperature is 
                        used as the cell temperature for calculating Voc. 
                        Daytime is defined as GHI greater than 150 W/m^2. The 
                        Voc is calculated assuming 1 sun irradiance (1000 
                        W/m^2), the mean minimum yearly daytime dry bulb 
                        temperature and the module paramaeters. 
                    
                        """
                    )),


                ])

        ], style={'marginLeft': 50}),
        html.P("""Key Voc values are shown in Figure 1. Hover to find more 
        information. 

        """),
        dcc.Graph(
            id='Voc-histogram',
            figure={
                'data': [
                    {'x': voc_hist_x, 'y': voc_hist_y, 'type': 'line',
                     'name': 'Voc'}
                ],
                'layout': go.Layout(
                    title=go.layout.Title(
                        text='Figure 1. Histogram of Voc values over the simultaion time.',
                        xref='paper',
                        x=0
                    ),
                    xaxis={'title': 'Voc (Volts)'},
                    yaxis={'title': 'hours/year'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    annotations=[
                        dict(
                            dict(
                                x=voc_summary['v_oc'][s],
                                y=voc_hist_y[np.argmin(
                                    np.abs(voc_summary['v_oc'][s] - voc_hist_x))],
                                xref='x',
                                yref='y',
                                xanchor='center',
                                text=s,
                                hovertext=voc_summary['long_note'][s],
                                textangle=0,
                                font=dict(
                                    color=plot_color[s]
                                ),
                                arrowcolor=plot_color[s],
                                # bordercolor=plot_color[s],
                                showarrow=True,
                                align='left',
                                standoff=2,
                                arrowhead=4,
                                ax=0,
                                ay=-40
                            ),
                            align='left'
                        )
                        for s in list(voc_summary.index)]
                )
            }
        ),
        html.P("""Figure 2 shows a histogram of the air and cell temperature. 
        A spike at 0 C is sometimes observed and explained below under 
        frequently asked questions. 

        """),
        dcc.Graph(
            id='temperature-histogram',
            figure={
                'data': [
                    {'x': temp_air_hist_x, 'y': temp_air_hist_y,
                     'type': 'line', 'name': 'Air Temperature'},
                    {'x': temp_cell_hist_x, 'y': temp_cell_hist_y,
                     'type': 'line', 'name': 'Cell Temperature'},
                ],
                'layout': go.Layout(
                    title=go.layout.Title(
                        text='Figure 2. Histogram of cell and air temperature',
                        xref='paper',
                        x=0
                    ),
                    xaxis={'title': 'Temperature (C)'},
                    yaxis={'title': 'hours/year'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    # annotations=[
                    #     dict(
                    #         dict(
                    #             x=temperature_poi[s]['value'],
                    #             y=temp_cell_hist_y[np.argmin(
                    #                 np.abs(temperature_poi[s][
                    #                            'value'] - temp_cell_hist_x))],
                    #             xref='x',
                    #             yref='y',
                    #             xanchor='center',
                    #             text=temperature_poi[s]['short_label'],
                    #             hovertext=temperature_poi[s]['hover_label'],
                    #             textangle=0,
                    #             font=dict(
                    #                 color=temperature_poi[s]['color']
                    #             ),
                    #             arrowcolor=temperature_poi[s]['color'],
                    #             showarrow=True,
                    #             align='left',
                    #             standoff=2,
                    #             arrowhead=4,
                    #             ax=0,
                    #             ay=-40
                    #         ),
                    #         align='left'
                    #     )
                    #     for s in temperature_poi]
                )
            }
        ),

        dcc.Markdown(
            """Figure 3 shows the time dependence of cell temperature, 
            air temperature and Voc around the time that the historical 
            maximum Voc was reached. 
            
            """
        ),
        dcc.Graph(
            id='time-plot',
            figure={
                'data': [
                    {'x': df.index[plot_min_index:plot_max_index],
                     'y': df['temp_cell'][plot_min_index:plot_max_index],
                     'type': 'line', 'name': 'Cell Temperature (C)'},
                    {'x': df.index[plot_min_index:plot_max_index],
                     'y': df['temp_air'][plot_min_index:plot_max_index],
                     'type': 'line', 'name': 'Air Temperature (C)'},
                    {'x': df.index[plot_min_index:plot_max_index],
                     'y': df['v_oc'][plot_min_index:plot_max_index],
                     'type': 'line', 'name': 'V_oc (V)'}
                ],
                'layout': go.Layout(
                    title=go.layout.Title(
                            text='Figure 3. Time dependence of air temperature, cell temperature, and Voc. Hist marks the historical maximum Voc.',
                            xref='paper',
                            x=0
                    ),
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Value'},
                    # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest',
                    annotations=[
                        dict(
                            dict(
                                x=weather.index[max_pos],
                                y=df['v_oc'][max_pos],
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
        dcc.Markdown(
            """Download the simulation results as csv files here: 
        
            """
        ),
        html.Div([
            html.A('Download csv summary',
                   id='download-link',
                   download='summary.csv',
                   href=summary_text_for_download,
                   target='_blank'),
        ]),
        # html.Div([
        #     html.A('Download 1 year raw data as csv',
        #        id='download-link',
        #        download='raw_data.csv',
        #        href=csv_string_one_year,
        #        target='_blank'),
        #     ]),
    ]

    return return_layout

    # system_parameters = {
    #     'racking_model': {'a': a, 'b': b, 'deltaT': DT},
    #     # 'racking_model': racking_model,
    #     'surface_tilt': float(surface_tilt),
    #     'surface_azimuth': float(surface_azimuth),
    #     'mount_type': mount_type,
    #     'axis_tilt': float(axis_tilt),
    #     'axis_azimuth': float(axis_azimuth),
    #     'max_angle': float(max_angle),
    #     'backtrack': float(backtrack),
    #     'ground_coverage_ratio': float(ground_coverage_ratio)}
    #
    # module_parameters = pvtoolslib.cec_modules[module_name]
    #
    # # Overwrite provided module parameters.
    # module_parameters['Voco'] = float(Voco)
    # module_parameters['Bvoco'] = float(Bvoco)
    # module_parameters['Mbvoc'] = float(Mbvoc)
    # module_parameters['Cells_in_Series'] = float(Cells_in_Series)
    # module_parameters['diode_ideality_factor'] = float(diode_ideality_factor)
    # module_parameters['FD'] = float(FD)
    #
    # module_parameters['A0'] = float(A0)
    # module_parameters['A1'] = float(A1)
    # module_parameters['A2'] = float(A2)
    # module_parameters['A3'] = float(A3)
    # module_parameters['A4'] = float(A4)
    # module_parameters['B0'] = float(B0)
    # module_parameters['B1'] = float(B1)
    # module_parameters['B2'] = float(B2)
    # module_parameters['B3'] = float(B3)
    # module_parameters['B4'] = float(B4)
    # module_parameters['B5'] = float(B5)
    #
    # filedata = pvtoolslib.get_s3_filename_df()
    # filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
    #                                                      filedata)
    #
    #
    #
    # print('Getting weather data...')
    # weather, info = pvtoolslib.get_s3_weather_data(filedata_closest['filename'].iloc[0])
    #
    # # print(info.keys())
    # print('Simulating system...')
    # (df, mc) = vocmaxlib.calculate_max_voc(weather, info,
    #                                        module_parameters=module_parameters,
    #                                        system_parameters=system_parameters)
    #
    #
    # info_df = pd.DataFrame(
    #     {'Weather data source': info['Source'],
    #      'Location ID': info['Location_ID'],
    #      'Latitude': info['Latitude'],
    #      'Longitude': info['Longitude'],
    #      'Elevation': info['Elevation'],
    #      'Time Zone': info['local_time_zone'],
    #      'Data time step (hours)': info['interval_in_hours'],
    #      'Data time length (years)': info['timedelta_in_years'],
    #      'PVTOOLS Version': pvtoolslib.version,
    #      'v_oc units':'Volts',
    #      'temp_air units': 'C',
    #      'wind_speed units': 'm/s',
    #      'dni units': 'W/m^2',
    #      'dhi units': 'W/m^2',
    #      'ghi units': 'W/m^2',
    #      },
    #     index=[0]
    # )
    # print('Generating files for downloading...')
    # df_temp = df.copy()
    # df_temp['wind_speed'] = df_temp['wind_speed'].map(lambda x: '%2.1f' % x)
    # df_temp['v_oc'] = df_temp['v_oc'].map(lambda x: '%3.2f' % x)
    # df_temp['temp_cell'] = df_temp['temp_cell'].map(lambda x: '%2.1f' % x)
    #
    # # csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(
    # #     df_temp.to_csv(index=False, encoding='utf-8',float_format='%.3f')
    # # )
    #
    # csv_string = "data:text/csv;charset=utf-8,"
    # csv_string_one_year = "data:text/csv;charset=utf-8," + \
    #     urllib.parse.quote(
    #         info_df.to_csv(index=False,
    #                                 encoding='utf-8',
    #                                 float_format='%.3f')
    #     ) + \
    #     urllib.parse.quote(
    #         df_temp[0:17520].to_csv(index=False,
    #                                 encoding='utf-8',
    #                                 float_format='%.3f')
    #     )
    #
    #
    #
    # print('done')
    #
    # y, c = np.histogram(df['v_oc'],
    #                     bins=np.linspace(df['v_oc'].max() * 0.75,
    #                                      df['v_oc'].max() + 1, 500))
    #
    # years = list(set(weather.index.year))
    # yearly_min_temp = []
    # yearly_min_daytime_temp = []
    # for j in years:
    #     yearly_min_temp.append(
    #         weather[weather.index.year == j]['temp_air'].min())
    #     yearly_min_daytime_temp.append(
    #         weather[weather.index.year == j]['temp_air'][
    #             weather[weather.index.year == j]['ghi'] > 150].min()
    #     )
    # mean_yearly_min_ambient_temp = np.mean(yearly_min_temp)
    # mean_yearly_min_daytime_ambient_temp = np.mean(yearly_min_daytime_temp)
    #
    # # min_daytime_temp = df['temp_air'][df['ghi']>150].min()
    #
    # voc_1sun_min_temp = mc.system.sapm(1, mean_yearly_min_ambient_temp)['v_oc']
    # voc_1sun_min_daytime_temp = \
    # mc.system.sapm(1, mean_yearly_min_daytime_ambient_temp)['v_oc']
    #
    # voc_dni_cell_temp = \
    # mc.system.sapm((df['dni'] + df['dhi']) / 1000, df['temp_cell'])[
    #     'v_oc'].max()
    # voc_P99p5 = np.percentile(
    #     df['v_oc'][np.logical_not(np.isnan(df['v_oc']))],
    #     99.5)
    # voc_P99 = np.percentile(df['v_oc'][np.logical_not(np.isnan(df['v_oc']))],
    #                         99)
    #
    # # results_dict = {
    # #     'Source': info['source'],
    # #     'Location ID': info['location_id'],
    # #     'Elevation': info['elevation'],
    # #     'Latitude': info['lat'],
    # #     'Longitude': info['lon'],
    # #     # 'DHI Units': info['DHI Units'][0],
    # #     # 'DNI Units': info['DNI Units'][0],
    # #     # 'GHI Units': info['GHI Units'][0],
    # #     # 'V_oc Units': 'V',
    # #     # 'Wind Speed Units': info['Wind Speed'][0],
    # #     'interval_in_hours': info['interval_in_hours'],
    # #     'timedelta_in_years': info['timedelta_in_years'],
    # #     'NSRDB Version': info['version'],
    # #     'PVLIB Version': pvlib._version.get_versions()['version'],
    # #     'PVTools Version': '0.0.1',
    # #     'Date Created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # # }
    # # info_df = pd.DataFrame(results_dict, index=[0])
    #
    # summary = [
    #     'Latitude: {:0.4f}'.format(info['Latitude']),
    #     'Longitude: {:0.4f}'.format(info['Longitude']),
    #     'Maximum Design String Voltage: {:0.2f} V'.format(max_string_voltage),
    #     'Historical Max Voc: {:0.3f} V'.format(df.v_oc.max()),
    #     'P99.5 Voc: {:0.3f} V'.format(voc_P99p5),
    #     'P99.5 Max String length: {:0.0f} modules'.format(
    #         np.floor(max_string_voltage / voc_P99p5)),
    #     'Traditional max Voc: {:0.3f} V'.format(voc_1sun_min_temp),
    #     'Traditional Max String length: {:0.0f} modules'.format(
    #         np.floor(max_string_voltage / voc_1sun_min_temp)),
    #     'Yearly mean minimum ambient temperature: {:0.3f} C'.format(mean_yearly_min_ambient_temp),
    #     'Weather data source: {}'.format(info['Source']),
    #     'Location ID: {}'.format(info['Location_ID']),
    #     'Weather data start date: {}'.format(
    #         df.index[0].strftime("%Y-%m-%d %H:%M:%S")),
    #     'Weather data end date: {}'.format(
    #         df.index[-1].strftime("%Y-%m-%d %H:%M:%S")),
    #
    # ]
    #
    # # summary.append('Sandia Module parameters')
    # # for p in list(module_parameters.keys()):
    # #     summary.append( p + ': {:0.3f}'.format(module_parameters[p]))
    #
    #
    #           # + \
    #           # 'Location ID, {}\n'.format(info['location_id']) + \
    #           # 'Weather data start date, {}\n'.format(
    #           #     df.index[0].strftime("%Y-%m-%d %H:%M:%S")) + \
    #           # 'Weather data end date, {}\n'.format(
    #           #     df.index[-1].strftime("%Y-%m-%d %H:%M:%S")) + \
    #           # 'Latitude, {:0.4f}\n'.format(info.Latitude[0]) + \
    #           # 'Longitude, {:0.4f}\n'.format(info.Longitude[0]) + \
    #           # 'P99 Voc (V), {:0.3f}\n'.format(np.percentile(df.v_oc, 99)) + \
    #           # 'Max Historical Voc (V), {:0.3f}\n'.format(df.v_oc.max()) + \
    #           # 'P01 Air Temp (C), {:0.2f}\n'.format(
    #           #     np.percentile(df['temp_air'], 1)) + \
    #           # 'Min Historical Air Temp (C), {:0.3f}\n'.format(
    #           #     df['temp_air'].min()) + \
    #           # 'P01 Cell Temp (C), {:0.2f}\n'.format(
    #           #     np.percentile(df['temp_cell'], 1)) + \
    #           # 'Min Historical Cell Temp (C), {:0.2f}\n'.format(
    #           #     df['temp_cell'].min())
    #
    # # print(info_df)
    #
    # # # Make a directory for saving session files.
    # # if not os.path.isdir(os.path.join('downloads',session_id)):
    # #     os.mkdir(os.path.join('downloads',session_id))
    # # save_filename = os.path.join('downloads',session_id,'maxvoc_data.csv')
    # # info_filename = os.path.join('downloads',session_id,'maxvoc_info.csv')
    # # temp_filename = os.path.join('downloads', session_id, 'maxvoc_temp.pkl')
    # # print('Saving data as ' + str(save_filename) + '...')
    # # with open(save_filename,'w') as f:
    # #     f.write(info_df.to_csv(index=False))
    # #     if len(generate_datafile)>0:
    # #         f.write(df.to_csv(float_format='%.2f'))
    # #
    # # with open(info_filename,'w') as f:
    # #     # f.write('hello')
    # #     # f.write(info_df.to_csv(index=False))
    # #     f.write(summary)
    # # print('done')
    #
    # # Make histograms
    # def scale_to_hours_per_year(y):
    #     return y / info['timedelta_in_years'] * info['interval_in_hours']
    #
    # y_scale = scale_to_hours_per_year(y)
    # voc_hist_y = y_scale[1:]
    # voc_hist_x = c[1:-1]
    #
    # temp_bins = np.arange(
    #     -4 + np.floor(np.min([df['temp_cell'].min(), df['temp_air'].min()])),
    #     1 + np.floor(np.max([df['temp_cell'].max(), df['temp_air'].max()]))
    # )
    #
    # temp_cell_hist, temp_cell_hist_bin = np.histogram(df['temp_cell'],
    #                                                   bins=temp_bins)
    # temp_cell_hist = scale_to_hours_per_year(temp_cell_hist)
    #
    # temp_air_hist, temp_air_hist_bin = np.histogram(df['temp_air'],
    #                                                 bins=temp_bins)
    # temp_air_hist = scale_to_hours_per_year(temp_air_hist)
    #
    # temp_cell_hist_x = temp_cell_hist_bin[1:-1]
    # temp_air_hist_x = temp_air_hist[1:-1]
    # temp_cell_hist_y = temp_cell_hist[1:]
    # temp_air_hist_y = temp_air_hist[1:]
    #
    # max_pos = np.argmax(np.array(df.v_oc))
    # plot_min_index = np.max([0, max_pos - 1500])
    # plot_max_index = np.min([len(df.v_oc), max_pos + 1500])
    #
    # colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    #
    # voc_poi = pd.DataFrame.from_dict(
    #     {
    #         # 'P99':
    #         #     ['P99',
    #         #      'P99 Voc: {:.3f} V<br>'
    #         #      'Maximum String length: {:.0f}<br>'.format(
    #         #          voc_P99,
    #         #          np.floor(max_string_voltage / voc_P99)
    #         #      ),
    #         #      voc_P99,
    #         #      'rgb(0, 0, 0)'
    #         #      ],
    #         'P99.5':
    #             ['P99.5',
    #              'P99.5 Voc: {:.3f} V<br>'
    #              'Maximum String length: {:.0f}<br>'
    #              'Recommended 690.7(A)(3) value'.format(
    #                  voc_P99p5,
    #                  np.floor(max_string_voltage / voc_P99p5)
    #              ),
    #              voc_P99p5,
    #              colors[2]
    #              ],
    #         'Max':
    #             ['Hist',
    #              'Historical Maximum Voc: {:.3f} V<br>'
    #              'Maximum String length: {:.0f}<br>'
    #              'Conservative 690.7(A)(3) value'.format(
    #                  df.v_oc.max(),
    #                  np.floor(max_string_voltage / df.v_oc.max())
    #              ),
    #              df.v_oc.max(),
    #              colors[3]
    #              ],
    #         'Trad':
    #             ['Trad',
    #              'Traditional Maximum Voc: {:.3f} V<br>'
    #              'Maximum String length: {:.0f}<br>'
    #              'Calculated using 1 sun and mean yearly min ambient temp of {:.1f} C<br>Conservative 690.7(A)(1) value'.format(
    #                  voc_1sun_min_temp,
    #                  np.floor(max_string_voltage / voc_1sun_min_temp),
    #                  mean_yearly_min_ambient_temp,
    #              ),
    #              voc_1sun_min_temp,
    #              colors[4]
    #              ],
    #         'Tradday':
    #             ['Day',
    #              'Traditional Maximum Daytime Voc: {:.3f} V<br>'
    #              'Maximum String length: {:.0f}<br>'
    #              'Calculated using 1 sun and mean yearly min daytime (GHI>150) temp of {:.1f} C<br>'
    #              'Recommended 690.7(A)(1) value'.format(
    #                  voc_1sun_min_daytime_temp,
    #                  np.floor(max_string_voltage / voc_1sun_min_daytime_temp),
    #                  mean_yearly_min_daytime_ambient_temp),
    #              voc_1sun_min_daytime_temp,
    #              colors[5]
    #              ],
    #         'dni':
    #             ['Normal',
    #              'Max Voc using DNI+DHI (simple calculation): {:.3f} V<br>'
    #              'Maximum String length: {:.0f}<br>'.format(
    #                  voc_dni_cell_temp,
    #                  np.floor(max_string_voltage / voc_dni_cell_temp)),
    #              voc_dni_cell_temp,
    #              colors[6]
    #              ],
    #
    #     },
    #     orient='index',
    #     columns=['short_label', 'hover_label', 'value', 'color']
    # ).transpose()
    #
    # temperature_poi = pd.DataFrame.from_dict(
    #     {
    #         'P1 Air':
    #             ['P1',
    #              '1 Percentile Air Temperature: {:.1f} C'.format(
    #                  np.percentile(df['temp_air'], 1)),
    #              np.percentile(df['temp_air'], 1),
    #              'rgb(0, 0, 0)'
    #              ],
    #         # 'P4 Air':
    #         #  ['P4',
    #         #   'P4 Air Temperature: {:.1f} C'.format(np.percentile(df['temp_air'], 4)),
    #         #   np.percentile(df['temp_air'], 4),
    #         #   'rgb(0, 0, 0)'
    #         #   ],
    #         'Hist':
    #             ['HA',
    #              'Historical Minimum Ambient Temperature: {:.1f} C'
    #              '<br>Conservative 690.7(A)(1) value'.format(
    #                  df['temp_air'].min()),
    #              df['temp_air'].min(),
    #              'rgb(0, 0, 0)'
    #              ],
    #         'Hist2':
    #             ['Day',
    #              'Historical Minimum Daytime Ambient Temperature: {:.1f} C'
    #              '<br>Recommended 690.7(A)(1) value'.format(
    #                  df['temp_air'][df['ghi'] > 150].min()),
    #              df['temp_air'][df['ghi'] > 150].min(),
    #              'rgb(0, 0, 0)'
    #              ],
    #         # 'Hist2':
    #         #     ['HC',
    #         #      'Historical Minimum Cell Temperature: {:.1f} C'.format(
    #         #      df['temp_cell'].min()),
    #         #      df['temp_cell'].min(),
    #         #      'rgb(0, 0, 0)'
    #         #      ],
    #         'TM':
    #             ['Max',
    #              'Cell Temperature when max Voc was reached: {:.1f} C'.format(
    #                  df['temp_cell'][max_pos]),
    #              df['temp_cell'][max_pos],
    #              'rgb(0, 0, 0)'
    #              ],
    #     },
    #     orient='index',
    #     columns=['short_label', 'hover_label', 'value', 'color']
    # ).transpose()
    #
    # #
    # #
    # # voc_poi = pd.DataFrame.from_dict(
    # #     {
    # #         'P99':
    # #          ['P99',
    # #           'P99 Voc ',
    # #           909
    # #           ]
    # #      },
    # #     orient='index',
    # #     columns = ['short_label','hover_label','value']
    # # ).transpose()
    #
    # #
    # # voc_poi = {'P99 Voc': np.percentile(df.v_oc, 99),
    # #            'P99.9 Voc (Recommended)': np.percentile(df.v_oc, 99.9),
    # #            'Historical Max Voc (Conservative)': df.v_oc.max(),
    # #            '1 sun, historical min temp (Traditional)': voc_1sun_min_temp
    # #            }
    #
    # print('making output graphs...')
    #
    # return_layout = [
    #     html.P('Simulation results for maximum Voc.'),
    #     dcc.Graph(
    #         id='Voc-histogram',
    #         figure={
    #             'data': [
    #                 {'x': voc_hist_x, 'y': voc_hist_y, 'type': 'line',
    #                  'name': 'Voc'}
    #             ],
    #             'layout': go.Layout(
    #                 xaxis={'title': 'Voc (Volts)'},
    #                 yaxis={'title': 'hours/year'},
    #                 # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #                 hovermode='closest',
    #                 annotations=[
    #                     dict(
    #                         dict(
    #                             x=voc_poi[s]['value'],
    #                             y=voc_hist_y[np.argmin(
    #                                 np.abs(voc_poi[s]['value'] - voc_hist_x))],
    #                             xref='x',
    #                             yref='y',
    #                             xanchor='center',
    #                             text=voc_poi[s]['short_label'],
    #                             hovertext=voc_poi[s]['hover_label'],
    #                             textangle=0,
    #                             font=dict(
    #                                 color=voc_poi[s]['color']
    #                             ),
    #                             arrowcolor=voc_poi[s]['color'],
    #                             showarrow=True,
    #                             align='left',
    #                             standoff=2,
    #                             arrowhead=4,
    #                             ax=0,
    #                             ay=-40
    #                         ),
    #                         align='left'
    #                     )
    #                     for s in voc_poi]
    #             )
    #         }
    #     ),
    #     dcc.Graph(
    #         id='temperature-histogram',
    #         figure={
    #             'data': [
    #                 {'x': temp_cell_hist_bin[1:-1], 'y': temp_cell_hist[1:],
    #                  'type': 'line', 'name': 'Cell Temperature'},
    #                 {'x': temp_air_hist_bin[1:-1], 'y': temp_air_hist[1:],
    #                  'type': 'line', 'name': 'Air Temperature'}
    #             ],
    #             'layout': go.Layout(
    #                 xaxis={'title': 'Temperature (C)'},
    #                 yaxis={'title': 'hours/year'},
    #                 # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #                 hovermode='closest',
    #                 annotations=[
    #                     dict(
    #                         dict(
    #                             x=temperature_poi[s]['value'],
    #                             y=temp_cell_hist_y[np.argmin(
    #                                 np.abs(temperature_poi[s][
    #                                            'value'] - temp_cell_hist_x))],
    #                             xref='x',
    #                             yref='y',
    #                             xanchor='center',
    #                             text=temperature_poi[s]['short_label'],
    #                             hovertext=temperature_poi[s]['hover_label'],
    #                             textangle=0,
    #                             font=dict(
    #                                 color=temperature_poi[s]['color']
    #                             ),
    #                             arrowcolor=temperature_poi[s]['color'],
    #                             showarrow=True,
    #                             align='left',
    #                             standoff=2,
    #                             arrowhead=4,
    #                             ax=0,
    #                             ay=-40
    #                         ),
    #                         align='left'
    #                     )
    #                     for s in temperature_poi]
    #             )
    #         }
    #     ),
    #     html.Div(
    #         'Calculation performed for {:.1f} years, showing position of maximum Voc'.format(
    #             info['timedelta_in_years'])),
    #     dcc.Graph(
    #         id='temperature-PLOT',
    #         figure={
    #             'data': [
    #                 {'x': weather.index[plot_min_index:plot_max_index],
    #                  'y': df['temp_cell'][plot_min_index:plot_max_index],
    #                  'type': 'line', 'name': 'Cell Temperature'},
    #                 {'x': weather.index[plot_min_index:plot_max_index],
    #                  'y': df['temp_air'][plot_min_index:plot_max_index],
    #                  'type': 'line', 'name': 'Air Temperature'}
    #             ],
    #             'layout': go.Layout(
    #                 xaxis={'title': 'Date'},
    #                 yaxis={'title': 'Temperature (C)'},
    #                 # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #                 hovermode='closest',
    #                 annotations=[
    #                     dict(
    #                         dict(
    #                             x=weather.index[max_pos],
    #                             y=df['temp_cell'][max_pos],
    #                             xref='x',
    #                             yref='y',
    #                             xanchor='center',
    #                             text='Hist',
    #                             hovertext='Historical max Voc: {:.2f} V<br>'
    #                                       'Air temperature: {:.0f} C<br>'
    #                                       'Cell temperature: {:.0f} C<br>'
    #                                       'GHI: {:.0f} W/m^2'.format(
    #                                 df['v_oc'][max_pos],
    #                                 df['temp_air'][max_pos],
    #                                 df['temp_cell'][max_pos],
    #                                 df['ghi'][max_pos]),
    #                             textangle=0,
    #                             showarrow=True,
    #                             standoff=2,
    #                             arrowhead=4,
    #                             borderwidth=2,
    #                             borderpad=4,
    #                             opacity=0.8,
    #                             bgcolor='#ffffff',
    #                             ax=0,
    #                             ay=-40
    #                         ),
    #                         align='center'
    #                     )]
    #             )
    #         }
    #     ),
    #     # html.A(html.Button('Download results as csv'),href=''),
    #     # dbc.Button('Download results as csv',id='download_csv',n_clicks=0),
    #     html.H4('Results summary'),
    #     # html.Details([
    #         # html.Summary('View text summary'),
    #     html.Div([html.P(s) for s in summary],
    #              style={'marginLeft': 10}),
    #     # ]),
    #     # html.P(
    #     #     html.A('Download full data as csv file (use firefox)', id='download-data',href=save_filename)
    #     # ),
    #     html.Div([
    #         html.A('Download 1 year raw data as csv',
    #            id='download-link',
    #            download='rawdata.csv',
    #            href=csv_string_one_year,
    #            target='_blank'),
    #         ]),
    #     html.Div([
    #     html.A('Download all raw data as csv (use firefox)',
    #            id='download-link',
    #            download='rawdata.csv',
    #            href=csv_string,
    #            target='_blank'),
    #         ]),
    #     # html.Button(id='download-summary', children='Download Summary'),
    #     # html.Button(id='download-data', children='Download Data as CSV')
    # ]
    #
    #
    #
    # # print('converting to json...')
    # # weather_json = weather.to_json()
    # # print('done')
    #
    # print('** Calculation done.')


    # return []
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



if __name__ == '__main__':
    app.run_server(debug=True)