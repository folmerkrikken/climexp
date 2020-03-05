import pandas as pd
import xarray as xr
import numpy as np    
import scipy.stats
import sys
#sys.path.insert(0,'/home/folmer/.local/lib/python3.6/site-packages')
from mpl_toolkits.basemap import Basemap
import numpy as np
import os

import chart_studio.plotly as py
#from plotly.graph_objs import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

import plotly.tools as tls
#import seaborn as sns

monthz = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


bd = '/home/oldenbor/climexp_data/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp_data/KPREPData/'
    
#bd = '/home/folmer/KPREP/'
bdnc = bd+'ncfiles_mdc/'


variables={'Maximum temperature':'TMAX','Precipitation':'PRECIP','MDC (from TP)':'MDC_FROM_TP','Monthly Drought Index':'MDC','Monthly Drought Index (from TP)':'MDC_FROM_TP'}
area_sizes = {u'1x1\N{DEGREE SIGN}':1,u'3x3\N{DEGREE SIGN}':3,u'5x5\N{DEGREE SIGN}':5,u'7x7\N{DEGREE SIGN}':7,u'10x10\N{DEGREE SIGN}':10}

#variables_prad={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}
#variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'}
variables_pred={'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'PRECIP','PERS':'PERS','PERS_TREND':'PERS_TREND','TMAX':'TMAX'}

regions={'Northern hemisphere':{'lon1':-180,'lon2':180,'lat1':0,'lat2':90},
         'Mediterranean':{'lon1':-12,'lon2':31,'lat1':34,'lat2':48},
         'Boreal Eurasia':{'lon1':4,'lon2':190,'lat1':50,'lat2':72},
         'Boreal North America':{'lon1':-168,'lon2':-52,'lat1':44,'lat2':72},
        }
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

plot_dict = {'TMAX':{'Forecast anomalies':{'vmin':-4.,'vmax':4.,'units':'[<sup>o</sup>C]',
                                 'fr':[0.0,0.01,0.25,0.375,0.46,0.54,0.625,0.75,0.99,1.0],
                                 'tv':[-2,-1,-0.5,-0.2,0.2,0.5,1.0,2.0]},                     
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'PRECIP':{'Forecast anomalies':{'vmin':-20.,'vmax':20.,'units':'[mm]',
                                'fr':[0.0,0.01,0.25,0.4,0.45,0.55,0.6,0.75,0.99,1.0],
                                'tv':[-50,-25,-10.,-5.,5,10,25,50]},                      
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                        ['#993300','#cc8800','#ffcc00','#ffee99','#ffffff','#ccff66','#33ff00','#009933','#006666']
                       },
            '20CRslp':{'Forecast anomalies':{'vmin':-4.,'vmax':4.,'units':'[hPa]',
                                'fr':[0.0,0.01,0.25,0.375,0.45,0.55,0.625,0.75,0.99,1.0],
                                'tv':[-4,-2,-1,-0.5,0.5,1,2,4]},                       
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                       ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'MDC':{'Forecast anomalies':{'vmin':-40.,'vmax':40,'units':'[-]',
                                'fr':[0.0,0.01,0.25,0.375,0.45,0.55,0.625,0.75,0.99,1.0],
                                'tv':[-40,-20,-10,-5,5,10,20,40]},                                              
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':
                       ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'MDC_FROM_TP':{'Forecast anomalies':{'vmin':-40.,'vmax':40,'units':'[-]',
                                'fr':[0.0,0.01,0.25,0.375,0.45,0.55,0.625,0.75,0.99,1.0],
                                'tv':[-40,-20,-10,-5,5,10,20,40]},                           
                       'RMSESS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'CRPSS':{'vmin':-0.5,'vmax':0.5,'units':'-'},
                       'Tercile summary plot':{'vmin':-100.,'vmax':100.,'units':'%'},
                       'Correlation':{'vmin':-1.,'vmax':1.,'units':'-'},
                       'colors':                      ['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022']
                       },
            'RMSESS':{'fr':[0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0],'tv':[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]},
            'CRPSS': {'fr':[0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0],'tv':[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]},
            'Tercile summary plot':{'fr':[0.0,0.15,0.2,0.25,0.3,0.7,0.75,0.8,0.85,1.0],'tv':[-100,-70,-60,-50,-40,40,50,60,70,100]},
            'Correlation':{'fr':[0.0,0.1,0.2,0.3,0.4,0.6,0.7,0.8,0.9,1.0],'tv':[-1,-0.8,-0.6,-0.4,-0.2,0.2,0.4,0.6,0.8,1.0]},
            }

clickData_start = dict({u'points': [{u'y': 50., u'x': 50., u'pointNumber': 6, u'curveNumber': 632}]})

axis_style = dict(
    zeroline=False,
    showline=False,
    showgrid=False,
    ticks='',
    showticklabels=False,
)



#tmp_nc = xr.open_dataset(bdnc+'predadata_v2_GCEcom.nc')
#timez = xr.open_mfdataset(bdnc+'scores*GCEcom*.nc',concat_dim='time').time.sortby('time').values
#timez = tmp_nc.time[-12:].values
#months12 = pd.to_datetime(timez).strftime('%Y-%m')[::-1]
#dict_times = dict(zip(months12,range(1,13)))
base_times = dict(zip(['March','April','May','June','July','August','September','October'],range(3,11)))
valid_times = dict(zip(['April','May','June','July','August','September','October'],range(4,11)))


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

plottypes={'Correlation':'cor','RMSESS':'rmsess','CRPSS':'crpss','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'}
#variables={'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'}
#variables={'Monthly Drought Code':'MDC'}
anno_text = "Data courtesy of Folmer Krikken"


def create_map_enduser(clickData,plot_type,region,base_time,valid_time,area_size,variable='MDC (from TP)'):
    return(create_map(clickData,plot_type,region,base_time,valid_time,area_size,variable=variable))

def create_map(clickData,plot_type,region,base_time,valid_time,area_size,variable='MDC (from TP)'):
    print(' ')
    print('>>> Starting create_map <<<')
    print(' ')
    print(regions[region])
    if clickData == None: clickData = clickData_start
    if variable == 'MDC (from TP)':
        predictand = 'MDC_FROM_TP'
    else:
        predictand = variables[variable]

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    print('lat = ',lat_click,'  lon = ',lon_click)
    print('base time = ',base_time)
    print('valid time = ',valid_time)
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    name1 = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    
    scores = xr.open_dataset(bdnc+'scores_mdc_v2_'+variables[variable]+'_'+name2).sel(leadtime=lt)
    times_m = scores['time.month']
    data_xr = scores[plottypes[plot_type]].values.squeeze()
    #data_xr = scores[plottypes[plot_type]].isel(time=-dict_times[fc_time]).values
    #data = scores[plottypes[plot_type]].sel(times_m == m).values
    #scores_1t = scores.isel(time=-dict_times[fc_time])
    
    if plot_type == 'Forecast anomalies': # Calculate significance of ensemble mean
        #print('still to implement')
        sig = scores.for_anom_sig.values.squeeze()
        #sig = scores.cor_sig.values.squeeze()
    elif plot_type == 'Correlation':
        sig = scores.cor_sig.values.squeeze()
        
    if 'sig' in locals():
       if plot_type == 'Forecast anomalies': 
           sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
           #sigvals = np.where(sig[:,:]<0.1)
           
       else: sigvals = np.where(sig[:,:]<0.1)
       lon2d, lat2d = np.meshgrid(scores.lon.values, scores.lat.values)

    
    titel = variable+" "+plot_type+', valid for: '+monthz[lt-1]+' '+str(year)
    #colorz = plot_dict[variables[variable]]['colors']
    
    #colorsceel=[ [0, colorz[0]],[0.1, colorz[1]], [0.3, colorz[2]], [0.45, colorz[3]], [0.55, colorz[4]], [0.67, colorz[5]], [0.9, colorz[6]], [1,colorz[7]]]
    colorz = plot_dict[variables[variable]]['colors']

    # Make traces of contour plot, marker where clicked and if possible significant markers
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
#    trace_contour = [Contour(z=data_xr,
#                                   x=scores.lon.values,
#                                   y=scores.lat.values,
#                                   zmin=plot_dict[predictand][plot_type]['vmin'],
#                                   zmax=plot_dict[predictand][plot_type]['vmax'],
#                                   colorscale=colorsceel,
#                                   opacity=1.,
#                                   colorbar=dict(
#                                    title=plot_dict[predictand][plot_type]['units'],
#                                    titleside='right',
#                                    titlefont=dict(size=18)),
#                                   )]
    #fig = go.Figure(go.Scattergeo())
    #fig.update_geos(projection_type="natural earth")
    #trace_cc = [go.Scattergeo(lat=scores.lat.values,lon=scores.lon.values)]
    #fig = go.Figure(go.Scattergeo())

    trace_contour = [go.Heatmap(z=data_xr,
                                   x=scores.lon.values,
                                   y=scores.lat.values,
                                   zmin=plot_dict[predictand][plot_type]['vmin'],
                                   zmax=plot_dict[predictand][plot_type]['vmax'],
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
                         ,marker=dict(size=10,color='black',line=dict(width=2))),
                       ]

    
    
    #import pdb;pdb.set_trace()
    if 'sig' in locals():
        trace_sig = [go.Scatter(x=lon2d[sigvals],
                            y=lat2d[sigvals],
                            mode='markers',
                            marker=dict(size=1,color='black'),
                            ),
]
        traces = traces_cc + trace_clickpoint + trace_sig + trace_contour
    else:
        traces = traces_cc + trace_clickpoint + trace_contour

    #print(variable,plot_type,lon_click,lat_click)
    print(' ')
    print('>>> Finished create_map <<<')
    #print(area_size)
    print(' ')

    
    return(go.Figure(
            data=traces,
            layout = go.Layout(
                title=titel,
                font=dict(size=14),
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
                       range=[regions[region]['lon1'],regions[region]['lon2']]
                                     ),
                yaxis=go.layout.YAxis(
                    axis_style,
                       range=[regions[region]['lat1'],regions[region]['lat2']],
                    scaleanchor = 'x',
                    scaleratio = 2.2                                     
                ),
                autosize=False,
                #width=1000,
                #height=500,
                shapes = [
                    # filled Rectangle
                    {
                    'type': 'rect',
                    'x0': lon_click-(area_sizes[area_size]/2),
                    'y0': lat_click-(area_sizes[area_size]/2),
                    'x1': lon_click+(area_sizes[area_size]/2),
                    'y1': lat_click+(area_sizes[area_size]/2),
                    'line': {'color': 'rgba(128, 0, 128, 1)','width': 2},
                    #'fillcolor': 'rgba(128, 0, 128, 0.7)',
                    }],
                )
            ))      
   

def create_mdc_time_series(clickData,base_time,valid_time,area_size,variable='MDC (from TP)'):
    print(' ')
    print('>>> Starting create_mdc_time_series <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
          
    #month = np.int(fc_time[5:])
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    name1 = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    predictand = variables[variable]
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']

    # Depending on 'area size', use either 1 grid point or the average over multiple
    if area_sizes[area_size] == 1:
        region = {'lat':lat_click,'lon':lon_click}#,'method':'nearest'}
        methode = 'nearest'
        print('method is ',methode,lat_click,lon_click)
    else:
        region = {'lat':slice(lat_click+0.1+area_sizes[area_size]/2,lat_click-0.1-area_sizes[area_size]/2),
                  'lon':slice(lon_click-0.1-area_sizes[area_size]/2,lon_click+0.1+area_sizes[area_size]/2)}
        methode = None
                
    pred_clim = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_3.nc')#.sel(time=str(year))
    pred_clim1d = pred_clim.sel(region,method=methode)
    obs_1d = xr.open_dataset(bdnc+'mdc_obs.nc').sel(region,method=methode).sel(time=str(year)).mdc_anom
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(time=str(year))
    pred1d = pred.sel(region,method=methode)
    scores = xr.open_dataset(bdnc+'scores_mdc_v2_'+variables[variable]+'_'+name2).sel(region,method=methode).crpss
    # Compute spatial averages if it is still gridded data
    print(area_size,pred_clim1d.coords)
    if area_sizes[area_size] != 1:
        pred_clim1d = pred_clim1d.mean(dim=['lat','lon']) #TODO, spatial averaging with area weights
        pred1d = pred1d.mean(dim=['lat','lon'])
        obs_1d = obs_1d.mean(dim=['lat','lon'])
        print('in lat if')


    #print(pred1d)
    time_pd = pred1d.time.to_pandas()
    kprep_mean = pred1d['kprep'].mean(dim='ens').values
    kprep_qt = pred1d['kprep'].quantile([0.05,0.5,0.95],dim='ens')
    clim_qt = pred_clim1d['obs'].quantile([0.05,0.5,0.95],dim='time')
    trend = pred1d['trend'].mean(dim='ens').values
    time_pd = pd.date_range(str(year)+'-04-01',freq='MS',periods=9)
    time_fc = pd.date_range(list(pd.to_datetime(pred1d.time.values).strftime('%Y-%m-%d'))[0],freq='MS',periods=len(pred1d.leadtime)+1)[1:]
    time_obs = time_pd[:-(len(time_fc)+1)]
    print('HELLOOOOO')
    #print(time_pd)
    #print(time_fc)
    #print(time_obs)
    print(' ')
    print('>>> Finished create_mdc_time_series <<<')
    print(' ')    

    fr = [0.0,0.01,0.15,0.3,0.4,0.6,0.7,0.85,0.99,1.0]
    tv = [-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]
    fr = [ 0.0, 0.1,0.3,0.45,0.7,0.99,1.0]
    tv = [-0.2,-0.1,0.1,0.30,0.5,0.8]
    
    
    colorz = ['#000099','#3355ff','#66aaff','#77ffff','#808080','#ffff33','#ffaa00','#ff4400','#cc0022']
    colorz = ['#77ffff','#808080','#ffff33','#ffaa00','#ff4400','#cc0022']
    colorsceel=[ 
                 [fr[0], colorz[0]], [fr[1], colorz[0]],   
                 [fr[1], colorz[1]], [fr[2], colorz[1]],  
                 [fr[2], colorz[2]], [fr[3], colorz[2]], 
                 [fr[3], colorz[3]], [fr[4], colorz[3]], 
                 [fr[4], colorz[4]], [fr[5], colorz[4]],
                 [fr[5], colorz[5]], [fr[6], colorz[5]],
                 #[fr[6], colorz[6]], [fr[7], colorz[6]],
                 #[fr[7], colorz[7]], [fr[8], colorz[7]],
                 #[fr[8], colorz[8]], [fr[9], colorz[8]],
               ]    
    
    shape = 'linear' # use hvh for stepline, linear for normal line
    fig = tls.make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.01,row_heights=[0.9,0.1])
    
    fig.add_trace(go.Scatter(x=time_fc,y=kprep_qt.sel(quantile=0.05).values.squeeze(),mode='lines',
                              fillcolor='rgba(0,100,80,0.2)',line=dict(color='rgba(0,100,80,0.2)',shape=shape),opacity=0.9,showlegend=False),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_fc,y=kprep_qt.sel(quantile=0.95).values.squeeze(),mode='lines',fill='tonexty',
                              fillcolor='rgba(0,100,80,0.2)',line=dict(color='rgba(0,100,80,0.2)',shape=shape),opacity=0.9,name='For. spread (5%-95%)'),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_fc,y=kprep_mean.squeeze(),
                              mode='lines',name='Forecast',line=dict(color='blue',width=4,shape=shape)),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_obs,y=obs_1d.sel(time=time_obs).values.squeeze(),
                              mode='lines',name='Observations (5%, 50% , 95%)',line=dict(color='black',shape=shape)),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.05).values.squeeze(),
                              mode='lines',name='Climatology',showlegend=False,line=dict(color='green',shape=shape)),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.95).values.squeeze(),
                              mode='lines',name='Climatology',showlegend=False,line=dict(color='green',shape=shape)),row=1,col=1)
    fig.add_trace(go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.5).values.squeeze()
                             ,mode='lines',name='Climatology',showlegend=True,line=dict(color='green',shape=shape)),row=1,col=1) 
    fig.add_trace(go.Heatmap(x=time_fc,
                             z=scores.values.T,
                             zmin=tv[0],
                             zmax=tv[-1],
                             zsmooth = 'best',
                             colorscale=colorsceel,
                             xgap=5,
                             ygap=5,
                             colorbar=dict(
                                    x=1.0,
                                    y=0.2,
                                    lenmode='fraction', len=0.8, 
                                    title='How good are the forecasts?',
                                    #fontsize=12,
                                    titleside='top',
                                    #titlefont=dict(size=18),
                                    tickvals = [-0.15,0,0.2,0.4,0.65],
                                    ticks='outside',
                                    ticktext = ['dangerous','no skill','reasonable skill','good skill','very good skill'],
                                    #yanchor = 'top',
                                    ),
                             ),row=2,col=1),
    #fig.update_xaxes(tickvals=time_pd + pd.DateOffset(days=15),ticktext=[i.strftime('%b %Y') for i in time_pd])

    fig.update_layout(go.Layout(
            title = 'Time series of the forecast, the climatology and observations for lat:'+str(lat_click)+', lon='+str(lon_click)+')',
            font=dict(size=14),
            #color="#7f7f7f"        
            #height =  225,
            #margin = {'l': 20, 'b': 30, 'r': 10, 't': 10},
            autosize=False,
            #width=800.,
            #height=400.,
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),  
            shapes = [
                # filled Rectangle
                {
                'type': 'line',
                'x0': time_fc[0],#-pd.DateOffset(days=15),
                'y0': 0,
                'x1': time_fc[0],#-pd.DateOffset(days=15),
                'y1': 1,
                'yref':'paper',
                'line': {'color': 'black','width': 2},
                #'fillcolor': 'rgba(128, 0, 128, 0.7)',
                }],            
            ))
    return(fig)
    

    
    


def create_obs_fires(clickData,base_time,valid_time,area_size,variable='MDC (from TP)'):
    print(' ')
    print('>>> Starting create_obs_fires <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
          
    #month = np.int(fc_time[5:])
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    name1 = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    
    print('name1',name1)
    print('name2',name2)
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    la1 = lat_click+0.1+area_sizes[area_size]/2
    la2 = lat_click-0.1-area_sizes[area_size]/2
    lo1 = lon_click-0.1-area_sizes[area_size]/2
    lo2 = lon_click+0.1+area_sizes[area_size]/2
    
    predictand = variables[variable]

    REGION = True
    if REGION:
        modis = xr.open_dataset(bdnc+'2001-2018-MODIS_BA_r10.nc').sel(lon=slice(lo1,lo2),lat=slice(la1,la2)).sum(dim=['lat','lon'])
        modis_m = modis.sel(time=modis['time.month'] == lt)
        
        obs_1d = xr.open_dataset(bdnc+'mdc_obs.nc').sel(lon=slice(lo1,lo2),lat=slice(la1,la2),time=slice('2000','2019')).mdc_anom.mean(dim=['lat','lon'])
        obs_1d_m = obs_1d.sel(time=obs_1d['time.month']==lt)
        pred1d = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(lon=slice(lo1,lo2),lat=slice(la1,la2),leadtime=lt,time=slice('2000','2019')).mean(dim=['lat','lon'])        
    else:
        modis = xr.open_dataset(bdnc+'2001-2018-MODIS_BA_r10.nc').sel(lon=lon_click,lat=lat_click,method='nearest')
        modis_m = modis.sel(time=modis['time.month'] == lt).load()# / 1e6
        obs_1d = xr.open_dataset(bdnc+'mdc_obs.nc').sel(lon=lon_click,lat=lat_click,method='nearest').mdc_anom.sel(time=slice('2000','2019'))
        obs_1d_m = obs_1d.sel(time=obs_1d['time.month']==lt)
        pred1d = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(lon=lon_click,lat=lat_click,method=str('nearest')).sel(leadtime=lt,time=slice('2000','2019'))
    
    ## Orig data
    
   
    
    time_pd = pred1d.time.to_pandas()
    #kprep_mean = pred1d['kprep'].mean(dim='ens').values
    kprep_qt = pred1d['kprep'].quantile([0.05,0.5,0.95],dim='ens')

  
    #line=go.Line(color='rgba(0,100,80,0.2)')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(     go.Scatter(x=modis_m.time.to_pandas(),y=modis_m.burned_area.values.squeeze()/1.e6,mode='lines',line=dict(color='black'),opacity=0.9,name='Burned Area (MODIS)'),secondary_y=False)
    fig.add_trace(
        go.Scatter(x=kprep_qt.time.to_pandas(),y=kprep_qt.sel(quantile=0.5).values.squeeze(),mode='lines',line=dict(color='red'),opacity=0.9,name='MDC forecast'),secondary_y=True)
    fig.add_trace(
        go.Scatter(x=obs_1d_m.time.to_pandas(),y=obs_1d_m.values.squeeze(),mode='lines',line=dict(color='blue'),opacity=0.9,name='MDC Observed'),secondary_y=True)
    fig.update_layout(go.Layout(
            title = 'Time series of the forecast, forecast only on CO2, climatology and observations (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            autosize=False,
            height=500,
            
            #yaxis=dict(title='Burned Area [km2]'),
            ))
    fig.update_yaxes(title_text="Burned Area [km2]", secondary_y=False)
    fig.update_yaxes(title_text="Monthly Drought Code [-]", secondary_y=True)
    fig.update_layout(legend_orientation="h",font=dict(size=16),legend=dict(x=0.17,y=-0.1,font=dict(size=16)))
    print(' ')
    print('>>> Finished create_mdc_time_series <<<')
    print(' ')      
    
    return(fig)



def create_cor_fires(clickData,base_time,valid_time,area_size,variable='MDC (from TP)'):
    print(' ')
    print('>>> Starting create_cor_fires <<<')
    print(' ')
    
    PRINT = False
    
    if clickData == None: clickData = clickData_start
          
    #month = np.int(fc_time[5:])
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    year = 2018
    name1 = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    la1 = lat_click+0.1+area_sizes[area_size]/2
    la2 = lat_click-0.1-area_sizes[area_size]/2
    lo1 = lon_click-0.1-area_sizes[area_size]/2
    lo2 = lon_click+0.1+area_sizes[area_size]/2  
    
    predictand = variables[variable]

    REGION = True
    if REGION:
        modis = xr.open_dataset(bdnc+'2001-2018-MODIS_BA_r10.nc').sel(lon=slice(lo1,lo2),lat=slice(la1,la2)).sum(dim=['lat','lon'])
        modis_m = modis.sel(time=modis['time.month'] == lt)
        print(modis)
        print(modis_m)
        pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(lon=slice(lo1,lo2),lat=slice(la1,la2),leadtime=lt,time=slice('2001','2019'))
        pred1d = pred.kprep.mean(dim=['lat','lon','ens'])
        obs1d = pred.obs.mean(dim=['lat','lon'])
    else:
        modis = xr.open_dataset(bdnc+'2001-2018-MODIS_BA_r10.nc').sel(lon=lon_click,lat=lat_click,method='nearest')
        modis_m = modis.sel(time=modis['time.month'] == lt).load()
        pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(lon=lon_click,lat=lat_click,method=str('nearest')).sel(leadtime=lt,time=slice('2001','2019'))
        pred1d = pred.kprep.mean(dim='ens')
        obs1d = pred.obs
        
        

    if PRINT: print('create_cor_fires - modis time',modis_m.time)
    pred1d = pred1d.assign_coords(time=modis_m.time) # Correct time, was base time iso valid time
    obs1d = obs1d.assign_coords(time=modis_m.time)  # Correct time, was base time iso valid time

    if PRINT: print('create_cor_fires - modis burned area',modis_m['burned_area'])
    if PRINT: print('create_cor_fires - krpep values',pred1d)
    
    cor_ba_kprep = scipy.stats.pearsonr(pred1d.values.squeeze()[:-1],modis_m['burned_area'].values.squeeze()[:-1])
    cor_ba_obs = scipy.stats.pearsonr(obs1d.values.squeeze()[:-1],modis_m['burned_area'].values.squeeze()[:-1])

    data = xr.merge([modis_m / 1.e6,obs1d,pred1d]).drop('leadtime').to_dataframe()
    # Rewrite data in order to use plotly express
    data_melt = data.dropna().melt(id_vars='burned_area', value_vars=['obs', 'kprep']) 

    fig = px.scatter(data_melt, x='value', y='burned_area', color='variable',trendline='ols')
    fig.data[-1].name = 'Diner'
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
            title = 'Correlation between burned area and observed and forecasted MDC (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            autosize=False,
            height=500,
            #yaxis=dict(title='Burned Area [km2]'),
            ))
    fig.update_yaxes(title_text="Burned Area [km2]")
    fig.update_xaxes(title_text="MDC [-]")
    #fig.update_yaxes(title_text="Monthly Drought Code [-]", secondary_y=True)

    print(' ')
    print('>>> Finished create_cor_time_series <<<')
    print(' ')        
    
    return(fig)

    
def create_time_series(clickData,base_time,valid_time,variable='MDC (from TP)'):
    print(' ')
    print('>>> Starting create_time_series <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
          
    #month = np.int(fc_time[5:])
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    name1 = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']
    
    
    predictand = variables[variable]

    
    ## Orig data
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(leadtime=lt)
    pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest'))
    
    time_pd = pred1d.time.to_pandas()
    kprep_mean = pred1d['kprep'].mean(dim='ens').values
    kprep_qt = pred1d['kprep'].quantile([0.05,0.95],dim='ens')
    clim_mean = pred1d['clim'].mean(dim='ens').values
    clim_qt = pred1d['clim'].quantile([0.05,0.95],dim='ens')
    trend = pred1d['trend'].mean(dim='ens').values
    #print(bdnc+'predadata_v2_'+predictand+name1)
    #print(pred1d)
    obs1d = pred1d.obs.sel(time=pred1d.obs['time.month']==st).load()
    
    # Ref data
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2).sel(leadtime=lt)
    pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest'))
    #time_pd = pred1d.time.to_pandas()
    kprep_mean_ref = pred1d['kprep'].mean(dim='ens').values
    kprep_qt_ref = pred1d['kprep'].quantile([0.05,0.95],dim='ens')
    
    
    
    #obs_nc = xr.open_dataset(bdnc+'predadata_v2_'+predictand+name1)
    #obs1d = obs_nc.to_array().sel(lat=lat_click,lon=lon_click,method='nearest',time=pred1d.obs['time.month']==st).load()
    time_pd_long = obs1d.time.to_pandas()
    
    #print(time_pd)
    #print(len(time_pd))
    print(' ')
    print('>>> Finished create_time_series <<<')
    print(' ')    
    return(
        go.Figure(
        data=
            [go.Scatter(x=time_pd,y=kprep_qt.sel(quantile=0.05).values,mode='lines',fillcolor='rgba(0,100,80,0.2)',line=dict(color='rgba(0,100,80,0.2)'),opacity=0.9,showlegend=False)]
            +
            [go.Scatter(x=time_pd,y=kprep_qt.sel(quantile=0.95).values,mode='lines',fill='tonexty',fillcolor='rgba(0,100,80,0.2)',line=dict(color='rgba(0,100,80,0.2)'),opacity=0.9,name='For. spread (2'+u"\u03C3"+')')]
            +
            [go.Scatter(x=time_pd,y=pred1d['kprep'].isel(ens=0).values,mode='lines',name='ens0')]
            +
            [go.Scatter(x=time_pd,y=kprep_mean,mode='lines',name='Forecast',line=dict(color='blue',width=4))]
            +
            [go.Scatter(x=time_pd_long,y=obs1d.values.squeeze(),mode='lines',name='Observations',line=dict(color='black'))]
            +[go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.05).values,mode='lines',name='Climatology',showlegend=False,line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=clim_qt.sel(quantile=0.95).values,mode='lines',name='Climatology',showlegend=False,line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=clim_mean,mode='lines',name='Climatology',line=dict(color='green'))]
            +[go.Scatter(x=time_pd,y=trend,mode='lines',name='Trend CO2',line=dict(color='red'))]
            #+[go.Scatter(x=time_pd,y=pred1d['obs'].values,mode='lines',name='Observations',line=dict(color='black'))]
            ,
            #),

        layout = go.Layout(
            title = 'Time series of the forecast, forecast only on CO2, climatology and observations (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            #height =  225,
            #margin = {'l': 20, 'b': 30, 'r': 10, 't': 10},
            autosize=False,
            #width=800.,
            #height=400.,
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
      
def create_bar_plot(clickData,plot_type,variable,base_time,valid_time):
    print(' ')
    print('>>> Starting create_bar_plot <<<')
    print(' ')
    
    predictand = variables[variable]
    if clickData == None: clickData = clickData_start

    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']        
        
    st = base_times[base_time]
    lt = valid_times[valid_time]
    name = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    
    # Load data
    pred_1d = xr.open_dataset(bdnc+'pred_v2_'+predictand+'_'+name2).sel(leadtime=lt,lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=-1)
    #for_anom = pred_1d['kprep'].mean(dim='ens')
    for_anom = pred_1d['kprep'].isel(ens=0)
    #co2_anom = pred_1d['trend'].mean(dim='ens')
    co2_anom = pred_1d['trend'].isel(ens=0)
    beta_1d = xr.open_dataset(bdnc+'beta_v2_'+predictand+'_'+name2).sel(leadtime=lt,lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=-1)
    predo_1d = xr.open_dataset(bdnc+'predodata_3m_fit_'+predictand+'_'+name).sel(lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=-1)
    predos = list(predo_1d.data_vars)
    sigp = ~np.isnan(beta_1d.beta.values)
    nr_sigp = np.sum(sigp)
    traces=[]
    fig = tls.make_subplots(rows=1,cols=1)
    #import pdb;pdb.set_trace()
    if nr_sigp == 0:
        print('no significant predictors..')
        return(fig)
    
    else:
        print('barplot - nr of significant predictors is ',nr_sigp)
        #print(np.asarray(predos))
        #print(sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        #print(predo_1d.to_array(dim='predictors').values*beta_1d.beta.values)
        #print(sigp)
        print('anomaly forecast is: ',for_anom.values)
        #print(predo_1d.to_array(dim='predictors').values)
        #print(beta_1d.beta.values)
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
            #width=500.,
            autosize=False,
            title='Individual contribution predictors (lat='+str(lat_click)+', lon='+str(lon_click)+')',
            yaxis=dict(title=variable+' '+plot_dict[predictand]['Forecast anomalies']['units']),
            )
   
        #fig = go.Figure(data=Data([trace]), layout=layout)
        fig = go.Figure(data=[trace], layout=layout)     
        return(fig)


        
def create_po_timeseries(clickData,variable,base_time,valid_time):
    print(' ')
    print('>>> Starting create_po_timeseries <<<')
    print(' ')
    
    if clickData == None: clickData = clickData_start
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    name = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    #month = np.int(fc_time[5:])
    #season = monthzz[month:month+3]
    year = 2018
    
    lat_click=clickData['points'][0]['y']
    lon_click=clickData['points'][0]['x']   
    
      
    tt = base_times[base_time]
    
    
    # Load monthly data for predictions
    pred = xr.open_dataset(bdnc+'pred_v2_'+variables[variable]+'_'+name2)#.sel(lon=lon_click,lat=lat_click,method=str('nearest'))
    pred_1d = pred.sel(leadtime=lt,lon=lon_click,lat=lat_click,method=str('nearest'))
    for_anom = pred_1d['kprep'].mean(dim='ens').isel(time=-1).values
    co2_anom = pred_1d['trend'].mean(dim='ens').isel(time=-1).values
    beta_1d = xr.open_dataset(bdnc+'beta_v2_'+variables[variable]+'_'+name2).sel(leadtime=lt,lon=lon_click,lat=lat_click,method=str('nearest'))#.isel(time=-1)
    print(beta_1d)
    # Load predictor data (fitted)
    predo = xr.open_dataset(bdnc+'predodata_3m_fit_'+variables[variable]+'_'+name)
    print(bdnc+'predodata_3m_fit_'+variables[variable]+'_'+name)
    predo_1d = predo.sel(lon=lon_click,lat=lat_click,method='nearest')
    print(predo_1d.NINO34.values)
    predos = list(predo_1d.data_vars)
    beta_1d = beta_1d.assign_coords(predictors=predos)
    sigp = ~np.isnan(beta_1d.beta.values).all(axis=0)
    print('high there')
    print(sigp,beta_1d.beta)
    nr_sigp = np.sum(sigp)
    time_pd = predo_1d.time.to_pandas()
    time_pd_beta = beta_1d.time.to_pandas()
    traces=[]
    xaxs = ['x1','x2','x3','x4','x5','x6','x7','x8']
    yaxs = ['y1','y2','y3','y4','y5','y6','y7','y8']
    specs=[[{'secondary_y':True}] for i in range(8)]
    fig = make_subplots(rows=np.int(nr_sigp), specs=specs[:nr_sigp])

    if nr_sigp == 0:
        print('no significant predictors..')
        return()
    else:
        print('timeseries plot - nr of significant predictors is ',nr_sigp)
        print('sig predictors: ',np.asarray(predos)[sigp])
        for ii,pre in enumerate(np.asarray(predos)[sigp]):
            print(pre)
            fig.add_trace(go.Scatter(
                x=time_pd,
                y=predo_1d[pre].values,
                xaxis=xaxs[ii],
                yaxis=yaxs[ii],
                text=pre,
                textposition='top center',
                name=pre,
                ),
                row=ii+1,col=1,secondary_y=False)
            fig.add_trace(go.Scatter(
                x=time_pd_beta, 
                y=beta_1d.beta.sel(predictors=pre).values.squeeze()*predo_1d[pre].values[10:],
                xaxis=xaxs[ii],
                yaxis=yaxs[ii],
                name="beta (regr. coef.)",
                ),
                row=ii+1,col=1,secondary_y=True)
        print(time_pd)            
        print(beta_1d.beta.sel(predictors=pre))
        fig['layout'].update(   autosize=False,
                                title='Time series of (fitted) predictor data (lat='+str(lat_click)+', lon='+str(lon_click)+')',
                            )
        
        return(fig)
    
def create_mapp(clickData,predictand,predictor,region,base_time,valid_time,data_name):
    print(region)
    #month = np.int(fc_time[5:])
    season = valid_time
    year = 2018
    
    st = base_times[base_time]
    lt = valid_times[valid_time]
    
    if clickData == None:
        lat_click = 0
        lon_click = 0
    else:
        lat_click=clickData['points'][0]['y']
        lon_click=clickData['points'][0]['x']
    
    #print(fc_time)
    #if data_name == 'cor_predictors':
    #    data_name2 = 'cor_orig'
    #else: data_name2 = 'cor_stepwise'
    data_name2 = 'sig'+data_name[3:]
    name = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    print(predictand)
    print(variables)
    print('hoi',bdnc+'cor_pred/'+data_name+'_'+variables[predictand]+'_'+name)
    cor_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name+'_'+variables[predictand]+'_'+name)[variables_pred[predictor]]
    sig_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name2+'_'+variables[predictand]+'_'+name)[variables_pred[predictor]]
    #cor_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name+'_'+variables_prad[predictand]+'_'+str(month).zfill(2)+'.nc')[variables_pred[predictor]]
    #sig_pred = xr.open_dataset(bdnc+'cor_pred/'+data_name2+'_'+variables_prad[predictand]+'_'+str(month).zfill(2)+'.nc')[variables_pred[predictor]]
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
        titel2 = 'No fit, The predictor data is the previous 3 month mean'
    else:
        titel2 = 'Differce in correlation (fisher transformed), fitted - nofit'
    #fig = go.Contour(
    print(sig_pred)
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
   
def create_map1(clickData,predictand,predictor,region,base_time,valid_time):
    return create_mapp(clickData,predictand,predictor,region,base_time,valid_time,'cor_predictors_fit')
    
   
def create_map2(clickData,predictand,predictor,region,base_time,valid_time):    
    return create_mapp(clickData,predictand,predictor,region,base_time,valid_time,'cor_predictors_nofit')
   
   
def create_xyplot(clickData,predictand,predictor,base_time,valid_time):
    #mo = np.int(fc_time[5:])
    if clickData == None:
        lat_click = 0
        lon_click = 0
    else:
        lat_click=clickData['points'][0]['y']
        lon_click=clickData['points'][0]['x']
    #print('Hello2!!')
    #print(lat_click,lon_click)
    #print(fc_time)           
    #print lat_click
    #tt = dict_times[fc_time]
    
    st = base_times[base_time]
    lt = valid_times[valid_time]    
    
    name = str(st)+'_'+str(lt)+'.nc'
    name2 = str(st)+'.nc'
    
    pred = xr.open_dataset(bdnc+'predodata_3m_nc_'+variables[predictand]+'_'+name)
    predfit = xr.open_dataset(bdnc+'predodata_3m_fit_'+variables[predictand]+'_'+name)
    #print(predictor)
    if predictor == 'CO2':
        prad = xr.open_dataset(bdnc+'predadata_v2_'+variables[predictand]+name)
    else:
        prad = xr.open_dataset(bdnc+'predadata_3m_nc_'+variables[predictand]+'_'+name)
    # Select right location and time slice
    #pred1d = pred.sel(lon=lon_click,lat=lat_click,method=str('nearest')).isel(time=slice(None,-tt))
    try: 
        #print('try for 3d predictor..')
        pred1d = pred[variables_pred[predictor]].sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(pred['time.month']==st))
        pred1d_fit = predfit[variables_pred[predictor]].sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(pred['time.month']==st))
    except ValueError:
        #print('.. went for 1d predictor')
        pred1d = pred[variables_pred[predictor]].sel(time=(pred['time.month']==st))
        pred1d_fit = predfit[variables_pred[predictor]].sel(time=(pred['time.month']==st))
        
    prad1d = prad.sel(lon=lon_click,lat=lat_click,
        method=str('nearest')).sel(time=(prad['time.month']==st))
    #print(pred1d)
    time_pd = pred1d.time.to_pandas()
    xdata = prad1d.to_array().values[0]
    y_orig = pred1d.values[:len(xdata)]
    y_fit = pred1d_fit.values[:len(xdata)]

    cor_orig = str(scipy.stats.pearsonr(xdata[10:],y_orig[10:]))[1:5]
    cor_fit = str(scipy.stats.pearsonr(xdata[10:],y_fit[10:]))[1:5]
    
    trace1 = go.Scatter(x=xdata[10:],y=y_orig[10:],mode='markers',name='original  '+cor_orig,marker=dict(color='blue'))
    trace2 = go.Scatter(x=xdata[10:],y=y_fit[10:],mode='markers',name='model fit '+cor_fit,marker=dict(color='green'))
    
    return( go.Figure(data = Data([trace1,trace2]),
                       layout = go.Layout(
                            title = 'Scatter plot of '+predictand+' with '+predictor+', lat='+str(lat_click)+', lon='+str(lon_click),
                            #height =  225,
                            margin = {'l': 20, 'b': 30, 'r': 10, 't': 30},
                            autosize=False,
                            width=500.,
                            height=500.,
                            xaxis=dict(title=predictand),
                            yaxis=dict(title=predictor),
                            )
                        )
        )    
