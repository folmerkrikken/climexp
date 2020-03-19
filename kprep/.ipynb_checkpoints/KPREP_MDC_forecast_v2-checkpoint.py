# -*- coding: utf-8 -*-
import os, sys, glob, re, pickle, time
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg') #Needed for parallel running
import matplotlib.pyplot as plt
import urllib.request, urllib.error, urllib.parse
from KPREP_forecast_v2_tools import *
import xarray as xr
import pandas as pd
import datetime
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

## TODO
# Check for valid values of climate indices, if the timestap is updated does not indicate the value is updated..
## Fix causal hindcast

dt = datetime.date.today()
#date_list = [dt.year, dt.month, dt.day]
start0 = time.time()

predictands = ['TMAX','PRECIP','MDC']#,'MDC_FROM_TP']
#predictands = ['MDC']
predictands = ['MDC_FROM_TP']
#predictands = ['PRECIP']

# Load these predictors, this does not mean that these are neceserally used.. see predictorz for those
predictors = ['CO2EQ','NINO34','PDO','AMO','IOD','TMAX','PRECIP','PERS','PERS_TREND']

# NAMELIST

## Resolution, currently only 25 or 50 is supported..
resolution = 10             # 10, 25 or 50

## Redo full hindcast period and remove original nc output file?
overwrite = True
## Redo a specific month / year?
overwrite_m = False          # Overwrite only the month specified with overw_m and overw_y
overw_m = 2                 # Jan = 1, Feb = 2.. etc
overw_y = 2019

time_end = '2018-12-01'

## Update indices if possible
UPDATE = True

## Save a figure with the correlation between predictors and predictand
PLOT_PREDCOR = True

##
VALIDATION = True           # Validates and makes figures of predicted values 

DYN_MONAVG = False          # Include the dynamical monthly averaging in the predictors
MLR_PRED = True             # Include the trend of the last 3 month as predictor

FORECAST = True             # Do forecast for given date?
HINDCAST = True             # Validate forecast based on hindcasts?
CROSVAL = True              # Use cross-validation for validation
CAUSAL = False              # Use causal method for validation
cv_years = 3                # Leave n out cross validation

## Validation period is 1961 - current

ens_size =      51
styear  =       1951    # Use data from this year until current
stvalyear =     1961    # Start validation from this year until previous year
endyear =       dt.year
endmonth =      dt.month-1  # -1 as numpy arrays start with 0
endyear = 2018
endmonth = 12

# Set working directories
bd = os.getcwd()
if bd == '/home/folmer/climexp/kprep': # We're home
    bd_data = '/home/folmer/climexp_data/KPREPData/'
else: # We're on climate explorer
    bd_data = '/home/oldenbor/climexp_data/KPREPData/'

bdid = bd_data+'inputdata/'
bdp = bd_data+'plots_mdc/'
bdnc = bd_data+'ncfiles_mdc/'

# Make directories if not already present
if not os.path.isdir(bd_data+'targetgrid'): os.system('mkdir -p '+bd_data+'targetgrid')
if not os.path.isdir(bdid): os.system('mkdir -p '+bdid)
if not os.path.isdir(bdp): os.system('mkdir -p '+bdp)
if not os.path.isdir(bdnc): os.system('mkdir -p '+bdnc)
if not os.path.isdir(bdnc+'cor_pred'): os.system('mkdir -p '+bdnc+'cor_pred')

# Defining some arrays used for writing labels and loading data
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthzz = 'JFMAMJJASONDJFMAMJJASOND'

print('Data from Jan '+str(styear)+' up to '+str(months[dt.month-2])+' '+str(dt.year))

print('Predictands = ',predictands)
print('Predictors = ',predictors)
print('Horizontal resolution is ',str(resolution/10.),' degrees')


# Create list of dates used
times = pd.date_range(str(styear)+'-01',str(dt.year)+'-'+str(dt.month),freq='M')

# ******************************************************************************
# First compute the MDC based on monthly Tmax (Berkely) and precipitation (GPCC)
# ******************************************************************************



# ************************************************************************
# Read in predictand data for fitting 
# ************************************************************************
start1 = time.time()
print('-- Read in predictand data for fitting --')
predictorz = []     # Predefine empty array, fill with specified predictors for predictand

#UPDATE_INDICES = check_updates2(inputdir=bdid) # if data can be update then returns TRUE
#if UPDATE_INDICES and UPDATE:
    #import subprocess
    #print("start updating monthly observations")
    #subprocess.check_call(["./update_indices.sh",str(resolution)])
    #print("done updating monthly observations")

#predictorz = ['CO2EQ','NINO34','PDO','AMO','IOD','CPREC','TMAX']
predictorz = []
    
# First calculate the mdc

# Get PREC and create climatology and anomalies
prec_long = xr.open_dataset(bdid+'gpcc_10_combined.nc',decode_times=False).squeeze().drop('level').precip.to_dataset()
prec_long = decode_timez(prec_long)
prec = prec_long.sel(time=slice(str(styear-1),time_end),lat=slice(72,0))
# Data is in mm/day.. go to mm/month
prec = prec * 30. # Assuming 30 day month now, update later to specific days in month #TODO

prec = prec.rename({'precip':'PRECIP'})
prec_clim = prec.sel(time=(prec['time.year']>1979) & (prec['time.year']<2011)).groupby('time.month').mean('time')
prec_clim.to_netcdf(bdnc+'prec_climatology.nc')
prec_anom = (prec.groupby('time.month') - prec_clim).drop('month')

        
# Then get TMAX, create climatology (already anomalies)
tmax_long = xr.open_dataset(bdid+'berk_tmax_1x1.nc',decode_times=False).temperature.rename({'latitude':'lat','longitude':'lon'}).to_dataset()
times_tmax = pd.date_range('1850-01-01',str(dt.year)+'-'+str(dt.month),freq='MS')
tmax_long = tmax_long.assign_coords(time=times_tmax[:len(tmax_long.time)])
#tmax_long.time.values = times_tmax[:len(tmax_long.time)]

tmax_clim = xr.open_dataset(bdid+'berk_tmax_1x1.nc',decode_times=False).climatology.rename({'latitude':'lat','longitude':'lon','month_number':'month'}).to_dataset()
tmax_clim = tmax_clim.assign_coords(month=np.arange(1,13,dtype='int')).rename({'climatology':'TMAX'})
tmax_clim.to_netcdf(bdnc+'tmax_climatology.nc')

tmax_anom = tmax_long.sel(time=slice(str(styear-1),time_end),lat=slice(72,0)).load()
tmax = ((tmax_anom.temperature.groupby('time.month') + tmax_clim.TMAX).drop('month')).to_dataset(name='TMAX')
tmax_anom = tmax_anom.temperature.to_dataset(name='TMAX') # Make the syntax the same as prec_anom

# Then calcualte the MDC  and construct anomalies relative to 1980-2010
mdc = mdi(tmax['TMAX'],prec.rename({'PRECIP':'precip'})) # Construct MDC from observations 
mdc_clim = mdc.sel(time=(mdc['time.year']>1979) & (mdc['time.year']<2011)).groupby('time.month').mean('time')
mdc_anom = (mdc.groupby('time.month') - mdc_clim).drop('month').rename({'mdc':'mdc_anom'})
mdc['mdc_anom'] = mdc_anom.to_array().squeeze().drop('variable')
mdc.time.attrs = {'standard_name':'time','long_name':'Time'}
mdc.to_netcdf(bdnc+'mdc_obs.nc')

    
  
for p,predictand in enumerate(predictands):

    if predictand == 'MDC':
        # First get precipation, need actual values, not anomalies
        predictorz.append(['CO2EQ','NINO34','PDO','AMO','IOD','PRECIP','TMAX','PERS'])

        if 'predadata' in locals():
            predadata = xr.merge([predadata,mdc.mdc_anom.to_dataset(name='MDC').astype('float32')])
        else:
            predadata = mdc.mdc_anom.to_dataset(name='MDC').astype('float32')
        
        #del(mdc)
        
    elif predictand == 'TMAX':
        predictorz.append(['CO2EQ','NINO34','PDO','AMO','IOD','PERS','PRECIP'])
        
        # To forecast anomalies use tmax_anom, to forecast real values use tmax
        if 'predadata' in locals():
            predadata = xr.merge([predadata,tmax_anom.astype('float32')])
        else:
            predadata = tmax_anom.astype('float32')
        #del(tmax)
        
    elif predictand == 'PRECIP':
        # These predictors are selelected for GPCCcom in the first predictor selection step
        predictorz.append(['CO2EQ','NINO34','PDO','AMO','IOD','PERS'])


        if 'predadata' in locals():
            predadata = xr.merge([predadata,prec_anom.astype('float32')])
        else:
            predadata = prec_anom.astype('float32')
        #del(prec)
        
    elif predictand == 'MDC_FROM_TP':
        continue

    else:
        print('predictand not yet known.. exiting!')
        sys.exit()

if 'predadata' in locals():
    predadata.time.attrs = {'standard_name':'time','long_name':'Time'}
 
print('-- Done reading in predictand data for fitting, time = ',str(np.int(time.time()-start1)),' seconds --') 
#sys.exit()

# ************************************************************************
# Read in predictor data for fitting 
# ************************************************************************
start1 = time.time()
print('-- Read in predictor data for fitting --')

indices_locs = {'CO2EQ':bdid+'RCP45_CO2EQ_mo.dat',
                'NINO34':bdid+'ersst_nino3.4a.dat',
                'QBO':bdid+'qbo?.dat',
                'IOD':bdid+'dmi_ersst.dat',
                'PDO':bdid+'pdo_ersst.dat',
                'AMO':bdid+'amo_ersst_ts.dat',
                'PERS':'not needed',
                'PERS_TREND':'not needed'}

# Load predictors (time,lat,lon)
for pred in predictors:
    print(pred)
    if pred in ['PERS','PERS_TREND']:
        continue

    elif pred == 'PRECIP':    # Cum precip [time,lat,lon] - 1901 -current
        if 'predodata' in locals(): 
            predodata = xr.merge([predodata,prec_anom.astype('float32')])
        else: predodata = prec_anom
        #del(prec)
        
    elif pred == 'TMAX':
        if 'predodata' in locals(): 
            predodata = xr.merge([predodata,tmax_anom.astype('float32')])
        else: predodata = tmax_anom        
        #del(tmax)
        
    else:
        df = load_clim_index(indices_locs[pred],styear-1,endyear,endmonth,pred)
        #print(df)
        if 'predodata' in locals():
            predodata = xr.merge([predodata,df.astype('float32')])    
        else: predodata = df
      
        
print('-- Done reading in predictor data for fitting, time = ',str(np.int(time.time()-start1)),' seconds --') 
if 'level' in predodata.coords: predodata = predodata.squeeze().drop(['level'])
if 'month' in predodata.coords: predodata = predodata.squeeze().drop(['months'])
if 'predadata' in locals():
    if 'level' in predadata.coords: predadata = predadata.squeeze().drop(['level'])
    if 'month' in predadata.coords: predadata = predadata.squeeze().drop(['months'])
    
#sys.exit()
# TODO > Sanity check on data, put somewhere here..

# *************************************************************************   
# Now start the predictor selection and the forecasting / hindcasting loop
# *************************************************************************

for p,predictand in enumerate(predictands):
    if predictand == 'MDC_FROM_TP':
        print('skip all forecasting stuff, direct to validation etc')
    else:
        # Fill persistence predictor with predictand data
        if 'PERS' in predictorz[p]:
            if 'PERS' in predodata:  predodata = predodata.drop('PERS')
            predodata = xr.merge([predodata,predadata[predictand].rename('PERS')])
        
        print('Predictand: ',predictand)
        print('Predictors: ',predictorz[p])

        if overwrite:
            print('overwrite is True, so remove all data and redo complete forecast cycle')
            mon_range = list(range(12))
            filez = glob.glob(bdnc+'*'+predictand+'*.nc')+ glob.glob(bdnc+'cor_pred/*'+predictand+'*.nc')
            for fil in filez: os.remove(fil)
        elif overwrite_m:
            mon_range = [overw_m]
            
            #filez = glob.glob(bdnc+'*'+predictand+'_'+str(overw_m).zfill(2)+'.nc')
            #for fil in filez: os.remove(fil)
            
        else:
            mon_range = [dt.month-1]

        # Rolling 3-month mean, first and last timestep become nans, so remove last timestep (slice(None,-1))
        # use predictorz[p][:-1] to exclude 'PERS_TREND' from this operation as this predictor is added later
        if 'PERS_TREND' == predictorz[p][-1]: # PERS_TREND should be last of predictorz
            predodata_3m = predodata[predictorz[p][:-1]].rolling(time=3,center=True).mean()#.isel(time=slice(None,-1))
        else:
            predodata_3m = predodata[predictorz[p]].rolling(time=3,center=True).mean()#.isel(time=slice(None,-1))
            
        #sys.exit()

        #predodata_3m = predodata_3m.assign(PERS=predodata['PERS'])
        # For March use previous last years value as PERS predictor
        #predodata_3m
        
        # No rolling mean over predadata cause we predict 1 month at a time, but keep _3m for consistency with other forecast script
        #predadata_3m = predadata[predictand]
        
        # Change time values of predictor and predictand data for simplicity. Add 2 months for predictor data and subtract 2 months for predicand data. This means the dates do not represent the exact time off the data anymore, but is much easier for selecting the right training / testing data etc.
        #predodata_3m['time'].values = pd.to_datetime(predodata_3m['time'].values) + pd.DateOffset(months=2)
        predodata_3m = predodata_3m.assign_coords(time=pd.to_datetime(predodata_3m['time'].values) + pd.DateOffset(months=2))
        predodata_3m = predodata_3m.isel(time=slice(None,-1)) # Throw out last year because it only has nans due to 3-month rolling mean
        
        # Use the previous month MDC as PERS predictor, and use the last years value as predictor for the first month when the MDC is calculated, i.e. overwintering
        if predictand == 'MDC':
            tmp_dmc = np.roll(predadata.MDC.values,-1,axis=0) # Roll needed because of changed time. Shift 1 hour iso 2 hours because no 3-month mean is performed
            tmp_dmc[0::12][1:] = tmp_dmc[8::12][:-1] # Fill february with last years value
            tmp_dmc[1::12][1:] = tmp_dmc[8::12][:-1] # Fill march with last years value
            
            predodata_3m['PERS'] = (('time','lat','lon'),tmp_dmc[:-1,:])
            #sys.exit()
        # Throw out first year
        predodata_3m = predodata_3m.sel(time=slice('1951',None))

    
    if MLR_PRED and not predictand == 'MDC_FROM_TP': 
        print('MLR_PRED is True, calculating trend over previous 3 months for all predictors')
        #sys.exit()
        #predodata_3m_trend = pred_trend(predodata[predictorz[p][:-1]]).isel(time=slice(None,-1))
        if 'PERS_TREND' in predictorz[p]:
            predodata_3m_trend = predodata[predictorz[p][:-1]].rolling(time=3,center=True).reduce(calc_trend) 
        else:
            predodata_3m_trend = predodata[predictorz[p]].rolling(time=3,center=True).reduce(calc_trend) 
        #predodata_3m_trend['time'].values = pd.DatetimeIndex(predodata_3m_trend['time'].values) + pd.DateOffset(months=2)
        predodata_3m_trend = predodata_3m_trend.assign_coords(time=pd.to_datetime(predodata_3m_trend['time'].values) + pd.DateOffset(months=2))
    #sys.exit()
    
    for st in range(3,10): # normally 3,10 - Loop over start dates from March to September 
        print('  ')
        print('prediction month = ',months[st-1])
        #print('predictor season = ', '-'.join([months[st-3],months[st-2],months[st-1]]))
        #lt_range = np.arange(4+(st-3),6)
        lt_range = np.arange(4+(st-3),11)
        #lt_range = np.arange(4+(st-3),4+(st-3)+1)
        #sys.exit()
        if predictand == 'MDC_FROM_TP':
            #if st == 4: sys.exit()
            # First load tmax and precip forecast and construct anomalies
            tm_anom = xr.open_dataset(bdnc+'pred_v2_TMAX_'+str(st)+'.nc').sel(quantile=0.5).squeeze().drop('quantile')
            tm_clim = xr.open_dataset(bdnc+'tmax_climatology.nc').rename({'month':'leadtime'})
            tm = tm_anom.kprep + tm_clim['TMAX'].sel(leadtime=tm_anom.leadtime.values)
            del(tm_clim,tm_anom)
            pr_anom = xr.open_dataset(bdnc+'pred_v2_PRECIP_'+str(st)+'.nc').sel(quantile=0.5).squeeze().drop('quantile')#mean(dim='ens').squeeze()
            pr_clim = xr.open_dataset(bdnc+'prec_climatology.nc').rename({'month':'leadtime'})#.drop('level')
            pr = pr_anom.kprep + pr_clim.sel(leadtime=pr_anom.leadtime.values)
            del(pr_clim,pr_anom)
            
            # Now construct MDC based on tmax and precip forecasts, if start time (st) larger
            # than 3, then put observed tmax and precip before the forecasted values
            old_leadtimes = tm.leadtime.values
            montz = {4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OKT'}
            #if st == 4: sys.exit()
            for elt in np.arange(4,11)[~np.isin(np.arange(4,11),old_leadtimes)]:
                print(st,'hellooo!!!!!',elt)
                # Construct time series that matches the times and leadtimes
                pd_times = pd.date_range(str(stvalyear),freq='AS-'+montz[elt],periods=len(tm.time))
                # Extract data at the correct times, and overwrite this time with the start date of the forecast
                tm_obs = tmax.TMAX.sel(time=pd_times).assign_coords(time=tm.time,leadtime=elt)
                prec_obs = prec.sel(time=pd_times).assign_coords(time=tm.time,leadtime=elt)
                tm = xr.concat([tm,tm_obs],dim='leadtime').sortby('leadtime')
                pr = xr.concat([pr,prec_obs],dim='leadtime').sortby('leadtime')

            # Now calculate the MDC and remove, if needed, the added leadtimes
            mdc_tp = mdi(tm,pr.rename({'PRECIP':'precip'}).squeeze()).sel(leadtime=old_leadtimes)
            print('shape mdc',st,mdc_tp.mdc.values.shape)
            #sys.exit()
            del(tm,pr)
            
            # Climatology based on forecasted mdc, is this right???
            mdc_clim_tp = mdc_tp.sel(time=(mdc_tp['time.year']>1979) & (mdc_tp['time.year']<2011)).groupby('time.month').mean('time').drop('month')
            mdc_tp_anom = (mdc_tp.groupby('leadtime') - mdc_clim_tp).squeeze()
            del(mdc_tp)
            if len(lt_range) == 1:
                mdc_tp_anom = mdc_tp_anom.expand_dims('leadtime',axis=0) #assign_coords(leadtime=lt).
            #obs_mdc = xr.open_dataset(bdnc+'pred_v2_MDC_'+str(st)+'.nc').obs
            obs_mdc = xr.open_dataset(bdnc+'mdc_obs.nc').mdc_anom
            
            # Rewrite data to have same years-months and leadtimes
            obs_mdc_lt = xr.full_like(mdc_tp_anom,np.nan)
            for i,leadt in enumerate(lt_range):
                tim = pd.DatetimeIndex(mdc_tp_anom.time.values) + pd.DateOffset(months=leadt-mdc_tp_anom['time.month'][0].values)
                obs_mdc_lt.mdc[{'leadtime':i}] = obs_mdc.sel(time=tim).values
            # lets construct ensemble
            #residuals = mdc_tp_anom.mdc - obs_mdc_lt
            residuals = obs_mdc_lt - mdc_tp_anom.mdc

            
            timez = pd.to_datetime(mdc_tp_anom.time[:-1].values)
            tests = []
            [tests.append(timez[y:y+3]) for y in np.arange(np.array(np.where(timez.year == stvalyear)).squeeze(),len(timez),cv_years)]
            tests.append(pd.to_datetime(mdc_tp_anom.time[-1].values))
            #for y in np.arange(np.array(np.where(timez.year == stvalyear)).squeeze(),len(timez),cv_years):
            
            for lt in lt_range:
                print('leadtime: ',lt)
                ens = np.full((len(obs_mdc_lt.time),51,len(obs_mdc_lt.lat),len(obs_mdc_lt.lon)),np.nan)
                clim = np.full_like(ens,np.nan)
                trend = np.full_like(ens,np.nan)                
                for test in tests:
                    if endyear in np.array(test.year):
                        train = timez
                        ii = [list(pd.to_datetime(mdc_tp_anom.time.values)).index(test)]
                        test = [test]
                    else:
                        train = timez.drop(test)
                        ii = [list(pd.to_datetime(mdc_tp_anom.time[:-1].values)).index(i) for i in list(test)]
                    print(test,ii)
                    #train = timez.drop(test)
                    rand_yrs = np.random.choice(list(range(len(train))), 51, replace=True)
                    #print(i,)
                    ens[ii,0,:,:] = mdc_tp_anom.mdc.sel(leadtime=lt,time=test).values
                    ens[ii,1:,:,:] = residuals.mdc.sel(leadtime=lt,time=train).values[rand_yrs[1:],:,:][np.newaxis,:] + ens[ii,0,:,:][:,np.newaxis,:,:]
                    clim[ii,:] = obs_mdc_lt.mdc.sel(leadtime=lt,time=train).values[rand_yrs,:][np.newaxis,:]
                    #if len(lt_range) == 1: taxis = 0
                    #else: taxis = 1
                    a, b = linregrez(predodata['CO2EQ'].sel(time=train).values,
                                     mdc_tp_anom.mdc.sel(leadtime=lt,time=train).values, 
                                     BETA=True,taxis=0)[:2]
                    trend_train = a[np.newaxis,:] * predodata['CO2EQ'].sel(time=train).values[:,None,None] + b[np.newaxis, :, :]
                    trend_test = a[np.newaxis,:] * predodata['CO2EQ'].sel(time=test).values[:,None,None] + b[np.newaxis, :, :]
                    residuals_trend = trend_train - mdc_tp_anom.mdc.sel(leadtime=lt,time=train).values
                    trend[ii,0,:,:] = trend_test
                    trend[ii,1:,:,:] = residuals_trend[rand_yrs[1:],:,:][np.newaxis,:] + trend[ii,0,:,:][:,np.newaxis,:,:]

                data_fit_tot = mdc_tp_anom.sel(leadtime=lt).drop('leadtime').copy(deep=True)
                data_fit_tot['obs'] = (('time','lat','lon'),obs_mdc_lt.sel(leadtime=lt).mdc)
                data_fit_tot['kprep'] = (('time','ens','lat','lon'),ens)
                data_fit_tot['clim'] = (('time','ens','lat','lon'),clim)
                data_fit_tot['trend'] = (('time','ens','lat','lon'),trend)
                #data_fit_tot = data_fit_tot_lt.assign_coords(ens=range(1,52))
                #data_fit_tot.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'.nc')  
                    
            #sys.exit()
            #ens = mdc_tp_anom.mdc.values + residuals.values[:,rand_yrs,:,:]
#                             ## Now calculate forecast scores
#             sys.exit()
#             data_fit_tot_lt = mdc_tp_anom.copy(deep=True)
#             data_fit_tot_lt['obs'] = (('leadtime','time','lat','lon'),obs_mdc_lt.mdc)
#             data_fit_tot_lt['kprep'] = (('leadtime','time','quantile','lat','lon'),ens)
#             data_fit_tot_lt['clim'] = (('leadtime','time','quantile','lat','lon'),clim)
#             data_fit_tot_lt['trend'] = (('leadtime','time','quantile','lat','lon'),trend)
#             data_fit_tot_lt = data_fit_tot_lt.assign_coords(ens=range(1,52))
#             data_fit_tot_lt.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'.nc')                
                
            #for i,lt in enumerate(lt_range):
                print('Calculating skill scores') 
                #data_fit_tot = data_fit_tot_lt.sel(leadtime=lt)
                t0 = time.time()
                timez = pd.DatetimeIndex(data_fit_tot['time'].values)
                scores = xr.Dataset(coords={'lat': data_fit_tot['lat'],
                        'lon': data_fit_tot['lon'],
                        'time': timez[-1]}).expand_dims('time')

                # Calculate significance of ensemble mean
                tmp = data_fit_tot.kprep.isel(time=-1).median('ens').values
                posneg = tmp > 0.
                above = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values>0,axis=0)/51.)
                below = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values<0,axis=0)/51.)
                sig_ensmean = np.ones((len(data_fit_tot.lat),len(data_fit_tot.lon)))
                sig_ensmean[posneg] = above[posneg]
                sig_ensmean[~posneg] = below[~posneg]

                print('month = ',str(lt))
                # Create correlation scores and its significance
                cor,sig = linregrez(data_fit_tot.kprep.median('ens').isel(time=slice(None,-1)).values,data_fit_tot.obs.isel(time=slice(None,-1)).values,COR=True)

                scores['cor'] = (('time','lat','lon'),cor[np.newaxis,:,:])
                scores['cor_sig'] = (('time','lat','lon'),sig[np.newaxis,:,:])

                scores['rmsess'] = (('time','lat','lon'),                            f_rmse(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values,SS=True)[np.newaxis,:,:])

                scores['crpss'] = (('time','lat','lon'),                        f_crps2(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,SS=True,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values)[np.newaxis,:,:])


                scores['tercile'] = (('time','lat','lon'), tercile_category(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['kprep'].isel(time=-1).values)[np.newaxis,:,:])

                scores['for_anom'] = (('time','lat','lon'),data_fit_tot['kprep'].isel(time=-1).median(dim='ens').values[np.newaxis,:,:])

                scores['for_anom_sig'] = (('time','lat','lon'),sig_ensmean[np.newaxis,:,:])


                print('Calculated skill scores for '+months[lt-1]+', total time is '+str(np.round(time.time()-t0,2))+' seconds')

                if lt == lt_range[0]:
                    scores_lt = scores.assign_coords(leadtime=lt).expand_dims('leadtime')
                else:
                    scores_lt = xr.concat([scores_lt,scores.assign_coords(leadtime=lt)],dim='leadtime')

                # Make quantiles from the ensemble to reduce memory usage
                print('Calculating quantiles, this will take some time...')
                data_fit_tot_qt = data_fit_tot.quantile([0.05,0.50,0.95],dim='ens')
                print('Done calculating quantiles..')
                
                # Store the first value of the ensemble, which is the actual model fit. I need to store this to check if the sum of the individual
                # predictor contributions matches with the forecasted value. I'll store it in the quantile dimension with 'fc' label
                data_fit_tot_qt = xr.concat([data_fit_tot_qt,data_fit_tot.isel(ens=0).assign_coords(quantile=0.51)],dim='quantile')[['kprep','clim','trend']]
                # Add obs again, had to remove it for the previous concat
                data_fit_tot_qt = xr.merge([data_fit_tot_qt,data_fit_tot.obs])
                
                if lt == lt_range[0]:
                    data_fit_tot_lt = data_fit_tot_qt.assign_coords(leadtime=lt).expand_dims('leadtime')
                else:
                    data_fit_tot_lt = xr.concat([data_fit_tot_lt,data_fit_tot_qt.assign_coords(leadtime=lt)],dim='leadtime')
    
                del(data_fit_tot)

            data_fit_tot_lt.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'.nc')
            scores_lt.to_netcdf(bdnc+'scores_mdc_v2_'+predictand+'_'+str(st)+'.nc')              
            

            del(ens,obs_mdc_lt,clim,trend)
            
            #sys.exit()
            
        else:
                                     
            
            
            
            for lt in lt_range: # Loop over lead times
                
                print('lead time =',lt-st,'predictand month = ',months[lt-1])
                #print('lead time =',lt-st)
                
            
                # Change time values in the same way as the predictor data, lt-st is lead time
                predadata_3m = predadata[predictand].copy()
                #predadata_3m['time'].values = pd.DatetimeIndex(predadata_3m['time'].values) - pd.DateOffset(months=lt-st)
                predadata_3m = predadata_3m.sel(time=slice('1951',None))
                predadata_3m = predadata_3m.assign_coords(time = (pd.DatetimeIndex(predadata_3m['time'].values) - pd.DateOffset(months=lt-st)))
                #sys.exit()
                if HINDCAST and CROSVAL:
                    print('Hindcasting mode, leave ',str(cv_years),' out cross-validation')
                    timez = pd.DatetimeIndex(predodata['time'].sel(time=predodata['time.month']==st).values)[1:-1]

                    for y in range(np.array(np.where(timez.year == stvalyear)).squeeze(),len(timez),cv_years):
                        test = timez[y:y+3]
                        train = timez.drop(test)
                        print('predictand: ',predictand)
                        print('start time: ',st)
                        print('lead time: ',lt)
                        print('test years: ',test)
                        #sys.exit()
                        data_fit,beta_xr = regr_loop(predodata_3m,predodata_3m_trend,predadata_3m,timez,train,test,ens_size,bdnc,25,predictand,predictorz[p], MLR_PRED,FC=False,sig_val = 0.05,MDC=True,lt=lt) # hier wil ik naartoe
                        try:
                            data_fit_tot = xr.concat([data_fit_tot,data_fit],dim='time')
                            beta_xr_tot = xr.concat([beta_xr_tot,beta_xr],dim='time')
                        except NameError:
                            data_fit_tot = data_fit.copy()
                            beta_xr_tot = beta_xr.copy()
                        

                elif HINDCAST:
                    print('either CROSVAL or CAUSAL should be set to true')
                    sys.exit()

                if FORECAST:
                    print('Forecasting mode')
                    print('Forecasting lead time is: ',lt-st,'months')
                    timez = pd.DatetimeIndex(predodata_3m['time'].sel(time=predodata_3m['time.month']==st).values)
                    if timez[0].year == 1901: timez = timez[1:]

                    # In forecast mode, the last timestep is the test data, the rest is training data.
                    train = timez[:-1]
                    test = timez[-1]
                    print('test years: ',test)

                    data_fit,beta_xr = regr_loop(predodata_3m,predodata_3m_trend,predadata_3m,timez,train,test,ens_size,bdnc,25,predictand,predictorz[p],MLR_PRED,FC=True,sig_val = 0.05,MDC=True,lt=lt) # hier wil ik naartoe
                    
                    try:
                        data_fit_tot = xr.concat([data_fit_tot,data_fit],dim='time')
                        beta_xr_tot = xr.concat([beta_xr_tot,beta_xr],dim='time')
                    except NameError:
                        data_fit_tot = data_fit.copy()
                        beta_xr_tot = beta_xr.copy()
                
                # Make quantiles from the ensemble to reduce memory usage
                data_fit_tot_qt = data_fit_tot.quantile([0.05,0.50,0.95],dim='ens')
                
                # Store the first value of the ensemble, which is the actual model fit. I need to store this to check if the sum of the individual
                # predictor contributions matches with the forecasted value. I'll store it in the quantile dimension with 'fc' label
                data_fit_tot_qt = xr.concat([data_fit_tot_qt,data_fit_tot.sel(ens=1).assign_coords(quantile=0.51)],dim='quantile').drop('ens')[['kprep','clim','trend']]
                # Add obs again, had to remove it for the previous concat
                data_fit_tot_qt = xr.merge([data_fit_tot_qt,data_fit_tot.obs])
                
                if lt == lt_range[0]:
                    data_fit_tot_lt = data_fit_tot_qt.assign_coords(leadtime=lt).expand_dims('leadtime')
                    beta_xr_tot_lt = beta_xr_tot.assign_coords(leadtime=lt).expand_dims('leadtime')
                else:
                    data_fit_tot_lt = xr.concat([data_fit_tot_lt,data_fit_tot_qt.assign_coords(leadtime=lt)],dim='leadtime')
                    beta_xr_tot_lt = xr.concat([beta_xr_tot_lt,beta_xr_tot.assign_coords(leadtime=lt)],dim='leadtime')
                
                
                ## Now calculate forecast scores
                
                print('Calculating skill scores') 
            
                t0 = time.time()
                timez = pd.DatetimeIndex(data_fit_tot['time'].values)
                scores = xr.Dataset(coords={'lat': data_fit_tot['lat'],
                        'lon': data_fit_tot['lon'],
                        'time': timez[-1]}).expand_dims('time')

                # Calculate significance of ensemble mean
                tmp = data_fit_tot.kprep.isel(time=-1).mean('ens').values
                posneg = tmp > 0.
                above = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values>0,axis=0)/51.)
                below = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values<0,axis=0)/51.)
                sig_ensmean = np.ones((len(data_fit_tot.lat),len(data_fit_tot.lon)))
                sig_ensmean[posneg] = above[posneg]
                sig_ensmean[~posneg] = below[~posneg]

                print('month = ',str(lt))
                # Create correlation scores and its significance
                cor,sig = linregrez(data_fit_tot.kprep.mean('ens').isel(time=slice(None,-1)).values,data_fit_tot.obs.isel(time=slice(None,-1)).values,COR=True)

                scores['cor'] = (('time','lat','lon'),cor[np.newaxis,:,:])
                scores['cor_sig'] = (('time','lat','lon'),sig[np.newaxis,:,:])
                
                scores['rmsess'] = (('time','lat','lon'),                            f_rmse(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values,SS=True)[np.newaxis,:,:])
            
                scores['crpss'] = (('time','lat','lon'),                        f_crps2(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,SS=True,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values)[np.newaxis,:,:])
                
                if predictand != 'MDC_FROM_TP':
                    scores['crpss_co2'] = (('time','lat','lon'),
f_crps2(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,SS=True,ref=data_fit_tot['trend'].isel(time=slice(None,-1)).values)[np.newaxis,:,:])                                   
                
                scores['tercile'] = (('time','lat','lon'), tercile_category(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['kprep'].isel(time=-1).values)[np.newaxis,:,:])
                
                scores['for_anom'] = (('time','lat','lon'),data_fit_tot['kprep'].isel(time=-1).mean(dim='ens').values[np.newaxis,:,:])
                
                scores['for_anom_sig'] = (('time','lat','lon'),sig_ensmean[np.newaxis,:,:])
                

                print('Calculated skill scores for '+months[lt]+', total time is '+str(np.round(time.time()-t0,2))+' seconds')

                if lt == lt_range[0]:
                    scores_lt = scores.assign_coords(leadtime=lt).expand_dims('leadtime')
                else:
                    scores_lt = xr.concat([scores_lt,scores.assign_coords(leadtime=lt)],dim='leadtime')
                
                del(data_fit_tot,beta_xr_tot,scores)
                
            #data_fit_tot_lt_qt.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'.nc')
            #beta_xr_tot_lt.to_netcdf(bdnc+'beta_v2_'+predictand+'_'+str(st)+'.nc')
            
                    
            #sys.exit()
            #data_fit_tot.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'_'+str(lt)+'.nc')
            #beta_xr_tot.to_netcdf(bdnc+'beta_v2_'+predictand+'_'+str(st)+'_'+str(lt)+'.nc')
            #data_fit_tot_lt_qt = data_fit_tot_lt.quantile([0.05,0.50,0.95],dim='ens')
            #data_fit_tot_lt_qt = data_fit_tot_lt[['.quantile([0.05,0.50,0.95],dim='ens')
            #data_fit_tot_lt_qt = xr.concat([data_fit_tot_lt_qt
            
            # Save data to netcdf
            data_fit_tot_lt.to_netcdf(bdnc+'pred_v2_'+predictand+'_'+str(st)+'.nc')
            beta_xr_tot_lt.to_netcdf(bdnc+'beta_v2_'+predictand+'_'+str(st)+'.nc')
            scores_lt.to_netcdf(bdnc+'scores_mdc_v2_'+predictand+'_'+str(st)+'.nc')             
            

#         if VALIDATION:
#             for lt in lt_range:
                
#                 data_fit_tot = data_fit_tot_lt.sel(leadtime=lt)
#                 #data_fit_tot = data_fit_tot_lt.drop('leadtime')
                
#                 print('Calculating skill scores') 
            
#                 #data_fit = xr.open_dataset(bdnc+'pred_v2_'+predictand+'.nc')#,chunks={'lat':1})

#                 t0 = time.time()
#                 timez = pd.DatetimeIndex(data_fit_tot['time'].values)
#                 scores = xr.Dataset(coords={'lat': data_fit_tot['lat'],
#                         'lon': data_fit_tot['lon'],
#                         'time': timez[-1]}).expand_dims('time')

#                 # Calculate significance of ensemble mean
#                 tmp = data_fit_tot.kprep.isel(time=-1).sel(quantile=0.5).values
#                 posneg = tmp > 0.
#                 above = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values>0,axis=0)/51.)
#                 below = 1.-(np.sum(data_fit_tot.kprep.isel(time=-1).values<0,axis=0)/51.)
#                 sig_ensmean = np.ones((len(data_fit_tot.lat),len(data_fit_tot.lon)))
#                 sig_ensmean[posneg] = above[posneg]
#                 sig_ensmean[~posneg] = below[~posneg]

#                 print('month = ',str(lt))
#                 # Create correlation scores and its significance
#                 cor,sig = linregrez(data_fit_tot.kprep.mean('ens').isel(time=slice(None,-1)).values,data_fit_tot.obs.isel(time=slice(None,-1)).values,COR=True)

#                 scores['cor'] = (('time','lat','lon'),cor[np.newaxis,:,:])
#                 scores['cor_sig'] = (('time','lat','lon'),sig[np.newaxis,:,:])
                
#                 scores['rmsess'] = (('time','lat','lon'),                            f_rmse(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values,SS=True)[np.newaxis,:,:])
            
#                 scores['crpss'] = (('time','lat','lon'),                        f_crps2(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,SS=True,ref=data_fit_tot['clim'].isel(time=slice(None,-1)).values)[np.newaxis,:,:])
                
#                 if predictand != 'MDC_FROM_TP':
#                     scores['crpss_co2'] = (('time','lat','lon'),
# f_crps2(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['obs'].isel(time=slice(None,-1)).values,SS=True,ref=data_fit_tot['trend'].isel(time=slice(None,-1)).values)[np.newaxis,:,:])                                   
                
#                 scores['tercile'] = (('time','lat','lon'), tercile_category(data_fit_tot['kprep'].isel(time=slice(None,-1)).values,data_fit_tot['kprep'].isel(time=-1).values)[np.newaxis,:,:])
                
#                 scores['for_anom'] = (('time','lat','lon'),data_fit_tot['kprep'].isel(time=-1).mean(dim='ens').values[np.newaxis,:,:])
                
#                 scores['for_anom_sig'] = (('time','lat','lon'),sig_ensmean[np.newaxis,:,:])
                

#                 print('Calculated skill scores for '+months[lt]+', total time is '+str(np.round(time.time()-t0,2))+' seconds')

#                 if lt == lt_range[0]:
#                     scores_lt = scores.assign_coords(leadtime=lt).expand_dims('leadtime')
#                 else:
#                     scores_lt = xr.concat([scores_lt,scores.assign_coords(leadtime=lt)],dim='leadtime')
                
#             scores_lt.to_netcdf(bdnc+'scores_mdc_v2_'+predictand+'_'+str(st)+'.nc')
                
          
            

        if VALIDATION:
            #predictand = 'GCEcom' 
            print('Start validation for the last year in mon_range')
            #data_fit = xr.open_dataset(bdnc+'pred_v2_'+predictand+'.nc')
            #scores = xr.open_dataset(bdnc+'scores_v2_'+predictand+'.nc')
            for lt in lt_range:
                scores = scores_lt.sel(leadtime=lt)
                    
                if predictand == 'MDC' or predictand == 'MDC_FROM_TP':      
                    var = 'Monthly Drought Code'
                    clevz = np.array((-2.,-1.,-0.5,-0.2,0.2,0.5,1.,2.))
                    cmap1 = matplotlib.colors.ListedColormap(['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022'])
                    cmap2 = matplotlib.colors.ListedColormap(['#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400'])
                    cmap_under = '#000099'
                    cmap_over = '#cc0022'
                if predictand == 'TMAX':      
                    var = 'Monthly maximum temperature'
                    clevz = np.array((-2.,-1.,-0.5,-0.2,0.2,0.5,1.,2.))
                    cmap1 = matplotlib.colors.ListedColormap(['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022'])
                    cmap2 = matplotlib.colors.ListedColormap(['#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400'])
                    cmap_under = '#000099'
                    cmap_over = '#cc0022'
                    
                elif predictand == 'PRECIP':   
                    var = 'Surface precipitation' 
                    clevz = np.array((-200.,-100.,-50.,-20.,20.,50.,100.,200.))
                    cmap1 = matplotlib.colors.ListedColormap(['#993300','#cc8800','#ffcc00','#ffee99','#ffffff','#ccff66','#33ff00','#009933','#006666'])
                    cmap2 = matplotlib.colors.ListedColormap(['#cc8800','#ffcc00','#ffee99','#ffffff','#ccff66','#33ff00','#009933'])
                    cmap_under = '#993300'
                    cmap_over = '#006666'
                    
                elif predictand == '20CRslp':
                    var = 'Mean sea level pressure'
                    clevz=np.array((-4.,-2.,-1.,-0.5,0.5,1.,2.,4.))
                    cmap1 = matplotlib.colors.ListedColormap(['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022'])
                    cmap2 = matplotlib.colors.ListedColormap(['#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400'])
                    cmap_under = '#000099'
                    cmap_over = '#cc0022'

                
            
            


                #timez = pd.DatetimeIndex(data_fit['time'].sel(time=data_fit['time.month']==m+1).values)
                year = str(data_fit_tot_lt['time.year'][-1].values)        #str(timez[-1].year)
                #season = monthzz[m+1:m+4]
                season = months[lt-1]
                print('validation for '+season+' '+year)
                mon = str(st).zfill(2)
                monv = str(lt).zfill(2)
                bdpo = bdp+predictand+'/'+str(resolution)+'/'+year+mon+'_'+monv+'/'
                if not os.path.exists(bdpo):
                    os.makedirs(bdpo)
                var = predictand

                
                plot_climexp(scores.rmsess.isel(time=-1),
                                'RMSESS hindcasts, climatology as reference (1961-current)',
                                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+' | base time: '+months[st-1]+' '+year+' | valid time: '+months[lt-1]+' '+year,
                                predictand = predictand,
                                fname=bdpo+predictand+'_rmsess_'+year+mon+'_'+monv+'.png',
                                clevs = np.array((-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5)),
                                cmap=cmap2,
                                cmap_under = cmap_under,
                                cmap_over = cmap_over,
                                PLOT=False,
                                )
                plot_climexp(scores.crpss.isel(time=-1),
                                'CRPSS hindcasts, reference: climatology (1961-'+str(int(year)-1)+')',
                                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+' | base time: '+months[st-1]+' '+year+' | valid time: '+months[lt-1]+' '+year,
                                predictand = predictand,
                                cmap=cmap2,
                                cmap_under = cmap_under,
                                cmap_over = cmap_over,
                                fname=bdpo+predictand+'_crpss_'+year+mon+'_'+monv+'.png',
                                clevs = np.array((-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5)),
                                )    
                #plot_climexp(scores.crpss_co2.isel(time=-1),
                #                'CRPSS hindcasts, reference: hindcasts with only CO2 as predictor (1961-'+str(int(year)-1)+')',
                #                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                #                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+' | base time: '+months[st-1]+' '+year+' | valid time: #'+months[lt-1]+' '+year,
                #                predictand = predictand,
                #                cmap = cmap2,
                #                cmap_under = cmap_under,
                #                cmap_over = cmap_over,
                #                fname=bdpo+predictand+'_crpss_detrended_clim_'+year+mon+'_'+monv+'.png',
                #                clevs = np.array((-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5)),
                #                )    
                plot_climexp(scores.for_anom.isel(time=-1),
                                'Ensemble mean anomaly (wrt 1980-2010)',
                                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+'  |  Stippled where NOT significant at 10% level'+' | base time: '+months[st-1]+' '+year+' | valid time: '+months[lt-1]+' '+year,
                                sig=scores.for_anom_sig.isel(time=-1).values,
                                cmap=cmap2,
                                predictand = predictand,
                                cmap_under = cmap_under,
                                cmap_over = cmap_over,
                                fname=bdpo+predictand+'_ensmean_'+year+mon+'_'+monv+'.png', 
                                clevs = clevz,
                                )
                plot_climexp(scores.cor.isel(time=-1),
                                'Correlation between hindcast anomaly and observations (1961-'+str(int(year)-1)+'',
                                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+'  |  Stippled where signficant at 5% level'+' | base time: '+months[st-1]+' '+year+' | valid time: '+months[lt-1]+' '+year,
                                sig = scores.cor_sig.isel(time=-1).values,
                                predictand = predictand,
                                fname=bdpo+predictand+'_correlation_'+year+mon+'_'+monv+'.png', 
                                clevs = np.arange(-1.,1.01,0.2),
                                )
                plot_climexp(scores.tercile.isel(time=-1),
                                'Probabilty (most likely tercile of '+var+'), based on 1961-'+str(int(year)-1)+' hindcasts',
                                'SPECS Empirical Seasonal Forecast: '+var+' ('+season+' '+year+')',
                                'Ensemble size: 51 | Forecast generation date: '+dt.strftime("%d/%m/%Y")+' | base time: '+months[st-1]+' '+year+' | valid time: '+months[lt-1]+' '+year,
                                cmap = cmap1,
                                predictand = predictand,
                                fname=bdpo+predictand+'_tercile_'+year+mon+'_'+monv+'.png', 
                                clevs = np.array((-100,-70,-60,-50,-40,40,50,60,70,100)),
                                barticks = ['100%','70%','60%', '50%', '40%', '40%', '50%','60%', '70%', '100%'],
                                )
                                #plt.annotate('<---- below lower tercile        
                
        if 'data_fit_tot_lt' in locals(): del(data_fit_tot_lt)
        if 'beta_xr_tot_lt' in locals(): del(beta_xr_tot_lt)
        if 'data_fit_tot' in locals(): del(data_fit_tot)
        
        
                
    import time        
    print('Total time taken is: ',np.int((time.time()-start0)//60),' minutes and ',np.int((time.time()-start0)%60), 'seconds')
    
#os.system('rsync -avt -e ssh /nobackup_1/users/krikken/KPREP/plots/ oldenbor@bvlclim.knmi.nl:climexp/SPES/plots/')
#os.system('rsync -avt /nobackup_1/users/krikken/KPREP/plots/ bhlclim:climexp/SPES/')
