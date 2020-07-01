# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Add these external stylesheets for nice loading phases
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(
    __name__, 
    #requests_pathname_prefix='/kprep_fc/',  # comment out when running locally
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    )

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.config.suppress_callback_exceptions = True
if __name__ == "__main__":
    app.run_server(debug=True,threaded=True)
