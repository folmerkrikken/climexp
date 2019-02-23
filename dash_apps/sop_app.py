#!/usr/bin/python
# -*- coding: utf-8 -*-


import pandas as pd
import xarray as xr
import numpy as np           
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
if not os.path.isfile(bd):
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




#tmp_nc = xr.open_dataset(bdnc+'predadata_v2_GCEcom.nc')
timez = xr.open_mfdataset(bdnc+'scores*.nc',concat_dim='time').time.sortby('time').values
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

clickData_start = dict({u'points': [{u'y': 0., u'x': 0., u'pointNumber': 6, u'curveNumber': 632}]})


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
        Dash: A web application framework for Python.
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

# Predefine clickdata, otherwise no figures besides the map

    
def create_map(clickData,plot_type,variable,fc_time):
    print(' ')
    print('>>> Starting create_map <<<')
    print(' ')
    if clickData == None: clickData = clickData_start

        
    print(clickData)
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
    print(data_xr.shape)
    print(np.nanmax(data_xr))
    print(np.nanmin(data_xr))
    #data_xr = scores[plottypes[plot_type]].isel(time=-dict_times[fc_time]).values
    #data = scores[plottypes[plot_type]].sel(times_m == m).values
    #scores_1t = scores.isel(time=-dict_times[fc_time])
    titel = u"variable = "+variable+", plot type = "+plot_type+', valid for: '+season+' '+str(year)
    colorsceel=[ [0, '#000099'],[0.2, '#3355ff'], [0.35, '#66aaff'], [0.45, '#77ffff'], [0.55, '#ffffff'], [0.65, '#ffff33'], [0.8, '#ff4400'], [1,'#cc0022']]
    colorsceel=[ [0, '#000099'],[0.1, '#3355ff'], [0.3, '#66aaff'], [0.45, '#77ffff'], [0.55, '#ffffff'], [0.67, '#ffff33'], [0.9, '#ff4400'], [1,'#cc0022']]
    
    #,colorscale=colorsceel,contours=dict(start=-maxval,end=maxval),
    #fig = go.Contour(
    maxval = np.nanmax(np.abs(data_xr))
    print('maxval',maxval)
    print(variable,plot_type)
    maxval = 2.
    #if plot_type is 'correlation':
    #    zmin=np.nanmin(data_xr)
    #    zmax=1.
    #if plot_type is 
    
    #plottypes={'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'}
    #variables={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}

    
    #maxval = 10.
    return( 
            #go.contour(z=data_xr,x=scores.lon.values,y=scores.lat.values,contours=dict(start=-2,end=2))autocolorscale=False,zauto=False,
            go.Figure(
            data=
                #Data(traces_cc+[Contour(z=data_xr,x=scores.lon.values,y=scores.lat.values,zmin=-maxval,zmax=maxval,colorscale=colorsceel,opacity=1.)]),#+traces_cc),
                traces_cc+[Contour(z=data_xr,x=scores.lon.values,y=scores.lat.values,zmin=-maxval,zmax=maxval,colorscale=colorsceel,opacity=1.)],
            layout = Layout(
                title=titel,
                showlegend=False,
                #clickmode="event",
                #autorange=False,
                hovermode='closest',        # highlight closest point on hover
                #colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']],
                #colorscale=colorsceel,
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
                #annotations=go.Annotations([
                    #Annotation(
                        #text=anno_text,
                        #xref='paper',
                        #yref='paper',
                        #x=0,
                        #y=1,
                        #yanchor='bottom',
                        #showarrow=False
                    #)
                #]),

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
    
    
    return(
        go.Figure(
        data=#Data(
            #[Scatter(x=time_pd,y=kprep_mean+kprep_std,mode='lines',fillcolor='rgba(0,100,80,0.2)',line=Line(color='gray'))]+
            #[Scatter(x=time_pd,y=kprep_mean-kprep_std,mode='lines',fill='tonexty',fillcolor='rgba(0,100,80,0.2)',line=Line(color='gray'))]+
            [go.Scatter(x=time_pd,y=kprep_mean,mode='lines',name='Forecast',line=dict(color='blue'))]
            +[go.Scatter(x=time_pd,y=clim_mean,mode='lines',name='Climatology',line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=trend,mode='lines',name='Trend CO2',line=dict(color='red'))]
            +[go.Scatter(x=time_pd,y=pred1d['obs'].values,mode='lines',name='Observations',line=dict(color='black'))],
            #),
        layout = Layout(
            title = 'Time series of the forecast, climatology and observations',
            #height =  225,
            margin = {'l': 20, 'b': 30, 'r': 10, 't': 10},
            autosize=False,
            width=1000.,
            height=400.,
            xaxis=dict(
                rangeselector=dict(
                buttons=list([
                dict(count=1,
                     label='12m',
                     step='year',
                     stepmode='backward'),
                dict(count=6,
                     label='120m',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
            )
            )
        ))   
      
def create_bar_plot(clickData,variable,fc_time):
    print(' ')
    print('>>> Starting create_bar_plot <<<')
    print(' ')
    

    if clickData == None: clickData = clickData_start

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']        
        
    month = np.int(fc_time[5:])

    # Load data
    pred_1d = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    #for_anom = pred_1d['kprep'].mean(dim='ens')
    for_anom = pred_1d['kprep'].isel(ens=0)
    #co2_anom = pred_1d['trend'].mean(dim='ens')
    co2_anom = pred_1d['trend'].isel(ens=0)
    beta_1d = xr.open_dataset(bdnc+'beta_v2_'+variables[variable]+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predo_1d = xr.open_dataset(bdnc+'predodata_3m_fit_'+variables[variable]+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predos = list(predo_1d.data_vars)
    sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    traces=[]
    fig = tls.make_subplots(rows=1,cols=1)
    if nr_sigp == 0:
        print('no significant predictors..')
    else:
        print('barplot - nr of significant predictors is ',nr_sigp)
        print(np.asarray(predos))
        print(sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        print(predo_1d.to_array(dim='predictors').values*beta_1d.beta.values)
        print(sigp)
        vals = np.asarray(np.append((predo_1d.to_array(dim='predictors').values*beta_1d.beta.values)[sigp],for_anom))
        
        if 'CO2EQ' in np.asarray(predos)[sigp]:
                vals[0]=co2_anom  
        dif = for_anom-np.sum(vals[:-1])
        vals = np.append(vals,dif)   
        trace = Bar(
                x=np.append(np.asarray(predos)[sigp],np.asarray(['Total','dif'])),
                y=vals
                )
        layout = go.Layout(
            height=500,
            width=500.,
            autosize=False,
            title='Individual contribution predictors (lat='+str(lat_click)+', lon='+str(lon_click)+')',
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
                            title='Time series of (fitted) predictor data',
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
     dash.dependencies.Input('variable','value'),
     dash.dependencies.Input('fc_time','value')])
def update_bar_plot(clickData,variable,fc_time):
    return create_bar_plot(clickData,variable,fc_time)
    
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
