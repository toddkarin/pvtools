# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
#
import app as app

#
# layout = dbc.Container([
# 	html.Div(['Under Construction'])
# 	])


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
# import dash_table_experiments as dte
from flask import send_file
import io
import flask
import pandas as pd


# app = dash.Dash()
layout = html.Div(children=[
    html.A("download csv", href="/download_csv/"),
])


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