#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
print(sys.path)

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

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

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

# Where is the data stored?

bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
    
#bd = '/home/folmer/KPREP/'
bdnc = bd+'ncfiles/'

#from SPECS_forecast_v5_tools import plot_climexp2

#dt = datetime.date.today()


# Make shortcut to Basemap object, 
# not specifying projection type for this example
m = Basemap() 

monthzz = 'JFMAMJJASONDJFMAMJJASOND'


# Make trace-generating function (return a Scatter object)
def make_scatter(x,y):
    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=go.scatter.Line(color="black"),
        name=' '  # no name on hover
    )

# Functions converting coastline/country polygons to lon/lat traces
def polygons_to_traces(poly_paths, N_poly):
    ''' 
    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    traces = []  # init. plotting list 

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]
        
        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0],vertex[1]) 
             for (vertex,code) in poly_path.iter_segments(simplify=False)]
        )
        
        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
        
        # add plot.ly plotting options
        traces.append(make_scatter(lon_cc,lat_cc))
     
    return traces

# Function generating coastline lon/lat traces
def get_coastline_traces():
    poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
    N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
    return polygons_to_traces(poly_paths, N_poly)

# Function generating country lon/lat traces
def get_country_traces():
    poly_paths = m.drawcountries().get_paths() # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    return polygons_to_traces(poly_paths, N_poly)

# Get list of of coastline and country lon/lat traces
traces_cc = get_coastline_traces()#+get_country_traces()

## Get all plotting infoH<sub>2</sub>O

plot_dict = {'GCEcom':{'Forecast anomalies':{'vmin':-2.,'vmax':2.,'units':'[<sup>o</sup>C]'},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'GPCCcom':{'Forecast anomalies':{'vmin':-50.,'vmax':50.,'units':'[mm]'},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                        ['#993300','#cc8800','#ffcc00','#ffee99','#ffffff','#ccff66','#33ff00','#009933','#006666']
                       },
            '20CRslp':{'Forecast anomalies':{'vmin':-4.,'vmax':4.,'units':'[hPa]'},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                       ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       }
            }


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

anno_text = "Data courtesy of Folmer Krikken"

clickData_start = dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]})


axis_style = dict(
    zeroline=False,
    showline=False,
    showgrid=False,
    ticks='',
    showticklabels=False,
)

## Start app layout

app.layout = html.Div(children=[
    html.H1(children='Sources of predictability - KPREP empirical forecast system'),

    html.Div(children='''
        This app is build using Dash, a web application framework for Python. It is used to study the sources of predictability in the KPREP empirical forecasting system.
    '''),
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
      
## End app layout

## Start plotting functions

    
def create_map(clickData,plot_type,variable,fc_time):
    print(' ')
    print('>>> Starting create_map <<<')
    print(' ')
    if clickData == None: clickData = clickData_start
    predictand = variables[variable]

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    print('lat = ',lat_click,'  lon = ',lon_click)
    print('forecating time = ',fc_time) 
    
    month = np.int(fc_time[5:])
    season = monthzz[month:month+3]
    year = np.int(fc_time[:4])
    
    scores = xr.open_dataset(bdnc+'scores_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc')
    times_m = scores['time.month']
    data_xr = scores[plottypes[plot_type]].values.squeeze()
    #data_xr = scores[plottypes[plot_type]].isel(time=-dict_times[fc_time]).values
    #data = scores[plottypes[plot_type]].sel(times_m == m).values
    #scores_1t = scores.isel(time=-dict_times[fc_time])
    
    if plot_type == 'Forecast anomalies': # Calculate significance of ensemble mean
        print('still to implement')
        #sig = scores.for_anom_sig
        sig = scores.cor_sig.values.squeeze()
    elif plot_type == 'Correlation':
        sig = scores.cor_sig.values.squeeze()
        
    if 'sig' in locals():
       if plot_type == 'Forecast anomalies': 
           #sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
           sigvals = np.where(sig[:,:]<0.05)
           
       else: sigvals = np.where(sig[:,:]<0.05)
       lon2d, lat2d = np.meshgrid(scores.lon.values, scores.lat.values)

    
    titel = u"variable = "+variable+", plot type = "+plot_type+', valid for: '+season+' '+str(year)
    colorz = plot_dict[variables[variable]]['colors']
    
    colorsceel=[ [0, colorz[0]],[0.1, colorz[1]], [0.3, colorz[2]], [0.45, colorz[3]], [0.55, colorz[4]], [0.67, colorz[5]], [0.9, colorz[6]], [1,colorz[7]]]
    
    # Make traces of contour plot, marker where clicked and if possible significant markers
    
    trace_contour = [Contour(z=data_xr,
                                   x=scores.lon.values,
                                   y=scores.lat.values,
                                   zmin=plot_dict[predictand][plot_type]['vmin'],
                                   zmax=plot_dict[predictand][plot_type]['vmax'],
                                   colorscale=colorsceel,
                                   opacity=1.,
                                   colorbar=dict(
                                    title=plot_dict[predictand][plot_type]['units'],
                                    titleside='right',
                                    titlefont=dict(size=18)),
                                   )]

    trace_clickpoint = [Scatter(x=[lon_click]
                         ,y=[lat_click]
                         ,mode='markers'
                         ,marker=dict(size=10,color='black',line=dict(width=2)))]
    
    
    
    if 'sig' in locals():
        trace_sig = [Scatter(x=lon2d[sigvals],
                            y=lat2d[sigvals],
                            mode='markers',
                            marker=dict(size=1,color='black'),
                            )]
        traces = traces_cc + trace_contour + trace_sig + trace_clickpoint
    else:
        traces = traces_cc + trace_contour + trace_clickpoint    

    print(variable,plot_type,lon_click,lat_click)

    return( 
            go.Figure(
            data=traces,
            layout = Layout(
                title=titel,
                showlegend=False,
                #clickmode="event",
                #autorange=False,
                hovermode='closest',        # highlight closest point on hover
                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=10,
                    t=70,
                    pad=4
                    ),
                xaxis=go.layout.XAxis(
                    axis_style,
                       range=[-180,180]
                ),
                yaxis=go.layout.YAxis(
                    axis_style,
                ),
                autosize=False,
                width=1000,
                height=500,)
            ))      
   
   
def create_time_series(clickData,variable,fc_time):
    print(' ')
    print('>>> Starting create_time_series <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
          
    month = np.int(fc_time[5:])
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    predictand = variables[variable]

    tt = dict_times[fc_time]
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc')
    # Select right location and time slice
    #pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=slice(None,-tt))
    pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).sel(time=(pred['time.month']==np.int(fc_time[5:])))
    
    time_pd = pred1d.time.to_pandas()
    kprep_mean = pred1d['kprep'].mean(dim='ens').values
    print('last value of forecast ensemble mean: ',kprep_mean[-1])
    kprep_std = pred1d['kprep'].std(dim='ens').values * 2.
    clim_mean = pred1d['clim'].mean(dim='ens').values
    clim_std = pred1d['clim'].std(dim='ens').values * 2.
    trend = pred1d['trend'].mean(dim='ens').values
    
    obs_nc = xr.open_dataset(bdnc+'predadata_v2_'+predictand+'.nc')
    obs1d = obs_nc.to_array().sel(lat=lat_click,lon=lon_click,method='nearest').sel(time=(obs_nc['time.month']==month)).load()
    time_pd_long = obs1d.time.to_pandas()
    #print(time_pd)
    #print(len(time_pd))
    return(
        go.Figure(
        data=
            [go.Scatter(x=time_pd,y=kprep_mean+kprep_std,mode='lines',fillcolor='rgba(0,100,80,0.2)',line=Line(color='rgba(0,100,80,0.2)'),opacity=0.9,showlegend=False)]
            +
            [go.Scatter(x=time_pd,y=kprep_mean-kprep_std,mode='lines',fill='tonexty',fillcolor='rgba(0,100,80,0.2)',line=Line(color='rgba(0,100,80,0.2)'),opacity=0.9,name='For. spread (2'+u"\u03C3"+')')]
            +
            [go.Scatter(x=time_pd,y=kprep_mean,mode='lines',name='Forecast',line=dict(color='blue',width=4))]
            +
            [go.Scatter(x=time_pd_long,y=obs1d.values.squeeze(),mode='lines',name='Observations',line=dict(color='black'))]
            +[go.Scatter(x=time_pd,y=clim_mean,mode='lines',name='Climatology',line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=trend,mode='lines',name='Trend CO2',line=dict(color='red'))]
            #+[go.Scatter(x=time_pd,y=pred1d['obs'].values,mode='lines',name='Observations',line=dict(color='black'))]
            ,
            #),

        layout = Layout(
            title = 'Time series of the forecast, forecast only on CO2, climatology and observations (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            #height =  225,
            #margin = {'l': 20, 'b': 30, 'r': 10, 't': 10},
            autosize=False,
            width=1000.,
            height=400.,
            xaxis=dict(
                rangeselector=dict(
                buttons=list([
                dict(count=len(time_pd_long),
                     label='1901-current',
                     step='year',
                     stepmode='backward'),
                dict(count=len(time_pd),
                     label='1961-current',
                     step='year',
                     stepmode='backward'),
                #dict(step='all')
                ]),
            ),
            rangeslider=dict(),
            type='date'
            ),
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),     
            )
        ))   
      
def create_bar_plot(clickData,plot_type,variable,fc_time):
    print(' ')
    print('>>> Starting create_bar_plot <<<')
    print(' ')
    
    predictand = variables[variable]
    if clickData == None: clickData = clickData_start

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']        
        
    month = np.int(fc_time[5:])

    # Load data
    pred_1d = xr.open_dataset(bdnc+'pred_v2_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    #for_anom = pred_1d['kprep'].mean(dim='ens')
    for_anom = pred_1d['kprep'].isel(ens=0)
    #co2_anom = pred_1d['trend'].mean(dim='ens')
    co2_anom = pred_1d['trend'].isel(ens=0)
    beta_1d = xr.open_dataset(bdnc+'beta_v2_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predo_1d = xr.open_dataset(bdnc+'predodata_3m_fit_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predos = list(predo_1d.data_vars)
    sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    traces=[]
    fig = tls.make_subplots(rows=1,cols=1)
    if nr_sigp == 0:
        print('no significant predictors..')
        return()
    
    else:
        print('barplot - nr of significant predictors is ',nr_sigp)
        print(np.asarray(predos))
        print(sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        print(predo_1d.to_array(dim='predictors').values*beta_1d.beta.values)
        print(sigp)
        print('anomaly forecast is: ',for_anom.values)
        print(predo_1d.to_array(dim='predictors').values)
        print(beta_1d.beta.values)
        vals = np.asarray(np.append((predo_1d.to_array(dim='predictors').values*beta_1d.beta.values)[sigp],for_anom.values))
        
        if 'CO2EQ' in np.asarray(predos)[sigp]: # add CO2 to first value of predictors
                vals[0]=co2_anom  
        # Check if sum of predictors matches the forecasted anomalie
        dif = for_anom.values-np.sum(vals[:-1])
        if abs(dif) > 0.001: # Difference too big, why?
            vals = np.append(vals,dif)   
            trace = Bar(
                x=np.append(np.asarray(predos)[sigp],np.asarray(['Total','dif'])),
                y=vals
                )
        else:
            trace = Bar(
                x=np.append(np.asarray(predos)[sigp],np.asarray(['Total'])),
                y=vals
                )
        
        layout = go.Layout(
            height=500,
            width=500.,
            autosize=False,
            title='Individual contribution predictors (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),
            )
   
        #fig = go.Figure(data=Data([trace]), layout=layout)
        fig = go.Figure(data=[trace], layout=layout)     
        return(fig)
        
def create_po_timeseries(clickData,variable,fc_time):
    print(' ')
    print('>>> Starting create_po_timeseries <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
    
    month = np.int(fc_time[5:])

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']   
    
       
    tt = dict_times[fc_time]
    mo = np.int(fc_time[5:])
    
    # Load monthly data for predictions
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc')#.sel(lon=lon_click,lat=lat_click,method=str('nearest'))
    pred_1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=(pred['time.month']==mo))
    for_anom = pred_1d['kprep'].mean(dim='ens').isel(time=-1).values
    co2_anom = pred_1d['trend'].mean(dim='ens').isel(time=-1).values
    beta_1d = xr.open_dataset(bdnc+'beta_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    # Load predictor data (fitted)
    predo = xr.open_dataset(bdnc+'predodata_3m_fit_'+variables[variable]+'_'+str(month).zfill(2)+'.nc')
    predo_1d = predo.sel(time=(predo['time.month']==mo),lon=lon_click,lat=lat_click,method='nearest')
    predos = list(predo_1d.data_vars)
    
    sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    time_pd = predo_1d.time.to_pandas()
    traces=[]
    xaxs = ['x1','x2','x3','x4','x5','x6','x7','x8']
    yaxs = ['y1','y2','y3','y4','y5','y6','y7','y8']
    if nr_sigp == 0:
        print('no significant predictors..')
        return()
    else:
        print('timeseries plot - nr of significant predictors is ',nr_sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        for ii in range(nr_sigp):
            traces.append(go.Scatter(
                x=time_pd,
                y=predo_1d[np.asarray(predos)[sigp][ii]].values,
                xaxis=xaxs[ii],
                yaxis=yaxs[ii],
                text=np.asarray(predos)[sigp][ii],
                textposition='top center',
                name=np.asarray(predos)[sigp][ii]
                ))
                
    
        fig = tls.make_subplots(rows=np.int(nr_sigp),cols=1)
        for ii in range(nr_sigp):
            fig.append_trace(traces[ii],ii+1,1)
        fig['layout'].update(   height=600,
                                width=1000.,
                                autosize=False,
                                title='Time series of (fitted) predictor data (lat='+str(lat_click)+', lon='+str(lon_click)+')',
                            )
        
        return(fig)
    
## End plotting functions

## Start callbacks

# Update predictand map      
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





#if __name__ == '__main__':
#    app.run_server(debug=True)
    
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)#,host='0.0.0.0')#,port=80)    
