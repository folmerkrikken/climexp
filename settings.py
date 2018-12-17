import platform
import os

if platform.system() == 'Darwin':
    # Mac computer
    HOME_DIR = ''
    WORKING_DIR = '/Users/gj/climexp'

    os.environ['PATH'] = '/sw/bin:{WORKING_DIR}/bin:'.format(
       WORKING_DIR=WORKING_DIR) + os.environ['PATH']

    # For NCL
    os.environ['PATH'] = '/usr/local/ncl/bin:' + os.environ['PATH']
    os.environ['NCARG_ROOT'] = '/usr/local/ncl'

else:
    # Linux computer
    HOME_DIR = '/home/oldenbor'
    WORKING_DIR = '{HOME_DIR}/climexp'.format(HOME_DIR=HOME_DIR)

    os.environ['PATH'] = '{HOME_DIR}/bin:{WORKING_DIR}/bin:{HOME_DIR}/local/lib:'.format(
       HOME_DIR=HOME_DIR, 
       WORKING_DIR=WORKING_DIR) + os.environ['PATH']

    # For NCL
    os.environ['PATH'] = '/usr/local/ncl/bin:'.format(
       WORKING_DIR=WORKING_DIR) + os.environ['PATH']
    os.environ['NCARG_ROOT'] = '/usr/local/ncl'.format(WORKING_DIR=WORKING_DIR)
    ### os.environ['HDF5_DISABLE_VERSION_CHECK'] = '1'

    # For the NetCDF library
    ## os.environ['LD_LIBRARY_PATH'] = '{HOME_DIR}/lib:'.format(HOME_DIR=HOME_DIR)

os.chdir(WORKING_DIR)
