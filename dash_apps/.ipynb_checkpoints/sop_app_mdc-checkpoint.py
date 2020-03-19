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

from utils import Header

print(dcc.__version__) # 0.6.0 or above is required
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

#app2= dash.Dash(__name__, external_stylesheets=external_stylesheets)


#app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)


ONLINE=False
if ONLINE:
    # Online modus
    app2 = dash.Dash(requests_pathname_prefix='/myapp2/',external_stylesheets=external_stylesheets)
    #app2 = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
    #print(app2.config.routes_pathname_prefix)
    #app2.config.requests_pathname_prefix = app2.config.routes_pathname_prefix.split('/')[-1]
    app2.css.config.serve_locally = True
    app2.scripts.config.serve_locally = True
    server = app2.server
    bd2 = '/myapp2'
else:
    # Offline modus
    app2 = dash.Dash(external_stylesheets=external_stylesheets)
    app2.css.config.serve_locally = True
    app2.scripts.config.serve_locally = True
    bd2 = ''

print('High!!',app2.config.routes_pathname_prefix.split('/')[-1])

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

app2.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to the Monthly Drought Code forecasts', href=bd2+'/kprep-mdc-enduser'),
    html.Br(),
    dcc.Link('Go to the KPREP sources of predictabily app '+bd2, href=bd2+'/kprep-mdc-sop'),
    html.Br(),
    dcc.Link('Go to the KRPEP predictor-predictand relations app '+bd2, href=bd2+'/kprep-mdc-pp'),
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

style_box = {'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': '#DCDCDC',# '#f9f9f9',
                                 'padding': '10px',
                                 'margin-bottom': '10px',
                                 'margin-left': '10px',
                                 'textAlign':'center',
            }

page_1_layout = html.Div(children=[


    #html.Div(children='- By clicking on the map you can further specify the region of interest. The square denotes the region on which the subsequent figures are based on'),
#    html.Br(),
#    dcc.Link('Click here to examine the sources of predictability', href=bd2+'/kprep-mdc-sop'),
#    html.Br(),
#    dcc.Link('Click here to examine predictor-predictand relations', href=bd2+'/kprep-mdc-pp'),
    html.Div([Header(app2)]),    
    html.Br(),

    # 
    html.Div(
        [
        html.Div(
            [

                html.Div(
                    [
                    #html.Div([
                        #html.Div(children='Select region  ',style={'width':'15%','display':'inline-block'}),
                        #html.Abbr("  \u003F ",title='Select your region of interest',style={'display':'inline-block'}),
                        #],
                        #style={'width': '2%', 'display': 'inline-block'}),
                        
                    #html.Abbr(" \u003F ",title='Select the forecast variable:'),    
                    #html.Div(children='Select forecasted variable',style={'width': '19vh', 'display': 'inline-block'}),
                    #html.Abbr(" \u003F ",title='Select the plot type'),     
                    #html.Div(children='Select plot type',style={'width': '19vh', 'display': 'inline-block'}),
                    #html.Abbr(" \u003F ",title='Select the month when the forecast is started from. Preferably, choose the latest month available for the most accurate forecast'),     
                    #html.Div(children='Select forecast base time',style={'width': '19vh', 'display': 'inline-block'}),
                    #html.Abbr(" \u003F ",title='Select the month for which you want the information. The data is plotted in Figure 1'), 
                    #html.Div(children='Select forecast valid time',style={'width': '19vh', 'display': 'inline-block'}),
                    #html.Abbr(" \u003F ",title='Select the area size, the data shown in figure 2 is the area averaged data over this area'),     
                    #html.Div(children='Select area size',style={'width': '19vh', 'display': 'inline-block'}),
                    #html.Br(),
                             #Select forecasted variable        Select plottype  Select forecast base time   Select valid forecast time'),
                    # Create dropdown menu to choose region
                    html.Div([
                            html.Label('Select region',title='Select you region of interest'),
                            dcc.Dropdown(
                                id='region',
                                options=[{'label': i,'value': i} for i in regions.keys()],
                                value='Northern hemisphere',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),
                    # Create dropdown menu to choose variable, and specify with which to start

                    html.Div([
                            html.Label('Select variable',title='Select the variable you are interested in'),
                            dcc.Dropdown(
                                id='variable',
                                options=[{'label': i,'value': i} for i in variables.keys()],
                                value='Monthly Drought Index',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),
                    # Create dropdown menu to choose plot type, and specify with which to start
                    html.Div([
                            html.Label('Select plot type',title='Select the plot type'),
                            dcc.Dropdown(
                                id='plot_type',
                                options=[{'label': i,'value': i} for i in plottypes.keys()],
                                value='Forecast anomalies',
                            ),

                        ],
                        style={'width': '20vh', 'display': 'inline-block'}),

                    # Create dropdown menu to choose base time, and specify with which to start (latest time)
                    html.Div([
                            html.Label('Select forecast base time',title='Select the month when the forecast is started from. Preferably, choose the latest month available for the most accurate forecast'),
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
                            html.Label('Select forecast valid time',title='Select the month for which you want the information. The data is plotted in Figure 1'),
                            dcc.Dropdown(
                                id='valid_time',
                                #options=[{'label': i,'value': i} for i in valid_times.keys()],
                                #value=list(valid_times.keys())[0],
                            ),
                        ],
                        style={'width': '20vh', 
                               'display': 'inline-block',
                               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                                }),
                    # Create dropdown menu to choose area size       
                    html.Div([
                            html.Label('Select area size',title='Select the area size, the data shown in figure 2 is the area averaged data over this area'),
                            dcc.Dropdown(
                                id='area_size',
                                options=[{'label': i,'value': i} for i in area_sizes.keys()],
                                value=list(area_sizes.keys())[0],
                            ),
                        ],
                        style={'width': '20vh', 
                               'display': 'inline-block',
                               'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
                                }),
                    html.Br(),                        
                    html.Div(
                        [
                        dcc.Checklist(
                            id='my-input',
                            options=[
                                {'label':'Study the relation between the observed burned area, the observed MDC and the forecasted MDC?','value':'plotcor'}],
                            value=[],
                            ),
                        ],   
                        style={'textAlign':'center','fontsize':'16'},
                        ),                        
                    ],
                    className='app-dropdown',
                    #style={'width': '75%', 'display': 'inline-block',
                    #                           'border-bottom': 'thin lightgrey solid',
                                             #'border-radius': '15px',
                                             #'box-shadow': '8px 8px 8px grey',
                                             #'background-color': '#f9f9f9',
                                             #'padding': '10px',
                                             #'margin-bottom': '10px',
                                             #'margin-left': '10px',
                                             #'textAlign':'center',
                     #   }
                    #style='app-header'
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
            dcc.Graph(id='mdc_plot_enduser')],
            #style={'width':'65vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '40%', 'display': 'inline-block',
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
                "Local forecast",
                className="subtitle padded",
            ),        
            dcc.Graph(id='mdc_time_series')],
            #style={'width':'100vh','display': 'inline-block','margin': {'b': 10, 'r': 10, 'l': 10, 't': 10}}),
            style= {'width': '55%', 'display': 'inline-block',
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
    html.Br(),
#     html.Div(
#         [
#         dcc.Checklist(
#             id='my-input',
#             options=[
#                 {'label':'Study the relation between the observed burned area, the observed MDC and the forecasted MDC?','value':'plotcor'}],
#             value=[],
#             style={'width': '40%', 'display': 'inline-block',
#                                              'border-radius': '15px',
#                                              'box-shadow': '8px 8px 8px grey',
#                                              'background-color': '#f9f9f9',
#                                              'padding': '10px',
#                                              'margin-bottom': '10px',
#                                              'margin-left': '10px',
#                                              'textAlign':'center'},
#             ),
#         ],   
#         style={'textAlign':'center'},
#         ),
    
#     dcc.Dropdown(
#         id="my-input",
#         options = [
#             {'label':'Yes', 'value':1},
#             {'label':'No', 'value':0}
#         ],
#         value = 1,
#         style={'width': '20vh', 
#                'display': 'inline-block',
#                'margin': {'b': 50, 'r': 10, 'l': 30, 't': 10}
#                 },
#     ),
#     html.Label("Study the relation between the observed burned area, the observed MDC and the forecasted MDC?"),
    html.Br(),
    html.Div(id='burned_area_plots',children=[
        html.Div([
            html.H6(
                "Time series of Burned Area, forecasted and observed MDC",
                className="subtitle padded",
            ),
            dcc.Graph(id='mdc_obs_fires')],
        style={'width': '47%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '20px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'height':'300px',               
                                             'textAlign':'center'}),
   
        html.Div([
            html.H6(
                "Correlation of Burned Area with forecasted and observed MDC",
                className="subtitle padded",
            ),            
            dcc.Graph(id='mdc_cor_fires')],
        style={'width': '46%', 'display': 'inline-block',
                                             'border-radius': '5px',
                                             'box-shadow': '4px 4px 4px grey',
                                             'background-color': '#f9f9f9',
                                             'padding': '20px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             #'height':'300px',
                                             'textAlign':'center'}),

        
        ],style={'width': '95%', 'display': 'inline-block',
                                             'border-radius': '15px',
                                             'box-shadow': '8px 8px 8px grey',
                                             'background-color': '#DCDCDC',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             'textAlign':'center'}),
    ])


page_2_layout = html.Div(children=[
    html.H1(children='Sources of predictability - KPREP empirical forecast system - Monthly Drought Code'),

    html.Div(children='''
        This app is constructed using Dash, a web application framework for Python. Any questions, suggestion or comments mail folmer.krikken@knmi.nl
    '''),
    #html.ObjectEl(type="text/html",name='../myvinkhead.cgi'),
    html.Br(),
    html.Div(children='This website can be used to study the sources of predictability in the KPREP empirical forecasting system. The dropdown menu allow to change the predictand, plot type and forecasting time.'),
    html.Div(children='By clicking on the map the barplot gives the contribution of the predictors to the forecasted anomalie, and the line plots give more information on the forecasts and predictors over time'),
    html.Br(),
    dcc.Link('Click here to examine the forecasting page', href=bd2+'/kprep-mdc-enduser'),
    html.Br(),
    dcc.Link('Click here to examine predictor-predictand relations', href=bd2+'/kprep-mdc-pp'),
    html.Br(),
    html.Br(),
    html.Br(),    
    html.Div(children='Select region',style={'width': '20vh', 'display': 'inline-block'}),
    html.Div(children='Select forecasted variable',style={'width': '20vh', 'display': 'inline-block'}),
    html.Div(children='Select plot type',style={'width': '20vh', 'display': 'inline-block'}),
    html.Div(children='Select forecast base time',style={'width': '20vh', 'display': 'inline-block'}),
    html.Div(children='Select forecast valid time',style={'width': '20vh', 'display': 'inline-block'}),
    html.Br(),
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

page_3_layout = html.Div(children=[
    html.H1(children='Sources of predictability - KPREP empirical forecast system'),

    html.Div(children='''
        Dash: A web app2lication framework for Python.
    '''),
    html.Br(),
    dcc.Link('Click here to go back to predictand info', href=bd2+'/kprep-sop'),
    html.Br(),
    html.Br(),
    # Create dropdown menu to choose predictand variable
    html.Div([
            dcc.Dropdown(
                id='region',
                options=[{'label': i,'value': i} for i in regions.keys()],
                value='Northern hemisphere',
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),
    # Create dropdown menu to choose predictand variable, and specify with which to start
    
    html.Div([
            dcc.Dropdown(
                id='predictand',
                options=[{'label': i,'value': i} for i in variables.keys()],
                value='Monthly Drought Index',
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
            
    # Create dropdown menu to choose base time, and specify with which to start (latest time)
    html.Div([
            dcc.Dropdown(
                id='base_time',
                options=[{'label': i,'value': i} for i in base_times.keys()],
                value=list(base_times.keys())[0],
            ),

        ],
        style={'width': '20%', 
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
        style={'width': '20%', 
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
                    
    
#options=[{'label': i,'value': i} for i in valid_times.keys()],
#value=list(valid_times.keys())[0]

#@app2.callback(dash.dependencies.Output('graph-container', 'style'), [dash.dependencies.Input('my-input', 'value')])
# @app2.callback(dash.dependencies.Output('mdc_obs_fires', 'style'), [dash.dependencies.Input('my-input', 'value')])
# def hide_graph(my_input):
#     print('my_input',my_input)
#     if my_input == ['plotcor']:
#         return {'display':'block'}
#     return {'display':'none'}

# @app2.callback(dash.dependencies.Output('mdc_cor_fires', 'style'), [dash.dependencies.Input('my-input', 'value')])
# def hide_graph(my_input):
#     if my_input == ['plotcor']:
#         print('returning block!')
#         return {'display':'block'}
#     return {'display':'none'}

# @app2.callback(dash.dependencies.Output('mdc_cor_fires', 'style'), [dash.dependencies.Input('my-input', 'value')])
# def hide_graph(my_input):
#     if my_input == ['plotcor']:
#         print('returning block!')
#         return {'display':'block'}
#     return {'display':'none'}
@app2.callback(dash.dependencies.Output('burned_area_plots', 'style'), [dash.dependencies.Input('my-input', 'value')])
def hide_graph(my_input):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',my_input)
    if not my_input == ['plotcor']:
        return {'display': 'none'}
    else:
        return {'width': '95%', 'display': 'inline-block',
                                             'border-radius': '15px',
                                             'box-shadow': '8px 8px 8px grey',
                                             'background-color': '#DCDCDC',
                                             'padding': '10px',
                                             'margin-bottom': '10px',
                                             'margin-left': '10px',
                                             'textAlign':'center'}

### Callbacks PAGE-1 ###
# Two callback in order to make the valid_time dependent on base_time (i.e., if May selected as base time
# then June, July etc are selected as valid times
@app2.callback(
    dash.dependencies.Output('valid_time', 'options'),
    [dash.dependencies.Input('base_time', 'value')])
def set_cities_options(base_time):
    tmp_options = dict([(i,base_times[i]) for i in list(base_times)[list(base_times).index(base_time)+1:]])
    return [{'label': i,'value': i} for i in tmp_options.keys()]
    
@app2.callback(
    dash.dependencies.Output('valid_time', 'value'),
    [dash.dependencies.Input('valid_time', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app2.callback(
    dash.dependencies.Output('mdc_plot_enduser', 'figure'),
    [dash.dependencies.Input('mdc_plot_enduser','clickData'),
     dash.dependencies.Input('plot_type', 'value'),
     dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('area_size','value'),
     dash.dependencies.Input('variable','value')])
def update_map(clickData,plot_type,region,base_time,valid_time,area_size,variable):
    return create_map_enduser(clickData,plot_type,region,base_time,valid_time,area_size,variable) 

@app2.callback(
    dash.dependencies.Output('mdc_time_series', 'figure'),
    [dash.dependencies.Input('mdc_plot_enduser', 'clickData'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('area_size','value'),
     dash.dependencies.Input('variable','value')])
def update_time_series(clickData,base_time,valid_time,area_size,variable):
    return create_mdc_time_series(clickData,base_time,valid_time,area_size,variable)

@app2.callback(
    dash.dependencies.Output('mdc_obs_fires', 'figure'),
    [dash.dependencies.Input('mdc_plot_enduser', 'clickData'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('area_size','value'),
     dash.dependencies.Input('variable','value')])
def update_obs_fires(clickData,base_time,valid_time,area_size,variable):
    return create_obs_fires(clickData,base_time,valid_time,area_size,variable)

@app2.callback(
    dash.dependencies.Output('mdc_cor_fires', 'figure'),
    [dash.dependencies.Input('mdc_plot_enduser', 'clickData'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value'),
     dash.dependencies.Input('area_size','value'),
     dash.dependencies.Input('variable','value')])
def update_cor_fires(clickData,base_time,valid_time,area_size,variable):
    return create_cor_fires(clickData,base_time,valid_time,area_size,variable)


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

### Callbacks PAGE-3 ###
# Update corplot map orig vs predictand
@app2.callback(
    dash.dependencies.Output('basemap_plot1', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])    
def update_map(clickData,predictand,predictor,region,base_time,valid_time):
    return create_map1(clickData,predictand,predictor,region,base_time,valid_time)

# Update corplot map fitted predictors vs predictand
@app2.callback(
    dash.dependencies.Output('basemap_plot2', 'figure'),
    [dash.dependencies.Input('basemap_plot1','clickData'),
     dash.dependencies.Input('predictand', 'value'),
     dash.dependencies.Input('predictor', 'value'),
     dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])      
def update_map(clickData,predictand,predictor,region,base_time,valid_time):
    return create_map2(clickData,predictand,predictor,region,base_time,valid_time)

   
# Update xyplot                    
@app2.callback(
    dash.dependencies.Output('xy_plot', 'figure'),
    [dash.dependencies.Input('basemap_plot1', 'clickData'),
     dash.dependencies.Input('predictand','value'),
     dash.dependencies.Input('predictor','value'),
     dash.dependencies.Input('base_time', 'value'),
     dash.dependencies.Input('valid_time','value')])
def update_time_series(clickData,predictand,predictor,base_time,valid_time):
    return create_xyplot(clickData,predictand,predictor,base_time,valid_time)





#@app2.callback(dash.dependencies.Output('page-1-content', 'children'),
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

#@app2.callback(dash.dependencies.Output('page-2-content', 'children'),
              #[dash.dependencies.Input('page-2-radios', 'value')])
#def page_2_radios(value):
    #return 'You have selected "{}"'.format(value)


# Update the index
@app2.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print('pathname is: ',pathname)
    if pathname == bd2+'/kprep-mdc-enduser':
        return page_1_layout
    elif pathname == bd2+'/kprep-mdc-sop':
        return page_2_layout
    elif pathname == bd2+'/kprep-mdc-pp':
        return page_3_layout
    else:
        return page_1_layout
    # You could also return a 404 "URL not found" page here

#if __name__ == '__main__':
    #app2.run_server(debug=True)
if __name__ == '__main__': 
    app2.run_server(debug=True,threaded=True)#,host='0.0.0.0')#,port=80)    
