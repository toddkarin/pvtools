import dash
import dash_bootstrap_components as dbc


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

# app.config.suppress_callback_exceptions = False
app.css.config.serve_locally = True
app.scripts.config.serve_locally = False


if __name__ == '__main__':
    app.run_server(debug=True)