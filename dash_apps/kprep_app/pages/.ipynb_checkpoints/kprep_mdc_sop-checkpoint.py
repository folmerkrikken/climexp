#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import xarray as xr
import numpy as np          
import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.6/site-packages')
import matplotlib
#matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import chart_studio.plotly as py
#import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly.tools as tls
from app_tools_mdc import *


import dash
import dash_core_components as dcc
import dash_html_components as html

from app_mdc import app2

from app_tools import Header

#print(dcc.__version__) # 0.6.0 or above is required
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

#app2= dash.Dash(__name__, external_stylesheets=external_stylesheets)


#app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Where is the data stored?

bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'


    
#bd = '/home/folmer/KPREP/'
bdnc = bd+'ncfiles/'


#tmp_nc = xr.open_dataset(bdnc+'predadata_v2_GCEcom.nc')
#timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',concat_dim='time').time.sortby('time').values
#timez = tmp_nc.time[-12:].values
#months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
base_times = dict(zip(['March','April','May','June','July','August','September','October'],range(3,11)))
valid_times = dict(zip(['April','May','June','July','August','September','October'],range(4,11)))
dict_times = base_times

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

plottypes={'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'}
regions={'Northern hemisphere':{'lon1':-180,'lon2':180,'lat1':0,'lat2':90},
         'Mediterranean':{'lon1':-12,'lon2':31,'lat1':34,'lat2':48},
         'Boreal Eurasia':{'lon1':4,'lon2':190,'lat1':50,'lat2':72},
         'Boreal North America':{'lon1':-168,'lon2':-52,'lat1':44,'lat2':72},
        }
#fc_time={'Stepwise':'stepwise','Not stepwise':'cor'}

#variables_prad={'Temperature':'TMAX','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}

#variables={'Maximum temperature':'TMAX','Precipitation':'GPCCcom','MDC (from TP)':'MDC_FROM_TP'}
variables={'Maximum temperature':'TMAX','Precipitation':'GPCCcom','Monthly Drought Index':'MDC','Monthly Drought Index (from TP)':'MDC_FROM_TP'}
variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'PRECIP','PERS':'PERS','PERS_TREND':'PERS_TREND','TMAX':'TMAX'}
area_sizes = {u'1x1\N{DEGREE SIGN}':1,u'3x3\N{DEGREE SIGN}':3,u'5x5\N{DEGREE SIGN}':5,u'7x7\N{DEGREE SIGN}':7,u'10x10\N{DEGREE SIGN}':10}
#degree_sign= u'\N{DEGREE SIGN}'


anno_text = "Data courtesy of Folmer Krikken"

clickData_start = dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]})




# Since we're adding callbacks to elements that don't exist in the app2.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app2.config.suppress_callback_exceptions = True

style_box = {'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': '#DCDCDC',# '#f9f9f9',
                                 'padding': '10px',
                                 'margin-bottom': '10px',
                                 'margin-left': '10px',
                                 'textAlign':'center',
            }

#def create_layout(app2):
page_2_layout = html.Div(children=[
    html.Div([Header(app2)]),    
    html.Br(),    
    html.H1(children='Sources of predictability - KPREP empirical forecast system - Monthly Drought Code'),

    html.Div(children='''
        This app is constructed using Dash, a web application framework for Python. Any questions, suggestion or comments mail folmer.krikken@knmi.nl
    '''),
    #html.ObjectEl(type="text/html",name='../myvinkhead.cgi'),
#     html.Br(),
#     html.Div(children='This website can be used to study the sources of predictability in the KPREP empirical forecasting system. The dropdown menu allow to change the predictand, plot type and forecasting time.'),
#     html.Div(children='By clicking on the map the barplot gives the contribution of the predictors to the forecasted anomalie, and the line plots give more information on the forecasts and predictors over time'),
#     html.Br(),
#     dcc.Link('Click here to examine the forecasting page', href=bd2+'/kprep-mdc-enduser'),
#     html.Br(),
#     dcc.Link('Click here to examine predictor-predictand relations', href=bd2+'/kprep-mdc-pp'),
#     html.Br(),
#     html.Br(),
#     html.Br(),    
#     html.Div(children='Select region',style={'width': '20vh', 'display': 'inline-block'}),
#     html.Div(children='Select forecasted variable',style={'width': '20vh', 'display': 'inline-block'}),
#     html.Div(children='Select plot type',style={'width': '20vh', 'display': 'inline-block'}),
#     html.Div(children='Select forecast base time',style={'width': '20vh', 'display': 'inline-block'}),
#     html.Div(children='Select forecast valid time',style={'width': '20vh', 'display': 'inline-block'}),
#     html.Br(),
             #Select forecasted variable        Select plottype  Select forecast base time   Select valid forecast time'),
    # Create dropdown menu to choose region
    html.Div([
            dcc.Dropdown(
                id='region',
                options=[{'label': i,'value': i} for i in regions.keys()],
                value='Northern hemisphere',
            ),

        ],
        style={'width': '20vh', 'display': 'inline-block'}),
    # Create dropdown menu to choose variable, and specify with which to start
    
    html.Div([
            dcc.Dropdown(
                id='variable',
                options=[{'label': i,'value': i} for i in variables.keys()],
                value='Maximum temperature',
            ),

        ],
        style={'width': '20vh', 'display': 'inline-block'}),
    # Create dropdown menu to choose plot type, and specify with which to start
    html.Div([
            dcc.Dropdown(
                id='plot_type',
                options=[{'label': i,'value': i} for i in plottypes.keys()],
                value='Forecast anomalies',
            ),

        ],
        style={'width': '20vh', 'display': 'inline-block'}),

    # Create dropdown menu to choose base time, and specify with which to start (latest time)
    html.Div([
            dcc.Dropdown(
                id='base_time',
                options=[{'label': i,'value': i} for i in base_times.keys()],
                value=list(base_times.keys())[0],
            ),

        ],
        style={'width': '20vh', 
               'display': 'inline-block',
               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                }),
    # Create dropdown menu to choose valid time, and specify with which to start (latest time)        
    html.Div([
            dcc.Dropdown(
                id='valid_time',
                options=[{'label': i,'value': i} for i in valid_times.keys()],
                value=list(valid_times.keys())[0],
            ),

        ],
        style={'width': '20vh', 
               'display': 'inline-block',
               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                }),
    # Create the different figures and specify the sizes    
    html.Br(),
    html.Div([
        dcc.Graph(id='mdc_plot')],
        style={'width':'60vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='basemap_plot')],
        style={'width':'60vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='bar_plot')],
        style={'width':'40vh','display': 'inline-block','margin': {'b': 200, 'r': 10, 'l': 30, 't': 10}}),
    html.Div([
        dcc.Graph(id='mdc_predictand_plot')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    html.Div([
        dcc.Graph(id='predictand_plot')],
        style={'width':'80vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align':'middle'}),
    html.Div([
        dcc.Graph(id='predictor_plot')],
        style={'width':'120vh','display': 'inline-block','margin': {'b': 50, 'r': 10, 'l': 30, 't': 10},'horizontal-align': 'middle'}),    
    

    ])

### Callbacks PAGE-2 ###
@app2.callback(
    dash.dependencies.Output('mdc_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot','clickData'),
     dash.dependencies.Input('plot_type', 'value'),
     dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])
def update_map(clickData,plot_type,region,base_time,valid_time,variable='MDC (from TP)'):
    return create_map(clickData,plot_type,region,base_time,valid_time,list(area_sizes.keys())[0],variable='MDC (from TP)')

@app2.callback(
    dash.dependencies.Output('basemap_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot','clickData'),
     dash.dependencies.Input('plot_type', 'value'),
     dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('variable', 'value')])
def update_map(clickData,plot_type,region,base_time,valid_time,variable):
    return create_map(clickData,plot_type,region,base_time,valid_time,list(area_sizes.keys())[0],variable)

# Update barplot
@app2.callback(
    dash.dependencies.Output('bar_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('plot_type','value'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])
def update_bar_plot(clickData,plot_type,variable,base_time,valid_time):
    return create_bar_plot(clickData,plot_type,variable,base_time,valid_time)
    
# Update predictand timeseries    
@app2.callback(
    dash.dependencies.Output('mdc_predictand_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('variable','value')])
def update_time_series(clickData,base_time,valid_time,variable='MDC (from TP)'):
    return create_time_series(clickData,base_time,valid_time,variable='MDC (from TP)')

@app2.callback(
    dash.dependencies.Output('predictand_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('variable','value')])
def update_time_series(clickData,base_time,valid_time,variable):
    return create_time_series(clickData,base_time,valid_time,variable)


# Update predictor timeseries
@app2.callback(
    dash.dependencies.Output('predictor_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot', 'clickData'),
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])
def update_po_timeseries(clickData,variable,base_time,valid_time):
    return create_po_timeseries(clickData,variable,base_time,valid_time)

