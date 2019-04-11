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
import flask
# import json
# import time
import datetime
import io
import pvtoolslib
import urllib


from app import app



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
    dcc.Markdown("""This tool predicts the maximum open circuit voltage (Voc) 
    expected to occur for modules in a solar installation at a particular 
    location. One application of this tool is to determine optimal string 
    sizes in accordance with national electric code (NEC) standards.

    """),

    dbc.Row([
        dbc.Col(
            [
            dbc.Button("Tell me more about NEC",
                       id="nec-button",
                       n_clicks=0,
                       color='light',
                       className="mb-3")
            ],width=3
        ),
        dbc.Col([
            dbc.Button("Show me more details",
                       id="details-button",
                       color='light',
                       n_clicks=0,
                   className="mb-3"),
        ],width=3)

    ],justify='start'),
#                            The maximum open circuit voltage(Voc) is a key design
#                            parameter for solar power
# plants.This
# application
# provides
# an
# industry - standard
# method
# for calculating the maximum open circuit voltage
# given weather data and module parameters.Weather data is sourced from the
# national solar radiation database (NSRDB)[1].The open circuit voltage
# is calculated using the Sandia PV models[2] as implemented in the open
# source python library PVLIB[3].This work is funded by the Duramat
# consortium[4].

    dbc.Collapse(
        dbc.Card(dbc.CardBody([

            dcc.Markdown("""### National Electric Code Standards
            
            The national electric code 2017 lists three different methods 
            for determining the maximum string length in Article 690.7:
        
            """.replace('    ','')
            ),
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
            html.P("""This tool provides standard values for methods 690.7(A)(1) 
            and 690.7(A)(3). For method 690.7(A)(1), The lowest 
            expected ambient temperature is calculated by finding the minimum 
            temperature during daylight hours, defined as GHI>150 W/m^2. For 
            method 690.7(A)(3), the full PVLIB model is run using weather 
            data from the selected location and module parameters. 
            
            """),

        ])),
        id="nec-collapse",
    ),

    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            dcc.Markdown("""
            ### Simulation methods
            
            The string voltage calculator uses the open 
            source [PVLIB](https://pvlib-python.readthedocs.io/en/latest/) 
            library to perform the calculation using the single diode model 
            and the De Soto parameterization [5]. Module parameters are 
            either taken from a standard database or entered manually. The 
            calculation conservatively assumes that all diffuse irradiance is 
            used (FD=1) and that there are no reflection losses from the top 
            cell (aoi_model='no_loss'). These two assumptions cause a small 
            increase in Voc and make the simulation more conservative. 
            Specific details on the exact calculation method are described in 
            [vocmax](https://github.com/toddkarin/vocmax).  
            
            ### Weather Data
            
            Weather data was sourced from the National Solar Radiation 
            Database (NSRDB) [1]. The data was sampled across the continental 
            US at approximately a 0.125 degree grid, and at a lower 
            resolution elsewhere. If a different weather data source is 
            desired, it is necessary to use the open source associated python 
            package [vocmax]( https://github.com/toddkarin/vocmax), 
            which performs the same calculation as this web tool. If the 
            particular weather data point is not on the map, please contact 
            us and we will try to provide it. 
            
            ### Who we are
            
            We are a collection of national lab researchers funded under the 
            [Durable module materials consortium (DuraMAT)](https://www.duramat.org/). 
            
            """.replace('    ','')
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
                        src=app.get_asset_url('LBL_Masterbrand_logo_with_Tagline-01.jpg'),
                        style={'height': 50})
                )
            ],justify='center'
            )
        ])), id="details-collapse"
    ),



    # html.H2('Simulation Input'),
    html.H2('Step 1: Provide location of installation'),
    dbc.Card([
        dbc.CardHeader('Choose Location'),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Latitude'),
                    dbc.Input(id='lat', value='37.88', type='text'),
                    dbc.Label('Longitude'),
                    dbc.Input(id='lon', value='-122.25', type='text'),
                    dbc.FormText(id='closest-message',
                             children='Closest point shown on map'),
                    html.P(''),
                    html.Div([
                    dbc.Button(id='get-weather', n_clicks=0,
                                           children='Get Weather Data'),
                        ]),
                    html.Div(id='weather_data_download'),

                ],md=4),
                dbc.Col([
                    html.Div(id='location-map', children=[dcc.Graph(id='map')]),
                    html.P('Find location on map, enter coordinates manually.')
                ],md=8)
            ]),
        ]),
    ]),
    html.H2('Step 2: Provide details on module and installation type'),
    dbc.Card([
        dbc.CardHeader('Module Parameters'),
        dbc.CardBody([
            dbc.Label("""To select module parameters from a library of common 
            modules, select 'Library Lookup'. Or select 'manual entry' to 
            enter the parameters for the De Soto model [5]. 
            
            """),
            dbc.Tabs([
                dbc.Tab([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Markdown("""**Module name** (from CEC database).
                                
                                """),
                                dcc.Dropdown(
                                    id='module_name',
                                    options=pvtoolslib.cec_module_dropdown_list,
                                    value=pvtoolslib.cec_module_dropdown_list[0]['value'],
                                    style={'max-width': 500}
                                ),
                                html.P(''),
                                html.Div(id='module_name_iv')
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
                                dbc.FormText("""Module name for records"""),
                                dbc.Label("""alpha_sc"""),
                                dbc.Input(id='alpha_sc', value='0.007997', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The short-circuit current 
                                temperature coefficient of the module in 
                                units of A/C 
        
                                """
                                ),
                                dbc.Label("""a_ref"""),
                                dbc.Input(id='a_ref', value='1.6413', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The product of the usual 
                                diode ideality factor (n, unitless), number 
                                of cells in series (Ns), and cell thermal 
                                voltage at reference conditions, in units of V. 
        
                                            """),
                                dbc.Label("""I_L_ref"""),
                                dbc.Input(id='I_L_ref', value='7.843', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The light-generated current (or 
                                photocurrent) at reference conditions, in amperes. 
        
                                            
                                """),

                                dbc.Label("""I_o_ref"""),
                                dbc.Input(id='I_o_ref', value='1.936e-09', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The dark or diode reverse 
                                saturation current at reference conditions, in amperes. 
                                """),

                                dbc.Label("""R_sh_ref
        
                                            """),

                                dbc.Input(id='R_sh_ref', value='839.4', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The shunt resistance at 
                                reference conditions, in ohms. 
                                 
                                """),

                                dbc.Label("""R_s"""),
                                dbc.Input(id='R_s', value='0.359', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""The series resistance at reference 
                                conditions, in ohms. 
                                
                                """),
                                # dbc.Label("""Adjust"""),
                                # dbc.Input(id='Adjust', value='16.5', type='text',
                                #           style={'max-width': 200}),
                                # dbc.FormText("""The adjustment to the
                                # temperature coefficient for short circuit
                                # current, in percent.
                                #
                                # """),
                                dbc.Label("""FD"""),
                                dbc.Input(id='FD', value='1', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""Fraction of diffuse 
                                irradiance arriving at cell.  
                                
                                """),
                                html.P(''),
                                # dbc.Button('Calculate module parameters',id='show_iv',n_clicks=0),
                                html.Div(id='manual_iv')
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
        ])
    ]),
    html.P(''),
    dbc.Card([
        dbc.CardHeader('Thermal model'),
        dbc.CardBody([
            html.P("""The thermal model parameters determine how the cell 
            temperature depends on ambient temperature, plane-of-array 
            irradiance and wind speed. 
            
            """),

            dbc.Tabs([
                dbc.Tab([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Markdown('**Racking Model**'),
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
                                dbc.FormText("""Standard coefficents for 
                                calculating temperature of cell based on 
                                ambient temperature, plane of array 
                                irradiance and wind speed. 
                                
                                """)
                             ],

                        )
                    )
                ], tab_id='lookup', label='Default models'),
                dbc.Tab([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("""a
                                """),
                                dbc.Input(id='a', value='-3.47', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""Empirically-determined coefficient 
                                establishing the upper limit for module temperature 
                                at low wind speeds and high solar irradiance 
                                
                                
                                """),
                                dbc.Label("""b"""),
                                dbc.Input(id='b', value='-0.0594', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(""" Empirically-determined coefficient 
                                establishing the rate at which module temperature 
                                drops as wind speed increases (s/m) 
                                
                                """),
                                dbc.Label("""DT"""),
                                dbc.Input(id='DT', value='3', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""Temperature difference between cell 
                                and module at reference irradiance (C) 
                                
                                """),
                             ]
                        )
                    )
                ], tab_id='manual', label='Manual Entry')
            ], id='thermal_model_input_type', active_tab='lookup'),
        ])
    ]),
    html.P(''),
    dbc.Card([
        dbc.CardHeader('Racking Type'),
        dbc.CardBody([
            dcc.Markdown("""Choose the mounting configuration of the array. 
            
            """),
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
                             dbc.FormText("""The tilt of the axis of rotation 
                             (i.e, the y-axis defined by axis_azimuth) with 
                             respect to horizontal, in decimal degrees."""),
                             dbc.Label('Axis Azimuth (degrees)'),
                             dbc.Input(id='axis_azimuth', value='0', type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""A value denoting the compass 
                             direction along which the axis of rotation lies. 
                             Measured in decimal degrees East of North."""),
                             dbc.Label('Max Angle (degrees)'),
                             dbc.Input(id='max_angle', value='90', type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""A value denoting the maximum 
                             rotation angle, in decimal degrees, of the 
                             one-axis tracker from its horizontal position (
                             horizontal if axis_tilt = 0). A max_angle of 90 
                             degrees allows the tracker to rotate to a 
                             vertical position to point the panel towards a 
                             horizon. max_angle of 180 degrees allows for 
                             full rotation."""),
                             dbc.Label('Backtrack'),
                             dbc.RadioItems(
                                 options=[
                                     {"label": "True", "value": True},
                                     {"label": "False", "value": False},
                                 ],
                                 value=True,
                                 id="backtrack",
                             ),
                             dbc.FormText("""Controls whether the tracker has 
                             the capability to ''backtrack'' to avoid 
                             row-to-row shading. False denotes no backtrack 
                             capability. True denotes backtrack 
                             capability."""),
                             dbc.Label('Ground Coverage Ratio'),
                             dbc.Input(id='ground_coverage_ratio', value='0.286',
                                       type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""A value denoting the ground 
                             coverage ratio of a tracker system which 
                             utilizes backtracking; i.e. the ratio between 
                             the PV array surface area to total ground area. 
                             A tracker system with modules 2 meters wide, 
                             centered on the tracking axis, with 6 meters 
                             between the tracking axes has a gcr of 
                             2/6=0.333. If gcr is not provided, a gcr of 2/7 
                             is default. gcr must be <=1"""),
                             ]
                        )
                    )
                ], tab_id='single_axis_tracker', label='Single Axis Tracker')
            ], id='mount_type', active_tab='fixed_tilt'),
        ])
    ]),
    html.P(''),
    html.H2('Step 3: Provide Desired Maximum String Voltage'),
    dbc.Card([
        dbc.CardHeader(['String Voltage Limit']),
        dbc.CardBody([
            dcc.Markdown("""Set the design max string voltage for the PV system. 
            
            """),
            dcc.Markdown('**Max string voltage (V)**'),
            dbc.Input(id='max_string_voltage',
                      value='1500',
                      type='text',
                      style={'max-width': 200}),
            dbc.FormText('Maximum string voltage for calculating string length'),
            ])
        ]),

    html.H2('Final Step: Run Calculation'),
    dbc.Card([
        dbc.CardHeader('Calculation'),
        dbc.CardBody([
            html.P('Press "Calculate" to run Voc calculation (~10 seconds)'),
            dbc.Button(id='submit-button', n_clicks=0, children='Calculate',
                       color="secondary"),
        ])
    ]),
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
            "What if I want to run the simulation myself? Where's the source code?"),
        html.Div([
            dcc.Markdown("""If you would like to run the calculation as a 
            python program, please visit the [github page for vocmax]( 
            https://github.com/toddkarin/vocmax) 
 

            """),
            dcc.Markdown("""Additionally, if you would like to take a look at 
            the source code for this website, please visit the [github page 
            for pvtools]( https://github.com/toddkarin/pvtools) 
            
            """)

        ],style={'marginLeft': 50}
        ),

    ]),
    html.Details([
        html.Summary(
            "Do you store any of my data?"),
        html.Div([
            dcc.Markdown("""We take your privacy seriously. We do not store 
            any metadata related to the simulation. For understanding the 
            usage of the app, we count the number of times the 'calculate' 
            button is pressed and also record whether default values were 
            used or not. We also count the number of unique users that use 
            the app. We specifically exclude logging any events that generate 
            identifiable metadata. 


            """),

        ], style={'marginLeft': 50}
        ),

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
    html.P('PVTOOLS Version ' + pvtoolslib.version),
    html.P('Author: Todd Karin')
],
    style={'columnCount': 1,
           'maxWidth': 1000,
           'align': 'center'})



@app.callback(
    Output("nec-collapse", "is_open"),
    [Input("nec-button", "n_clicks")],
    [State("nec-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("details-collapse", "is_open"),
    [Input("details-button", "n_clicks")],
    [State("details-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



# Callback for finding closest lat/lon in database.
@app.callback(
    Output('weather_data_download', 'children'),
    [Input('lat', 'value'),
     Input('lon', 'value')]
)
def update_output_div( lat, lon):
    return html.A('Download weather data',
        href='/download_weather/get?lat={}&lon={}'.format(lat, lon)
                                        )

    # return str(n_clicks)


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
    if n_clicks>0:
        print('String Voltage Calculator:new weather location:')
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
            autosize=True,
            # width=1000,
            # height=600,
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


#


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
    return str(pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][0]), \
        str(pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][1]), \
        str(pvlib.pvsystem.TEMP_MODEL_PARAMS['sapm'][racking_model][2])

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


def make_iv_summary_layout(module_parameters):

    extra_parameters = vocmaxlib.calculate_extra_module_parameters(
        module_parameters)
    extra_parameters['Value'] = extra_parameters['Value'].map(
        lambda x: '%2.3f' % x)

    # Calculate some IV curves.
    irradiance_list = [1000, 800, 600, 400, 200]
    iv_curve = []
    for e in irradiance_list:
        ret = vocmaxlib.calculate_iv_curve(e, 25, module_parameters)
        ret['effective_irradiance'] = e
        ret['legend'] = str(e) + ' W/m^2'
        iv_curve.append(ret)
    return [
        html.P(''),
        dbc.Row([
            dbc.Col([
                html.P('I-V curves at 25 C.'),
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': s['v'], 'y': s['i'], 'type': 'line',
                             'name': s['legend']} for s in iv_curve
                        ],
                        'layout': go.Layout(
                            # title=go.layout.Title(
                            #     text='I-V curves at 25 C.',
                            #     xref='paper',
                            #     x=0
                            # ),
                            legend=dict(x=.05, y=0.05),
                            autosize=True,
                            xaxis={'title': 'Voltage (V)'},
                            yaxis={'title': 'Current (A)'},
                            margin={'l': 40, 'b': 90, 't': 10, 'r': 10},
                        hovermode='closest',
                        )
                    }
                ),
            ],md=6),
            dbc.Col([
                dcc.Markdown("""Predicted module parameters from CEC model 
                are shown in the table below. It is highly recommended to 
                cross-check these values with the module datasheet provided 
                by the manufacturer. 
        
                    """),
                dbc.Table.from_dataframe(extra_parameters,
                                         striped=False,
                                         bordered=True,
                                         hover=True,
                                         index=False,
                                         size='sm',
                                         style={'font-size':'0.8rem'})
            ],md=6)
        ])
    ]

@app.callback(Output('module_name_iv', 'children'),
              [Input('module_name', 'value')
               ])
def prepare_data(module_name):
    """
    Callback for IV curve plotting in setting module parameters.

    Parameters
    ----------
    module_name

    Returns
    -------

    """
    # print(module_name)
    module_parameters = pvtoolslib.cec_modules[module_name].to_dict()
    module_parameters['FD'] = 1
    module_parameters['name'] = module_name
    module_parameters['aoi_model'] = 'no_loss'
    module_parameters['iv_model'] = 'desoto'

    info_df = pd.DataFrame.from_dict({
        'Parameter': list(module_parameters.keys())
    })
    info_df['Value'] = info_df['Parameter'].map(module_parameters)

    info_layout = [
        html.Details([
            html.Summary('View database parameters for module'),
            dcc.Markdown("""For convenience, all parameters in the PVLIB CEC 
            database related to the selected module are shown in the table. 
            However, only the following subset are used in the calculation 
            using the De Soto model [5]: 
    
            * **alpha_sc**. The short-circuit current temperature coefficient of 
            the module in units of A/C
    
            * **a_ref**. The product of the usual diode ideality factor (n, 
            unitless), number of cells in series (Ns), and cell thermal 
            voltage at reference conditions, in units of V. 
    
            * **I_L_ref**. The light-generated current (or photocurrent) at 
            reference conditions, in amperes. 
    
            * **I_o_ref**. The dark or diode reverse saturation current at 
            reference conditions, in amperes.
    
            * **R_sh_ref**. The shunt resistance at reference conditions, 
            in ohms. 
    
            * **R_s**. The series resistance at reference conditions, in ohms.
    
            * **FD**. Fraction of diffuse irradiance arriving at the PV cell.
    
            """.replace('    ', '')),
            dbc.Table.from_dataframe(info_df,
                                     striped=False,
                                     bordered=True,
                                     hover=True,
                                     index=False,
                                     size='sm')
        ])
        ]

    temp_layout = make_iv_summary_layout(module_parameters)

    # Return flattened list.
    return [item for sublist in [info_layout,temp_layout] for item in sublist]


@app.callback(Output('manual_iv', 'children'),
              [
                  # Input('show_iv', 'n_clicks')
                  Input('module_name_manual', 'value'),
                  Input('alpha_sc', 'value'),
                  Input('a_ref', 'value'),
                  Input('I_L_ref', 'value'),
                  Input('I_o_ref', 'value'),
                  Input('R_sh_ref', 'value'),
                  Input('R_s', 'value'),
                  # Input('Adjust', 'value'),
                  Input('FD', 'value'),
               ]
              )
def prepare_data(module_name_manual,
                 alpha_sc, a_ref, I_L_ref, I_o_ref, R_sh_ref, R_s, FD):
    try:
        module_parameters = {
            'name': module_name_manual,
            'alpha_sc': float(alpha_sc),
            'a_ref': float(a_ref),
            'I_L_ref': float(I_L_ref),
            'I_o_ref': float(I_o_ref),
            'R_sh_ref': float(R_sh_ref),
            'R_s': float(R_s),
            # 'Adjust': float(Adjust),
            'FD': float(FD)
        }

        return make_iv_summary_layout(module_parameters)

    except:
        return [
            html.P('Input values invalid.')
        ]
    # # print(module_name)
    # module_parameters = pvtoolslib.cec_modules[module_name].to_dict()
    # module_parameters['FD'] = 1
    # module_parameters['name'] = module_name
    # module_parameters['aoi_model'] = 'no_loss'
    #


#
#
# def process_simulation_input(lat, lon,  module_parameter_input_type, module_name, module_name_manual,
#                  alpha_sc, a_ref, I_L_ref, I_o_ref, R_sh_ref, R_s, Adjust, FD,
#                  thermal_model_input_type, racking_model, a, b, DT,
#                  mount_type, surface_tilt, surface_azimuth,
#                  axis_tilt, axis_azimuth, max_angle, backtrack, ground_coverate_ratio,
#                  max_string_voltage):
#
#
#
#     lat = float(lat)
#     lon = float(lon)
#     return lat,lon, module_parameters, thermal_model, racking_parameters, max_string_voltage



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


def get_weather_data(lat,lon):
    """
    Get the weather data and info file. If the default location is chosen,
    then return file from current directory for speed.


    Parameters
    ----------
    lat
    lon

    Returns
    -------

    """

    # Get weather
    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(lat), float(lon),
                                                         filedata)

    filename = filedata_closest['filename'].iloc[0]

    if filename=='124250_37.93_-122.3.npz':
        weather, info = pvtoolslib.get_local_weather_data(filename)
    else:
        weather, info = pvtoolslib.get_s3_weather_data(filename)

    return weather, info




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
                # State('Adjust','value'),
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
                 alpha_sc, a_ref, I_L_ref, I_o_ref, R_sh_ref, R_s, FD,
                 thermal_model_input_type, racking_model, a, b, DT,
                 mount_type, surface_tilt, surface_azimuth,
                 axis_tilt, axis_azimuth, max_angle, backtrack, ground_coverate_ratio,
                 max_string_voltage):

    """

    Method for pressing 'calculate' button. Runs the main calculation and
    formats results.


    Parameters
    ----------
    n_clicks
    lat
    lon
    module_parameter_input_type
    module_name
    module_name_manual
    alpha_sc
    a_ref
    I_L_ref
    I_o_ref
    R_sh_ref
    R_s
    Adjust
    FD
    thermal_model_input_type
    racking_model
    a
    b
    DT
    mount_type
    surface_tilt
    surface_azimuth
    axis_tilt
    axis_azimuth
    max_angle
    backtrack
    ground_coverate_ratio
    max_string_voltage

    Returns
    -------

    """
# def run_simulation(*argv):



    if n_clicks<1:
        # print('Not running simulation.')
        return []



    all_params = {
        'lat': lat,
        'lon': lon,
        'module_parameter_input_type': module_parameter_input_type,
        'module_name': module_name,
        'module_name_manual': module_name_manual,
        'alpha_sc': alpha_sc,
        'a_ref': a_ref,
        'I_L_ref': I_L_ref,
        'I_o_ref': I_o_ref,
        'R_sh_ref': R_sh_ref,
        'R_s': R_s,
        # 'Adjust': Adjust,
        'FD': FD,
        'thermal_model_input_type': thermal_model_input_type,
        'racking_model': racking_model,
        'a':a,
        'b': b,
        'DT': DT,
        'mount_type': mount_type,
        'surface_tilt': surface_tilt,
        'surface_azimuth': surface_azimuth,
        'axis_tilt': axis_tilt,
        'axis_azimuth': axis_azimuth,
        'max_angle': max_angle,
        'backtrack': str(backtrack),
        'ground_coverage_ratio': ground_coverate_ratio,
        'max_string_voltage': max_string_voltage
    }


    request_str = '?'
    for p in all_params:
        request_str = request_str  + p + '=' + str(all_params[p]) + '&'

    request_str = request_str[0:-1]
    request_str = request_str.replace(' ','_')



    is_default_calculation = request_str == '?lat=37.88&lon=-122.25&module_parameter_input_type=lookup&module_name=1Soltech_1STH_215_P&module_name_manual=Custom_Module&alpha_sc=0.007997&a_ref=1.6413&I_L_ref=7.843&I_o_ref=1.936e-09&R_sh_ref=839.4&R_s=0.359&FD=1&thermal_model_input_type=lookup&racking_model=open_rack_cell_glassback&a=-3.47&b=-0.0594&DT=3&mount_type=fixed_tilt&surface_tilt=30&surface_azimuth=180&axis_tilt=0&axis_azimuth=0&max_angle=90&backtrack=True&ground_coverage_ratio=0.286&max_string_voltage=1500'
    print('String Voltage Calculator:Calculate started:default=' + str(is_default_calculation))
    # print(request_str)



    # print('/'.join(all_params))

    if module_parameter_input_type=='lookup':
        module_parameters = pvtoolslib.cec_modules[module_name].to_dict()
        module_parameters['FD'] = 1
        module_parameters['name'] = module_name
        module_parameters['aoi_model'] = 'no_loss'
        module_parameters['iv_model'] = 'desoto'
    elif module_parameter_input_type=='manual':
        module_parameters = {
            'name': module_name_manual,
            'alpha_sc': float(alpha_sc),
            'a_ref': float(a_ref),
            'I_L_ref': float(I_L_ref),
            'I_o_ref': float(I_o_ref),
            'R_sh_ref': float(R_sh_ref),
            'R_s': float(R_s),
            # 'Adjust': float(Adjust),
            'FD': float(FD),
            'iv_model': 'desoto'
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


    # print('Getting weather data...')
    weather, info = get_weather_data(lat,lon)

    df = vocmaxlib.simulate_system(weather, info,module_parameters,
                                   racking_parameters, thermal_model)

    voc_summary = vocmaxlib.make_voc_summary(df, module_parameters,
                                   max_string_voltage=max_string_voltage)


    voc_summary_table = voc_summary.rename(index=str,columns={'v_oc':'Voc',
                                                     'max_string_voltage':'Max String Voltage',
                                                     'string_length':'String Length',
                                                     'long_note':'Note'
                                                     })
    voc_summary_table['Note'] = voc_summary_table['Note'].apply(
        lambda s : s.replace('<br>','.  '))
    voc_summary_table['Voc'] = voc_summary_table['Voc'].apply(
        lambda s: '{:2.2f}'.format(s))

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
    # sim_params_embedded =

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
                        bins=np.linspace(df['v_oc'].max() * 0.6,
                                         df['v_oc'].max() + 1, 400))

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

    # print('making the layout')
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
        dbc.Table.from_dataframe(voc_summary_table,
                                 striped=False,
                                 bordered=True,
                                 hover=True,
                                 index=True,
                                 size='sm',
                                 style={'font-size': '0.8rem'}),
        html.Details([
            html.Summary('Details on key names'),
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
        ]),
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
                            text='Figure 3. Time dependence of air temperature, cell temperature, and Voc around the time of historical maximum Voc.',
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
            """Download the simulation results as csv files here (use chrome or firefox)
        
            """
        ),
        html.Div([
            html.A('Download csv summary',
                   id='download-link',
                   download='summary.csv',
                   href=summary_text_for_download,
                   target='_blank'),
        ]),
        html.Div([
            html.A('Download full simulation data as csv',
               id='download-link',
               download='raw_data.csv',
               href='/dash/download_simulation_data' + request_str,
               target='_blank'),
            ]),
    ]

    return return_layout


@app.server.route('/dash/download_simulation_data')
def download_simulation_data():
    print('String Voltage Calculator:Download Simulation Data:')
    # value = flask.request.args.get('lat')
    p = flask.request.args



    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(p['lat']),
                                                         float(p['lon']),
                                                         filedata)

    # print('/'.join(all_params))



    if p['module_parameter_input_type']=='lookup':
        module_parameters = pvtoolslib.cec_modules[p['module_name']].to_dict()
        module_parameters['FD'] = 1
        module_parameters['name'] = p['module_name']
        module_parameters['aoi_model'] = 'no_loss'
    elif p['module_parameter_input_type']=='manual':
        module_parameters = {
            'name': p['module_name_manual'],
            'alpha_sc': float(p['alpha_sc']),
            'a_ref': float(p['a_ref']),
            'I_L_ref': float(p['I_L_ref']),
            'I_o_ref': float(p['I_o_ref']),
            'R_sh_ref': float(p['R_sh_ref']),
            'R_s': float(p['R_s']),
            # 'Adjust': float(p['Adjust']),
            'FD': float(p['FD'])
        }
    else:
        print('input type not understood.')

    if p['thermal_model_input_type']=='lookup':
        thermal_model = p['racking_model']
        thermal_model_dict = {'thermal_model': thermal_model}
    elif p['thermal_model_input_type']=='manual':
        thermal_model = {
            'a':float(p['a']),
            'b':float(p['b']),
            'deltaT':float(p['DT'])
        }
        thermal_model_dict = thermal_model
    else:
        print('Racking model not understood')

    if p['mount_type']=='fixed_tilt':
        racking_parameters = {
            'racking_type': 'fixed_tilt',
            'surface_tilt': float(p['surface_tilt']),
            'surface_azimuth': float(p['surface_azimuth'])
        }
    elif p['mount_type']=='single_axis_tracker':
        racking_parameters = {
            'racking_type': 'single_axis',
            'axis_tilt': float(p['axis_tilt']),
            'axis_azimuth': float(p['axis_azimuth']),
            'max_angle': float(p['max_angle']),
            'backtrack': p['backtrack'],
            'gcr': float(p['ground_coverage_ratio'])
        }
    else:
        print('error getting racking type')

    max_string_voltage = float(p['max_string_voltage'])



    weather, info = pvtoolslib.get_s3_weather_data(
        filedata_closest['filename'].iloc[0])



    df = vocmaxlib.simulate_system(weather, info,module_parameters,
                                   racking_parameters, thermal_model)

    # df_temp = pd.DataFrame(info,index=[0])
    df_temp = df.copy()
    df_temp['wind_speed'] = df_temp['wind_speed'].map(lambda x: '%2.1f' % x)
    df_temp['v_oc'] = df_temp['v_oc'].map(lambda x: '%3.2f' % x)
    df_temp['temp_cell'] = df_temp['temp_cell'].map(lambda x: '%2.1f' % x)
    df_temp['aoi'] = df_temp['aoi'].map(lambda x: '%3.0f' % x)


    #Create DF
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)



    #Convert DF
    str_io = io.StringIO()
    pd.DataFrame(
        {**info, **module_parameters, **thermal_model_dict, **racking_parameters},
                 index=['']).to_csv(str_io, sep=",",index=False)
    # pd.DataFrame(module_parameters, index=['']).to_csv(str_io, sep=",")
    # pd.DataFrame(racking_parameters, index=['']).to_csv(str_io, sep=",")
    df_temp.to_csv(str_io, sep=",",index=False)

    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()



    return flask.send_file(mem,
					   mimetype='text/csv',
					   attachment_filename='simulation_data_full.csv',
					   as_attachment=True)


@app.server.route('/download_weather/get')
def download_weather_data():
    # print('Values found:')
    param = flask.request.args


    # print('Sending download weather data')


    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(param['lat']),
                                                         float(param['lon']),
                                                         filedata)
    weather, info = pvtoolslib.get_s3_weather_data(
        filedata_closest['filename'].iloc[0])


    #
    # df = weather

    #Create DF
    # d = {'col1': [1, 2,3], 'col2': [3, 4,5]}
    # df = pd.DataFrame(data=d)


    #Convert DF
    # with str_io as io.StringIO():
    str_io = io.StringIO()
    pd.DataFrame(info,index=['']).to_csv(str_io, sep=",",index=False)
    weather.to_csv(str_io, sep=",",index=False)
    # df.to_csv(str_io, sep=",")


    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()

    # print(str_io)

    return flask.send_file(mem,
					   mimetype='text/csv',
					   attachment_filename='weather.csv',
					   as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)