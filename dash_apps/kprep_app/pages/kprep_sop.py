#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import xarray as xr
import numpy as np          
#import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.6/site-packages')
#import matplotlib
#matplotlib.use('Agg')
#from mpl_toolkits.basemap import Basemap
#import numpy as np
#import os
#import chart_studio.plotly as py
#import plotly.plotly as py
#from plotly.graph_objs import *
#import plotly.graph_objs as go
#import plotly.tools as tls
from app_tools import *


import dash
import dash_core_components as dcc
import dash_html_components as html

from app_kprep import app

from utils import Header_sop,info,info_sop

# Where is the data stored?
bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
bdnc = bd+'ncfiles/'


# Create dictionary with available times
timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',combine='by_coords',concat_dim='time').time.sortby('time').values
months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
dict_times = dict(zip(months12,range(1,13)))

# Create all info needed for the dropdowns
# info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'},
#         'variables':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
#         'variables_prad':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
#         'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
#         'bdnc':bdnc,
#         'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
#         }


# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

style_box = {'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': '#DCDCDC',# '#f9f9f9',
                                 'padding': '10px',
                                 'margin-bottom': '10px',
                                 'margin-left': '10px',
                                 'textAlign':'center',
            }

## Set page layout

page_1_layout = html.Div(children=[
    html.Div([Header_sop(app)]),    
    html.Br(),

    # 
    html.Div(
        [
        html.Div(
            [
            html.Div(
                [
                html.Div(
                    [
                    dcc.Markdown(info_sop),#,style=style_box),
                    ],style={'width': '60%', 'display': 'inline-block','textAlign':'center'}),
                ],style={'textAlign':'center'}),
                html.Div(
                    [

                    html.Div([
                            html.Label('Select variable',title='Select the variable you are interested in'),
                            dcc.Dropdown(
                                id='variable',
                                options=[{'label': i,'value': i} for i in info['variables'].keys()],
                                value='Temperature',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),
                    # Create dropdown menu to choose plot type, and specify with which to start
                    html.Div([
                            html.Label('Select plot type',title='Select the plot type'),
                            dcc.Dropdown(
                                id='plot_type',
                                options=[{'label': i,'value': i} for i in info['plottypes'].keys()],
                                value='Forecast anomalies',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),

                    # Create dropdown menu to choose base time, and specify with which to start (latest time)
                    html.Div([
                            html.Label('Select forecast time',title='Select the months when the forecast is started from. The forecast is then valid for the next three months'),
                            dcc.Dropdown(
                                id='fc_time',
                                options=[{'label': i,'value': i} for i in dict_times.keys()],
                                value=list(dict_times.keys())[0],
                            ),

                        ],
                        style={'width': '20vh', 
                               'display': 'inline-block',
                               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                                }),
                   
                    ],
                    className='app-dropdown',
                ),
                ],style={'textAlign':'center'},
        ),

        #html.Div(id='display-selected-values')
        # Create the different figures and specify the sizes    
        html.Br(),
        html.Div([
            html.H6(
                "Forecasting map",
                className="subtitle padded",
            ),
            #html.H6('By clicking on the map you can further specify the region of interest'),
            dcc.Graph(id='basemap_plot')],
            #style={'width':'65vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '50%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'textAlign':'center',
                    }),
        html.Div([
            html.H6(
                "Individual contribution predictors",
                className="subtitle padded",
            ),        
            dcc.Graph(id='bar_plot')],
            #style={'width':'100vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '39%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'textAlign':'center',
                   }),
        html.Div([
            html.H6(
                "Historical forecasts overview",
                className="subtitle padded",
            ),              
            dcc.Graph(id='predictand_plot')],
            #style={'width':'100vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '47%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'textAlign':'center',
                   }),
        html.Div([
            html.H6(
                "Predictor time series",
                className="subtitle padded",
            ),              
            dcc.Graph(id='predictor_plot')],
            #style={'width':'100vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '47%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'textAlign':'center',
                   }),
                                    
        ],style = {'width': '95%', 'display': 'inline-block',
                                             'border-radius': '15px',
                                             'box-shadow': '8px 8px 8px grey',
                                             'background-color': '#DCDCDC',#f9f9f9',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             'textAlign':'center',
                    }
    ),            
    ])
     


### Callbacks PAGE-1 ###

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

