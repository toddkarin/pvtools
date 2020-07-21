# -*- coding: utf-8 -*-
"""

This script builds a Dash web application for calculating string length for a
PV System. Specifically, it builds the layout that is called by index.py

Todd Karin

toddkarin

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
# import dash_table
import plotly.colors
import plotly.graph_objs as go
import plotly.figure_factory as ff
# import plotly.plotly as py
# from flask_caching import Cache
from dash.dependencies import Input, Output, State
import vocmax
import numpy as np
import pvlib
import nsrdbtools
import pandas as pd
# import uuid
# import os
import flask
import json
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
        html.H1("Solar Photovoltaic String Length Calculator"),
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
    dcc.Markdown("""This tool determines the maximum string length for a 
    solar PV installation in a particular location. The method is in 
    accordance with National Electric Code (NEC) 690.7(A) standards. 

    **We would highly appreciate any feedback** (praise, bug reports, 
    suggestions, etc.). Please contact us at pvtools.lbl@gmail.com. 
    
    """.replace('    ', '')
                 ),

    dbc.Row([
        dbc.Col([
            dbc.Button("Show me more details",
                       id="details-button",
                       color='light',
                       n_clicks=0,
                       className="mb-3"),
        ], width=3)

    ], justify='start'),
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            dcc.Markdown("""
            
            ### Summary
            
            The calculation proceeds with the following steps:
            
            - Load historical weather data for a location.
            - Provide details on module and installation type
            - Set maximum allowable string voltage
            - Model Voc for user-specified module technology, installation 
            parameters and weather data.
            - Analyze results, providing a standard value for string length.

            ### Weather Data
            
            Weather data was sourced from the National Solar Radiation 
            Database (NSRDB) [1]. The data was sampled across the continental 
            US at approximately a 0.125 degree grid, and at a lower 
            resolution elsewhere. If a different weather data source is 
            desired, it is necessary to use the open source associated python 
            package [vocmax]( https://github.com/toddkarin/vocmax), 
            which performs the same calculation as this web tool. If the 
            particular weather data point is not on the map, please contact 
            us at {} and we will try to provide it. 
            
            ### Simulation methods
            
            The string voltage calculator uses the open source [PVLIB]( 
            https://pvlib-python.readthedocs.io/en/latest/) library to 
            perform the calculation. The first step is to determine the 
            plane-of-array irradiance given the mounting configuration and 
            weather data. If the California energy Commission (CEC) lookup 
            table is used, the relevant module parameters are calculated 
            using the single diode model under the De Soto parameterization [ 
            5]. The relevant module parameters are the open-circuit voltage 
            at reference conditions (Voco), the temperature coefficient of 
            the open circuit voltage in V/C (Bvoco), the number of cells in 
            series in each module (cells_in_series) and the diode ideality 
            factor (n_diode). Alternately, module parameters 
            from the datasheet can be entered manually. 
             
            The calculation conservatively assumes that all diffuse 
            irradiance is used (FD=1) and that there are no reflection losses 
            from the top cell (aoi_model='no_loss'). These two assumptions 
            cause a small increase in Voc and make the simulation more 
            conservative. Specific details on the exact calculation method 
            are described in [vocmax](https://github.com/toddkarin/vocmax).
            
            The open circuit voltage is modeled using the equation:
            
            Voc = Voco + cells_in_series·delta·log(E/E0) + Bvoc·(T-T0)
            
            where delta = n_diode·k_B·T/q is the thermal voltage, Bvoc 
            = Bvoco + Mbvoc·(1-E/E0), Mbvoc is the coefficient of the 
            irradiance dependence of the temperature coefficient of open 
            circuit voltage, E is the plane-of-array irradiance, E0 = 1000 
            W/m^2 is the reference irradiance, T0 = 25 C is the reference 
            temperature, kB is the Boltzmann constant, T is the cell 
            temperature and q is the electron charge. 
            
            ### National Electric Code Standards
            
            The National Electric Code 2017 lists three different methods 
            for determining the maximum string length in Article 690.7:
            
            - 690.7(A)(1) Instruction in listing or labeling of module: The 
            sum of the PV module-rated open-circuit voltage of the 
            series-connected modules corrected for the lowest expected 
            ambient temperature using the open-circuit voltage temperature 
            coefficients in accordance with the instructions included in the 
            listing or labeling of the module. 
            
            - 690.7(A)(2) Crystalline and multicrystalline modules: For 
            crystalline and multicrystalline silicon modules, the sum of the 
            PV module-rated open-circuit voltage of the series-connected 
            modules corrected for the lowest expected ambient temperature 
            using the correction factor provided in Table 690.7(A). 
            
            - 690.7(A)(3) PV systems of 100 kW or larger: For PV systems with 
            a generating capcity of 100 kW or greater, a documented and 
            stamped PV system design, using an industry standard method and 
            provided by a licensed professional electrical engineer, shall be 
            permitted. 
            
            This tool provides standard values for the trhee 690.7(A) 
            methods. For method 690.7(A)(3), the system is modeled using 18
            years of NSRDB weather from the selected location and module 
            parameters. 
                
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
        ])), id="details-collapse"
    ),

    # html.H2('Simulation Input'),
    html.P(''),
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
                                   children='Show nearest location on map'),
                    ]),
                    html.Div(id='weather_data_download'),

                ], md=4),
                dbc.Col([
                    html.Div(id='location-map', children=[dcc.Graph(id='map')]),
                    html.P(
                        'Either enter coordinates manually or click on point.')
                ], md=8)
            ]),
        ]),
    ]),
    html.P(''),
    html.H2('Step 2: Provide details on module and installation type'),
    dbc.Card([
        dbc.CardHeader('Module Parameters'),
        dbc.CardBody([
            dbc.Label("""To select module parameters from a library of common 
            modules, select 'Library Lookup'. Or select 'manual entry' to 
            enter the parameters manually. 
            
            """),
            dbc.Tabs([
                dbc.Tab([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Markdown("""Module name (from CEC database).
                                
                                """),
                                dcc.Dropdown(
                                    id='module_name',
                                    options=pvtoolslib.cec_module_dropdown_list,
                                    value=
                                    pvtoolslib.cec_module_dropdown_list[0][
                                        'value'],
                                    style={'max-width': 500}
                                ),
                                html.P(''),
                                dcc.Markdown("""Bifaciality

                                """),
                                dcc.Dropdown(
                                    id='lookup_is_bifacial',
                                    options=[
                                        {'label': 'Monofacial Module',
                                         'value': 0},
                                        {'label': 'Bifacial Module',
                                         'value': 1},
                                    ],
                                    value=0,
                                    style={'max-width': 500}
                                ),
                                dbc.FormText("""Select 'bifacial' if the 
                                module is bifacial and is mounted so that the 
                                backside receives irradiance.
                                
                                """),
                                html.P(''),
                                html.Div([
                                    dbc.Label(
                                        """Module bifaciality coefficient"""),
                                    dbc.Input(id='lookup_bifaciality',
                                              value='0.7',
                                              type='text',
                                              style={'max-width': 200}),
                                    dbc.FormText(
                                        """Efficiency of the backside of the module relative to the frontside."""),
                                    html.P(''),
                                ], id='lookup_bifaciality_div'),
                                html.Div(id='module_name_iv')
                            ],
                        )
                    )
                ], tab_id='lookup', label='Library Lookup'),

                dbc.Tab([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Markdown("""Manually set module parameters.
                                
                                """),
                                html.Details([
                                    html.Summary(
                                        "What about using PVsyst data from a PAN file?"),
                                    html.Div([
                                        dcc.Markdown("""In order to use a PAN 
                                        file from PVsyst, use the following 
                                        translation: 
                                
                                    """),
                                    ], style={'marginLeft': 50}
                                    ),
                                    dbc.Table.from_dataframe(pd.DataFrame(
                                        {'pvtools': ['Voco', 'Bvoco', 'Mbvoc',
                                                     'cells_in_series',
                                                     'n_diode',
                                                     'efficiency',
                                                     'Module bifaciality coefficient'],
                                         'pvSyst': ['Voc', 'muVocSpec/1000',
                                                    '0',
                                                    'NCelS', 'Gamma',
                                                    'Imp*Vmp/Height/Width',
                                                    'BifacialityFactor']
                                         }),
                                        striped=False,
                                        bordered=True,
                                        hover=True,
                                        index=False,
                                        size='sm',
                                        style={
                                            'font-size': '0.8rem'}),
                                ]),

                                dbc.Label("""Module name"""),
                                dbc.Input(id='module_name_manual',
                                          value='Custom Module',
                                          type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""Module name for outfile"""),
                                html.P(''),
                                dbc.Label("""Voco"""),
                                dbc.Input(id='Voco', value='48.5', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['Voco']),
                                html.P(''),
                                dbc.Label("""Bvoco"""),
                                dbc.Input(id='Bvoco', value='-0.163',
                                          type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['Bvoco']),
                                html.P(''),
                                dbc.Label("""Mbvoc"""),
                                dbc.Input(id='Mbvoc', value='0', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['Mbvoc']),
                                html.P(''),
                                dbc.Label("""cells_in_series"""),
                                dbc.Input(id='cells_in_series', value='72',
                                          type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['cells_in_series']),
                                html.P(''),
                                dbc.Label("""n_diode"""),
                                dbc.Input(id='n_diode', value='1.05',
                                          type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['n_diode'] +
                                             '. Suggested values are 1.1 for mono-c-Si, 1.2 for multi-c-Si, and 1.4 for CdTe.'),
                                html.P(''),
                                dbc.Label("""efficiency"""),
                                dbc.Input(id='efficiency', value='0.17',
                                          type='text',
                                          style={'max-width': 200}),
                                dbc.FormText('Module efficiency, unitless'),
                                html.P(''),
                                dbc.Label("""FD"""),
                                dbc.Input(id='FD', value='1', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(vocmax.explain['FD']),
                                html.P(''),
                                dcc.Markdown("""Bifaciality

                                """),
                                dcc.Dropdown(
                                    id='manual_is_bifacial',
                                    options=[
                                        {'label': 'Monofacial Module',
                                         'value': 0},
                                        {'label': 'Bifacial Module',
                                         'value': 1},
                                    ],
                                    value=0,
                                    style={'max-width': 500}
                                ),
                                dbc.FormText("""Select 'bifacial' if the 
                                module is bifacial and is mounted so that the 
                                backside receives irradiance. 
                                    
                                """),
                                html.P(''),
                                html.Div([
                                    dbc.Label(
                                        """Module bifaciality coefficient"""),
                                    dbc.Input(id='manual_bifaciality',
                                              value='0.7',
                                              type='text',
                                              style={'max-width': 200}),
                                    dbc.FormText(
                                        """Efficiency of the backside of the module relative to the frontside."""),
                                    html.P(''),
                                ], id='manual_bifaciality_div'),
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
                ], tab_id='manual', label='Manual Entry'),
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
                                dcc.Markdown('Racking Model'),
                                dcc.Dropdown(
                                    id='racking_model',
                                    options=[
                                        {'label': 'open rack glass polymer',
                                         'value': 'open_rack_glass_polymer'},
                                        {'label': 'open rack glass glass',
                                         'value': 'open_rack_glass_glass'},
                                        {'label': 'close mount glass glass',
                                         'value': 'close_mount_glass_glass'},
                                        {
                                            'label': 'insulated back glass polymer',
                                            'value': 'insulated_back_glass_polymer'},
                                    ],
                                    value='open_rack_glass_polymer',
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
                            [html.P(
                                ['Enter thermal model parameters from the ',
                                 html.A('Sandia array performance model',
                                        href='https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2004/043535.pdf',
                                        target='_blank'),
                                 '.'
                                 ]),

                                dbc.Label("""a
                                """),
                                dbc.Input(id='a', value='-3.47', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText("""Empirically-determined coefficient 
                                establishing the upper limit for module temperature 
                                at low wind speeds and high solar irradiance 
                                
                                
                                """),
                                html.P(''),
                                dbc.Label("""b"""),
                                dbc.Input(id='b', value='-0.0594', type='text',
                                          style={'max-width': 200}),
                                dbc.FormText(""" Empirically-determined coefficient 
                                establishing the rate at which module temperature 
                                drops as wind speed increases (s/m) 
                                
                                """),
                                html.P(''),
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
            html.P(''),
            dcc.Markdown("""Open-Circuit Temperature Rise

                                """),
            dcc.Dropdown(
                id='open_circuit_rise',
                options=[
                    {'label': 'Open-circuit temperature rise included',
                     'value': 1},
                    {'label': 'Open-circuit temperature rise excluded',
                     'value': 0},
                ],
                value=0,
                style={'max-width': 500}
            ),
            dbc.FormText("""Modules at open-circuit voltage are slightly 
            warmer than those at max-power point because at open-circuit 
            absorbed energy is not exported as electricity. However, for the 
            first few minutes of a shutdown the modules have not had time to 
            equilibrate to the higher temperature. 

                                """),
        ]),
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
                             dbc.Input(id='surface_tilt', value='30',
                                       type='text',
                                       style={'max-width': 200}),

                             dbc.Label('Surface Azimuth (degrees)'),
                             dbc.Input(id='surface_azimuth', value='180',
                                       type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""For module face oriented due South use 180. 
                             For module face oreinted due East use 90"""),
                             dbc.Label("""Ground albedo"""),
                             dbc.Input(id='fixed_tilt_albedo',
                                       value='0.25',
                                       type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""Ground albedo is used to 
                             calculate light reflected from the ground onto 
                             front or backside of module. 

                             """),
                             html.Div([
                                 dbc.Label("""Backside irradiance fraction"""),
                                 dbc.Input(
                                     id='fixed_tilt_backside_irradiance_fraction',
                                     value='0.2',
                                     type='text',
                                     style={'max-width': 200}),
                                 dbc.FormText("""Fraction of light falling on 
                                 back of a bifacial module relative to the front. 
                                 Unused if module is not bifacial. 
                                 
                                 """),
                             ],
                                 id='fixed_tilt_backside_irradiance_fraction_div'),
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
                             dbc.Input(id='axis_azimuth', value='0',
                                       type='text',
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
                             dbc.Input(id='ground_coverage_ratio',
                                       value='0.286',
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
                             dbc.Label("""Ground albedo"""),
                             dbc.Input(id='single_axis_albedo',
                                       value='0.25',
                                       type='text',
                                       style={'max-width': 200}),
                             dbc.FormText("""Ground albedo is used to 
                             calculate light reflected from the ground onto 
                             front or backside of module. 
                             
                             """),
                             html.Div([
                                 dbc.Label("""Backside irradiance fraction"""),
                                 dbc.Input(
                                     id='single_axis_backside_irradiance_fraction',
                                     value='0.2',
                                     type='text',
                                     style={'max-width': 200}),
                                 dbc.FormText("""Fraction of light falling on 
                                 back of a bifacial module relative to the front. 
                                 Unused if module is not bifacial. 
                                        
                                    """),
                             ], 'single_axis_backside_irradiance_fraction_div')
                             ]
                        )
                    )
                ], tab_id='single_axis_tracker', label='Single Axis Tracker')
            ], id='mount_type', active_tab='fixed_tilt'),
        ])
    ]),
    html.P(''),
    html.H2('Step 3: Provide Design Maximum String Voltage and Safety Factor'),
    dbc.Card([
        dbc.CardHeader(['String Voltage Limit']),
        dbc.CardBody([
            dcc.Markdown('String design voltage (V)'),
            dbc.Input(id='string_design_voltage',
                      value='1500',
                      type='text',
                      style={'max-width': 200}),
            dbc.FormText(
                'Maximum string design voltage (Vdesign) for calculating string length, in Volts'),
        ])
    ]),
    html.P(''),
    dbc.Card([
        # XX
        dbc.CardHeader(['Safety factor']),
        dbc.CardBody([
            dcc.Markdown(
                'Safety factor due to NSRDB weather uncertainty (%).  Use look up button to get suggested value for current lat/lon.'),
            dbc.Row([
                dbc.Col([
                    dbc.Button(id='nsrdb_get_weather_data_uncertainty',
                               n_clicks=0,
                               children='Look up',
                               color="secondary")
                ], width='auto'),
                dbc.Col([
                    dbc.Input(id='nsrdb_weather_data_safety_factor',
                              value='2.3',
                              type='text',
                              style={'max-width': 200}
                              ),
                ], width='auto'),
            ], justify='start'),
            dbc.FormText(id='nsrdb_safety_factor_inform',
                         children="""Safety factor due to NSRDB uncertainty is found 
                by comparing NSRDB and ASHRAE extreme yearly minimum dry bulb 
                temperatures for the location of interest. The temperature 
                difference is multiplied by the absolute value of the 
                temperature coefficient of open-circuit voltage in %/C 
                Alternately, can use a standard NSRDB weather uncertainty of 
                2.3 %. 
                
                """.replace('    ', '')),
            html.P(''),
            dcc.Markdown(
                'Optional safety factor due to extreme cold temperatures, only consider including if using 690.7(A)(3)-P99.5 standard.'),
            dbc.Row([
                dbc.Col([
                    dbc.Button(id='get_extreme_cold_uncertainty',
                               n_clicks=0,
                               children='Look up',
                               color="secondary")
                ], width='auto'),
                dbc.Col([
                    dbc.Input(id='extreme_cold_uncertainty',
                              value='0.0',
                              type='text',
                              style={'max-width': 200}
                              ),
                ], width='auto'),
                dbc.Col([
                    dcc.Dropdown(
                        id='extreme_cold_include',
                        options=[
                            {'label': 'Include',
                             'value': 1},
                            {'label': 'Exclude',
                             'value': 0},
                        ],
                        value=0,
                        style={'max-width': 1000}
                    ),
                ], width=2),
                dbc.Col([
                    dcc.Loading(html.Div(
                        id='extreme_cold_safety_factor_loading_div'))
                ], width=1),
            ], justify='start'),
            dbc.FormText(id='extreme_cold_safety_factor_inform'),
            html.P(''),
            dcc.Markdown(
                'Additional additive safety factor.'),
            dbc.Row([
                dbc.Col([
                    dbc.Button(id='get_suggested_additional_safety_factor',
                               n_clicks=0,
                               children='Get Suggestion',
                               color="secondary")
                ], width='auto'),
                dbc.Col([dbc.Input(id='additional_safety_factor',
                                   value='1.6',
                                   type='text',
                                   style={'max-width': 200}
                                   )
                         ], width='auto'),
                dbc.Col([
                    dcc.Loading(html.Div(
                        id='additional_safety_factor_loading_div'))
                ], width=1),
            ], justify='start'),
            dbc.FormText(id='additional_safety_factor_inform',
                         children="""Additional safety factor in percent of 
                         system Voc. Suggested value is 1.0% to account for 
                         Voc manufacturing uncertainty plus 0.6% for wind 
                         speed uncertainty. If the diode ideality factor is 
                         unknown, add an additional 0.4%. """

                         ),
            html.P(''),
            dcc.Markdown('Total safety factor, in percent.'),
            dbc.Row([
                dbc.Col([dbc.Input(id='safety_factor',
                                   value='3.3',
                                   type='text',
                                   style={'max-width': 200}),
                         ], width='auto'),
            ], justify='start'),
            dbc.FormText(id='total_safety_factor_inform',
                         children='Safety factor as a percent of system Voc. Number of modules in string is chosen to satisfy Nstring*Vmax<(1-safety_factor)*Vdesign'),
        ])
    ]),
    html.P(''),
    html.H2('Final Step: Run Calculation'),
    dbc.Card([
        dbc.CardHeader('Calculation'),
        dbc.CardBody([
            html.P('Press "Calculate" to run Voc calculation (~10 seconds)'),
            dbc.Button(id='submit-button',
                       n_clicks=0,
                       children='Calculate',
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

    html.P(''),
    html.H2('Results'),
    # html.Div(id='load'),
    dcc.Loading(html.Div(id='graphs')),
    # dcc.Store(id='annotation-store'),
    dcc.Store(id='results-store'),
    # html.Div(id='voc-hist-results-store', style={'display': 'none'}),
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
    html.P(''),
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

        ], style={'marginLeft': 50}
        ),

    ]),
    html.Details([
        html.Summary(
            "Where can I find an index of parameters?"),
        html.Div([
            # dcc.Markdown("""Right here!"""),
            dcc.Markdown('**' + p + '**: ' + vocmax.explain[p]) for p in
            vocmax.explain

        ], style={'marginLeft': 50}
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
    html.P(''),
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
    html.P('Author: Todd Karin'),
    html.P('Contact: ' + pvtoolslib.contact_email)
],
    style={'columnCount': 1,
           'maxWidth': 1000,
           'align': 'center'})


#
# @app.callback(
#     Output("nec-collapse", "is_open"),
#     [Input("nec-button", "n_clicks")],
#     [State("nec-collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("calculation_result", "children"),
#     [Input("input", "value")],
# )
# def toggle_collapse(input):
#     # Do really long calculation
#     dash.dependencies.Update_Output(id='progress_bar',value=10)
#     # Do some more calculations
#     dash.dependencies.Update_Output(id='progress_bar', value=30)
#     # And some more
#     dash.dependencies.Update_Output(id='progress_bar', value=100)
#     return result


@app.callback(
    Output("details-collapse", "is_open"),
    [Input("details-button", "n_clicks")],
    [State("details-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Functions for hiding input when bifacial is not selected
@app.callback(
    Output("lookup_bifaciality_div", "style"),
    [Input("lookup_is_bifacial", "value")],
)
def hide_lookup_bifaciality_input(is_bifacial):
    if is_bifacial:
        style = {}
    else:
        style = {'display': 'none'}
    return style


@app.callback(
    Output("manual_bifaciality_div", "style"),
    [Input("manual_is_bifacial", "value")],
)
def hide_manual_bifaciality_input(is_bifacial):
    if is_bifacial:
        style = {}
    else:
        style = {'display': 'none'}

    return style


@app.callback(
    [Output("single_axis_backside_irradiance_fraction_div", "style"),
     Output("fixed_tilt_backside_irradiance_fraction_div", "style"),
     ],
    [Input("lookup_is_bifacial", "value"),
     Input("manual_is_bifacial", "value"),
     ],
    [State('module_parameter_input_type', 'active_tab'),
     ]
)
def hide_backside_irradiance_fraction_input(lookup_is_bifacial,
                                            manual_is_bifacial,
                                            module_parameter_input_type):
    if module_parameter_input_type == 'lookup':
        is_bifacial = lookup_is_bifacial
    elif module_parameter_input_type == 'manual':
        is_bifacial = manual_is_bifacial

    if is_bifacial:
        style = {}
    else:
        style = {'display': 'none'}

    return [style, style]


# XX

@app.callback(
    [Output('additional_safety_factor', 'value'),
     Output('additional_safety_factor_loading_div', 'chiildren'),
     ],
    [Input('get_suggested_additional_safety_factor', 'n_clicks')
     ],
    [State('module_parameter_input_type', 'active_tab')]
)
def update_additional_safety_factor(n_clicks, module_parameter_input_type):
    if n_clicks == 0:
        return ['1.0', '']

    add_diode_factor = module_parameter_input_type == 'manual'

    additional_safety_factor = 1.0 + 0.6 + add_diode_factor * 0.4

    return ['{:1.1f}'.format(additional_safety_factor), '']


@app.callback(
    [Output('nsrdb_weather_data_safety_factor', 'value'),
     Output('nsrdb_safety_factor_inform', 'children'),
     ],
    [Input('nsrdb_get_weather_data_uncertainty', 'n_clicks')
     ],
    [State('lat', 'value'),
     State('lon', 'value'),
     State('module_parameter_input_type', 'active_tab'),
     State('module_name', 'value'),
     State('Bvoco', 'value'),
     State('Voco', 'value'),
     ]
)
def update_output_div(n_clicks, lat, lon, module_parameter_input_type,
                      module_name, Bvoco_manual, Voco_manual):
    """
    Callback for updating safety factor

    Parameters
    ----------
    lat
    lon

    Returns
    -------

    """

    if n_clicks == 0:
        return '2.3', 'NSRDB safety factor in percent of system Voc'

    lat = float(lat)
    lon = float(lon)
    temperature_error = vocmax.get_nsrdb_temperature_error(lat, lon)

    if module_parameter_input_type == 'lookup':

        module_parameters = pvtoolslib.cec_modules[module_name].to_dict()

        Bvoco = module_parameters['beta_oc']
        Voco = module_parameters['V_oc_ref']

    elif module_parameter_input_type == 'manual':
        Bvoco = float(Bvoco_manual)
        Voco = float(Voco_manual)
    else:
        raise Exception('module parameter lookup type not understood')

    if temperature_error < 0:
        temperature_error = 0
    nsrdb_safety_factor = temperature_error * np.abs(Bvoco / Voco)

    return ['{:1.1f}'.format(nsrdb_safety_factor * 100), \
            """NSRDB safety factor in percent of system Voc. For 
            the chosen location (lat {:3.2f}, lon {:3.2f}), the NSRDB temperature 
            error of {:2.1f} C combined with Voc temperature coefficient of {:1.2f}%/C 
            leads to NSRDB data uncertainty of {:2.1%}.
            
            """.format(lat,
                       lon,
                       temperature_error,
                       Bvoco / Voco * 100,
                       temperature_error * np.abs(Bvoco / Voco),
                       )
            ]


@app.callback(
    [Output('extreme_cold_uncertainty', 'value'),
     Output('extreme_cold_safety_factor_inform', 'children'),
     Output('extreme_cold_safety_factor_loading_div', 'children'),
     ],
    [Input('get_extreme_cold_uncertainty', 'n_clicks')
     ],
    [State('lat', 'value'),
     State('lon', 'value'),
     State('module_parameter_input_type', 'active_tab'),
     State('module_name', 'value'),
     State('Bvoco', 'value'),
     State('Voco', 'value'),
     ]
)
def extreme_cold_safety_factor(n_clicks, lat, lon, module_parameter_input_type,
                               module_name, Bvoco_manual, Voco_manual):
    """
    Callback for updating safety factor

    Parameters
    ----------
    lat
    lon

    Returns
    -------

    """

    if n_clicks == 0:
        return ['0.0', 'Extreme cold safety factor in percent', '']

    lat = float(lat)
    lon = float(lon)
    temperature_error = vocmax.get_nsrdb_temperature_error(lat, lon)

    if module_parameter_input_type == 'lookup':

        module_parameters = pvtoolslib.cec_modules[module_name].to_dict()

        Bvoco = module_parameters['beta_oc']
        Voco = module_parameters['V_oc_ref']

    elif module_parameter_input_type == 'manual':
        Bvoco = float(Bvoco_manual)
        Voco = float(Voco_manual)
    else:
        raise Exception('module parameter lookup type not understood')

    weather, info = get_weather_data(lat, lon)
    extreme_cold_delta_T = vocmax.calculate_mean_yearly_min_temp(
        weather.index, weather['temp_air']) - weather['temp_air'].min()

    extreme_cold_safety_factor = extreme_cold_delta_T * np.abs(Bvoco / Voco)

    return ['{:1.1f}'.format(extreme_cold_safety_factor * 100), \
            """Extreme cold safety factor in percent. For the chosen location 
            (lat {:3.2f}, lon {:3.2f}), the difference between the mean of 
            the yearly minimum temperatures and the 19-year minimum is {:2.1f} C 
            using NSRDB data. Combined with Voc temperature coefficient of {:1.2f}%/C 
            leads to an extreme cold safety factor of {:2.1%}. 
        
            """.format(lat,
                       lon,
                       extreme_cold_delta_T,
                       Bvoco / Voco * 100,
                       extreme_cold_safety_factor,
                       ),
            ''
            ]


@app.callback(
    [Output('safety_factor', 'value'),
     ],
    [Input('nsrdb_weather_data_safety_factor', 'value'),
     Input('extreme_cold_uncertainty', 'value'),
     Input('extreme_cold_include', 'value'),
     Input('additional_safety_factor', 'value'),
     ]
)
def sum_safety_factor(nsrdb_weather_data_safety_factor,
                      extreme_cold_uncertainty, extreme_cold_include,
                      additional_safety_factor):
    if extreme_cold_include == None:
        extreme_cold_include = 0

    try:

        safety_factor = float(nsrdb_weather_data_safety_factor) + \
                    float(extreme_cold_include) * float(
            extreme_cold_uncertainty) + \
                    float(additional_safety_factor)
        safety_factor_str = '{:1.1f}'.format(safety_factor)
    except:
        PreventUpdate
        safety_factor_str = ''

    return [safety_factor_str]


# Callback for finding closest lat/lon in database.
@app.callback(
    Output('weather_data_download', 'children'),
    [Input('lat', 'value'),
     Input('lon', 'value')]
)
def update_output_div(lat, lon):
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
    # if n_clicks==0:
    #     return ''

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
    [Output('map', 'figure'),
     Output('map', 'config')
     ],
    [Input('get-weather', 'n_clicks')],
    [State('lat', 'value'),
     State('lon', 'value')])
def update_map_callback(n_clicks, lat, lon):
    # print('Updating the map')
    # if n_clicks>0:
    # print('Verbose:String Voltage Calculator:new weather location:')
    print('Getting map data...')
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
    print('Map done.')
    return map_figure, dict(scrollZoom=True)


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

    param = pvlib.temperature._temperature_model_params('sapm', racking_model)
    return str(param['a']), \
           str(param['b']), \
           str(param['deltaT'])


@app.callback(
    [Output('lat', 'value'),
     Output('lon', 'value'),
     Output('get-weather', 'n_clicks')
     ],
    [Input('map', 'clickData')
     ],
    [State('get-weather', 'n_clicks')
     ])
def display_click_data(clickData, n_clicks):
    # If no type given, do not change lat or lon
    if type(clickData) == type(None):
        d = {'lat': 37.88, 'lon': -122.25}
    else:
        click_dict = eval(str(clickData))
        d = click_dict['points'][0]

    # update_map(d['lat'],d['lon'])

    return ['{:1.3f}'.format(d['lat']), '{:1.3f}'.format(d['lon']),
            n_clicks + 1]


def make_iv_summary_layout(module_parameters):
    #
    extra_parameters_dict = vocmax.cec_to_sapm(module_parameters)

    extra_parameters = pd.DataFrame(extra_parameters_dict,
                                    index=['Value']).transpose()
    extra_parameters['Parameter'] = extra_parameters.index
    extra_parameters = extra_parameters[['Parameter', 'Value']]

    # extra_parameters = vocmax.calculate_sapm_module_parameters_df(module_parameters)

    extra_parameters = extra_parameters.drop('iv_model')

    extra_parameters['Value'] = extra_parameters['Value'].map(
        lambda x: '%2.3g' % x)

    # Calculate some IV curves.
    irradiance_list = [1000, 800, 600, 400, 200]
    iv_curve = []
    for e in irradiance_list:
        ret = vocmax.calculate_iv_curve(e, 25, module_parameters)
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
                    },
                    config=dict(
                        toImageButtonOptions=dict(
                            scale=5,
                            filename='IV_curves',
                        )
                    )
                ),
            ], md=6),
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
                                         style={'font-size': '0.8rem'})
            ], md=6)
        ])
    ]


@app.callback(Output('module_name_iv', 'children'),
              [Input('module_name', 'value')
               ])
def plot_lookup_IV(module_name):
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
    module_parameters['aoi_model'] = 'ashrae'
    module_parameters['ashrae_iam_param'] = 0.05
    module_parameters['iv_model'] = 'sapm'

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
    return [item for sublist in [info_layout, temp_layout] for item in sublist]


# TODO: make input parsers for all fields.


# @app.callback(Output('manual_iv', 'children'),
#               [
#                   Input('module_name_manual', 'value'),
#                   Input('Voco', 'value'),
#                   Input('Bvoco', 'value'),
#                   Input('Mbvoc', 'value'),
#                   Input('n_diode', 'value'),
#                   Input('cells_in_series', 'value'),
#                   Input('FD', 'value'),
#                   Input('efficiency', 'value'),
#                   Input('lookup_bifaciality', 'value'),
#                ]
#               )
# def plot_manual_IV(module_name_manual,
#                  Voco, Bvoco, Mbvoc, n_diode, cells_in_series, FD,efficiency,lookup_bifaciality):
#     # try:
#     module_parameters = {
#             'name': module_name_manual,
#             'Voco': float(Voco),
#             'Bvoco': float(Bvoco),
#             'Mbvoc': float(Mbvoc),
#             'n_diode': float(n_diode),
#             'cells_in_series': float(cells_in_series),
#             'iv_model':'sapm',
#             'FD': float(FD),
#             'efficiency': float(efficiency),
#             'lookup_bifaciality': float(lookup_bifaciality),
#         }
#
#     return html.P('Valid Input')
#
#     #
#     # except:
#     #     return [
#     #         html.P('Input values invalid.')
#     #     ]


# @app.callback(Output('load', 'children'),
#               [Input('submit-button', 'n_clicks')
#                ])
# def make_calculating_screen(categ):
#     if categ:
#         return html.Div([
#             dbc.Alert("Calculating...",
#                                    color="primary")
#                 ],
#             id='graphs')


def get_weather_data(lat, lon):
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

    if filename == '124250_37.93_-122.3.npz':
        weather, info = nsrdbtools.get_local_weather_data(filename)
    else:
        weather, info = pvtoolslib.get_s3_weather_data(filename)

    return weather, info


@app.callback([Output('graphs', 'children'),
               Output('results-store', 'data'),
               # Output('voc-hist-results-store', 'children'),
               ],
              [Input('submit-button', 'n_clicks')
               ],
              [State('lat', 'value'),
               State('lon', 'value'),
               State('module_parameter_input_type', 'active_tab'),
               State('module_name', 'value'),
               State('module_name_manual', 'value'),
               State('Voco', 'value'),
               State('Bvoco', 'value'),
               State('Mbvoc', 'value'),
               State('n_diode', 'value'),
               State('cells_in_series', 'value'),
               State('FD', 'value'),
               State('efficiency', 'value'),
               State('thermal_model_input_type', 'active_tab'),
               State('racking_model', 'value'),
               State('a', 'value'),
               State('b', 'value'),
               State('DT', 'value'),
               State('open_circuit_rise', 'value'),
               State('mount_type', 'active_tab'),
               State('surface_tilt', 'value'),
               State('surface_azimuth', 'value'),
               State('axis_tilt', 'value'),
               State('axis_azimuth', 'value'),
               State('max_angle', 'value'),
               State('backtrack', 'value'),
               State('ground_coverage_ratio', 'value'),
               State('string_design_voltage', 'value'),
               State('safety_factor', 'value'),
               State('lookup_is_bifacial', 'value'),
               State('manual_is_bifacial', 'value'),
               State('lookup_bifaciality', 'value'),
               State('manual_bifaciality', 'value'),
               State('fixed_tilt_albedo', 'value'),
               State('single_axis_albedo', 'value'),
               State('fixed_tilt_backside_irradiance_fraction', 'value'),
               State('single_axis_backside_irradiance_fraction', 'value'),
               ]
              )
def run_simulation(n_clicks, lat, lon, module_parameter_input_type, module_name,
                   module_name_manual,
                   Voco, Bvoco, Mbvoc, n_diode, cells_in_series, FD, efficiency,
                   thermal_model_input_type, racking_model, a, b, DT,
                   open_circuit_rise,
                   mount_type, surface_tilt, surface_azimuth,
                   axis_tilt, axis_azimuth, max_angle, backtrack,
                   ground_coverate_ratio,
                   string_design_voltage, safety_factor,
                   lookup_is_bifacial, manual_is_bifacial,
                   lookup_bifaciality, manual_bifaciality,
                   fixed_tilt_albedo, single_axis_albedo,
                   fixed_tilt_backside_irradiance_fraction,
                   single_axis_backside_irradiance_fraction):
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
    efficiency
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
    string_design_voltage
    safety_factor

    Returns
    -------

    """
    # def run_simulation(*argv):
    print('Calback: run_simulation()')
    print('n_clicks: ', n_clicks)
    if n_clicks < 1:

        raise PreventUpdate

        print('Not running simulation.')
        return [
            [], {'simulation-performed':False}
        ]

    all_params = {
        'lat': lat,
        'lon': lon,
        'module_parameter_input_type': module_parameter_input_type,
        'module_name': module_name,
        'module_name_manual': module_name_manual,
        'Voco': Voco,
        'Bvoco': Bvoco,
        'Mbvoc': Mbvoc,
        'n_diode': n_diode,
        'cells_in_series': cells_in_series,
        'FD': FD,
        'efficiency': efficiency,
        'thermal_model_input_type': thermal_model_input_type,
        'racking_model': racking_model,
        'a': a,
        'b': b,
        'DT': DT,
        'open_circuit_rise': open_circuit_rise,
        'mount_type': mount_type,
        'surface_tilt': surface_tilt,
        'surface_azimuth': surface_azimuth,
        'axis_tilt': axis_tilt,
        'axis_azimuth': axis_azimuth,
        'max_angle': max_angle,
        'backtrack': str(backtrack),
        'ground_coverage_ratio': ground_coverate_ratio,
        'string_design_voltage': string_design_voltage,
        'iv_model': 'sapm',
        'safety_factor': safety_factor,
        'lookup_is_bifacial': lookup_is_bifacial,
        'manual_is_bifacial': manual_is_bifacial,
        'manual_bifaciality': manual_bifaciality,
        'lookup_bifaciality': lookup_bifaciality,
        'fixed_tilt_albedo': fixed_tilt_albedo,
        'single_axis_albedo': single_axis_albedo,
        'fixed_tilt_backside_irradiance_fraction': fixed_tilt_backside_irradiance_fraction,
        'single_axis_backside_irradiance_fraction': single_axis_backside_irradiance_fraction,
    }

    request_str = '?'
    for p in all_params:
        request_str = request_str + p + '=' + str(all_params[p]) + '&'

    request_str = request_str[0:-1]
    request_str = request_str.replace(' ', '_')

    is_default_calculation = request_str[0:22] == '?lat=37.88&lon=-122.25'
    print('Verbose;String Voltage Calculator;Calculate started;default=' + str(
        is_default_calculation))
    # print(request_str)

    if module_parameter_input_type == 'lookup':
        cec_parameters = pvtoolslib.cec_modules[module_name].to_dict()
        cec_parameters['FD'] = 1
        cec_parameters['name'] = module_name

        # cec_parameters['aoi_model'] = 'no_loss'
        cec_parameters['aoi_model'] = 'ashrae'
        cec_parameters['ashrae_iam_param'] = 0.05

        sapm_parameters = vocmax.cec_to_sapm(
            cec_parameters)

        module = {**sapm_parameters, **cec_parameters}

        module['is_bifacial'] = lookup_is_bifacial
        module['bifaciality_factor'] = float(lookup_bifaciality)

    elif module_parameter_input_type == 'manual':
        module = {
            'name': module_name_manual,
            'Voco': float(Voco),
            'Bvoco': float(Bvoco),
            'Mbvoc': float(Mbvoc),
            'n_diode': float(n_diode),
            'cells_in_series': float(cells_in_series),
            'aoi_model': 'ashrae',
            'ashrae_iam_param': 0.05,
            'iv_model': 'sapm',
            'FD': float(FD),
            'efficiency': float(efficiency),
            'is_bifacial': manual_is_bifacial,
            'bifaciality_factor': float(manual_bifaciality)
        }
    else:
        print('input type not understood.')

    if thermal_model_input_type == 'lookup':
        thermal_model = {
            'named_model': racking_model,
            'open_circuit_rise': open_circuit_rise,
        }
    elif thermal_model_input_type == 'manual':
        thermal_model = {
            'named_model': 'explicit',
            'a': float(a),
            'b': float(b),
            'deltaT': float(DT),
            'open_circuit_rise': open_circuit_rise,
        }
    else:
        print('Racking model not understood')

    if mount_type == 'fixed_tilt':
        racking_parameters = {
            'racking_type': 'fixed_tilt',
            'surface_tilt': float(surface_tilt),
            'surface_azimuth': float(surface_azimuth),
            'albedo': float(fixed_tilt_albedo),
            'backside_irradiance_fraction': float(
                fixed_tilt_backside_irradiance_fraction),
            'bifacial_model': 'proportional',

        }
    elif mount_type == 'single_axis_tracker':
        racking_parameters = {
            'racking_type': 'single_axis',
            'axis_tilt': float(axis_tilt),
            'axis_azimuth': float(axis_azimuth),
            'max_angle': float(max_angle),
            'backtrack': backtrack,
            'gcr': float(ground_coverate_ratio),
            'albedo': float(single_axis_albedo),
            'backside_irradiance_fraction': float(
                single_axis_backside_irradiance_fraction),
            'bifacial_model': 'proportional',
        }
    else:
        print('error getting racking type')

    string_design_voltage = float(string_design_voltage)
    safety_factor = float(safety_factor) / 100

    # print('Getting weather data...')
    weather, info = get_weather_data(lat, lon)

    # Simulate system.
    df = vocmax.simulate_system(weather, info, module,
                                racking_parameters,
                                thermal_model)

    voc_summary = vocmax.make_voc_summary(df, info, module,
                                          string_design_voltage=string_design_voltage,
                                          safety_factor=safety_factor,
                                          ashrae=pvtoolslib.ashrae)

    voc_summary_for_plot = voc_summary.rename(index={
        '690.7(A)(3)-P99.5': '690.7(A)(3)-P99.5 + SF',
        '690.7(A)(3)-P100': '690.7(A)(3)-P100 + SF'}
    )

    voc_summary_for_plot['plot_voltage'] = voc_summary_for_plot[
                                               'max_module_voltage'] * (
                                                   1 + voc_summary_for_plot[
                                               'safety_factor'])

    voc_summary_table = voc_summary.rename(index=str, columns={
        'max_module_voltage': 'Max Module Voltage',
        'safety_factor': 'Safety Factor',
        'string_design_voltage': 'String Design Voltage',
        'string_length': 'String Length',
        'short_note': 'Note'
    })

    # voc_summary_table['Note'] = voc_summary_table['Note'].apply(
    #     lambda s : s.replace('<br>','.  '))
    voc_summary_table['Max Module Voltage'] = voc_summary_table[
        'Max Module Voltage'].apply(
        lambda s: '{:2.2f}'.format(s))
    voc_summary_table['Cell Temperature'] = voc_summary_table[
        'Cell Temperature'].apply(
        lambda s: '{:2.1f}'.format(s))
    voc_summary_table['Safety Factor'] = voc_summary_table[
        'Safety Factor'].apply(
        lambda s: '{:2.1%}'.format(s))
    voc_summary_table['POA Irradiance'] = voc_summary_table[
        'POA Irradiance'].apply(
        lambda s: '{:4.0f}'.format(s))

    voc_summary_table = voc_summary_table[
        ['Max Module Voltage', 'String Design Voltage', 'Safety Factor',
         'String Length', 'Cell Temperature', 'POA Irradiance', 'Note']]

    info['pvtoolslib version'] = pvtoolslib.version
    summary_text = vocmax.make_simulation_summary(df,
                                                  info,
                                                  module,
                                                  racking_parameters,
                                                  thermal_model,
                                                  string_design_voltage,
                                                  safety_factor,
                                                  ashrae=pvtoolslib.ashrae)

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
    for s in list(voc_summary_for_plot.index):
        voc_summary_for_plot.loc[s, 'plot_color'] = colors[pc]
        pc = pc + 1

    # voc_summary['plot_color'] = colors[0:len(voc_summary)]

    # Make histograms
    def scale_to_hours_per_year(y):
        return y / info['timedelta_in_years'] * info['interval_in_hours']

    # Voc histogram
    voc_hist_y_raw, voc_hist_x_raw = np.histogram(df['v_oc'],
                                                  bins=np.linspace(
                                                      df['v_oc'].max() * 0.6,
                                                      df['v_oc'].max() + 1,
                                                      200))

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

    # POA/temperature 2D histogram
    df_day = df[df['ghi'] > 0]
    x = df_day['effective_irradiance']
    y = df_day['temp_cell']
    v_oc = df_day['v_oc']

    P99 = np.percentile(df['v_oc'], 99.9)

    poa_smooth = np.linspace(1, 1100, 100)

    T_smooth = vocmax.sapm_temperature_to_get_voc(poa_smooth,
                                                  P99,
                                                  Voco=module['Voco'],
                                                  Bvoco=module['Bvoco'],
                                                  diode_factor=module['n_diode'],
                                                  cells_in_series=module['cells_in_series'])



    # Plotting
    max_pos = np.argmax(np.array(df['v_oc']))
    plot_min_index = np.max([0, max_pos - 1000])
    plot_max_index = np.min([len(df), max_pos + 1000])

    low_pot_color = 'rgb(31, 119, 180)'
    high_pot_color = 'rgb(255, 127, 14)'

    annotation_dropdown_choices = [{'label': k, 'value': k} for k in
                                   voc_summary_for_plot.index]

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
        dcc.Dropdown(
            id='annotation_voc_histogram',
            options=annotation_dropdown_choices,
            multi=True,
            value=voc_summary_for_plot.index
        ),
        html.P(''),
        dcc.Loading(
            html.Div(
                id='Voc-histogram-div',
                children=[]
                # make_voc_histogram_figure(voc_hist_x,voc_hist_y,voc_summary_for_plot)
            ),
        ),
        html.P(''),
        html.P("""The table below shows the recommended Voc values, voltage 
        in Volts, cell temperature in Celsius and plane-of-array (POA) 
        irradiance in W/m^2. 

        """),
        html.Div([
            dbc.Table.from_dataframe(voc_summary_table,
                                     striped=False,
                                     bordered=True,
                                     hover=True,
                                     index=True,
                                     size='sm',
                                     style={'font-size': '0.8rem'}),
            html.Details([
                html.Summary('Details on index names'),
                dcc.Markdown("""The string voltage calculation provides 
                several standard values for designing string lengths. For 
                P99.5 and Hist, we provide the lowest temperature during the 
                simulation time and the associated plane-of-array (POA) 
                irradiance that produces the given voltage. The various 
                standard named values for Voc are: 
                
                - **690.7(A)(3)-P99.5** is the 99.5 percentile Voc value over 
                the simulation time. This is the recommended value of Voc to 
                use for designing PV string lengths. Statistically Voc will 
                exceed this value only 0.5% of the year. Suppose that open 
                circuit conditions occur 1% of the time randomly. In this 
                case the probability that the weather and system design 
                maintain the system voltage under the standard limit is 
                99.995%, i.e. max system voltage would statistically be 
                exceeded for 26 minutes per year. 
                
                - **690.7(A)(3)-P100** is the historical maximum Voc over the 
                {:.0f} years of simulation. 
                
                - **690.7(A)(1)-ASHRAE** is the traditional value used for 
                maximum Voc. This is found using the mean minimum yearly dry 
                bulb temperature (i.e. find the minimum temperature in each 
                year and take the mean of those values) from the ASHRAE 2017 
                database. The Voc is calculated assuming 1 sun irradiance (
                1000 W/m^2), the mean minimum yearly dry bulb temperature and 
                the module paramaeters. 
                
                - **690.7(A)(2)-ASHRAE** uses the temperature derate table in 
                NEC 2017 and the ASHRAE mean minimum yearly dry bulb 
                temperature. 
                
                
                - **690.7(A)(1)-NSRDB** is similar to 690.7(A)(1)-ASHRAE 
                except it uses the NSRDB as the datasource. 
                
                - **690.7(A)(3)-DAY** is similar to the 690.7(A)(1)-NSRDB 
                value, except the mean minimum yearly daytime dry bulb 
                temperature is used as the cell temperature for calculating 
                Voc. Daytime is defined as GHI greater than 150 W/m^2. The 
                Voc is calculated assuming 1 sun irradiance (1000 W/m^2), 
                the mean minimum yearly daytime dry bulb temperature and the 
                module paramaeters. 
    
                 """.replace('    ', '')
                             ),
            ]),
        ], style={'margin-bottom': 30}),
        html.P(''),
        html.P("""Figure 2 shows a scatter plot of POA irradiance and cell 
        temperature, highlighting the region with a Voc greater than the 
        99.9'th percentile. This is useful for statistically inspecting which 
        conditions will lead to maximum Voc. 

        """),
        dcc.Graph(
            figure=dict(
                data=[
                    go.Scattergl(
                        x=x[v_oc <= P99],
                        y=y[v_oc <= P99],
                        mode='markers',
                        name='Voc<P99.9 Voc',
                        marker=dict(color=low_pot_color, size=4, opacity=0.04)
                    ),
                    go.Histogram(
                        x=x[v_oc <= P99],
                        name='Voc<P99.9',
                        marker=dict(color=low_pot_color),
                        yaxis='y2',
                        nbinsx=100,
                        showlegend=False
                    ),
                    go.Histogram(
                        x=np.tile(x[v_oc > P99], (100)),
                        name='Voc>P99.9',
                        marker=dict(color=high_pot_color),
                        yaxis='y2',
                        nbinsx=100,
                        showlegend=False
                    ),
                    go.Histogram(
                        y=y[v_oc <= P99],
                        name='Voc<P99.9',
                        marker=dict(color=low_pot_color),
                        xaxis='x2',
                        nbinsy=100,
                        showlegend=False
                    ),
                    go.Histogram(
                        y=np.tile(y[v_oc > P99], (100)),
                        name='Voc>P99.9',
                        marker=dict(color=high_pot_color),
                        xaxis='x2',
                        nbinsy=100,
                        showlegend=False
                    ),
                    go.Scattergl(
                        x=x[v_oc > P99],
                        y=y[v_oc > P99],
                        mode='markers',
                        name='Voc>P99.9 Voc',
                        marker=dict(color=high_pot_color, size=4, opacity=0.4)
                    ),
                    go.Scatter(
                        x=poa_smooth,
                        y=T_smooth,
                        mode='lines',
                        name='P99.9 Voc Threshold',
                    ),
                ],
                layout=go.Layout(
                    title=go.layout.Title(
                        text='Figure 2. Scatterplot of POA irradiance and cell temperature.',
                        xref='paper',
                        x=0
                    ),
                    margin={'l': 60, 'b': 120, 't': 30, 'r': 60},
                    showlegend=True,
                    legend=dict(x=.05, y=0.75),
                    autosize=True,
                    # width=1100,
                    height=700,
                    xaxis=dict(
                        domain=[0, 0.85],
                        showgrid=True,
                        zeroline=False,
                        title='POA Irradiance (W/m2)'
                    ),
                    yaxis=dict(
                        domain=[0, 0.85],
                        showgrid=True,
                        zeroline=False,
                        title='Cell Temperature (C)',
                        range=[np.min(y), np.max(y)]
                    ),
                    hovermode='closest',
                    bargap=0,
                    barmode='overlay',
                    xaxis2=dict(
                        domain=[0.85, 1],
                        showgrid=False,
                        zeroline=False,
                        title='Occurrences (AU)'
                    ),
                    yaxis2=dict(
                        domain=[0.85, 1],
                        showgrid=False,
                        zeroline=False,
                        title='Occurrences (AU)'
                    )
                )
            ),
            config=dict(
                toImageButtonOptions=dict(
                    scale=5,
                    filename='poa_cell-temp_2D_scatter',
                )
            )
        ),

        # html.P("""Figure 3 shows a histogram of the air and cell temperature.
        # A spike at 0 C is sometimes observed and explained below under
        # frequently asked questions.
        #
        # """),
        # dcc.Graph(
        #     id='temperature-histogram',
        #     figure={
        #         'data': [
        #             {'x': temp_air_hist_x, 'y': temp_air_hist_y,
        #              'type': 'line', 'name': 'Air Temperature'},
        #             {'x': temp_cell_hist_x, 'y': temp_cell_hist_y,
        #              'type': 'line', 'name': 'Cell Temperature'},
        #         ],
        #         'layout': go.Layout(
        #             title=go.layout.Title(
        #                 text='Figure 3. Histogram of cell and air temperature',
        #                 xref='paper',
        #                 x=0
        #             ),
        #             xaxis={'title': 'Temperature (C)'},
        #             yaxis={'title': 'hours/year'},
        #             margin={'l': 60, 'b': 120, 't': 30, 'r': 60},
        #             hovermode='closest',
        #             # annotations=[
        #             #     dict(
        #             #         dict(
        #             #             x=temperature_poi[s]['value'],
        #             #             y=temp_cell_hist_y[np.argmin(
        #             #                 np.abs(temperature_poi[s][
        #             #                            'value'] - temp_cell_hist_x))],
        #             #             xref='x',
        #             #             yref='y',
        #             #             xanchor='center',
        #             #             text=temperature_poi[s]['short_label'],
        #             #             hovertext=temperature_poi[s]['hover_label'],
        #             #             textangle=0,
        #             #             font=dict(
        #             #                 color=temperature_poi[s]['color']
        #             #             ),
        #             #             arrowcolor=temperature_poi[s]['color'],
        #             #             showarrow=True,
        #             #             align='left',
        #             #             standoff=2,
        #             #             arrowhead=4,
        #             #             ax=0,
        #             #             ay=-40
        #             #         ),
        #             #         align='left'
        #             #     )
        #             #     for s in temperature_poi]
        #         )
        #     }
        # ),

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
                    margin={'l': 60, 'b': 120, 't': 30, 'r': 60},
                    hovermode='closest',
                    legend=dict(x=.02, y=0.95),
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
            },
            config=dict(
                toImageButtonOptions=dict(
                    scale=5,
                    filename='timeseries',
                )
            )
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
        html.P([
            html.A('Download full simulation data as csv',
                   id='download-link',
                   download='raw_data.csv',
                   href='/dash/download_simulation_data' + request_str,
                   target='_blank'),
            ' (10-20 seconds)'
        ]),
    ]

    print('voc_summary_for_plot storage values: ')
    print(voc_summary_for_plot)
    results_store = dict(voc_hist_x=voc_hist_x,
             voc_hist_y=voc_hist_y,
             voc_summary_for_plot_json=voc_summary_for_plot.to_json()
             )

    # results_store = {'am_i_cool': True}
    # print(voc_summary_for_plot.to_json())
    # voc_hist_store = pd.DataFrame({'voc_hist_x': voc_hist_x,
    #                                'voc_hist_y': voc_hist_y})
    # print(voc_hist_x)

    return [
        return_layout,
        results_store,
    ]


def make_voc_histogram_figure(voc_hist_x, voc_hist_y, voc_summary_for_plot,
                              annotation_voc_histogram_choice):
    """

    Make the voc histogram figure. Needs to be in a separate function so that
    the dropdown callback works.

    Parameters
    ----------
    voc_hist_x
    voc_hist_y
    voc_summary_for_plot
    annotation_voc_histogram_choice

    Returns
    -------

    """
    return dcc.Graph(
        id='Voc-histogram',
        figure={
            'data': [
                {'x': voc_hist_x,
                 'y': voc_hist_y,
                 'type': 'bar',
                 'name': 'Voc'}
            ],
            'layout': go.Layout(
                title=go.layout.Title(
                    text='Figure 1. Histogram of Voc values over the simulation time.',
                    xref='paper',
                    x=0
                ),
                xaxis={'title': 'Voc (Volts)'},
                yaxis={'title': 'hours/year'},
                margin={'l': 60, 'b': 120, 't': 30, 'r': 60},
                hovermode='closest',
                annotations=[
                    dict(
                        dict(
                            x=voc_summary_for_plot['plot_voltage'][s],
                            y=voc_hist_y[np.argmin(
                                np.abs(voc_summary_for_plot['plot_voltage'][
                                           s] - voc_hist_x))],
                            xref='x',
                            yref='y',
                            xanchor='left',
                            yanchor='middle',
                            text=s,
                            hovertext=voc_summary_for_plot['long_note'][s],
                            textangle=-90,
                            font=dict(
                                color=voc_summary_for_plot['plot_color'][s]
                            ),
                            arrowcolor=voc_summary_for_plot['plot_color'][s],
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
                    for s in list(annotation_voc_histogram_choice)]
            )
        },
        config=dict(
            toImageButtonOptions=dict(
                scale=5,
                filename='Voc_histogram',
            )
        )
    )


@app.callback(Output('Voc-histogram-div', 'children'),
              [
                Input('annotation_voc_histogram', 'value'),
               Input('results-store', 'modified_timestamp')
               ],
              [State('results-store', 'data'),
               ])
def make_voc_histogram_callback(annotation_voc_histogram_choice, ts, results):
    if ts is None:
        raise PreventUpdate

        return []

    voc_summary_for_plot = pd.read_json(results['voc_summary_for_plot_json'])

    return make_voc_histogram_figure(results['voc_hist_x'],
                                     results['voc_hist_y'],
                                     voc_summary_for_plot,
                                     annotation_voc_histogram_choice
                                     )


@app.server.route('/dash/download_simulation_data')
def download_simulation_data():
    print('Verbose;String Voltage Calculator;Download Simulation Data;')
    # value = flask.request.args.get('lat')
    p = flask.request.args

    filedata = pvtoolslib.get_s3_filename_df()
    filedata_closest = nsrdbtools.find_closest_datafiles(float(p['lat']),
                                                         float(p['lon']),
                                                         filedata)

    if p['module_parameter_input_type'] == 'lookup':
        cec_parameters = pvtoolslib.cec_modules[p['module_name']].to_dict()
        cec_parameters['FD'] = 1
        cec_parameters['name'] = p['module_name']
        cec_parameters['aoi_model'] = 'ashrae'
        cec_parameters['ashrae_iam_param'] = 0.05
        sapm_parameters = vocmax.cec_to_sapm(cec_parameters)
        sapm_parameters['iv_model'] = 'sapm'
        module = {**sapm_parameters, **cec_parameters}

        module['is_bifacial'] = p['lookup_is_bifacial'] == 'True'
        module['bifaciality_factor'] = float(p['lookup_bifaciality'])



    elif p['module_parameter_input_type'] == 'manual':
        module = {
            'name': p['module_name_manual'],
            'Voco': float(p['Voco']),
            'Bvoco': float(p['Bvoco']),
            'Mbvoc': float(p['Mbvoc']),
            'n_diode': float(p['n_diode']),
            'cells_in_series': float(p['cells_in_series']),
            'aoi_model': 'ashrae',
            'ashrae_iam_param': 0.05,
            'iv_model': 'sapm',
            'FD': float(p['FD']),
            'efficiency': float(p['efficiency']),
            'is_bifacial': p['manual_is_bifacial'] == 'True',
            'bifaciality_factor': float(p['manual_bifaciality']),
        }


    else:
        print('input type not understood.')


    if p['thermal_model_input_type'] == 'lookup':

        thermal_model = {
            'named_model': p['racking_model'],
            'open_circuit_rise': float(p['open_circuit_rise'])>0.5
        }

    elif p['thermal_model_input_type'] == 'manual':
        thermal_model = {
            'named_model': 'explicit',
            'a': float(p['a']),
            'b': float(p['b']),
            'deltaT': float(p['DT']),
            'open_circuit_rise': float(p['open_circuit_rise'])>0.5,
        }
    else:
        print('Verbose:Racking model not understood')

    print('Thermal model: ', thermal_model)

    if p['mount_type'] == 'fixed_tilt':
        racking_parameters = {
            'racking_type': 'fixed_tilt',
            'surface_tilt': float(p['surface_tilt']),
            'surface_azimuth': float(p['surface_azimuth']),
            'albedo': float(p['fixed_tilt_albedo']),
            'backside_irradiance_fraction': float(
                p['fixed_tilt_backside_irradiance_fraction']),
            'bifacial_model': 'proportional',
        }
    elif p['mount_type'] == 'single_axis_tracker':
        racking_parameters = {
            'racking_type': 'single_axis',
            'axis_tilt': float(p['axis_tilt']),
            'axis_azimuth': float(p['axis_azimuth']),
            'max_angle': float(p['max_angle']),
            'backtrack': p['backtrack'],
            'gcr': float(p['ground_coverage_ratio']),
            'albedo': float(p['single_axis_albedo']),
            'backside_irradiance_fraction': float(
                p['single_axis_backside_irradiance_fraction']),
            'bifacial_model': 'proportional',
        }
    else:
        print('Verbose:error getting racking type')

    string_design_voltage = float(p['string_design_voltage'])

    # print('String Voltage Calculator:Input processed:')

    weather, info = pvtoolslib.get_s3_weather_data(
        filedata_closest['filename'].iloc[0])

    df = vocmax.simulate_system(weather, info, module,
                                racking_parameters,
                                thermal_model)

    # df_temp = pd.DataFrame(info,index=[0])
    # df_temp = df.copy()

    # print(df_temp.keys())

    # df_temp = df.copy()
    # df_temp = df_temp.drop('aoi')
    df = df[['year', 'month', 'day', 'hour', 'minute', 'dni', 'ghi', 'dhi',
             'temp_air', 'wind_speed', 'temp_cell', 'effective_irradiance',
             'v_oc']]

    df['wind_speed'] = df['wind_speed'].map(lambda x: '%.1f' % x)
    df['v_oc'] = df['v_oc'].map(lambda x: '%.4g' % x)
    df['temp_cell'] = df['temp_cell'].map(lambda x: '%.0f' % x)
    # df_temp['aoi'] = df_temp['aoi'].map(lambda x: '%3.0f' % x)
    df['effective_irradiance'] = df['effective_irradiance'].map(
        lambda x: '%.0f' % x)


    pvtools_info = {'PVTOOLS version': pvtoolslib.version}
    # print('String Voltage Calculator:df made:')

    # Create DF
    # d = {'col1': [1, 2], 'col2': [3, 4]}
    # df = pd.DataFrame(data=d)

    # Convert DF
    str_io = io.StringIO()
    pd.DataFrame(
        {**pvtools_info, **info, **module, **thermal_model, **racking_parameters},
        index=['']).to_csv(str_io, sep=",", index=False)
    # pd.DataFrame(module_parameters, index=['']).to_csv(str_io, sep=",")
    # pd.DataFrame(racking_parameters, index=['']).to_csv(str_io, sep=",")
    df.to_csv(str_io, sep=",", index=False)

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

    # Convert DF
    # with str_io as io.StringIO():
    str_io = io.StringIO()
    pd.DataFrame(info, index=['']).to_csv(str_io, sep=",", index=False)
    weather.to_csv(str_io, sep=",", index=False)
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
