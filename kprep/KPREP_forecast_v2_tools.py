import os, sys, glob, re, pickle
import numpy as np
import datetime
import time
import scipy
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date, date2num
from matplotlib import cm as CM
from matplotlib import colors
from scipy import stats
from sklearn import linear_model
from sklearn import feature_selection
import urllib.request, urllib.error, urllib.parse, zipfile, gzip, shutil, tempfile
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import properscoring as ps
import ftplib
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
from joblib import Parallel,delayed
from sklearn.linear_model import Lasso


month_nr = [
 '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthzz = 'JFMAMJJASONDJFMAMJJASOND'
month_nm = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
month_ss = ['FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ', 'DJF', 'JFM']

#def get_landmask(resolution):
    #try:
        #mask = np.load('pickle/mask_' + str(resolution) + '.npy')
    #except IOError:
        #gpccprec = cdo.remapbil('targetgrid/griddes' + str(resolution) + '.txt', input='inputdata/gpcc_10_combined.nc', returnMaArray='prcp')
        #mask = np.any(gpccprec.mask, axis=0)
        #np.save('pickle/mask_' + str(resolution) + '.npy', mask)

    #return mask


def regr_loop(predodata_3m, predodata_3m_trend, predadata_3m, timez, train, test, ens_size, bdnc, resolution, predictand,predictors,MLR_PRED, FC=True, sig_val=0.1,MDC=False,lt=0):
    ## Some notes..
    # 1 - The times written in the output files are all set to the month when the model is run, so the predictand data and the predictor data get the same timestamp in the output files, though they represent past (-2 months) and future (+2 months) data relative to the time stamp. The time stamp is the month the model is run. Hence, e.g. 2015-05-01 represent the forecast of May in 2015, with predictand data from FMA and predictor season is JJA.
    # 2 - ...
    print('     Started regression loop')
    t0 = time.time()



    # Make list of times that would give the future state of predictor data
    timez_f = timez + pd.DateOffset(months=4)
    #print(FC)
    if FC: test = [test]
    else:  test = test
       
    yr = test[0].year
    mo = timez.month[0]       
       
    # Detrend data trough removing linear relation with co2, using only training data to determine the fit    
    #import pdb;pdb.set_trace()
    #print('timez',timez)
    #print('train',train)
    print('test',test)
    predodata_3m_nc = remove_co2_po(predodata_3m.sel(time=timez), predodata_3m['CO2EQ'].sel(time=timez), train)
    predadata_3m_nc = remove_co2_pa(predadata_3m.sel(time=train), predodata_3m['CO2EQ'].sel(time=train), train)
    
    # If MLR, then use mean and trend of last 3 months of predictor to predict the future state of the predictor
    #import pdb;pdb.set_trace()
    if MLR_PRED:
        print('     MLR_PRED is True, fitting individual models for better estimate of future state of predictor')
        # Detrend 3-month trend data..
        predodata_3m_trend_nc = remove_co2_po(predodata_3m_trend.sel(time=timez), predodata_3m['CO2EQ'].sel(time=timez), train)
        # Detrend future state of predictor
        if FC:
            predodata_3m_f_nc = remove_co2_po(predodata_3m.sel(time=timez_f[:-1]), predodata_3m['CO2EQ'].sel(time=timez_f[:-1]), train+pd.DateOffset(months=4))
        else:
            predodata_3m_f_nc = remove_co2_po(predodata_3m.sel(time=timez_f), predodata_3m['CO2EQ'].sel(time=timez_f), train+pd.DateOffset(months=4))

        predodata_3m_fit = fit_predictors(y=predodata_3m_f_nc, x1=predodata_3m_nc, x2=predodata_3m_trend_nc, train_p=train, train_f=train+pd.DateOffset(months=4))
        if 'PERS_TREND' in predictors:
            predodata_3m_fit['PERS_TREND'] = predodata_3m_trend_nc['PERS']
    else:
        predodata_3m_fit = predodata_3m_nc  # Check if I shouldn't add .sel(time=timez)

    #print(predodata_3m_fit)
    # Get the correlation between predictor and predictand with stepwise selection
    cor_nc, sig_nc = get_sig_pred(predodata_3m_fit.sel(time=train), predadata_3m_nc.sel(time=train), predadata_3m.sel(time=train))
    #print(cor_nc)
    # Get correlation between predictor and predictand   
    #import pdb;pdb.set_trace()
    if FC:
        bdp = bdnc+'../plots/'
        # Get the correlation between predictor and predictand without stepwise selection
        cor_nc_orig, sig_nc_orig = cor_pred(predodata_3m_nc.sel(time=train), predadata_3m_nc.sel(time=train), y=predadata_3m.sel(time=train))
        plotcor_pred(cor_nc_orig,sig=sig_nc_orig,bd=bdp+predictand+'/predcor/',savename='corr_pred_orig_'+str(test[0])[:7],suptitle=predictand+' '+str(test[0])[:7])
        if MDC: name = predictand+'_'+str(mo)+'_'+str(lt)+'.nc'
        else: name = predictand+'_'+str(mo).zfill(2)+'.nc'
        cor_nc_orig.to_netcdf(bdnc+'cor_pred/cor_predictors_nofit_'+name)
        sig_nc_orig.to_netcdf(bdnc+'cor_pred/sig_predictors_nofit_'+name)
    
        # Get the correlation between predictor and predictand without stepwise selection
        cor_nc_fit, sig_nc_fit = cor_pred(predodata_3m_fit.sel(time=train), predadata_3m_nc.sel(time=train), y=predadata_3m.sel(time=train))
        plotcor_pred(cor_nc_fit,sig=sig_nc_fit,bd=bdp+predictand+'/predcor/',savename='corr_pred_fit_'+str(test[0])[:7],suptitle=predictand+' '+str(test[0])[:7])
        if MDC: name = predictand+'_'+str(mo)+'_'+str(lt)+'.nc'
        else: name = predictand+'_'+str(mo).zfill(2)+'.nc'
        cor_nc_fit.to_netcdf(bdnc+'cor_pred/cor_predictors_fit_'+name)
        sig_nc_fit.to_netcdf(bdnc+'cor_pred/sig_predictors_fit_'+name)

        # Plot and save the correlation obtained with the stepwise selection
        plotcor_pred(cor_nc,sig=sig_nc,bd=bdp+predictand+'/predcor/',savename='corr_pred_stepwise_'+str(test[0])[:7],suptitle=predictand+' '+str(test[0])[:7])
        if MDC: name = predictand+'_'+str(mo)+'_'+str(lt)+'.nc'
        else: name = predictand+'_'+str(mo).zfill(2)+'.nc'
        cor_nc.to_netcdf(bdnc+'cor_pred/cor_predictors_stepwise_'+name)
        sig_nc.to_netcdf(bdnc+'cor_pred/sig_predictors_stepwise_'+name)
    
    #import pdb;pdb.set_trace()
    
    # Predefine dataset to write output to, and fill with nans
    data_fit = xr.Dataset(coords={'lat': predadata_3m.lat,
                             'lon': predadata_3m.lon,
                             'time': test,      
                             'ens': list(range(1, ens_size + 1))})    
    
    kprep = np.full((len(test), ens_size, len(predodata_3m.lat), len(predodata_3m.lon)),np.nan,dtype='float32')
    clim = np.full_like(kprep,np.nan)
    trend = np.full_like(kprep,np.nan)
    obs = np.full((len(test), len(predodata_3m.lat), len(predodata_3m.lon)),np.nan,dtype='float32')
    
                          
    beta = np.full((len(test),len(list(predodata_3m_fit.data_vars.keys())),len(predodata_3m.lat), len(predodata_3m.lon)),np.nan,dtype='float32')

    beta_xr = xr.Dataset(coords={'time':test,'predictors':list(range(beta.shape[1])),'lat':predadata_3m.lat,'lon':predadata_3m.lon})
    #beta_xr.time.attrs = {'units':'days since 1901-01-01'}  
    
    # Create array with randomly selecting 51 years from training data for every test year
    for n in range(len(test)):
        if n == 0: rand_yrs = np.random.choice(list(range(len(train))), 51, replace=True)[None,:]
        else: rand_yrs = np.vstack((rand_yrs,np.random.choice(list(range(len(train))), 51, replace=True)))
    
    # Put linear relation CO2EQ with predictand (trend) as separate variable in ouput dataset. Linear trend is calculated by removing the detrended predictor data from the original predictor data
    if MDC:
        trend[:,0,:,:] =  trend_pred(predadata_3m.sel(time=train),predodata_3m['CO2EQ'].sel(time=timez),xr.full_like(predodata_3m[predictors[-1]].sel(time=timez),np.nan),train).sel(time=test).values
    else:
        trend[:,0,:,:] =  trend_pred(predadata_3m.sel(time=train),predodata_3m['CO2EQ'].sel(time=timez),xr.full_like(predodata_3m['PERS'].sel(time=timez),np.nan),train).sel(time=test).values
    # Loop over different test years to fill the trend and climatolgy ensembles
    for n in range(len(test)):
        trend[n,1:,:,:] = trend[n,0,:,:] + predadata_3m_nc.sel(time=train).values[rand_yrs[n,1:], :, :]
        clim[n,:] = predadata_3m.sel(time=train).values[rand_yrs[n,:], :, :]
    
    sig_nc = sig_nc.to_array(dim='predictors').values
    
    # Create boolean arrays where no significant predictors and where only co2 as significant predictor, these are used to fill in the data prior to the 'expensive' loop over most grid points..
    onlynans = np.all(np.isnan(predadata_3m.sel(time=train).values), axis=0)
    nosig = (np.sum(sig_nc < sig_val, axis=0) == 0) != onlynans
    onlyco2 = (np.sum(sig_nc[1:, :] < sig_val, axis=0) == 0) & (sig_nc[0, :] < sig_val)
    nosigs = np.tile(nosig[None, :], (51, 1, 1))
    onlyco2s = np.tile(onlyco2[None, :], (51, 1, 1))
    
    # Fill in fit_test where possible, so if no sig predictors then clim and only co2 then trend
    kprep[:,nosigs] = clim[:,nosigs] #data_fit['clim'].sel(time=test).values[:,nosigs]
    kprep[:,onlyco2s] = trend[:,onlyco2s] #data_fit['trend'].sel(time=test).values[:,onlyco2s]
    beta[:,0,sig_nc[0,:]<sig_val] =  linregrez(predodata_3m['CO2EQ'].sel(time=train),predadata_3m.sel(time=train),BETA=True)[0][sig_nc[0,:]<sig_val]
    
    # Create boolean array where there are significant predictors (excluding CO2EQ)
    pred_sel = sig_nc[1:, :, :] < sig_val

    ## Get grid points where we still need to loop over to get the model fit, i.e. where beside CO2EQ there are significant predictors            
    rest = np.sum(sig_nc[1:, :] < sig_val, axis=0) > 0    
    ii, jj = np.where(rest)   
    
    ### REGRESSION LOOP

    t1 = time.time()
    # Convert data to numpy arrays before loop as it is very slow to do this in the loop per grid point..
    Y_tr = predadata_3m_nc.sel(time=train).values                   # Detrended predictand training data
    X_tr = predodata_3m_fit.sel(time=train).to_array().values       # Detrended predictor training data
    X_te = predodata_3m_fit.sel(time=test).to_array().values        # Detrended predictor test data
    
    fit_train = np.full_like(Y_tr,np.nan)
    # Parallelized regression input > y,X_tr,X_te,sig, output > fit_train,fit_test,beta
    #import pdb;pdb.set_trace()
    PARALLEL = False
    if PARALLEL:
        regr_output = np.asarray(Parallel(n_jobs=4)(delayed(regrezzion)(Y_tr[:,i,j],X_tr[1:,:,i,j],X_te[1:,:,i,j],pred_sel[:,i,j])for i,j in zip(ii,jj)))
        
        
        # Put data obtained in regression back to right place..
        fit_train[:,rest] = np.vstack(regr_output[:,0]).T
        kprep[:,0,rest] = np.vstack(regr_output[:,1]).T 
        beta[:,1:,rest] = np.vstack(regr_output[:,2]).T
    else:    
        for i,j in zip(ii,jj):
            #print(i,j)
            fit_train[:,i,j],kprep[:,0,i,j],beta[:,1:,i,j] = regrezzion(Y_tr[:,i,j],X_tr[1:,:,i,j],X_te[1:,:,i,j],pred_sel[:,i,j])
            #fit_train[:,i,j],kprep[:,0,i,j],beta[:,1:,i,j] = lasso_regr(Y_tr[:,i,j],X_tr[1:,:,i,j],X_te[1:,:,i,j],alpha=0.1)#,pred_sel[:,i,j])
    # Generate ensemble based on random sampling 50 years from residuals (fit_train - Y_tr)
    # The transpose is needed because numpy changes the axis order when combining advanced and normal indexing
    for n in range(len(test)): 
        kprep[n,1:,rest] = (kprep[n,0,rest] - (fit_train[:,rest] - Y_tr[:,rest])[rand_yrs[n,1:],:]).T

    # Create boolean array where to apply trend is significant and rest = True
    rest_sig = rest & (sig_nc[0,:]<sig_val)
    
    kprep[:,:,rest_sig] = kprep[:,:,rest_sig] + trend[:,0,rest_sig][:,None,:]  # Manually add trend due to CO2 after regression
            
    t2 = time.time()
    #if test[0].month == 7:
        #import pdb;pdb.set_trace()
    if not FC:
        obs = predadata_3m.sel(time=test).values
    data_fit['kprep'] = (('time','ens','lat','lon'),kprep)
    data_fit['trend'] = (('time','ens','lat','lon'),trend)
    data_fit['clim'] = (('time','ens','lat','lon'),clim)
    data_fit['obs'] = (('time','lat','lon'),obs)
    beta_xr['beta'] = (('time','predictors','lat','lon'),beta)

    t3=time.time()
    
    #import pdb;pdb.set_trace()
    ### WRITE OUTPUT TO NETCDF

   
    print('     Writing to netcdf')

    if FC:
        if MDC: name = str(mo)+'_'+str(lt)+'.nc'
        else: name = str(mo).zfill(2)+'.nc'
        #to_nc3(predodata_3m_nc,bdnc + 'predictors_v2_'+predictand)
        #to_nc3(predodata_3m_fit,bdnc + 'predictors_fit_v2_'+predictand)
        print(predadata_3m.attrs)
        if MDC: predadata_3m.to_netcdf(bdnc + 'predadata_v2_'+predictand+'_'+name,'w')
        else: predadata_3m.to_netcdf(bdnc + 'predadata_v2_'+predictand+'.nc','w')
        
        predodata_3m_nc.to_netcdf(bdnc + 'predodata_3m_nc_'+predictand+'_'+name)
        predodata_3m_fit.to_netcdf(bdnc + 'predodata_3m_fit_'+predictand+'_'+name)
        predadata_3m_nc.to_netcdf(bdnc + 'predadata_3m_nc_'+predictand+'_'+name)
    #if FC:
    #    predodata_3m_nc.to_netcdf(bdnc + 'predictors_v2_'+predictand+'.nc')
    #    predodata_3m_fit.to_netcdf(bdnc + 'predictors_fit_v2_'+predictand+'.nc')
    #import pdb;pdb.set_trace()
    print('     regression loop done')
    print('     full function is: ',np.round((time.time()-t0),1),' seconds')
    print('     regr loop is: ',np.round((t2-t1),1),' seconds')
    print('     writing netcdf is: ',np.round((time.time()-t3),1),' seconds')
    
    return(data_fit,beta_xr)





def lasso_regr(y_train,x_train,x_test,alpha=0.1):
    lassoReg = Lasso(alpha=alpha, normalize=True)
    lassoReg.fit(x_train.T,y_train)
    pred = lassoReg.predict(x_test.T)
    
    fit_train = lassoReg.predict(x_train.T)
    fit_test = lassoReg.predict(x_test.T)
    beta = lassoReg.coef_
    return(fit_train,fit_test,beta)
    
    

def regrezzion(y,X_tr,X_te,sig):
    beta = np.full_like(sig,np.nan,dtype='float64')
    X_tr2 = sm.add_constant(X_tr[sig,:].T)
    X_te2 = sm.add_constant(X_te[sig,:].T,has_constant='add')
    model = sm.OLS(y,X_tr2,missing='drop')
    results = model.fit()
    fit_train = results.predict(X_tr2)
    fit_test = results.predict(X_te2)
    beta[sig] = results.params[1:]
    return fit_train,fit_test,beta

def calc_trend(self,axis=-1):
    x_a = np.array([-1.,0.,1.])
    y_a = self - self.mean(axis=axis,keepdims=True)
    beta = (y_a * x_a).mean(axis=axis) / (x_a**2).mean()
    return beta*3.


def xr_regression(y,sig):
    # Test to do a pure xarray regression by xr.groupby
    X = sm.add_constant(y.drop('predictand').to_array(dim='new_dim').values.squeeze().T)#,prepend=True)
    #print(np.max(X,axis=0))
    #print(X.shape)
    model = sm.OLS(y['predictand'].values,X,missing='drop')
    #model = sm.GLSAR(y['predictand'].values,X,2,missing='drop')
    results = model.fit()
        
        # Save model fit to numpy arrays
    fit = results.predict(X)    
    beta = results.params[1:]
    return xr.DataArray(fit),xr.DataArray(beta)

def xr_regression2(Y,dim):
    return xr.apply_ufunc(xr_regression,Y,
                        input_core_dims=[[dim]],
                        dask='parallelized')

def xr_regression_orig(y,dim):
    X = sm.add_constant(reg, prepend=True) # regressor matrix
    mod = sm.GLSAR(y.values, X, 2, missing = 'drop') # MLR analysis with AR2 modeling
    res = mod.iterative_fit()

    return xr.DataArray(res.params[1:])

def to_nc2(data_xr,path_filename,mode = 'w'):
    if not os.path.isfile(path_filename+'.nc'):
        data_xr.to_netcdf(path_filename+'.nc',mode='w',unlimited_dims='time',encoding={'time':{'units':'days since 1901-01-01'}})
        #print data_xr.time.values
    else:
        #print(path_filename)
        nc_data = Dataset(path_filename+'.nc','a')
        t_old = nc_data.variables['time']
        lentime=len(t_old[:])

        for v,var in enumerate(data_xr.data_vars): # Assuming all variables are already in old netcdf file
            appendvar = nc_data.variables[var]
            for t,tt in enumerate(data_xr['time'].values):
                #print t,tt
                t_int = int(date2num(pd.to_datetime(tt),units='days since 1901-01-01'))
                if t_int in t_old[:]: # If time already in dataset, then overwrite
                    idx = np.where(t_int == t_old[:])
                    #print np.asarray(idx).squeeze()
                    appendvar[np.asarray(idx).squeeze(),:] = data_xr[var].values[t,:]
                else:               # If new timestep, then append to dataset
                    appendvar[lentime+t,:] = data_xr[var].values[t,:]
                    if v == len(data_xr.data_vars)-1:   # If last variable, than add time to time dimension
                        t_old[lentime+t] = t_int
        nc_data.close()

        
def to_nc3(data_xr,path_filename):
    if not os.path.isfile(path_filename+'.nc'):
        data_xr.to_netcdf(path_filename+'.nc',mode='w',unlimited_dims='time')
    else:
        data_old = xr.open_dataset(path_filename+'.nc')
        #data_new = xr.merge([data_old,data_xr])
        data_new = xr.concat([data_old,data_xr],dim='time').sortby('time')
        os.remove(path_filename+'.nc')
        data_new.to_netcdf(path_filename+'.nc','w')
    

def check_updates(url,ret=False,inputdir='inputdata/'):
    if 'cpc.ncep.noaa' in url:
        f = ftplib.FTP()
        f.connect("ftp.cpc.ncep.noaa.gov")
        f.login()
        modifiedTime = f.sendcmd('MDTM ' + 'wd51yf/GHCN_CAMS/ghcn_cams_1948_cur_2.5.grb')
        year = modifiedTime[4:8]
        month = modifiedTime[8:10]
        day = modifiedTime[10:12]
        date_time = day+'.'+month+'.'+year
        pattern = '%d.%m.%Y'
        meta_modifiedtime = int(time.mktime(time.strptime(date_time, pattern)))
        #print meta_modifiedtime

    else:
        u = urllib.request.urlopen(url)
        meta = u.info()
        # CONVERTING HEADER TIME TO UTC TIMESTAMP
        # ASSUMING 'Sun, 28 Jun 2015 06:30:17 GMT' FORMAT
        meta_modifiedtime = time.mktime(datetime.datetime.strptime(meta.get("Last-Modified")[:16], "%a, %d %b %Y").timetuple())
        #print datetime.datetime.strptime(meta.getheaders("Last-Modified")[0], "%a, %d %b %Y %X GMT")
    dt = datetime.date.today()

    ref_time = os.path.getmtime(inputdir+os.path.split(url)[1])
    if meta_modifiedtime > ref_time:
        print('Data can be updated!','  --- ',url.rsplit('/',1)[1])
        update=True
    else:
        print('Data can NOT be updated','  --- ',url.rsplit('/',1)[1])
        update=False
    if ret: return update


def check_updates2(inputdir='inputdata/'):
    c=[]
    try:
        c.append( check_updates("http://climexp.knmi.nl/NCDCData/ersstv5.nc",ret=True,inputdir=inputdir) )
    except FileNotFoundError:
        return True
    c.append( check_updates("ftp://ftp.cpc.ncep.noaa.gov/wd51yf/GHCN_CAMS/ghcn_cams_1948_cur_2.5.grb",ret=True,inputdir=inputdir) )
    #c.append( check_updates("http://www-users.york.ac.uk/~kdc3/papers/coverage2013/had4_krig_v2_0_0.nc.gz") )
    c.append( check_updates("http://climexp.knmi.nl/GPCCData/gpcc_10_combined.nc",ret=True,inputdir=inputdir) )
    #url_prmsl ='http://climexp.knmi.nl/20C/prmsl.mon.mean.nc'
    #check_updates(url_prmsl)
    c.append( check_updates('http://climexp.knmi.nl/NCEPNCAR40/slp.mon.mean.nc',ret=True,inputdir=inputdir) )
    c.append( check_updates("http://climexp.knmi.nl/NCDCData/ersst_nino3.4a.dat",ret=True,inputdir=inputdir) )
    #url_qbo="http://climexp.knmi.nl/data/iqbo_30.dat"
    #check_updates(url_qbo)
    c.append( check_updates("http://climexp.knmi.nl/NCDCData/dmi_ersst.dat",ret=True,inputdir=inputdir) )
    c.append( check_updates("http://climexp.knmi.nl/UWData/pdo_ersst.dat",ret=True,inputdir=inputdir) )
    c.append( check_updates("http://climexp.knmi.nl/NCDCData/amo_ersst_ts.dat",ret=True,inputdir=inputdir) )
    return np.asarray(c,dtype='bool').all()


def remove_co2_po(data, data_co2, train):
    data_out = xr.full_like(data, np.nan)
    predos = data.data_vars
    for pred in data.data_vars:
        if pred == 'CO2EQ':
            data_out[pred].values = data[pred].values
        else:
            #import pdb;pdb.set_trace()
            #print(data)
            a, b = linregrez(data_co2.sel(time=train).values, data[pred].sel(time=train).values, BETA=True)[:2]
            if a.ndim == 1:
                data_out_co2 = a * data_co2.values + b
            else:
                data_out_co2 = a[np.newaxis, :, :] * data_co2.values[:, np.newaxis, np.newaxis] + b[np.newaxis, :, :]
                
            data_out[pred].values = data[pred].values - data_out_co2

    return data_out


def remove_co2_pa(data, data_co2, train):
    data_out = xr.full_like(data, np.nan) # Create empty DataArray 
    # Fit is based on training data
    a, b = linregrez(data_co2.sel(time=train).values, data.sel(time=train).values, BETA=True)[:2]
    # linear trend calculated for full time series (i.e. timez)
    data_out_co2 = a[np.newaxis, :, :] * data_co2.values[:, np.newaxis, np.newaxis] + b[np.newaxis, :, :]
    data_out.values = data.values - data_out_co2
    return data_out

def trend_pred(data,pred,data_out,train,taxis=0):
    # Calculate linear relation of certain data with a predictor, fit based on training data
    #data_out = xr.full_like(pred, np.nan) # Create empty DataArray 
    # Fit is based on training data
    a, b = linregrez(pred.sel(time=train).values, data.sel(time=train).values, BETA=True,taxis=taxis)[:2]
    # linear trend calculated for full time series (i.e. timez)
    #data_out.values =  a[np.newaxis, :, :] * pred.values[:, np.newaxis, np.newaxis] + b[np.newaxis, :, :]
    data_out.values =  np.expand_dims(a,taxis) * pred.values[:, np.newaxis, np.newaxis] + b[np.newaxis, :, :]
    return data_out
    

def remove_co2(data, data_co2):
    a, b = linregrez(data_co2, data, BETA=True)[:2]
    data_out_co2 = a * data_co2 + b
    return data - data_out_co2


def nans(shape, dtype='float64'):
    out = np.zeros(shape, dtype=dtype)
    out[:] = np.nan
    return out


def nans_like(data):
    out = np.zeros_like(data)
    out[:] = np.nan
    return out


def rewrite_time(df):
    time_idx = pd.DatetimeIndex(df.time.values)
    df2 = pd.DataFrame({'year': time_idx.year,'month': time_idx.month,'day': np.ones(len(df.time.values))})
    #df2.time.attrs = {'standard_name':'time','long_name':'Time','reference_time': pd.Timestamp('1891-01-01')}
    time = pd.to_datetime(df2)
    return time.values


import statsmodels.api as sm
from statsmodels.api import add_constant

def fit_predictors(y=[], x1=[], x2=[], train_p=[], train_f=[]):
    data_out = xr.full_like(x1, np.nan)
    for pred in y.data_vars:
        if pred in ('CO2EQ', 'PERS', 'CPREC','TMAX','PRECIP'):
            data_out[pred].values = x1[pred].values
        else:
            x_pred_train = xr.merge([x1[pred].sel(time=train_p), x2[pred].sel(time=train_p).rename('TREND')]).to_array(dim='predictors').values.T
            x_pred_train = add_constant(x_pred_train)
            model = sm.OLS(y[pred].sel(time=train_f).values, x_pred_train, missing='drop')
            results = model.fit()
            x_pred_full = xr.merge([x1[pred], x2[pred].rename('TREND')]).to_array(dim='predictors').values.T
            x_pred_full = add_constant(x_pred_full)
            data_out[pred].values = results.predict(x_pred_full)

    return data_out



def anom_df(data_df, y1, y2, styear):
    '''
    Function to remove climatology in order to create anomalies, where the climatology period is based on y1 and y2
    data_df = original data
    y1 = start year of climatology
    y2 = end year of climatology
    styear = start year of dataset
    '''
    data = data_df.values
    if data.ndim > 1:
        clim = np.nanmean(data[(y1 - styear) * 12:(y2 - styear) * 12, :].reshape((y2 - y1, 12, data.shape[1], data.shape[2])), axis=0)
        climm = np.concatenate((np.tile(clim, (data.shape[0] // 12, 1, 1)), clim[:data.shape[0] % 12, :]), axis=0)
    else:
        if data.ndim == 1:
            clim = np.nanmean(data[(y1 - styear) * 12:(y2 - styear) * 12].reshape((y2 - y1, 12)), axis=0)
            climm = np.concatenate((np.tile(clim, data.shape[0] // 12), clim[:data.shape[0] % 12]), axis=0)
    return data - climm


def pred_trend(data):
    data_out = xr.full_like(data, np.nan)
    for pred in data.data_vars:
        data_out[pred].values[1:-1] = seazon_trend2(data[pred].values)

    return data_out


def seazon_trend2(pred):
    if pred.ndim == 1:
        pred = pred[:, np.newaxis, np.newaxis]
    pred_stack = np.stack((pred[:-2, :], pred[1:-1, :], pred[2:, :]), axis=3)
    print(pred_stack.shape)
    return linregrez(np.array([1.0, 2.0, 3.0]), pred_stack, taxis=3, BETA=True)[0].squeeze()


def load_clim_index(fileloc, styear, endyear, endmonth, name):
    data = np.genfromtxt(fileloc)
    if data.shape[1] == 2:
        data_subset = data[(styear - int(data[(0, 0)])) * 12:(endyear - int(data[(0, 0)])) * 12 + endmonth, :]
        df = pd.DataFrame({'year': data_subset[:, 0].astype(int),'month': np.rint((data_subset[:, 0] - data_subset[:, 0].astype(int)) * 12) + 1,
           'day': np.ones(data_subset.shape[0])
           })
        da = xr.DataArray(data_subset[:, 1], coords=[pd.to_datetime(df)], dims=['time'], name=name)
    else:
        if data.shape[1] == 13:
            data_yrs = data[:, 0]
            data_vals = data[:, 1:].ravel()
            data_yrs_ss = data_yrs[styear - int(data[(0, 0)]):endyear - int(data[(0,
                                                                                  0)]) + 1]
            data_subset = data_vals[(styear - int(data[(0, 0)])) * 12:(endyear - int(data[(0,
                                                                                           0)])) * 12 + endmonth]
            df = pd.DataFrame({'year': data_yrs_ss.astype(int).repeat(12)[:len(data_subset)],'month': np.tile(list(range(1, 13)), len(data_subset) // 12 + 1)[:len(data_subset)],
               'day': np.ones(data_subset.shape[0])
               })
            da = xr.DataArray(data_subset, coords=[pd.to_datetime(df)], dims=['time'], name=name)
        else:
            print('unknown file format..', data.shape)
    return da


def linregrez(x, y, taxis=0, COR=False, BETA=False, COV=False):
    if COR or BETA or COV:
        ALL = False
    else:
        ALL = True
    if x.ndim == 1 and y.ndim == 1:
        x = x[:, np.newaxis]
        y = y[:, np.newaxis]
    else:
        if x.ndim == 1 and y.ndim > 1:
            a = list(np.shape(y) + (1, ))
            #print(a)
            a.pop(taxis)
            #print(a)
            x = np.rollaxis(np.tile(x, a), len(a) - 1, taxis)
            #print(x.shape)
            #print(y.shape)
        else:
            if x.ndim > 1 and y.ndim == 1:
                a = list(np.shape(x) + (1, ))
                a.pop(taxis)
                y = np.rollaxis(np.tile(y, a), len(a) - 1, taxis)
    if x.shape != y.shape:
        print('wrong dimensions.. x=', x.shape, ' and y=', y.shape)
        sys.exit()
    if x.ndim > 1 and y.ndim > 1:
        x_a = x - np.nanmean(x, axis=taxis, keepdims=True)
        y_a = y - np.nanmean(y, axis=taxis, keepdims=True)
        if COR or ALL:
            pearson = np.nansum(x_a * y_a, axis=taxis) / np.sqrt(np.nansum(np.power(x_a, 2), axis=taxis) * np.nansum(np.power(y_a, 2), axis=taxis))
            rdf = x.shape[taxis]
            t = pearson / np.sqrt((1 - np.power(pearson, 2)) / (rdf - 2))
            p = stats.t.sf(np.abs(t), rdf - 1) * 2
            if COR:
                return (pearson, p)
        if BETA or ALL:
            beta = np.nanmean(x_a * y_a, axis=taxis) / np.nanmean(x_a ** 2, axis=taxis)
            inter = np.nanmean(y, axis=taxis) - beta * np.nanmean(x, axis=taxis)
            yp = np.expand_dims(inter, axis=taxis) + np.expand_dims(beta, axis=taxis) * x
            sse = np.nansum((y - yp) ** 2, axis=taxis)
            mse = sse / (x.shape[taxis] - 2)
            rdf = x.shape[taxis]
            se_inter = np.sqrt(mse) * np.sqrt(1.0 / rdf + np.nanmean(x, axis=taxis) / np.nansum(x_a ** 2, axis=taxis))
            se_beta = np.sqrt(mse) * np.sqrt(1.0 / np.nansum(x_a ** 2, axis=taxis))
            return (
             beta, inter, se_beta, se_inter)
        if COV or ALL:
            cov = np.nanmean(x_a * y_a, axis=taxis)
            return cov
        if ALL:
            return (pearson, p, beta, se_beta, inter, se_inter, cov)
        

def load_ecmwf_s5(predictand,m,obs,bias_correct=True,resolution=25):
    namez = {'GCEcom':'t2m','20CRslp':'msl','GPCCcom':'tprate'}
    data_s5 = xr.open_dataset('../../climexp_data/KPREPData/ecmwf_s5/'
                             +namez[predictand]+'_s5_seas_'+str(m+1).zfill(2)+'_r'+str(resolution)+'.nc').rename({namez[predictand]:predictand})
    data_s5_anom = data_s5 - data_s5.sel(time=slice('1980','2010')).mean('time')
    if bias_correct:
        data_s5_anom_bc = data_s5_anom + (obs.sel(time=slice(data_s5.time[0],obs.time[-1])).mean(dim='time')-data_s5_anom.sel(time=slice(data_s5.time[0],obs.time[-1])).mean(dim='time'))
        return(data_s5_anom_bc)
    else:
        return(data_s5_anom)        
       
def linregrez_short(x, y, taxis=0):
    x_a = x - np.nanmean(x, axis=taxis, keepdims=True)
    y_a = y - np.nanmean(y, axis=taxis, keepdims=True)
    
    pearson = np.nansum(x_a * y_a, axis=taxis) / np.sqrt(np.nansum(np.power(x_a, 2), axis=taxis) * np.nansum(np.power(y_a, 2), axis=taxis))
    rdf = x.shape[taxis]
    t = pearson / np.sqrt((1 - np.power(pearson, 2)) / (rdf - 2))
    p = stats.t.sf(np.abs(t), rdf - 1) * 2

    beta = np.nanmean(x_a * y_a, axis=taxis) / np.nanmean(x_a ** 2, axis=taxis)
    inter = np.nanmean(y, axis=taxis) - beta * np.nanmean(x, axis=taxis)

    return pearson,p,beta,inter

def comb_pvalues(sige): # Combine p-values using fishers method
    X_var = -2. * np.nansum(np.log(sige),axis=0)
    sig = 1. - stats.chi2.cdf(X_var,2*sige.shape[0])
    return(sig)

def comb_rvalues(core): # Combine r-values using ...
    core = core - 0.0001 # Make small error to avoid divide by zero
    z = 0.5 * np.log((1.+core)/(1.-core))
    ze = np.nanmean(z,axis=0)
    cor = (np.exp(2*ze)-1)/(np.exp(2*ze)+1)
    return cor


def linregrez_short_bs(x,y,taxis=0,bsn=20):
    #import pdb;pdb.set_trace()
    t0 = time.time()
    pv = np.zeros((bsn,x.shape[1],x.shape[2]))
    pearson = np.zeros_like(pv)
    beta = np.zeros_like(pv)
    inter = np.zeros_like(pv)
    
        
                 
    for bsi in range(bsn):
        rand_yrs = np.random.choice(list(range(x.shape[0])), x.shape[0], replace=True)
        x2 = x[rand_yrs,:]
        y2 = y[rand_yrs,:]
        
        x_a = x2 - np.nanmean(x2, axis=taxis, keepdims=True)
        y_a = y2 - np.nanmean(y2, axis=taxis, keepdims=True)

        pearson[bsi,:] = np.nansum(x_a * y_a, axis=taxis) / np.sqrt(np.nansum(np.power(x_a, 2), axis=taxis) * np.nansum(np.power(y_a, 2), axis=taxis))
        rdf = x2.shape[taxis]
        t = pearson[bsi,:] / np.sqrt((1 - np.power(pearson[bsi,:], 2)) / (rdf - 2))
        pv[bsi,:] = stats.t.sf(np.abs(t), rdf - 1) * 2

        beta[bsi,:] = np.nanmean(x_a * y_a, axis=taxis) / np.nanmean(x_a ** 2, axis=taxis)
        inter[bsi,:] = np.nanmean(y2, axis=taxis) - beta[bsi,:] * np.nanmean(x2, axis=taxis)
    
    p_avg = comb_pvalues(pv)
    r_avg = comb_rvalues(pearson)
    print('bootstrap function:',time.time()-t0)
    #import pdb;pdb.set_trace()             
    return p_avg,r_avg,np.nanmean(beta,axis=0),np.nanmean(inter,axis=0)

def get_sig_pred(po_nc, pa_nc, pa, sig_val=0.1, BOOTSTRAP=False):
    # Predictors should be CO2 removed, but not the predictand!!

    # Get correlation and significance of relation predictors with predictand, for CO2 this is the relation with the original data, for the others both the predictor data and the predictand data is trend (co2) corrected
    cor1, sig1 = cor_pred(po_nc, pa_nc, y=pa)
    cor_np = cor1.to_array(dim='predictors').values
    argsort1 = np.zeros_like(cor_np)[:, np.newaxis, :, :]
    # Get information how to sort the array in order to get low to high values of correlation
    # CO2EQ is always first, and then the other predictors
    argsort1[1:, :] = np.argsort(np.abs(cor_np[1:, :]), axis=0)[:, np.newaxis, :, :][::-1,:,:,:] + 1
    argsort2 = np.argsort(argsort1, axis=0)
    #print argsort1.dtype
    # Rewrite po_nc to numpy
    #po_nc_np = xr2np(po_nc)
    po_nc_np = po_nc.to_array().values
    # Sort predictor data based on correlation scores
    po_nc_sorted = po_nc_np[(argsort1.astype(int),
     np.arange(po_nc_np.shape[1])[np.newaxis, :, np.newaxis, np.newaxis],
     np.arange(po_nc_np.shape[2])[np.newaxis, np.newaxis, :, np.newaxis],
     np.arange(po_nc_np.shape[3])[np.newaxis, np.newaxis, np.newaxis, :])]
    data = pa.values
    cor_sorted = np.full_like(cor_np,np.nan)
    sig_sorted = np.full_like(cor_np,np.nan)
    for p in range(po_nc_np.shape[0]):
        # Get correlation of sorted (from high to low correlation) predictors with predictand
        cor_sorted[p, :], sig_sorted[p, :],beta,inter = linregrez_short(po_nc_sorted[p, :], data) 
        #cor_sorted[p, :], sig_sorted[p, :] = linregrez(po_nc_sorted[p, :], data, COR=True) 
        # Get regression coefficients of sorted predictor data with predictand
        #a, b = linregrez(po_nc_sorted[p, :], data, BETA=True)[:2]
        # Create boolean array where True if significant correlation
        sign = sig_sorted[p, :] < sig_val
        # Get relation between sorted predictor data and predictand
        data_fit = beta * po_nc_sorted[p, :] + inter
        # Where correlation is significant, remove this relation from the predictand data
        data[:, sign] = data[:, sign] - data_fit[:, sign]
    
    cor = xr.full_like(cor1,np.nan).to_array(dim='predictors')
    sig = xr.full_like(sig1,np.nan).to_array(dim='predictors')
    # Unsort the correlation and significance values
    cor.values[:] = cor_sorted[(argsort2.squeeze(),
     np.arange(cor_np.shape[1])[np.newaxis, :, np.newaxis],
     np.arange(cor_np.shape[2])[np.newaxis, np.newaxis, :])]
    sig.values[:] = sig_sorted[(argsort2.squeeze(),
     np.arange(cor_np.shape[1])[np.newaxis, :, np.newaxis],
     np.arange(cor_np.shape[2])[np.newaxis, np.newaxis, :])]
    return cor.to_dataset(dim='predictors'), sig.to_dataset(dim='predictors')

#def xr2np1(data_xr):
    #data_np = np.zeros((len(data_xr.data_vars), len(data_xr['PERS'].lat), len(data_xr['PERS'].lon)))
    #for i, pred in enumerate(data_xr.data_vars):
        #data_np[i, :] = data_xr[pred].values
    #return data_np

#def xr2np(data_xr):
    #try:data_np = np.zeros((len(data_xr.data_vars), len(data_xr.coords['time']), len(data_xr.coords['lat']),
        #len(data_xr.coords['lon'])))
    #except TypeError: data_np = np.zeros((len(data_xr.data_vars), len(data_xr.coords['lat']),
        #len(data_xr.coords['lon'])))
    #for i, pred in enumerate(data_xr.data_vars):
        
        #if len(data_xr[pred].dims) > 1:
            #data_np[i, :] = data_xr[pred].values
        #else:
            #data_np[i, :] = data_xr[pred].values[:, np.newaxis, np.newaxis]
    #return data_np


def cor_pred(x_nc, y_nc, y=[]):
    '''Calculate correlation between predictor and predictand:
        x_nc = the detrended predictor
        y_nc = the detrended predictand
        y = the original predictand, only needed if CO2EQ is one of the predictors'''
    corr = xr.Dataset(coords={'lat':x_nc['lat'],'lon':x_nc['lon']})
    for pred in x_nc.data_vars:
        corr[pred] = (('lat','lon'),np.full((len(x_nc['lat']),len(x_nc['lon'])),np.nan))
    sigg = xr.full_like(corr,np.nan)
    for i, pred in enumerate(x_nc.data_vars):
        if pred == 'CO2EQ':
            #a,b = linregrez(x_nc[pred].values, y.values, COR=True)
            corr[pred].values , sigg[pred].values = linregrez(x_nc[pred].values, y.values, COR=True)
        else:
            corr[pred].values , sigg[pred].values = linregrez(x_nc[pred].values, y_nc.values, COR=True)
    return corr, sigg


#def cor_pred(x_nc, y_nc, y=[]):
    #'''Calculate correlation between predictor and predictand:
        #x_nc = the detrended predictor
        #y_nc = the detrended predictand
        #y = the original predictand, only needed if CO2EQ is one of the predictors'''
    #cor,sig = linregrez(x_nc,y_nc,taxis=0,COR=True)
    #if y != []: cor[0,:],sig[0,:] = linregrez(x_nc[0,:],y,taxis=0,COR=True)
    #return cor,sig 

def mdi(tmax,prec,NH=True,CARRYOVER=False,con_a=0.5,con_b=0.5):
    # First select only AMJJASO
    tm = tmax['time.month']
    #tmax_ss = tmax.sel(time=(tm>3) & (tm<11))
    #prec_ss = prec.sel(time=(tm>3) & (tm<11))
    #mdc = xr.full_like(prec_ss,np.nan).rename({'precip':'mdc'})
    #nr_years = len(np.unique(tmax_ss.time['time.year'].values))
    #print(tmax.values.shape)
    if 'leadtime' in tmax.coords:
        tmax_ss = tmax
        prec_ss = prec
        mdc = xr.full_like(prec,np.nan).rename({'precip':'mdc'})
        #print(mdc)
        idx_leadtime = list([i<8 for i in tmax_ss.values.shape]).index(1)
        # move leadtime dimension to second place
        print(idx_leadtime)
        print('high',tmax_ss.values.shape)
        tmax_np = np.moveaxis(tmax_ss.values,idx_leadtime,1)
        prec_np = np.moveaxis(prec_ss.precip.values,idx_leadtime,1)
        print(tmax_np.shape)
        print(prec_np.shape)
    else:
        tmax_ss = tmax.sel(time=(tm>3) & (tm<11))
        prec_ss = prec.sel(time=(tm>3) & (tm<11))
        mdc = xr.full_like(prec_ss,np.nan).rename({'precip':'mdc'})
        nr_years = len(np.unique(tmax_ss.time['time.year'].values))
        # If the last year does not cover at least up to october, then add nans 
        tmax_vals = tmax_ss.values
        print(prec_ss)
        prec_vals = prec_ss.precip.values
        if (len(tmax_ss.time) % 7) != 0:
            tmax_vals = np.concatenate((tmax_vals,
                    np.full((7 - (len(prec_ss.time) % 7),tmax_vals.shape[1],tmax_vals.shape[2]),np.nan)),
                    axis=0)
            print(prec_vals.shape)
            prec_vals = np.concatenate((prec_vals,
                    np.full((7 - (len(prec_ss.time) % 7),tmax_vals.shape[1],tmax_vals.shape[2]),np.nan)),
                    axis=0)
            print(prec_vals.shape)
        tmax_np = np.reshape(tmax_vals,(nr_years,7,len(tmax_ss.lat),len(tmax_ss.lon)))
        prec_np = np.reshape(prec_vals,(nr_years,7,len(prec_ss.lat),len(prec_ss.lon)))
    #print(tmax_np.shape)
    tmax_np[tmax_np<0.]=0.    # Remove freezing days
    ndays_NH = np.array([30,31,30,31,31,30,31])
    ndays_SH = np.array([31,30,31,31,28,31,30])
    Lf = np.array([0.9,3.8,5.8,6.4,5.0,2.4,0.4])
    MDC_0 = 15. # Initiate with no drought.. assuming fully saturated at spring
    MDC = nans_like(tmax_np)
    #print(tmax_np.shape[1],MDC.shape)
    for m in range(tmax_np.shape[1]):
        #print(tmax_np.shape)
        Em = ndays_NH[m] * (0.36 * tmax_np[:,m,:] + Lf[m])
        RMeff = 0.83 * prec_np[:,m,:]

        DC_half = MDC_0 + 0.25 * Em

        Qmr = 800. * np.exp(-DC_half / 400.) + 3.937 * RMeff
        Qmr[Qmr>800.] = 800.

        MDC_m = 400.*np.log(800./Qmr) + 0.25* Em
        MDC[:,m,:] = (MDC_0 + MDC_m) / 2.
        MDC_0 = MDC_m
    #print(MDC)    
    if 'leadtime' in tmax.coords:
        print(MDC.shape)
        print(np.moveaxis(MDC,1,idx_leadtime).shape)
        print(mdc.mdc.values.shape)
        mdc.mdc.values = np.moveaxis(MDC,1,idx_leadtime)#[:,tmax_ss.shape[0],:,:]
        #print(mdc)
    else:
        mdc.mdc.values = np.reshape(MDC,tmax_vals.shape)[:tmax_ss.shape[0],:,:]
    
    mdc.attrs = []
    #mdc.time.attrs = []
    
    # Put nans at times when no mdc is calculated, i.e. november to march
    mdc_filled = xr.full_like(tmax,np.nan).combine_first(mdc)

    return mdc_filled

# def mdi_overwinter(mdc,precip,a=0.5,b=0.5):
#     mdc_oct = mdc.sel(mdc['time.month']==10)
#     precip_winter = precip.resampe(time='AS-NOV')
    
#     return 

def decode_timez(ds):
    timez = pd.date_range(ds.time.units.split(' ')[-1],periods=len(ds.time),freq='MS')
    ds.time.attrs = []
    ds = ds.assign_coords(time=timez)
    #ds.time.values = timez
    ds.time.attrs = {'standard_name':'time','long_name':'Time','units': 'days since 1891-01-01'}
    return ds
    
def plotcor_pred(cor,sig=[],bd=[],savename=None,sig_val=0.1,suptitle=''):
    '''Plot the correlation between the predictor and predictand
    cor = correlation
    sig = plot significance
    bd = path where to save figure
    savename = name of saved figure, no .png needed
    sig_val = significance threshold values
    suptitle = title of plot
    '''
    if not os.path.exists(bd): os.makedirs(bd)
    proj = ccrs.PlateCarree()
    fig, axes = plt.subplots(4, 2, subplot_kw=dict(projection=proj),figsize=(9,12))
    lons,lats = cor.lon.values,cor.lat.values
    cmap = 'RdYlBu_r'
    for ax,pred in zip(axes.flat[:len(cor.data_vars)],cor.data_vars):
        if np.isnan(cor[pred].values).all():
            continue
        else:
            pcont = ax.contourf(lons,lats,cor[pred].values,levels=np.arange(-1.,1.1,.2),cmap=cmap)
            try:
                xx,yy = np.where(sig[pred].values<sig_val)
                ax.scatter(lons[yy],lats[xx],marker='.',c='k',s=0.7,lw=0.)
            except:
                print('no sig values')
            ax.coastlines()
            ax.set_title(pred)
    cax = matplotlib.axes.Axes(fig,[0.83, 0.4, 0.09, 0.3])
    fig.colorbar(pcont,ax=cax)  
    fig.suptitle(suptitle,fontsize=12)
    if savename == None:
        plt.show()
    else: 
        plt.savefig(bd+savename+'.png')
        plt.close('all')
    

def f_rmse(data,obs,SS=False,ref=[],MDI=False):
    if MDI:      # Calculate RMSE per month, input data [year,leadtime,ens,lat,lon]
        rmse_fc = np.sqrt(np.nanmean( (np.nanmean(data,axis=2) - obs )**2,axis=0))
        if SS: rmse_ref = np.sqrt(np.nanmean( (np.nanmean(ref,axis=2) - obs )**2,axis=0))
        if SS: return (1- (rmse_fc/rmse_ref))
        else: return rmse_fc
    else:           # Calculate RMSE per month, input data [year,month,ens,lat,lon]
        rmse_fc = np.sqrt(np.nanmean( (np.nanmean(data,axis=1) - obs )**2,axis=0))
        if SS: rmse_ref = np.sqrt(np.nanmean( (np.nanmean(ref,axis=1) - obs )**2,axis=0))    
        if SS: return (1- (rmse_fc/rmse_ref))
        else: return rmse_fc


def f_crps2(data,obs,SS=False,ref=[],MDI=False):
    if MDI: crps_fc = np.zeros((data.shape[1],data.shape[3],data.shape[4]))
    else: crps_fc = np.zeros((data.shape[2],data.shape[3]))
    if SS: crps_ref = np.zeros_like(crps_fc)
    if MDI:
        for i in range(data.shape[3]):
            crps_fc[:,i,:] = np.nanmean(ps.crps_ensemble(obs[:,:,i,:],data[:,:,:,i,:],axis=2),axis=0)
            if SS: crps_ref[:,i,:] = np.nanmean(ps.crps_ensemble(obs[:,:,i,:],ref[:,:,:,i,:],axis=2),axis=0)
    else:
        for i in range(data.shape[2]):
            #for j in range(data.shape[3]):
            crps_fc[i,:] = np.nanmean(ps.crps_ensemble(obs[:,i,:],data[:,:,i,:],axis=1),axis=0)
                #crps_fc[i,j] = np.nanmean(ps.crps_ensemble(obs[:,i,j],data[:,:,i,j]),axis=0)
            if SS: crps_ref[i,:] = np.nanmean(ps.crps_ensemble(obs[:,i,:],ref[:,:,i,:],axis=1),axis=0)
                #if SS: crps_ref[i,j] = np.nanmean(ps.crps_ensemble(obs[:,i,j],ref[:,:,i,j]),axis=0)
    if SS: return 1. - (crps_fc / crps_ref)
    else: return crps_fc

def f_crps(data,obs,ref=[],MDI=False,ens_axis=1,mean=False):
    
    crps_fc = np.zeros((np.delete(np.asarray(data.shape),ens_axis)))
    if ref != []: crps_ref = np.zeros_like(crps_fc)

    for i in range(data.shape[2]): # Loop over latitude to reduce the memory load..
        crps_fc[:,i,:] = ps.crps_ensemble(obs[:,i,:],data[:,:,i,:],axis=ens_axis)
            #crps_fc[i,j] = np.nanmean(ps.crps_ensemble(obs[:,i,j],data[:,:,i,j]),axis=0)
        if ref != []: crps_ref[:,i,:] = ps.crps_ensemble(obs[:,i,:],ref[:,:,i,:],axis=ens_axis)
            #if SS: crps_ref[i,j] = np.nanmean(ps.crps_ensemble(obs[:,i,j],ref[:,:,i,j]),axis=0)
    if mean:
        crps_fc = np.nanmean(crps_fc,axis=0)
        crps_ref = np.nanmean(crps_ref,axis=0)
    if ref != []: return 1. - (crps_fc / crps_ref)
    else: return crps_fc

#def f_crps2(data,obs,ref=[],ens_axis=0):
    ## Function to calculte CRPS or CRPSS
    #t0 = time.time()
    #if ref == []:
        #crps = ps.crps_ensemble(obs,data,axis=ens_axis)
    #else:
        #crps_fc = ps.crps_ensemble(obs,data,axis=ens_axis)
        #cprs_ref = ps.crps_ensemble(obs,ref,axis=ens_axis)
        #crps = 1.-(crps_fc/cprs_ref)
    #print time.time()-t0
    #return crps


#def tercile_category_xr(hc,fc,yrs=None): # Note, last hindcast is forecast..
#    lt = hc.quantile([0.33,0.67],dim=['time','ens'])
    #lower_tercile = np.nanpercentile(hc[:,:].reshape(((hc.shape[0])*hc.shape[1],hc.shape[2],hc.shape[3])),33.33,axis=0)
    #upper_tercile = np.nanpercentile(hc[:,:].reshape(((hc.shape[0])*hc.shape[1],hc.shape[2],hc.shape[3])),66.67,axis=0)
#    sum_ut = np.sum(fc>upper_tercile,axis=0)
    #sum_lt = np.sum(fc<lower_tercile,axis=0)
    #tercile = np.where(sum_ut>sum_lt,sum_ut/0.51,-sum_lt/0.51)
#    return tercile

def tercile_category(hc,fc,yrs=None): # Note, last hindcast is forecast..
    lower_tercile = np.nanpercentile(hc[:,:].reshape(((hc.shape[0])*hc.shape[1],hc.shape[2],hc.shape[3])),33.33,axis=0)
    upper_tercile = np.nanpercentile(hc[:,:].reshape(((hc.shape[0])*hc.shape[1],hc.shape[2],hc.shape[3])),66.67,axis=0)
    sum_ut = np.sum(fc>upper_tercile,axis=0)
    sum_lt = np.sum(fc<lower_tercile,axis=0)
    tercile = np.where(sum_ut>sum_lt,sum_ut/0.51,-sum_lt/0.51)
    return tercile



def plot_climexp(data,line1,line2,line3,cmap=[],cmap_under=[],cmap_over=[],predictand=[],sig=[],fname=[],PLOT=False,clevs=[],barticks=[]):
    #print('plotting '+data.name)
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12,8))
    ax = plt.subplot(111, projection=ccrs.PlateCarree())
    ax.set_facecolor('red')
    ax.set_global()
    if data.shape[1] == 360: # only northern hemisphere for MDC
        ax.set_extent([-180,180,90,0], ccrs.PlateCarree())
    else:
        ax.set_extent([-180,180,90,-90], ccrs.PlateCarree())
    lons,lats = data.lon.values,data.lat.values
    lon2d, lat2d = np.meshgrid(lons, lats)
    ax.annotate(line1, xy=(0, 1.10), xycoords='axes fraction',fontsize=14,ha='left',va='center')
    ax.annotate(line2, xy=(0, 1.15), xycoords='axes fraction',fontsize=18,ha='left',va='center')
    ax.annotate(line3, xy=(0, 1.05), xycoords='axes fraction',fontsize=10,ha='left',va='center')
    if clevs == []:
        clevs = np.arange(np.nanmin(data),np.nanmax(data), 0.1)#[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]
    if cmap == []: cmap = plt.cm.RdYlBu_r
    if cmap_under != []: cmap.set_under(cmap_under)
    if cmap_over != []: cmap.set_over(cmap_over)
    norm = matplotlib.colors.BoundaryNorm(clevs, cmap.N)

    if data.name in ['tercile','cor']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap)#,clevs,norm,cmap)
    elif data.name in ['crpss','rmsess','kprep','crpss_co2','for_anom']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap,extend='both')
    ax.coastlines()
    if sig != []:
       if data.name == 'for_anom': sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
       else: sigvals = np.where(sig[:,:]<0.05)
       ax.scatter(lon2d[sigvals],lat2d[sigvals],marker='.',c='k',s=5.,lw=0.)
                    
    ax.background_patch.set_facecolor('lightgray')
        
    #cbar = fig.colorbar(cs,cmap=cmap,norm=norm,boundaries=clevs,location='bottom',pad="10%")
    cax = matplotlib.axes.Axes(fig,[0.1, 0.15, 0.8, 0.25])
    cbar = fig.colorbar(cs,ax=cax,cmap=cmap,norm=norm,boundaries=clevs,orientation='horizontal',shrink=0.8)
    
    #fig.colorbar(pcont,ax=cax)  
    if barticks != []: cbar.ax.set_xticklabels(barticks)
    if fname != []: plt.savefig(fname)    
    if PLOT: plt.show()
    else: plt.close('all')
    
def plot_climexp2(data,line1,line2,line3,cmap=[],cmap_under=[],cmap_over=[],predictand=[],sig=[],fname=[],PLOT=False,clevs=[],barticks=[]):
    #print('plotting '+data.name)
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12,8))
    ax = plt.subplot(111, projection=ccrs.PlateCarree())
    ax.set_facecolor('red')
    ax.set_global()
    ax.set_extent([-180,180,90,-90], ccrs.PlateCarree())
    lons,lats = data.lon.values,data.lat.values
    lon2d, lat2d = np.meshgrid(lons, lats)
    ax.annotate(line1, xy=(0, 1.10), xycoords='axes fraction',fontsize=14,ha='left',va='center')
    ax.annotate(line2, xy=(0, 1.15), xycoords='axes fraction',fontsize=18,ha='left',va='center')
    ax.annotate(line3, xy=(0, 1.05), xycoords='axes fraction',fontsize=10,ha='left',va='center')
    if clevs == []:
        clevs = np.arange(np.nanmin(data),np.nanmax(data), 0.1)#[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]
    if cmap == []: cmap = plt.cm.RdYlBu_r
    if cmap_under != []: cmap.set_under(cmap_under)
    if cmap_over != []: cmap.set_over(cmap_over)
    norm = matplotlib.colors.BoundaryNorm(clevs, cmap.N)

    if data.name in ['tercile','cor']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap)#,clevs,norm,cmap)
    elif data.name in ['crpss','rmsess','kprep','crpss_co2']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap,extend='both')
    ax.coastlines()
    if sig != []:
       if data.name == 'kprep': sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
       else: sigvals = np.where(sig[:,:]<0.05)
       ax.scatter(lon2d[sigvals],lat2d[sigvals],marker='.',c='k',s=5.,lw=0.)
                    
    ax.background_patch.set_facecolor('lightgray')
        
    #cbar = fig.colorbar(cs,cmap=cmap,norm=norm,boundaries=clevs,location='bottom',pad="10%")
    cax = matplotlib.axes.Axes(fig,[0.1, 0.15, 0.8, 0.25])
    cbar = fig.colorbar(cs,ax=cax,cmap=cmap,norm=norm,boundaries=clevs,orientation='horizontal',shrink=0.8)
    
    #fig.colorbar(pcont,ax=cax)  
    if barticks != []: cbar.ax.set_xticklabels(barticks)
    if fname != []: plt.savefig(fname)
    return fig
    #if PLOT: plt.show()
    #else: plt.close('all')    

  
def check_results(predictand,plottype='ensmean',mm=[],extra='',version='',bdnc='/nobackup/users/krikken/SPESv2/ncfiles/'):
    #bdnc = '/nobackup/users/krikken/SPESv2/ncfiles/test/' 
    cmap1 = matplotlib.colors.ListedColormap(['#000099','#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400','#cc0022'])
    cmap2 = matplotlib.colors.ListedColormap(['#3355ff','#66aaff','#77ffff','#ffffff','#ffff33','#ffaa00','#ff4400'])
    cmap_u = '#000099'
    cmap_o = '#cc0022'
    if plottype == 'ensmean':   
        fit_data = xr.open_dataset(bdnc+'pred_v2_'+predictand+'.nc')
        timez = pd.DatetimeIndex(fit_data['time'].sel(time=fit_data['time.month']==mm+1).values)[-1]
        
        if predictand in ['GCEcom','GISTEMP']:  clevz = np.array((-2.,-1.,-0.5,-0.2,0.2,0.5,1.,2.))
        if predictand == 'GPCCcom': clevz = np.array((-200.,-100.,-50.,-20.,20.,50.,100.,200.))
        if predictand == '20CRslp': clevz=np.array((-4.,-2.,-1.,-0.5,0.5,1.,2.,4.))
        
        plotdata(fit_data.kprep.sel(time=timez).mean('ens'),title=predictand+' - '+plottype+' - '+str(timez)[:7],CLICK_D=False,CLICK_C=False,CLICK_R=False,cmap=cmap2,clevs=clevz,cmap_under=cmap_u,cmap_over=cmap_o,predictand=predictand,mm=mm,bdnc=bdnc)

    else:
        scores = xr.open_dataset(bdnc+'scores_v2_'+predictand+'.nc')
        timez = pd.DatetimeIndex(scores['time'].sel(time=scores['time.month']==mm+1).values)[-1]
        if plottype in ['crpss','rmsess']:
            clev = np.array((-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5))
        elif plottype == 'tercile':
            clev = np.array((-100,-70,-60,-50,-40,40,50,60,70,100))
        else: print('plottype not known..');sys.exit()
        plotdata(scores[plottype].sel(time=timez),title=predictand+' - '+plottype+' - '+str(timez)[:7],CLICK_D=True,CLICK_C=False,CLICK_R=False,cmap=cmap2,clevs=clev,cmap_under=cmap_u,cmap_over=cmap_o,predictand=predictand,mm=mm,bdnc=bdnc) 
            
def plotdata(data,cmap=[],cmap_under=[],cmap_over=[],predictand=[],sig=[],fname=[],PLOT=True,clevs=[],barticks=[],CLICK_C=False,CLICK_R=False,CLICK_D=False,clev=[],title=[],mm=[],bdnc=[]):
    print('plotting '+data.name)
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12,8))
    ax = plt.subplot(111, projection=ccrs.PlateCarree())
    ax.set_facecolor('red')
    ax.set_global()
    ax.set_extent([-180,180,90,-90], ccrs.PlateCarree())
    lons,lats = data.lon.values,data.lat.values
    lon2d, lat2d = np.meshgrid(lons, lats)
    if clevs == []:
        clevs = np.arange(np.nanmin(data),np.nanmax(data), 0.1)#[-0.5,-0.35,-0.2,-0.1,0.1,0.2,0.35,0.5]
    if cmap == []: cmap = plt.cm.RdYlBu_r
    if cmap_under != []: cmap.set_under(cmap_under)
    if cmap_over != []: cmap.set_over(cmap_over)
    norm = matplotlib.colors.BoundaryNorm(clevs, cmap.N)

    if data.name in ['tercile','cor']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap)#,clevs,norm,cmap)
    elif data.name in ['crpss','rmsess','kprep']:
        cs = ax.contourf(lons,lats,data.values,clevs,norm=norm,cmap=cmap,extend='both')
    ax.coastlines()
    if sig != []:
       if data.name == 'kprep': sigvals = np.where(np.logical_and(sig[:,:]>0.1,sig[:,:]<1.))
       else: sigvals = np.where(sig[:,:]<0.05)
       ax.scatter(lon2d[sigvals],lat2d[sigvals],marker='.',c='k',s=5.,lw=0.)
                    
    ax.set_facecolor('lightgray')
        
    #cbar = fig.colorbar(cs,cmap=cmap,norm=norm,boundaries=clevs,location='bottom',pad="10%")
    cax = matplotlib.axes.Axes(fig,[0.1, 0.15, 0.8, 0.25])
    cbar = fig.colorbar(cs,ax=cax,cmap=cmap,norm=norm,boundaries=clevs,orientation='horizontal',shrink=0.8)
    ax.set_title(title)
    #fig.colorbar(pcont,ax=cax)  
    if barticks != []: cbar.ax.set_xticklabels(barticks)
    if fname != []: plt.savefig(fname)    
    if CLICK_D: 
            cid = fig.canvas.mpl_connect('button_press_event', onclick_locdata) 
            pickle.dump([ax,lats,lons,predictand,mm,bdnc],open('locdata.pkl','wb'))
    if CLICK_R:
            cid = fig.canvas.mpl_connect('button_press_event', onclick_locregr2d) 
            pickle.dump([ax,lats,lons,predictand,mm,bdnc],file('locregr.pkl','w'))
    print(PLOT)
    if PLOT: plt.show()
    else: plt.close('all')    


def onclick_locdata(event):
    # First return the data from the selected gridpoint
    print(('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        (event.button, event.x, event.y, event.xdata, event.ydata)))
    ax,lats,lons,predictand,mm,bdnc = pickle.load(open('locdata.pkl','rb'))
    # Retrieve associated array indices for the coordinates
    #bdnc = '/nobackup/users/krikken/SPESv2/ncfiles/test/'
    #print(ax,lats,lons,predictand)
    #sys.exit()
    ## Plot model fit data..
    
    data_fit = xr.open_dataset(bdnc+'pred_v2_'+predictand+'.nc')
    timez = pd.DatetimeIndex(data_fit['time'].sel(time=data_fit['time.month']==mm+1).values)[1:]
    data_1d = data_fit.sel(time=timez,lat=event.ydata,lon=event.xdata,method=str('nearest'))
    #print timez
    scores = xr.open_dataset(bdnc+'scores_v2_'+predictand+'.nc')
    timez_sc = pd.DatetimeIndex(scores['time'].sel(time=scores['time.month']==mm+1).values)[1:]
    scores_1d = scores.sel(time=timez_sc,lat=event.ydata,lon=event.xdata,method=str('nearest'))
     
    #predadata = xr.open_dataset(bdnc+'predadata_v2_'+predictand+'.nc')
    #timez2 = pd.DatetimeIndex(predadata['time'].sel(time=predadata['time.month']==mm+1).values)[1:]
    #preda_1d = predadata.sel(time=timez2,lat=event.ydata,lon=event.xdata,method=str('nearest'))
 
    #sys.exit()
    kprep = data_1d.kprep.values
    clim = data_1d.clim.values
    trend = data_1d.trend.values
    obs = data_1d.obs.values
    
    #fig = plt.figure()
    #scores_1d['crpss'].plot()
    #plt.plot(timez_sc,scores_1d['crpss'].sel(time=timez_sc).values)
     

    fig = plt.figure(figsize=(12,4))
    plt.plot(timez,np.nanmean(kprep,axis=1),'r',lw=2,label='fc kprep')
    plt.fill_between(timez,np.nanmean(kprep,axis=1)-np.nanstd(kprep,axis=1),np.nanmean(kprep,axis=1)+np.nanstd(kprep,axis=1),color='r',alpha=0.25)
    
    plt.plot(timez,np.nanmean(clim,axis=1),'b',lw=2,label='fc clim')
    plt.fill_between(timez,np.nanmean(clim,axis=1)+np.nanstd(clim,axis=1),np.nanmean(clim,axis=1)-np.nanstd(clim,axis=1),color='b',alpha=0.25)
    
    plt.plot(timez,obs,'k',lw=2,label='observations')
    plt.plot(timez,trend[:,0],'g',lw=2,label='lin. regr. co2')
    plt.plot(timez,np.nanmean(trend,axis=1)+np.nanstd(trend,axis=1),'g',ls=':',lw=2)
    plt.plot(timez,np.nanmean(trend,axis=1)-np.nanstd(trend,axis=1),'g',ls=':',lw=2)
    #plt.plot(timez2,preda_1d[predictand].sel(time=timez2).values,'k:',lw=2)
    plt.legend()
    
    ## Plot predictor data..
    beta = xr.open_dataset(bdnc+'beta_v2_'+predictand+'.nc')
    timez_b = pd.DatetimeIndex(beta['time'].sel(time=beta['time.month']==mm+1).values)[1:]
    beta_1d = beta.sel(time=timez_b,lat=event.ydata,lon=event.xdata,method=str('nearest'))
    #beta_1d = beta.sel(time=timez_b,lat=20.,lon=20.,method=str('nearest'))

    predodata = xr.open_dataset(bdnc+'predictors_v2_'+predictand+'.nc')
    timez_p = pd.DatetimeIndex(predodata['time'].sel(time=predodata['time.month']==mm+1).values)[1:]

    predodata_1d = predodata.sel(time=timez_p,lat=event.ydata,lon=event.xdata,method=str('nearest'))
    #predodata_1d = predodata.sel(time=timez_p,lat=20.,lon=20.,method=str('nearest'))
    
    
    nr_sigp = np.sum(~np.isnan(beta_1d.beta.values).any(axis=0))
    if nr_sigp == 0:
        print('no significant predictors..')
    else:    
        fig,axs = plt.subplots(nr_sigp,1,sharex=True)
        if nr_sigp == 1: axs = [axs]
        i=0
        for p,pred in enumerate(predodata_1d.data_vars):
            if np.isnan(beta_1d.beta[:,p]).any():
                continue
            else:
                print(i)
                ax2 = axs[i].twinx()
                beta_1d.beta[:,p].plot(ax=ax2)
                predodata_1d[pred].plot(ax=axs[i],color='k')
                if p != 0:axs[i].axhline(color='k')
                #ax2.set_title='hello'
                #axs[i].set_title='be gone with it..'
                i=i+1
        for i,ax in enumerate(axs): ax.set_title('')
        plt.tight_layout()
    
    plt.show()
    
    
