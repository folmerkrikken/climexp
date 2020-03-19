# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys, glob, re, pickle, time
import numpy as np
import scipy
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import scipy.stats

bd = '~/climexp_data/KPREPData/ncfiles/'

cor_fit = np.zeros((4,12))
cor_orig = np.zeros((4,12))
for m in range(1,13):
    # Month 1 (january) is data from OND, and is fitted on FMA data, hence month 3
    pred_fit = xr.open_dataset(bd+'predodata_3m_fit_GCEcom_'+str(m).zfill(2)+'.nc')
    if m+4 > 12:
        pred_fut = xr.open_dataset(bd+'predodata_3m_nc_GCEcom_'+str(m+4-12).zfill(2)+'.nc')
    else:
        pred_fut = xr.open_dataset(bd+'predodata_3m_nc_GCEcom_'+str(m+4).zfill(2)+'.nc')
    
    pred_orig = xr.open_dataset(bd+'predodata_3m_nc_GCEcom_'+str(m).zfill(2)+'.nc')    
    
    for i,var in enumerate(['NINO34','PDO','AMO','IOD']):
        timez = pd.to_datetime(pred_fit.time.values)[:-1]
        timez_f = timez + pd.DateOffset(months=4)
        
        cor_fit[i,m-1] = scipy.stats.pearsonr(pred_fit[var].sel(time=timez).values,
                                              pred_fut[var].sel(time=timez_f).values)[0]
        cor_orig[i,m-1] = scipy.stats.pearsonr(pred_orig[var].sel(time=timez).values,
                                              pred_fut[var].sel(time=timez_f).values)[0]
                                        
f,axs = plt.subplots(2,2,sharex=True,sharey=True)

for i,ax in enumerate(axs.flat):
    ax.plot(cor_fit[i,:],'b')
    ax.plot(cor_orig[i,:],'r')
    ax.set_title(['NINO34','PDO','AMO','IOD'][i])
    ax.set_xticks(np.arange(12))
    ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'])
plt.show()
    
    #sys.exit()
