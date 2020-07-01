#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import xarray as xr
import numpy as np          
import sys
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

from utils import Header_pp,info


# Where is the data stored?
bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
bdnc = bd+'ncfiles/'

# Create dictionary with available times
timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',combine='by_coords',concat_dim='time').time.sortby('time').values
months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
dict_times = dict(zip(months12,range(1,13)))

# # Create all info needed for the dropdowns
# info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary  plot':'tercile','Forecast anomalies':'for_anom'},
#         'variables':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
#         'variables_prad':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
#         'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
#         'bdnc':bdnc,
#         'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
#         }

# Don't know what this is for..
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



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

#def create_layout(app):

page_2_layout = html.Div(children=[
    html.Div([Header_pp(app)]),    
    html.Br(),

    # 
    html.Div(
        [
        html.Div(
            [

                html.Div(
                    [

                    html.Div([
                            html.Label('Select variable',title='Select the variable you are interested in'),
                            dcc.Dropdown(
                                id='predictand',
                                options=[{'label': i,'value': i} for i in info['variables'].keys()],
                                value='Temperature',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),
                    # Create dropdown menu to choose plot type, and specify with which to start
                    html.Div([
                            html.Label('Select predictor',title='Select the predictor'),
                            dcc.Dropdown(
                                id='predictor',
                                options=[{'label': i,'value': i} for i in info['variables_pred'].keys()],
                                value='CO2',
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
                    html.Br(),                        
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
                "Predictor-Predictand correlation map - original predictor data",
                className="subtitle padded",
            ),
            #html.H6('By clicking on the map you can further specify the region of interest'),
            dcc.Graph(id='basemap_plot1')],
            #style={'width':'65vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
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
                "Predictor-Predictand correlation map - after predictor selection",
                className="subtitle padded",
            ),        
            dcc.Graph(id='basemap_plot2')],
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
                "Scatter plot predictor-predictand",
                className="subtitle padded",
            ),        
            dcc.Graph(id='xy_plot')],
            #style={'width':'100vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '40%', 'display': 'inline-block',
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

                    
    


# ### Callbacks PAGE-2 ###
# # Update corplot map orig vs predictand
@app.callback(
    dash.dependencies.Output('basemap_plot1', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('fc_time','value'),
    ])
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

# # Update xyplot                    
@app.callback(
    dash.dependencies.Output('xy_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot1', 'clickData'),
     dash.dependencies.Input('predictand','value'),
     dash.dependencies.Input('predictor','value'),
     dash.dependencies.Input('fc_time','value')])
def update_time_series(clickData,predictand,predictor,fc_time):
    return create_xyplot(clickData,predictand,predictor,fc_time,bdnc,info)
