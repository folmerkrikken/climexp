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

from utils import Header_overview as Header

# Where is the data stored?
bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
bdnc = bd+'ncfiles/'


# Create dictionary with available times
timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',concat_dim='time').time.sortby('time').values
months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
dict_times = dict(zip(months12,range(1,13)))

# Create all info needed for the dropdowns
info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary  plot':'tercile','Forecast anomalies':'for_anom'},
        'variables':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_prad':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
        'bdnc':bdnc,
        'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
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

## Set page layout
page_3_layout = html.Div(children=[
    html.Div([Header(app)]),    
    html.Br(),
    html.Div(html.Img(src=app.get_asset_url('workinprogress.jpeg')),style={'textAlign':'center'}),
    ])

