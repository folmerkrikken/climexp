# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#from pages import kprep_mdc_forecast
#     kprep_mdc_forecast,
#     kprep_mdc_sop,
#     kprep_mdc_pp,
#     #feesMins,
#     #distributions,
#     #newsReviews,
#     )


# ONLINE=False
# if ONLINE:
#     # Online modus
#     app2 = dash.Dash(requests_pathname_prefix='/fire_weather/',external_stylesheets=external_stylesheets)
#     #app2 = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
#     #print(app2.config.routes_pathname_prefix)
#     #app2.config.requests_pathname_prefix = app2.config.routes_pathname_prefix.split('/')[-1]
#     app2.css.config.serve_locally = True
#     app2.scripts.config.serve_locally = True
#     server = app2.server
#     bd2 = '/myapp2'
# else:
#     # Offline modus
#     app2 = dash.Dash(external_stylesheets=external_stylesheets)
#     app2.css.config.serve_locally = True
#     app2.scripts.config.serve_locally = True
#     bd2 = ''

# print('High!!',app2.config.routes_pathname_prefix.split('/')[-1])

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

#if __name__ != '__main__':
#    app.config.request_pathname_prefix = '/kprep_fc/'
    
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True   
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
print('app layout',app.layout)
#server = app.server

server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.config.suppress_callback_exceptions = True
if __name__ == "__main__":
    app.run_server(debug=True,threaded=True)
