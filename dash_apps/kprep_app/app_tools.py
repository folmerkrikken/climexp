import pandas as pd
import xarray as xr
import numpy as np    
import scipy.stats
import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.6/site-packages')
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import plotly.express as px

#import plotly.plotly as py
import chart_studio.plotly as py
#from plotly.graph_objs import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.tools as tls
import datetime
from utils import info_titles
import calendar
#print(bdnc)
global bdnc

bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
    
#bd = '/home/folmer/KPREP/'
#bdnc = bd+'ncfiles/'
#global bdnc
#variables_prad={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}
#variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'}

# Make shortcut to Basemap object, 
# not specifying projection type for this example
m = Basemap() 

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
monthzz = 'JFMAMJJASONDJFMAMJJASOND'

plot_dict = {'GCEcom':{'Forecast anomalies':{'vmin':-2.,'vmax':2.,'units':'[<sup>o</sup>C]',
                                 'fr':[0.0,0.01,0.25,0.375,0.46,0.54,0.625,0.75,0.99,1.0],
                                 'tv':[-2,-1,-0.5,-0.2,0.2,0.5,1.0,2.0]},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-',},
                       'CRPSS (clim)':{'vmin':-0.5,'vmax':0.5,'units':'-',},
                       'CRPSS (S5)':{'vmin':-0.5,'vmax':0.5,'units':'-',},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'GPCCcom':{'Forecast anomalies':{'vmin':-50.,'vmax':50.,'units':'[mm]',
                                'fr':[0.0,0.01,0.25,0.4,0.45,0.55,0.6,0.75,0.99,1.0],
                                'tv':[-50,-25,-10.,-5.,5,10,25,50]},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS (clim)':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS (S5)':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                        ['#993300','#cc8800','#ffcc00','#ffee99','#ffffff','#ccff66','#33ff00','#009933','#006666']
                       },
            '20CRslp':{'Forecast anomalies':{'vmin':-4.,'vmax':4.,'units':'[hPa]',
                                'fr':[0.0,0.01,0.25,0.375,0.45,0.55,0.625,0.75,0.99,1.0],
                                'tv':[-4,-2,-1,-0.5,0.5,1,2,4]},
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS (clim)':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS (S5)':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                       ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'RMSESS':{'fr':[0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0],'tv':[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]},
            'CRPSS (clim)': {'fr':[0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0],'tv':[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]},
            'CRPSS (S5)': {'fr':[0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0],'tv':[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]},
            'Tercile summary plot':{'fr':[0.0,0.15,0.2,0.25,0.3,0.7,0.75,0.8,0.85,1.0],'tv':[-100,-70,-60,-50,-40,40,50,60,70,100]},
            'Correlation':{'fr':[0.0,0.1,0.2,0.3,0.4,0.6,0.7,0.8,0.9,1.0],'tv':[-1,-0.8,-0.6,-0.4,-0.2,0.2,0.4,0.6,0.8,1.0]},
            }

hbd_test = '/home/folmer/kprep_test/'
hbd_ref = '/home/folmer/climexp_data/KPREPData/'
#bd = '/home/folmer/KPREP/'
bdnc = bd+'ncfiles/'


axis_style = dict(
    zeroline=False,
    showline=False,
    showgrid=False,
    ticks='',
    showticklabels=False,
)




styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



def create_map(clickData,plot_type,variable,fc_time,info,testdir=None,refdir=None):
    print(' ')
    print('>>> Starting create_map <<<')
    print(' ')
    bdnc = info['bdnc']
    predictand = info['variables'][variable]
    
    if clickData == None:
        clickData = info['clickData']
    #print(clickData)
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    print('lat = ',lat_click,'  lon = ',lon_click)
    print('forecating time = ',fc_time) 
    
    month = np.int(fc_time[5:])
    season = monthzz[month:month+3]
    year = np.int(fc_time[:4])

    zmin=plot_dict[predictand][plot_type]['vmin']
    zmax=plot_dict[predictand][plot_type]['vmax']
    if testdir and refdir:
        print('diff plotted')
        scores = xr.open_dataset(info['testdirs'][testdir]+'scores_v2_ref_'+info['variables'][variable]+'_'+str(month).zfill(2)+'.nc')
        zmin = -0.2
        zmax = 0.2
    elif testdir:
        print('test plotted')
        scores = xr.open_dataset(info['testdirs'][testdir]+'scores_v2_'+info['variables'][variable]+'_'+str(month).zfill(2)+'.nc')
    else:
        print('ref plotted')
        scores = xr.open_dataset(bdnc+'scores_v2_'+info['variables'][variable]+'_'+str(month).zfill(2)+'.nc')
    times_m = scores['time.month']
    data_xr = scores[info['plottypes'][plot_type]].values.squeeze()
    #data_xr = scores[plottypes[plot_type]].isel(time=-dict_times[fc_time]).values
    #data = scores[plottypes[plot_type]].sel(times_m == m).values
    #scores_1t = scores.isel(time=-dict_times[fc_time])
    
    if plot_type == 'Forecast anomalies': # Calculate significance of ensemble mean
        print('still to implement')
        sig = scores.for_anom_sig.squeeze()
        #sig = scores.cor_sig.values.squeeze()
    elif plot_type == 'Correlation':
        sig = scores.cor_sig.values.squeeze()
        
    if 'sig' in locals():
        if plot_type == 'Forecast anomalies': 
            #sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
            sigvals = np.where(sig[:,:]<0.1)
        else: 
             sigvals = np.where(sig[:,:]<0.05)
        lon2d, lat2d = np.meshgrid(scores.lon.values, scores.lat.values)
    titel = info_titles[variable]+' ('+season+' '+str(year)+') - '+info_titles[plot_type][0]+'<br>'+'Ens. size: 51 | Forecast base time: '+calendar.month_name[month]+' '+str(year)+' | '+info_titles[plot_type][1]
    #titel = variable+", "+plot_type+', valid for: '+season+' '+str(year)
    #titel = u"variable = "+variable+", plot type = "+plot_type+', valid for: '+season+' '+str(year)
    colorz = plot_dict[info['variables'][variable]]['colors']
    #calendar.month_name[3]
    if plot_type == 'Forecast anomalies':
        fr = plot_dict[predictand][plot_type]['fr']
        tv = plot_dict[predictand][plot_type]['tv']
    else: 
        fr = plot_dict[plot_type]['fr']
        tv = plot_dict[plot_type]['tv']
    
    colorsceel=[ 
                 [fr[0], colorz[0]], [fr[1], colorz[0]],   
                 [fr[1], colorz[1]], [fr[2], colorz[1]],  
                 [fr[2], colorz[2]], [fr[3], colorz[2]], 
                 [fr[3], colorz[3]], [fr[4], colorz[3]], 
                 [fr[4], colorz[4]], [fr[5], colorz[4]],
                 [fr[5], colorz[5]], [fr[6], colorz[5]],
                 [fr[6], colorz[6]], [fr[7], colorz[6]],
                 [fr[7], colorz[7]], [fr[8], colorz[7]],
                 [fr[8], colorz[8]], [fr[9], colorz[8]],
               ]

    
    # Make traces of contour plot, marker where clicked and if possible significant markers
    
    trace_contour = [go.Heatmap(z=data_xr,
                                   x=scores.lon.values,
                                   y=scores.lat.values,
                                   zmin=zmin,
                                   zmax=zmax,
                                   zsmooth = 'best',
                                   colorscale=colorsceel,
                                   opacity=1.,
                                   colorbar=dict(
                                    lenmode='fraction', len=0.75, 
                                    title=plot_dict[predictand][plot_type]['units'],
                                    titleside='right',
                                    titlefont=dict(size=18),
                                    tickvals = tv
                                    ),
                                   name=predictand,
                                   )]

    trace_clickpoint = [go.Scatter(x=[lon_click]
                         ,y=[lat_click]
                         ,mode='markers'
                         ,marker=dict(size=10,color='black',line=dict(width=2)))]
    
    
    
    if 'sig' in locals():
        trace_sig = [go.Scatter(x=lon2d[sigvals],
                            y=lat2d[sigvals],
                            mode='markers',
                            marker=dict(size=1,color='black'),
                            )]
        traces = traces_cc + trace_clickpoint + trace_sig + trace_contour
        #traces = traces_cc + trace_contour + trace_clickpoint
    else:
        traces = traces_cc + trace_clickpoint + trace_contour   

    print(variable,plot_type,lon_click,lat_click)
    #print(
    return( 
            go.Figure(
            data=traces,
            layout = go.Layout(
                title=titel,
                showlegend=False,
                #clickmode="event",
                #autorange=False,
                hovermode='closest',        # highlight closest point on hover
                #hoverlabel='test',
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
                #width='100px',
                #height=400,)
            )
            ))      
   
   
def create_time_series(clickData,variable,ncdir,fc_time,info):
    print(' ')
    print('>>> Starting create_time_series <<<')
    print(' ')
    
    if clickData == None:
        clickData = info['clickData']     
    month = np.int(fc_time[5:])
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    predictand = info['variables'][variable]
    
    
    #try: ncdir = info['testdirs'][ncdir]
    #except KeyError: ncdir = info['refdirs'][ncdir]
    
    
    pred = xr.open_dataset(ncdir+'pred_v2_'+predictand+'_'+str(month).zfill(2)+'.nc')
    # Select right location and time slice
    #pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=slice(None,-tt))
    pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).sel(time=(pred['time.month']==np.int(fc_time[5:])))
    
    time_pd = pred1d.time.to_pandas()
    kprep_mean = pred1d['kprep'].mean(dim='ens').values
    
    kprep_std = pred1d['kprep'].std(dim='ens').values * 2.
    kprep_qt = pred1d['kprep'].quantile([0.05,0.5,0.95],dim='ens')
    clim_qt = pred1d['clim'].quantile([0.05,0.5,0.95],dim='ens')
    clim_mean = pred1d['clim'].mean(dim='ens').values
    clim_std = pred1d['clim'].std(dim='ens').values * 2.
    trend = pred1d['trend'].mean(dim='ens').values
    s5_qt = pred1d['ecmwf_s5'].quantile([0.05,0.5,0.95],dim='ens')
    
    obs_nc = xr.open_dataset(ncdir+'predadata_v2_'+predictand+'.nc')
    obs1d = obs_nc.to_array().sel(lat=lat_click,lon=lon_click,method='nearest').sel(time=(obs_nc['time.month']==month)).load()
    time_pd_long = obs1d.time.to_pandas()
    #print(time_pd)
    #print(len(time_pd))
    fig = go.Figure(
        data=
            [go.Scatter(x=time_pd,y=kprep_qt.sel(quantile=0.95).values,mode='lines',fillcolor='rgba(0,100,80,0.2)',line=go.scatter.Line(color='rgba(0,100,80,0.2)'),opacity=0.9,showlegend=False)]
            +
            [go.Scatter(x=time_pd,y=kprep_qt.sel(quantile=0.05).values,mode='lines',fill='tonexty',fillcolor='rgba(0,100,80,0.2)',line=go.scatter.Line(color='rgba(0,100,80,0.2)'),opacity=0.9,name='For. spread (5-95%)')]
            +
            [go.Scatter(x=time_pd,y=kprep_qt.sel(quantile=0.50),mode='lines',name='Forecast',line=dict(color='blue',width=4))]
            +
            [go.Scatter(x=time_pd_long,y=obs1d.values.squeeze(),mode='lines',name='Observations',line=dict(color='black'))]
            +[go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.50),mode='lines',name='Climatology (5-50-95%)',showlegend=True,legendgroup='clim',line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.95),mode='lines',name='Clim. spread (5-95%)',showlegend=False,legendgroup='clim',line=dict(color='green',dash='dash'))]
            +[go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.05),mode='lines',name='Clim. spread (5-95%)',showlegend=False,legendgroup='clim',line=dict(color='green',dash='dash'))]
            +[go.Scatter(x=time_pd,y=s5_qt.sel(quantile=0.50),mode='lines',name='ECMWF S5 (5-50-95%)',line=dict(color='orange'),legendgroup='s5',visible='legendonly')]
            +[go.Scatter(x=time_pd,y=s5_qt.sel(quantile=0.95),mode='lines',name='S5 spread (5-95%)',showlegend=False,line=dict(color='orange',dash='dash'),legendgroup='s5',visible='legendonly')]
            +[go.Scatter(x=time_pd,y=s5_qt.sel(quantile=0.05),mode='lines',showlegend=False,line=dict(color='orange',dash='dash'),legendgroup='s5',visible='legendonly')]
                    
            +[go.Scatter(x=time_pd,y=trend,mode='lines',name='Trend CO2',line=dict(color='red'),visible='legendonly')]
            #+[go.Scatter(x=time_pd,y=pred1d['obs'].values,mode='lines',name='Observations',line=dict(color='black'))]
            ,
            #),

        layout = go.Layout(
            title = 'Time series of the forecast, forecast only on CO2, climatology and observations (lat='+str(lat_click)+', lon='+str(lon_click)+')<br>Click on the legend entries to add or remove lines from the plot',
            #height =  225,
            margin = {'b': 40},
            autosize=False,
            #width=1000.,
            #height=400.,
            xaxis=dict(
                rangeselector=dict(
                x=0.05,
                y=0.85,
                buttons=list([
                dict(count=len(time_pd),
                     label='1961-2020',
                     step='year',
                     stepmode='backward'),                    
                dict(count=len(time_pd_long),
                     label='1901-2020',
                     step='year',
                     stepmode='backward'),
                ]),
            ),
            rangeslider=dict(),
            type='date'
            ),
            #legend_orientation="h",
            #font=dict(size=14),
            #legend=dict(x=1.,y=1.15,font=dict(size=14)),            
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),     
            )
    )
    initial_range=['1961-01-01', time_pd[-1]]
    fig['layout']['xaxis'].update(range=initial_range)   
    return(fig)
            
            
      
def create_bar_plot(clickData,plot_type,ncdir,variable,fc_time,info):
    print(' ')
    print('>>> Starting create_bar_plot <<<')
    print(' ')
    
    predictand = info['variables'][variable]
    if clickData == None:
        clickData = info['clickData']
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']        
        
    month = np.int(fc_time[5:])
    # Load data
    pred_1d = xr.open_dataset(ncdir+'pred_v2_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    #for_anom = pred_1d['kprep'].mean(dim='ens')
    for_anom = pred_1d['kprep'].isel(ens=0)
    #co2_anom = pred_1d['trend'].mean(dim='ens')
    co2_anom = pred_1d['trend'].isel(ens=0)
    beta_1d = xr.open_dataset(ncdir+'beta_v2_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predo_1d = xr.open_dataset(ncdir+'predodata_3m_fit_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=fc_time+'-01')
    predos = list(predo_1d.data_vars)
    sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    traces=[]
    fig = tls.make_subplots(rows=1,cols=1)
    if nr_sigp == 0:
        print('no significant predictors..')
        fig = go.Figure(data=[],layout=go.Layout(title='No significant predictors..'))
        fig.add_trace(go.Scatter(x=[0.5],y=[0.5],mode="text",name="no significant predictors.."))
        return(fig)
    
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
            trace = go.Bar(
                x=np.append(np.asarray(predos)[sigp],np.asarray(['Total','dif'])),
                y=vals
                )
        else:
            trace = go.Bar(
                x=np.append(np.asarray(predos)[sigp],np.asarray(['Total'])),
                y=vals
                )
        
        layout = go.Layout(
            #height=500,
            #width='30%',
            margin={'b':30},
            autosize=False,
            title='Individual contribution predictors (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),
            )
   
        #fig = go.Figure(data=Data([trace]), layout=layout)
        fig = go.Figure(data=[trace], layout=layout)     
        return(fig)
        
def create_po_timeseries(clickData,variable,ncdir,fc_time,info):
    print(' ')
    print('>>> Starting create_po_timeseries <<<')
    print(' ')
    
    if clickData == None:
        clickData = info['clickData']
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']           

    month = np.int(fc_time[5:])
    predictand = info['variables'][variable]
    
    # Load monthly data for predictions
    pred = xr.open_dataset(ncdir+'pred_v2_'+predictand+'_'+str(month).zfill(2)+'.nc')#.sel(lon=lon_click,lat=lat_click,method=str('nearest'))
    pred_1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest'),time=(pred['time.month']==month))
    for_anom = pred_1d['kprep'].mean(dim='ens').isel(time=-1).values
    co2_anom = pred_1d['trend'].mean(dim='ens').isel(time=-1).values
    
    predo = xr.open_dataset(bdnc+'predodata_3m_fit_'+predictand+'_'+str(month).zfill(2)+'.nc')
    predo_1d = predo.sel(time=(predo['time.month']==month),lon=lon_click,lat=lat_click,method='nearest')
    predos = list(predo_1d.data_vars)

    beta_1d = xr.open_dataset(ncdir+'beta_v2_'+predictand+'_'+str(month).zfill(2)+'.nc').sel(lon=lon_click,lat=lat_click,method=str('nearest'))#,time=fc_time+'-01')
    # Load predictor data (fitted)    
    beta_1d = beta_1d.assign_coords(predictors=predos)
    sigp = ~np.isnan(beta_1d.beta.values).all(axis=0)
    #sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    time_pd = predo_1d.time.to_pandas()
    time_pd_beta = beta_1d.time.to_pandas()
    traces=[]
    xaxs = ['x1','x2','x3','x4','x5','x6','x7','x8']
    yaxs = ['y1','y2','y3','y4','y5','y6','y7','y8']
    specs=[[{'secondary_y':True}] for i in range(8)]
    fig = make_subplots(rows=np.int(nr_sigp),
                        specs=specs[:nr_sigp],
                        subplot_titles=np.asarray(predos)[sigp],
                        shared_xaxes=True,
                       )

    if nr_sigp == 0:
        print('no significant predictors..')
        return()
    else:
        print('timeseries plot - nr of significant predictors is ',nr_sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        for ii,pre in enumerate(np.asarray(predos)[sigp]):
            print(pre)
            #print(beta_1d)
            #print(time_pd_beta)
            fig.add_trace(go.Scatter(
                x=time_pd,
                y=predo_1d[pre].values,
                xaxis=xaxs[ii],
                yaxis=yaxs[ii],
                text=pre,
                textposition='top center',
                name=pre,
                showlegend=False
                ),
                row=ii+1,col=1,secondary_y=False)
            if pre == 'CO2EQ':
                yy = pred_1d['trend'].isel(ens=0).values
            else:  
                yy = beta_1d.beta.sel(predictors=pre).values.squeeze()*predo_1d[pre].sel(time=beta_1d.time).values
            fig.add_trace(go.Scatter(
                x=time_pd_beta, 
                y=yy,
                xaxis=xaxs[ii],
                yaxis=yaxs[ii],
                line=dict(color='black'),
                showlegend=False,
                #name="beta (regr. coef.)",
                ),
                row=ii+1,
                col=1,
                secondary_y=True,
                
                )
            fig.update_yaxes(title_text=plot_dict[predictand]['Forecast anomalies']['units'], row=ii+1,col=1,secondary_y=True)
        print(time_pd)            
        print(beta_1d.beta.sel(predictors=pre))
        fig['layout'].update(   autosize=False,
                                margin = {'b': 40},                             
                                title='Time series of (fitted) predictor data (lat='+str(lat_click)+', lon='+str(lon_click)+') <br>The black lines shows the contribution of a predictor to the hindcasts (secondary y-axis)',
                            )
        return(fig)
    
def create_mapp(clickData,predictand,predictor,fc_time,data_name,bdnc,info):
    month = np.int(fc_time[5:])
    season = monthzz[month:month+3]
    year = np.int(fc_time[:4])
    
    if clickData == None:
        clickData = info['clickData']
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']

    predictand = info['variables'][predictand]
    predictor = info['variables_pred'][predictor]
    
    data_name2 = 'sig'+data_name[3:]
    if data_name == 'diff':
        cor_pred = xr.open_dataset(bdnc+'cor_pred/'+'cor_predictors_fit'+'_'+predictand+'_'+str(month).zfill(2)+'.nc')[predictor]
        cor_pred2 = xr.open_dataset(bdnc+'cor_pred/'+'cor_predictors_nofit'+'_'+predictand+'_'+str(month).zfill(2)+'.nc')[predictor]
        sig_pred = xr.open_dataset(bdnc+'cor_pred/'+'sig_predictors_fit'+'_'+predictand+'_'+str(month).zfill(2)+'.nc')[predictor]
        cor1 = 0.5 * np.log((1+cor_pred.values) / (1-cor_pred.values))
        cor2 = 0.5 * np.log((1+cor_pred2.values) / (1-cor_pred2.values))
        data_xr = cor1 - cor2
        #print(data_xr)
        zmin = -0.3; zmax=0.3
        #fr = [0.0,0.167,0.25,0.333,0.4,0.6,0.7,0.8,0.9,1.0]
        tv = [-0.3,-0.2,-0.15,-0.1,-0.05,0.05,0.1,0.15,0.2,0.3]
        fr = (np.array(tv) / zmax + 1) / 2.
    else:
        cor_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name+'_'+predictand+'_'+str(month).zfill(2)+'.nc')[predictor]
        sig_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name2+'_'+predictand+'_'+str(month).zfill(2)+'.nc')[predictor]
        data_xr = cor_pred.values#.isel(time=-dict_times[fc_time]).values
        zmin = -1.; zmax=1.
        #fr = [0.0,0.1,0.2,0.3,0.4,0.6,0.7,0.8,0.9,1.0]
        tv = [-1,-0.8,-0.6,-0.4,-0.2,0.2,0.4,0.6,0.8,1.0]
        fr = (np.array(tv) / zmax + 1) / 2.
    #cor_pred = xr.open_dataset(bdnc+'cor_predictors_stepwise_'+variables_prad[predictand]+'.nc')
    #times_m = cor_pred['time.month']
    colorz = ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
    colorsceel=[ 
                [fr[0], colorz[0]], [fr[1], colorz[0]],   
                [fr[1], colorz[1]], [fr[2], colorz[1]],  
                [fr[2], colorz[2]], [fr[3], colorz[2]], 
                [fr[3], colorz[3]], [fr[4], colorz[3]], 
                [fr[4], colorz[4]], [fr[5], colorz[4]],
                [fr[5], colorz[5]], [fr[6], colorz[5]],
                [fr[6], colorz[6]], [fr[7], colorz[6]],
                [fr[7], colorz[7]], [fr[8], colorz[7]],
                [fr[8], colorz[8]], [fr[9], colorz[8]],
            ]

    
    titel = u'Correlation between '+predictand+' and '+predictor+', valid for: '+season+' '+str(year)
    if data_name == 'cor_predictors_fit':
        titel2 = 'Fitted, The predictor data is fitted on previous 3 month mean and trend'
    elif data_name == 'cor_predictors_nofit':
        #titel2 = 'No fit, The predictor data is the previous 3 month mean'
        titel2 = 'Correlation after stepwise predicter selection'
    else:
        #titel2 = 'Differce in correlation (fisher transformed), fitted - nofit'
        titel2 = 'Correlation after stepwise predicter selection'
    #fig = go.Contour(
    #print(sig_pred)
    sigvals = np.where(sig_pred.values[:,:]<0.05)
    lon2d, lat2d = np.meshgrid(sig_pred.lon.values, sig_pred.lat.values)

    
    trace_contour = [go.Heatmap(z=data_xr,
                                   x=cor_pred.lon.values,
                                   y=cor_pred.lat.values,
                                   zmin=zmin,
                                   zmax=zmax,
                                   colorscale=colorsceel,
                                   colorbar=dict(
                                    title='[-]',
                                    titleside='right',
                                    titlefont=dict(size=18),
                                    tickvals = tv,
                                    )
                                   )]

    trace_clickpoint = [go.Scatter(x=[lon_click]
                         ,y=[lat_click]
                         ,mode='markers'
                         ,marker=dict(size=10,color='black',line=dict(width=2)))]
    
    
    trace_sig = [go.Scatter(x=lon2d[sigvals],
                            y=lat2d[sigvals],
                            mode='markers',
                            marker=dict(size=1,color='black'),
                            )]
    traces = traces_cc + trace_sig + trace_clickpoint + trace_contour
    
    return( 
            go.Figure(
            data = traces,
            layout = go.Layout(
                title=titel+'<br>'+titel2,
                showlegend=False,
                #clickmode="event",
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
                       range=[-180,180]),
                yaxis=go.layout.YAxis(
                    axis_style),
                )
            ))      
   
def create_map1(clickData,predictand,predictor,fc_time,bdnc,info):
    return create_mapp(clickData,predictand,predictor,fc_time,'cor_predictors_fit',bdnc,info)
    
def create_map2(clickData,predictand,predictor,fc_time,bdnc,info):    
    return create_mapp(clickData,predictand,predictor,fc_time,'cor_predictors_stepwise',bdnc,info)
   
def create_map3(clickData,predictand,predictor,fc_time,bdnc,info):    
    return create_mapp(clickData,predictand,predictor,fc_time,'diff',bdnc,info)
      
   
def create_xyplot(clickData,predictand,predictor,fc_time,bdnc,info):
    mo = np.int(fc_time[5:])
    if clickData == None:
        clickData = info['clickData']

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    print('!!!!!!!!!!!!!!!!!!!!')
    print(predictand)
    pa = info['variables_prad'][predictand]
    po = info['variables_pred'][predictor]
    print(predictand)
    #print('Hello2!!')
    #print(lat_click,lon_click)
    #print(fc_time)           
    #print lat_click
    #tt = dict_times[fc_time]
    pred = xr.open_dataset(bdnc+'predodata_3m_nc_'+pa+'_'+str(mo).zfill(2)+'.nc')
    predfit = xr.open_dataset(bdnc+'predodata_3m_fit_'+pa+'_'+str(mo).zfill(2)+'.nc')
    #print(predictor)
    if po == 'CO2EQ':
        prad = xr.open_dataset(bdnc+'predadata_v2_'+pa+'.nc')
    else:
        prad = xr.open_dataset(bdnc+'predadata_3m_nc_'+pa+'_'+str(mo).zfill(2)+'.nc')
    # Select right location and time slice
    #pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=slice(None,-tt))
    try: 
        #print('try for 3d predictor..')
        pred1d = pred[po].sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(pred['time.month']==mo))
        pred1d_fit = predfit[po].sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(pred['time.month']==mo))
    except ValueError:
        #print('.. went for 1d predictor')
        pred1d = pred[po].sel(time=(pred['time.month']==mo))
        pred1d_fit = predfit[po].sel(time=(pred['time.month']==mo))
        
    prad1d = prad.sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(prad['time.month']==mo))
    
    print('prad1d',prad1d.month)
    print('pred1d',pred1d.month)
    print('pred1d_fit',pred1d_fit.month)

    data_orig = xr.merge([prad1d.to_array(name='predictand').squeeze(),pred1d.rename('orig'),pred1d_fit.rename('fit')]).to_dataframe()
    #data_fit = xr.merge([prad1d.to_array(name='predictand').squeeze(),pred1d_fit]).to_dataframe()
    print(data_orig)    
    data_melt_orig = data_orig.dropna().melt(id_vars='predictand',value_vars=['orig','fit'])
    #data_melt_fit = data_fit.dropna(dim='time').melt(id_vars='predictand',value_vars=['predictor_fit'])
    print(data_melt_orig)

    fig = px.scatter(data_melt_orig, x='value', y='predictand', color='variable',trendline='ols')
    #fig.data[-1].name = 'Diner'
    fig.data[-1].showlegend = True

    results = px.get_trendline_results(fig)
    print(results.iloc[0])

    fig.update_layout(
        legend=go.layout.Legend(
            #x=0.8,
            #y=0.9,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            #bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )    
    
    fig.update_layout(go.Layout(
            title = 'Correlation between '+predictand+' - '+predictor+' (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            autosize=False,
            height=500,
            #yaxis=dict(title='Burned Area [km2]'),
            ))
    fig.update_yaxes(title_text=predictand)
    fig.update_xaxes(title_text=predictor)
    #fig.update_yaxes(title_text="Monthly Drought Code [-]", secondary_y=True)

    print(' ')
    print('>>> Finished create_cor_time_series <<<')
    print(' ')        
    
    return(fig)    
    
    
#     time_pd = pred1d.time.to_pandas()
#     xdata = prad1d.to_array().values[0]
#     y_orig = pred1d.values[:len(xdata)]
#     y_fit = pred1d_fit.values[:len(xdata)]

#     cor_orig = str(scipy.stats.pearsonr(xdata[10:],y_orig[10:]))[1:5]
#     cor_fit = str(scipy.stats.pearsonr(xdata[10:],y_fit[10:]))[1:5]
   
    
#     trace1 = go.Scatter(x=xdata[10:],y=y_orig[10:],mode='markers',name='original  '+cor_orig,marker=dict(color='blue'))
#     trace2 = go.Scatter(x=xdata[10:],y=y_fit[10:],mode='markers',name='model fit '+cor_fit,marker=dict(color='green'))
    
        
#     return( go.Figure(data = [trace1,trace2],
#                        layout = go.Layout(
#                             title = 'Scatter plot of '+predictand+' with '+predictor+', lat='+str(lat_click)+', lon='+str(lon_click),
#                             #height =  225,
#                             margin = {'l': 70, 'b': 70, 'r': 10, 't': 100},
#                             autosize=False,
#                             #width=500.,
#                             #height=500.,
#                             xaxis=dict(title=predictand),
#                             yaxis=dict(title=predictor),
#                             legend=dict(x=0,y=1,font=dict(size=14)),
#                             )
#                         )
#         )    
