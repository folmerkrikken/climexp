# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Add these external stylesheets for nice loading phases
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

ONLINE=True
if ONLINE:
    app = dash.Dash(
        __name__, 
        requests_pathname_prefix='/kprep_fc/',
        #meta_tags=[{"name": "viewport", "content": "width=device-width"}],
        external_stylesheets=external_stylesheets,
        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
        #serve_locally=False,
        #app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]

        #app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
        #routes_pathname_prefix='/kprep_sf/',
        )
else:
    app = dash.Dash(external_stylesheets=external_stylesheets)


print('app layout',app.layout)

server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.config.suppress_callback_exceptions = True
if __name__ == "__main__":
    app.run_server(debug=True,threaded=True)
