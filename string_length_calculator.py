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
                        html.H2(["String Lengths!!!!"]),
                        html.P(
                            """PVTOOLS is a set of web applications and 
                            python libraries for photovoltaic-specific 
                            applications. This work is funded by the Duramat coalition.
                            
                            """
                        ),
                        dbc.Button("Learn More", color="secondary"),
                    ],
                    md=4,
                )
            ]
        )
    ],
    className="mt-4",
)

# layout = [header, navbar, body]


# app.layout = html.Div(layout)

if __name__ == "__main__":
    app.run_server()