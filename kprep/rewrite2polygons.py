import xarray as xr
import xshape
import numpy as np
import matplotlib.pyplot as plt
import salem

shapefile = '/home/folmer/Dropbox/werk/natural_earth/ne_10m_admin_1_states_provinces'

fields, polygons = xshape.parse_shapefile(shapefile,encoding='latin1') 

ds = xr.open_dataset('/home/folmer/climexp_data/KPREPData/ncfiles_mdc/pred_v2_TMAX_3.nc')

ds.kprep[0,0,0,:].xshape.overlay(shapefile,encoding='latin1')

shdf = salem.read_shapefile(shapefile+'.shp')
