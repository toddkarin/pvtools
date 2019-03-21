import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)



# # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server
#
# app.layout = html.Div([
#     html.H2('Hello World')
# ])
#
#
# app.config.suppress_callback_exceptions = True
#
# # app.config.suppress_callback_exceptions = False
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = False
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)