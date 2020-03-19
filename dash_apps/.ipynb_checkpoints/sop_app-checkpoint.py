#!/usr/bin/python3
import numpy
#print(numpy.__file__)
import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.7/site-packages')
import pandas as pd
import xarray as xr
import numpy as np          

import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import os

#import plotly.plotly as py
import chart_studio.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly.tools as tls
from app_tools import *


import dash
import dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


ONLINE=True
if ONLINE:
    print('<<< ONLINE MODUS >>>')
    # Online modus
    app = dash.Dash(__name__,requests_pathname_prefix='/kprep_fc/')
    #app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
    #print(app.config.routes_pathname_prefix)
    #app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    server = app.server
    bd2 = '/kprep_fc'      # For local (through apache) and remote climexp.knmi.nl
else:
    print('<<< OFFLINE MODUS >>>')
    # Offline modus
    app = dash.Dash()
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    #app = dash.Dash(requests_pathname_prefix='/myapp/')
    bd2 = ''            # For local (python) running
#css_link = '/static/my-stylesheet.css' # update with your stylesheet. could be https://... as well
#js_link = '/static/my-script.js' # update with your custom JS link if applicable. again, could be a remote url prefixed with e.g. https://... as well
#js_link = 'https://unpkg.com/react@16.8.6/umd/react.production.min.js'


print('High!!',app.config.routes_pathname_prefix.split('/')[-1])

# Where is the data stored?

bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'

#


    
#bd = '/home/folmer/KPREP/'
bdnc = bd+'ncfiles/'


#tmp_nc = xr.open_dataset(bdnc+'predadata_v2_GCEcom.nc')
timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',concat_dim='time').time.sortby('time').values
#timez = tmp_nc.time[-12:].values
months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
dict_times = dict(zip(months12,range(1,13)))


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#plottypes={'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'}
#variables={'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'}
##fc_time={'Stepwise':'stepwise','Not stepwise':'cor'}
#variables_prad={'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'}
#variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'}
info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary  plot':'tercile','Forecast anomalies':'for_anom'},
        'variables':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_prad':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
        'bdnc':bdnc,
        'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
        }

anno_text = "Data courtesy of Folmer Krikken"

#clickData_start = dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]})




# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
#    html.Link(rel='stylesheet', href=css_link),
    #html.Script(type='text/javascript', src=js_link),
])


index_page = html.Div([
    dcc.Link('Go to the KPREP sources of predictabily app ', href=bd2+'/kprep-sop'),
    html.Br(),
    dcc.Link('Go to the KRPEP predictor-predictand relations app ', href=bd2+'/kprep-pp'),
])

#page_1_layout = html.Div([
    #html.H1('Page 1'),
    #dcc.Dropdown(
        #id='page-1-dropdown',
        #options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        #value='LA'
    #),
    #html.Div(id='page-1-content'),
    #html.Br(),
    #dcc.Link('Go to Page 2', href='/page-2'),
    #html.Br(),
    #dcc.Link('Go back to home', href='/'),

#])
page_1_layout = html.Div(children=[
    html.H1(children='Sources of predictability - KPREP empirical forecast system'),

    html.Div(children='''
        This app is constructed using Dash, a web application framework for Python. Any questions, suggestion or comments mail folmer.krikken@knmi.nl
    '''),
    #html.ObjectEl(type="text/html",name='../myvinkhead.cgi'),
    html.Br(),
    html.Div(children="This website can be used to study the sources of predictability in the KPREP empirical forecasting system. The dropdown menu's allow to change the predictand, plot type and forecasting time. By clicking on the map the barplot gives the contribution of the predictors to the forecasted anomalie, and the line plots give more information on the forecasts and predictors over time"),
    html.Br(),
    dcc.Link('Click here to examine predictor-predictand relations', href=bd2+'/kprep-pp'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    #html.Div(children='Select region',style={'width': '20%', 'display': 'inline-block'}),
    html.Div(children=' Select forecasted variable',style={'width': '25vh', 'display': 'inline-block'}),
    html.Div(children=' Select plot type',style={'width': '25vh', 'display': 'inline-block'}),
    html.Div(children=' Select forecast base time',style={'width': '25vh', 'display': 'inline-block'}),
    html.Br(),
    #html.Div(children='Select forecast valid time',style={'width': '20%', 'display': 'inline-block'}),
    # Create dropdown menu to choose variable, and specify with which to start
    
    html.Div([
            dcc.Dropdown(
                id='variable',
                options=[{'label': i,'value': i} for i in info['variables'].keys()],
                value='Temperature',
            ),

        ],
        style={'width': '25vh', 'display': 'inline-block'}),
    # Create dropdown menu to choose plot type, and specify with which to start
    html.Div([
            dcc.Dropdown(
                id='plot_type',
                options=[{'label': i,'value': i} for i in info['plottypes'].keys()],
                value='Forecast anomalies',
            ),

        ],
        style={'width': '25vh', 'display': 'inline-block'}),

    # Create dropdown menu to choose time step, and specify with which to start (latest time)
    html.Div([
            dcc.Dropdown(
                id='fc_time',
                options=[{'label': i,'value': i} for i in dict_times.keys()],
                value=list(dict_times.keys())[0],
            ),

        ],
        style={'width': '25vh', 
               'display': 'inline-block',
               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                }),
    # Create the different figures and specify the sizes    
    html.Br(),
    html.Div([
        dcc.Graph(id='basemap_plot')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='bar_plot')],
        style={'width':'40vh','display': 'inline-block','margin': {'b': 200, 'r': 10, 'l': 30, 't': 10}}),
    

    html.Div([
        dcc.Graph(id='predictand_plot')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    html.Div([
        dcc.Graph(id='predictor_plot')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align': 'middle'}),    
    

    ])

page_2_layout = html.Div(children=[
    html.H1(children='KPREP empirical forecast system - Sources of predictability'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Br(),
    dcc.Link('Click here to go back to predictand info', href=bd2+'/kprep-sop'),
    html.Br(),
    html.Br(),
    # Create dropdown menu to choose predictand variable
    html.Div([
            dcc.Dropdown(
                id='predictand',
                options=[{'label': i,'value': i} for i in info['variables_prad'].keys()],
                value='Temperature',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),
    # Create dropdown menu to choose predictor variable
    html.Div([
            dcc.Dropdown(
                id='predictor',
                options=[{'label': i,'value': i} for i in info['variables_pred'].keys()],
                value='CO2',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),

    # Create dropdown menu to choose time step
    html.Div([
            dcc.Dropdown(
                id='fc_time',
                options=[{'label': i,'value': i} for i in dict_times.keys()],
                value=list(dict_times.keys())[0],
            ),

        ],
        style={'width': '30%', 
               'display': 'inline-block',
               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                }),
    # Create     
    html.Div([
        dcc.Graph(id='basemap_plot1')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    html.Div([
        dcc.Graph(id='xy_plot')],
        style={'width':'50vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    
    html.Div([
        dcc.Graph(id='basemap_plot2')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    
    html.Div([
        dcc.Graph(id='basemap_plot3')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    
    ])
      


@app.callback(
    dash.dependencies.Output('basemap_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot','clickData'),
     dash.dependencies.Input('plot_type', 'value'),
     dash.dependencies.Input('variable', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map1(clickData,plot_type,variable,fc_time):
    return create_map(clickData,plot_type,variable,fc_time,info)

# Update barplot
@app.callback(
    dash.dependencies.Output('bar_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('plot_type','value'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_bar_plot(clickData,plot_type,variable,fc_time):
    return create_bar_plot(clickData,plot_type,bdnc,variable,fc_time,info)
    
# Update predictand timeseries                    
@app.callback(
    dash.dependencies.Output('predictand_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_time_series(clickData,variable,fc_time):
    return create_time_series(clickData,variable,bdnc,fc_time,info)


# Update predictor timeseries
@app.callback(
    dash.dependencies.Output('predictor_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_po_timeseries(clickData,variable,fc_time):
    return create_po_timeseries(clickData,variable,bdnc,fc_time,info)


### Updating Page 2 ###

# Update corplot map orig vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot1', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map2(clickData,predictand,predictor,fc_time):
    return create_map1(clickData,predictand,predictor,fc_time,bdnc,info)

# Update corplot map fitted predictors vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot2', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map3(clickData,predictand,predictor,fc_time):
    return create_map2(clickData,predictand,predictor,fc_time,bdnc,info)

# Update corplot map fitted predictors vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot3', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map4(clickData,predictand,predictor,fc_time):
    return create_map3(clickData,predictand,predictor,fc_time,bdnc,info)

   
# Update xyplot                    
@app.callback(
    dash.dependencies.Output('xy_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot1', 'clickData'),
     dash.dependencies.Input('predictand','value'),
     dash.dependencies.Input('predictor','value'),
     dash.dependencies.Input('fc_time','value')])
def update_time_series(clickData,predictand,predictor,fc_time):
    return create_xyplot(clickData,predictand,predictor,fc_time,bdnc,info)




# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print('pathname is: ',pathname)
    if pathname == bd2+'/kprep-sop':
        return page_1_layout
    elif pathname == bd2+'/kprep-pp':
        return page_2_layout
    else:
        return page_1_layout
    # You could also return a 404 "URL not found" page here


# Dash CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(ssl_context='adhoc',debug=True,threaded=True)#,host='0.0.0.0')#,port=80)    
