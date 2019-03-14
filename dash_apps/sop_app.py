import pandas as pd
import xarray as xr
import numpy as np          
import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.6/site-packages')
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import os

import plotly.plotly as py
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
    # Online modus
    app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
    app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
    server = app.server
else:
    # Offline modus
    app = dash.Dash()
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

print('High!!',app.config.routes_pathname_prefix.split('/')[-1])

# Where is the data stored?

bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'

bd2 = ''            # For local running
bd2 = '/myapp'      # For local and remote climexp.knmi.nl

    
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

plottypes={'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'}
variables={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}
#fc_time={'Stepwise':'stepwise','Not stepwise':'cor'}
variables_prad={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}
variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'}


anno_text = "Data courtesy of Folmer Krikken"

clickData_start = dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]})




# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to the KPREP sources of predictabily app '+bd2, href=bd2+'/kprep-sop'),
    html.Br(),
    dcc.Link('Go to the KRPEP predictor-predictand relations app '+bd2, href=bd2+'/kprep-pp'),
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
    html.ObjectEl(type="text/html",name='../myvinkhead.cgi'),
    html.Br(),
    html.Div(children='This website can be used to study the sources of predictability in the KPREP empirical forecasting system. The dropdown menu allow to change the predictand, plot type and forecasting time. By clicking on the map the barplot gives the contribution of the predictors to the forecasted anomalie, and the line plots give more information on the forecasts and predictors over time'),
    html.Br(),
    dcc.Link('Click here to examine predictor-predictand relations', href=bd2+'/kprep-pp'),
    html.Br(),
    html.Br(),
    # Create dropdown menu to choose variable, and specify with which to start
    
    html.Div([
            dcc.Dropdown(
                id='variable',
                options=[{'label': i,'value': i} for i in variables.keys()],
                value='Temperature',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),
    # Create dropdown menu to choose plot type, and specify with which to start
    html.Div([
            dcc.Dropdown(
                id='plot_type',
                options=[{'label': i,'value': i} for i in plottypes.keys()],
                value='Forecast anomalies',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),

    # Create dropdown menu to choose time step, and specify with which to start (latest time)
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
    # Create the different figures and specify the sizes    
    html.Div([
        dcc.Graph(id='basemap_plot')],
        style={'width':'65%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='bar_plot')],
        style={'width':'25%','display': 'inline-block','margin': {'b': 200, 'r': 10, 'l': 30, 't': 10}}),
    

    html.Div([
        dcc.Graph(id='predictand_plot')],
        style={'width':'55%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    html.Div([
        dcc.Graph(id='predictor_plot')],
        style={'width':'55%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align': 'middle'}),    
    

    ])

page_2_layout = html.Div(children=[
    html.H1(children='Sources of predictability - KPREP empirical forecast system'),

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
                options=[{'label': i,'value': i} for i in variables_prad.keys()],
                value='Temperature',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),
    # Create dropdown menu to choose predictor variable
    html.Div([
            dcc.Dropdown(
                id='predictor',
                options=[{'label': i,'value': i} for i in variables_pred.keys()],
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
        style={'width':'65%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='xy_plot')],
        style={'width':'25%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    
    html.Div([
        dcc.Graph(id='basemap_plot2')],
        style={'width':'55%','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    
    ])
      


@app.callback(
    dash.dependencies.Output('basemap_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot','clickData'),
     dash.dependencies.Input('plot_type', 'value'),
     dash.dependencies.Input('variable', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map(clickData,plot_type,variable,fc_time):
    return create_map(clickData,plot_type,variable,fc_time)

# Update barplot
@app.callback(
    dash.dependencies.Output('bar_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('plot_type','value'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_bar_plot(clickData,plot_type,variable,fc_time):
    return create_bar_plot(clickData,plot_type,variable,fc_time)
    
# Update predictand timeseries                    
@app.callback(
    dash.dependencies.Output('predictand_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_time_series(clickData,variable,fc_time):
    return create_time_series(clickData,variable,fc_time)


# Update predictor timeseries
@app.callback(
    dash.dependencies.Output('predictor_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_po_timeseries(clickData,variable,fc_time):
    return create_po_timeseries(clickData,variable,fc_time)


# Update corplot map orig vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot1', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map(clickData,predictand,predictor,fc_time):
    return create_map1(clickData,predictand,predictor,fc_time)

# Update corplot map fitted predictors vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot2', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value')])
def update_map(clickData,predictand,predictor,fc_time):
    return create_map2(clickData,predictand,predictor,fc_time)

   
# Update xyplot                    
@app.callback(
    dash.dependencies.Output('xy_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot1', 'clickData'),
     dash.dependencies.Input('predictand','value'),
     dash.dependencies.Input('predictor','value'),
     dash.dependencies.Input('fc_time','value')])
def update_time_series(clickData,predictand,predictor,fc_time):
    return create_xyplot(clickData,predictand,predictor,fc_time)





#@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              #[dash.dependencies.Input('page-1-dropdown', 'value')])
#def page_1_dropdown(value):
    #return 'You have selected "{}"'.format(value)


#page_2_layout = html.Div([
    #html.H1('Page 2'),
    #dcc.RadioItems(
        #id='page-2-radios',
        #options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        #value='Orange'
    #),
    #html.Div(id='page-2-content'),
    #html.Br(),
    #dcc.Link('Go to Page 1', href='/page-1'),
    #html.Br(),
    #dcc.Link('Go back to home', href='/')
#])

#@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              #[dash.dependencies.Input('page-2-radios', 'value')])
#def page_2_radios(value):
    #return 'You have selected "{}"'.format(value)


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
        return index_page
    # You could also return a 404 "URL not found" page here


#if __name__ == '__main__':
    #app.run_server(debug=True)
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)#,host='0.0.0.0')#,port=80)    
