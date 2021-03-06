import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
#
# header = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.Img(
#                 src=app.get_asset_url('LBL_Masterbrand_logo_with_Tagline-01.jpg'),
#                 style={'height': 50})
#             ],width=4),
#         dbc.Col([
#             html.Img(
#                 src=app.get_asset_url('duramat_logo.png'),
#                 style={'height': 50})
#             ],width=4)
#
#         ],justify='between')
# ])
#
# navbar = dbc.NavbarSimple(
#     children=[
#         # dbc.NavItem(dbc.NavLink("DURAMAT", href="index")),
#         dbc.DropdownMenu(
#             nav=True,
#             in_navbar=True,
#             label="Tools",
#             children=[
#                 dbc.DropdownMenuItem("String Length Calculator",href='apps/string-length-calculator'),
#                 dbc.DropdownMenuItem("Photovoltaic Climate Zones"),
#                 dbc.DropdownMenuItem(divider=True),
#                 dbc.DropdownMenuItem("Documentation"),
#             ],
#         ),
#         dbc.NavItem(dbc.NavLink("Contact", href="#")),
#     ],
#     brand="PVTOOLS",
#     brand_href="#",
#     sticky="top",
# )

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(["About"]),
                        html.P(
                            """PVTOOLS is a set of web applications and 
                            python libraries for photovoltaic-specific 
                            applications. This work is funded by the Duramat coalition.
                            
                            """
                        ),
                        # html.A( dbc.Button("Learn More", color="secondary"),
                        #         href='about'),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2(["String Length Calculator "]),
                        html.P(
                            """The string length calculator is an industry 
                            standard tool for calculating the maximum string 
                            length for a PV system in a given location.  
                        
                            """
                        ),
                        html.A( dbc.Button("Launch Tool", color="secondary"),
                                href='string-length-calculator'),
                        html.A(
                            html.Img(
                                src=app.get_asset_url(
                                    'string_length_screenshot.png'),
                                style={'width': '100%'}),
                            href='string-length-calculator'
                        ),
                        html.H2([
                            "Photovoltaic Climate Zones ",
                            dbc.Badge("New!", color="success")]
                        ),
                        html.P(
                            """Explore the geographic distribution of 
                            environmental stress on solar photovoltaics. 

                            """
                        ),
                        # html.A( dbc.Button("Launch Tool", color="secondary"),
                        #         href='pv-climate-stressors'),
                        html.P(''),
                        html.A(
                            html.Img(
                                src=app.get_asset_url(
                                    'pvcz_screenshow2.jpg'),
                                style={'width': '100%'}),
                            href='pv-climate-stressors'
                        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)

# layout = [header, navbar, body]




if __name__ == "__main__":
    app.layout = html.Div(layout)
    app.run_server()