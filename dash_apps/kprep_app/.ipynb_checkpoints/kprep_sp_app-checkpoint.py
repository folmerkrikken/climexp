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

from dash.dependencies import Input,Output

import dash
import dash_core_components as dcc
import dash_html_components as html
from utils import Header_pp as Header

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary  plot':'tercile','Forecast anomalies':'for_anom'},
        'variables':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_prad':{'Temperature':'GCEcom','Precipitation':'PRECIP','Sea-level pressure':'20CRslp'},
        'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
        'bdnc':bdnc,
        'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
        }

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
#    html.Link(rel='stylesheet', href=css_link),
    #html.Script(type='text/javascript', src=js_link),
])
## Set page layout

page_1_layout = html.Div(children=[
    html.Div([Header(app)]),    
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
                "Individual contribution predicotrs",
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


page_2_layout = html.Div(children=[
    html.Div([Header(app)]),    
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
                "Predictor plot 1",
                className="subtitle padded",
            ),
            #html.H6('By clicking on the map you can further specify the region of interest'),
            dcc.Graph(id='basemap_plot1')],
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
                "Local scatter plot",
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
        html.Div([
            html.H6(
                "Local forecast",
                className="subtitle padded",
            ),        
            dcc.Graph(id='basemap_plot2')],
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



# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/kprep_fc/kprep_sop":
        return page_1_layout
    elif pathname == "/kprep_fc/kprep_pp":
        return page_2_layout
    elif pathname == "/kprep_fc/kprep_overview":
        return page_3_layout
    else:
        return page_1_layout



# Dash CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(ssl_context='adhoc',debug=True,threaded=True)#,host='0.0.0.0')#,port=80)    
