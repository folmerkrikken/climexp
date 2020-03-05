# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

app2 = dash.Dash(
    __name__, 
    requests_pathname_prefix='/kprep_mdc/',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets,
    )
server = app2.server

app2.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app2.config.suppress_callback_exceptions = True

if __name__ == "__main__":
    app2.run_server(debug=True,threaded=True)