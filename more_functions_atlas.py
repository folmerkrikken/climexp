"""more functions, these are only for the web version"""

import glob
import re
import os
import sys
import logging
import settings
import subprocess
from formparameters import obs_var_values, obs_tas_values, obs_tasmax_values, obs_tasmin_values, obs_pr_values, obs_psl_values

class GetModelError(Exception):
    """Raised when a error occured in function get_model."""
    pass


def lookup_region(params, lwrite=False):
    """in order to use the Atlas routine in the KNMI Atlas
       a routine to translate the srex+ name into the Atlas region/subregion convention."""

    log = logging.getLogger('lookup_region')
    log.setLevel(logging.DEBUG)

    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    log.addHandler(hdlr)
    del hdlr

    paramsDict = params.__dict__

    if lwrite:
        print "lookup_region: input %(FORM_srex)s<br>" % paramsDict
    
#log.debug('')        
#    log.debug("lookup_region: input %(FORM_srex)s" % paramsDict)

    regions = {'world': ['world', 3],
               'worldland': ['world', 1],
               'worldsea': ['world', 2],
               'NAmerica': ['NAmerica', 1],
               'SAmerica': ['SAmerica', 1],
               'Europe': ['Europe', 1],
               'Africa': ['Africa', 1],
               'Asia': ['Asia', 1],
               'Australia': ['Australia', 1],
               'Arcticland': ['arctic', 1],
               'Arcticsea': ['arctic', 2],
               'CGI': ['highlatitudes', 1],
               'NAS': ['highlatitudes', 2],
               'ALA': ['westnorthamerica', 1],
               'WNA': ['westnorthamerica', 2],
               'CNA': ['eastnorthamerica', 1],
               'ENA': ['eastnorthamerica', 2],
               'CAM': ['centralamerica', 1],
               'Caribbean': ['centralamerica', 2],
               'AMZ': ['northsouthamerica', 1],
               'NEB': ['northsouthamerica', 2],
               'WSA': ['southsouthamerica', 1],
               'SSA': ['southsouthamerica', 2],
               'NEU': ['northeurope', 1],
               'CEU': ['northeurope', 2],
               'MED': ['mediterranean', 1],
               'SAH': ['mediterranean', 2],
               'WAF': ['weafrica', 1],
               'EAF': ['weafrica', 2],
               'SAF': ['southafrica', 1],
               'WIndian': ['southafrica', 2],
               'WAS': ['centralasia', 1],
               'CAS': ['centralasia', 2],
               'TIB': ['eastasia', 2],
               'EAS': ['eastasia', 1],
               'SAS': ['southasia', 1],
               'NIndian': ['southasia', 2],
               'SEA': ['southeastasia', 1],
               'SEAsia_sea': ['southeastasia', 2],
               'NAU': ['australia', 1],
               'SAU': ['australia', 2],
               'NTPacific': ['pacific', 1],
               'EQPacific': ['pacific', 2],
               'STPacific': ['pacific', 3],
               'Antarcticland': ['antarctica', 1],
               'Antarcticsea': ['antarctica', 2]}

    # TODO; raise an exception
#       echo "lookup_region: error: cannot find input $FORM_srex"; exit -1;;
    region, subregion = regions[params.FORM_srex]

    if lwrite:
        print "lookup_region: found region={region}, subregion={subregion}<br>".format(region=region, subregion=subregion)
    
#    log.debug("lookup_region: found region={region}, subregion={subregion}".format(region=region, subregion=subregion))

    return region, subregion     


def get_file_list(exp, params):
    """
    Input:
        AtlasParams object
        .FORM_var
        .FORM_output
        .FORM_dataset

    Output:
        (typeVar, dir ,files)
    """
    
    files = []
    paramsDict = params.__dict__
    res = ''
    typeVar = ''

    if params.FORM_output == 'map' or params.FORM_region == 'mask':
        # interpolated fields
        res = '_144'

    if params.FORM_dataset in ['CMIP5', 'CMIP5one']:

        # output a list of files in $files and a dirName to put the output $dirName
        var = params.FORM_var
        if var in ['tas', 'tasmin', 'tasmax', 'pr', 'evspsbl', 'pme', 'huss', 'hurs', 'rsds', 'psl']:
            typeVar = 'Amon'
        elif var in ['tos', 'sos', 'zos']:
            typeVar = 'Omon'
        elif var in ['mrso', 'mrro', 'mrros']:
            typeVar = 'Lmon'
        elif var == 'sic':
            typeVar = 'OImon'
        else:
            raise ValueError("get_file_list: error: unknown variable {var}".format(var=var))

        paramsDict['type'] = typeVar
        paramsDict['res'] = res

    elif params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:

        # output a list of files in $files and a dirName to put the output $dirName
        var = params.FORM_var
        typeVar = 'yr'
        paramsDict['type'] = typeVar
        paramsDict['res'] = res

    elif params.FORM_dataset == 'CMIP3':
    
        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        typeVar = 'A1'
        paramsDict['type'] = typeVar
        paramsDict['res'] = res
    
    if params.FORM_dataset == 'CMIP5':

        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        if params.FORM_plotvar == 'mean':
            fileName = 'CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_modmean_{exp}_000.nc'.format(exp=exp, **paramsDict)
            files.append(fileName)
        else:
            # we know that p goes to 3...
            maskFile1 = "CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p1{res}.nc".format(exp=exp, **paramsDict)
            maskFile2 = "CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p2{res}.nc".format(exp=exp, **paramsDict)
            maskFile3 = "CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p3{res}.nc".format(exp=exp, **paramsDict)

            files += glob.glob(maskFile1)
            files += glob.glob(maskFile2)
            files += glob.glob(maskFile3)

    elif params.FORM_dataset == 'CMIP5one':

        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        if params.FORM_plotvar == 'mean':
            files.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_onemean_{exp}_000.nc".format(exp=exp, **paramsDict))
        else:
            if exp == 'rcp45to85':
                explist = [ 'rcp45', 'rcp60', 'rcp85']
            else:
                explist = [ exp ]
            for e in explist:
                # we know that p goes to 3...
                maskFiles = []
                maskFiles.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_[!E]*_{exp}_r1i1p1{res}.nc".format(exp=e, **paramsDict))
                maskFiles.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_EC-EARTH_{exp}_r8i1p?{res}.nc".format(exp=e, **paramsDict))
                maskFiles.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_HadGEM2-ES_{exp}_r2i1p?{res}.nc".format(exp=e, **paramsDict))
                maskFiles.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_GISS*_{exp}_r1i1p2{res}.nc".format(exp=e, **paramsDict))
                maskFiles.append("CMIP5/monthly/{FORM_var}/{FORM_var}_{type}_GISS*_{exp}_r1i1p3{res}.nc".format(exp=e, **paramsDict))

                for mask in maskFiles:
                    files += glob.glob(mask)

            # get rid of the HadGEM2-ES_*_r1i1p1 one...
            newfiles = []
            for file in files:
                if not re.match(".*HadGEM2-ES_.*_r1i1p1_.*",file):
                    newfiles.append(file)
            files = newfiles

    elif params.FORM_dataset == 'CMIP5ext':

        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        if params.FORM_plotvar == 'mean':
            fileName = 'CMIP5/annual/{FORM_var}/{FORM_var}_{type}_modmean_{exp}_000.nc'.format(exp=exp, **paramsDict)
            files.append(fileName)
        else:
            # we know that p goes to 3...
            maskFile1 = "CMIP5/annual/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p1{res}.nc".format(exp=exp, **paramsDict)
            maskFile2 = "CMIP5/annual/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p2{res}.nc".format(exp=exp, **paramsDict)
            maskFile3 = "CMIP5/annual/{FORM_var}/{FORM_var}_{type}_*_{exp}_r*i1p3{res}.nc".format(exp=exp, **paramsDict)

            files += glob.glob(maskFile1)
            files += glob.glob(maskFile2)
            files += glob.glob(maskFile3)

    elif params.FORM_dataset == 'CMIP5extone':

        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        if params.FORM_plotvar == 'mean':
            files.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_onemean_{exp}_000.nc".format(exp=exp, **paramsDict))
        else:
            # we know that p goes to 3...
            maskFiles = []
            maskFiles.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_[!EH]*_{exp}_r1i1p1{res}.nc".format(exp=exp, **paramsDict))
            maskFiles.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_HadGEM2-CC_{exp}_r8i1p?{res}.nc".format(exp=exp, **paramsDict))
            maskFiles.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_HadGEM2-ES_{exp}_r2i1p?{res}.nc".format(exp=exp, **paramsDict))
            maskFiles.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_GISS*_{exp}_r1i1p2{res}.nc".format(exp=exp, **paramsDict))
            maskFiles.append("CMIP5/annual/{FORM_var}/{FORM_var}_{type}_GISS*_{exp}_r1i1p3{res}.nc".format(exp=exp, **paramsDict))

            for mask in maskFiles:
                files += glob.glob(mask)

    elif params.FORM_dataset == 'CMIP3':

        dirName = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
        if params.FORM_plotvar == 'mean':
            files.append("IPCCData/{FORM_scenario_cmip3}/{FORM_var}_cmip3_ave_mean{res}.nc".format(exp=exp, **paramsDict))
        else:
            cmip3models = [ "bccr_bcm2_0", "cccma_cgcm3_1", "cccma_cgcm3_1_t63", "cnrm_cm3", "csiro_mk3_0", "csiro_mk3_5", "gfdl_cm2_0", "gfdl_cm2_1", "giss_aom", "giss_model_e_h", "giss_model_e_r", "ingv_echam4", "inmcm3_0", "ipsl_cm4", "miroc3_2_medres", "miroc3_2_hires", "miub_echo_g", "mpi_echam5", "mri_cgcm2_3_2a", "ncar_ccsm3_0", "ncar_pcm1", "ukmo_hadgem1", "ukmo_hadcm3" ]
            for model in cmip3models:
                file="IPCCData/{FORM_scenario_cmip3}/{FORM_var}_{typeVar}_{model}_144.nc".format(dirName=dirName, typeVar=typeVar, model=model, **paramsDict)
###                os.environ['FORM_field'] = FORM_field
###                output = subprocess.check_output("./call_queryfield.cgi", shell = True)
###                file = re.search(r"file=(.*)\s", output).groups()[0]
                if os.path.exists(file):
                    # one run only
                    files.append(file)
                else:
                    # ensemble
                    file = file.replace("_144","_%%_144")
                    i = 0
                    ii = '00'
                    ensfile = file.replace("%%",ii)
                    while os.path.exists(ensfile):
                        files.append(ensfile)
                        i += 1
                        ii = '%2.2i' % i
                        ensfile = file.replace("%%",ii)


#    elif params.FORM_dataset == 'RT2b':
#        if params.FORM_plotvar == 'mean':
#            files='ENSEMBLES_RCM/rt2b/rt2b_modmean_%(FORM_scenario_rt2b)s_25km_%(FORM_var)s_00.nc' % paramsDict
#        else
#            files='ENSEMBLES_RCM/rt2b/rt2b_*_%(FORM_scenario_rt2b)s_25km_%(FORM_var)s_MM.nc' % paramsDict
#        fi
#
#    elif params.FORM_dataset == 'RT3':
#        if params.FORM_plotvar == mean:
#            files = 'ENSEMBLES_RCM/rt3/rt3_modmean_25km_%(FORM_var)s_00.nc' % paramsDict
#        else
#            files='ENSEMBLES_RCM/rt3/rt3_*_25km_%(FORM_var)s_MM.nc' % paramsDict
#        fi
#
    elif params.FORM_dataset == 'ERAi':
        dirName = '{FORM_dataset}'.format(**paramsDict)
        FORM_field = 'erai_%(FORM_var)s' % paramsDict
        os.environ['FORM_field'] = FORM_field
        output = subprocess.check_output("./call_queryfield.cgi", shell = True)
        file = re.search(r"file=(.*)\s", output)
        if file:
            file = file.groups()[0]
        else:
            print "get_file_list: error: cannot find %s<br>" % FORM_field
        files = [file]

    elif params.FORM_dataset == '20CR':
        dirName = '{FORM_dataset}'.format(**paramsDict)
        FORM_field = 'c%(FORM_var)s' % paramsDict
        os.environ['FORM_field'] = FORM_field
        output = subprocess.check_output("./call_queryfield.cgi", shell = True)
        file = re.search(r"file=(.*)\s", output)
        if file:
            file = file.groups()[0]
        else:
            print "get_file_list: error: cannot find %s<br>" % FORM_field
        files = [file]

    elif params.FORM_dataset == 'obs':
        dirName = '{FORM_dataset}'.format(**paramsDict)
        var = params.FORM_var
        if var in [el[0] for el in obs_var_values]: # make sure it is trusted input
            variable = 'params.FORM_obs_{var}'.format(var=var)
            FORM_field = eval(variable)
        else:
            print 'get_file_list: unknown value for var %s<br>' % var
        os.environ['FORM_field'] = FORM_field
        output = subprocess.check_output("./call_queryfield.cgi", shell = True)
        file = re.search(r"file=(.*)\s", output)
        if file:
            file = file.groups()[0]
        else:
            print "get_file_list: error: cannot find %s<br>" % FORM_field
        files = [file]

    

#    elif params.FORM_dataset == 'obs':
#        field_name=FORM_obs_$FORM_obs
#        FORM_field=${!field_name}
#        . ./queryfield.cgi
#        files=$fileName
    else:
        print "get_file_list: error: unknown dataset %s<br>" % params.FORM_dataset


    return (typeVar, dirName, files)

def strip_begin(text, prefix):
    if not text.startswith(prefix):
        return text
    return text[len(prefix):]

def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def get_model(params, filename, typeVar):
    """get the model name back from the file name :-(
       also set LSMASK while we are at it."""

    paramsDict = params.__dict__
    var = params.FORM_var
    LSMASK = None

    if params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:

        model = os.path.basename(filename)
        model = strip_begin(model, '{var}_{type}_'.format(var=var, type=typeVar))           
        idx = model.rfind('_rcp')
        if idx >= 0:
            model = model[:idx]


        if model.endswith('mean'):
            # coordinate with queryfield...
            if var in ['sic', 'tos', 'sos']:
                LSMASK = 'CMIP5/monthly/lsmask_cmip3_288.nc'
            else:
                LSMASK = 'CMIP5/monthly/lsmask_cmip3_144.nc'
        else:
            if typeVar in ['Amon', 'Lmon', 'yr']:
                if model == 'EC-EARTH':
                    trylsmask = 'CMIP5/fixed/sftlf.EC-EARTH.nc'
                elif model == 'FIO-ESM':
                    trylsmask = 'CMIP5/fixed/sftlf.FIO-ESM.nc'
                elif model == 'GISS-E2-H-CC':
                    trylsmask = 'CMIP5/fixed/sftlf_fx_GISS-E2-H_historical_r0i0p0.nc'
                elif model == 'GISS-E2-R-CC':
                    trylsmask = 'CMIP5/fixed/sftlf_fx_GISS-E2-R_historical_r0i0p0.nc'
                elif model.startswith('HadGEM2'):
                    trylsmask = 'CMIP5/fixed/sftlf_fx_HadGEM2-ES_historical_r1i1p1.nc'
                elif model == 'inmcm4':
                    trylsmask = 'CMIP5/fixed/sftlf_fx_{model}_rcp45_r0i0p0.nc'.format(model=model)
                else:
                    trylsmask = 'CMIP5/fixed/sftlf_fx_{model}_historical_r0i0p0.nc'.format(model=model)

            # TODO: implement this                    
            trylsmask_home = '{workingDir}/{trylsmask}'.format(workingDir=settings.WORKING_DIR, trylsmask=trylsmask)

            if (os.path.exists(trylsmask) and os.path.getsize(trylsmask) !=0) or (os.path.exists(trylsmask_home) and os.path.getsize(trylsmask_home) != 0):
                LSMASK = trylsmask
            else:
                print '<b>Cannot find mask file %s</b><br>' % trylsmask
                raise PlotSeriesError('<b>Cannot find mask file %s</b><br>' % trylsmask)

    elif params.FORM_dataset in ['CMIP3', 'ERAi', '20CR', 'obs']:

        ensfile = re.sub(r'_0[0-9]_', '_%%_', os.path.basename(filename))
        ensfile = ensfile.replace("_144.nc","")
        ###print "ensfile = %s<br>" % ensfile

        f = open('queryfield.cgi','r')
        line = "aap"
        while line != "":
            line = f.readline()
            if line.find(ensfile) >= 0:
                i = line.find(')')
                FORM_field = line[:i]
                i = FORM_field.rfind('|')
                if i >= 0:
                    FORM_field = FORM_field[i+1:]
                ###print "FORM_field = %s<br>" % FORM_field
                if params.FORM_dataset == 'CMIP3':
                    i = FORM_field.find("_")
                    model = FORM_field[i+1:]
                    i = model.rfind("_")
                    model = model[:i]
                elif params.FORM_dataset == 'ERAi':
                    model = 'erai'
                elif params.FORM_dataset == '20CR':
                    model = 'c'
                elif params.FORM_dataset == 'obs':
                    model = FORM_field
                else:
                    print 'error4: unknown dataset {dataset}<br>'.format(dataset=params.FORM_dataset) 
                ###print "model = %s<br>" % model
                i = line.find('LSMASK=')
                if i < 0:
                    print 'get_model: cannot find LSMASK in %s<br>' % line
                    LSMASK = 'unknown'
                else:
                    LSMASK = line[i+7:]
                    i = LSMASK.find(';')
                    LSMASK = LSMASK[:i]
                    LSMASK = LSMASK.replace('"','')
                    ###print "LSMASK = %s<br>" % LSMASK
                break
        f.close()

#    RT2b)
#        model=`basename $file .nc`
#        model=${model#rt2b_}
#        model=${model%_${FORM_scenario_rt2b}*};;
#    RT3)
#        model=`basename $file .nc`
#        model=${model#rt2b_}
#        model=${model%_25km*};;
#    obs)
#        model=$FORM_field;;
#    *) echo "error: unknown dataset $FORM_dataset"; . ./myvinkfoot.cgi; exit;;
#    esac
    else:
        raise GetModelError("get_model: unknown dataset {FORM_dataset}".format(**paramsDict))

    if not model:
        raise GetModelError("Something went wrong in get_model with filename '{filename}' dataset '{FORM_dataset}' and var '{var}'".format(var=var, LSMASK=LSMASK, filename=filename, **paramsDict))
   
#    if LSMASK is None:
#        raise GetModelError("Cannot find LSMASK '{LSMASK}' with filename '{filename}', dataset '{FORM_dataset}' and var '{var}'.".format(var=var, LSMASK=LSMASK, filename=filename, **paramsDict))

    return model, LSMASK        

def get_rip(params, filename):
    """get the RIP string and integers from the file name."""

    paramsDict = params.__dict__
    rip = ""
    r = -1
    i = -1
    p = -1

    if params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
        rip = os.path.basename(filename)
        idx = rip.rfind('_r')
        if idx >= 0:
            rip = rip[idx+1:]
        idx = rip.rfind('_')
        if idx >= 0:
            rip = rip[:idx]
        idx = rip.rfind('.')
        if idx >= 0:
            rip = rip[:idx]
        
        idx = rip.find('i')
        if idx >= 0:
            r = int(rip[1:idx])
            i = int(rip[idx+1:idx+2])
            p = int(rip[idx+3:idx+4])
    
    elif params.FORM_dataset == 'CMIP3':

        rip = os.path.basename(filename)
        ###print 'file = %s<br>' % rip
        idx = rip.rfind('_0')
        if idx >= 0 and rip[idx+3:idx+4] == '_':
            rip = rip[idx+1:idx+3]
            ###print 'rip = %s<br>' % rip
            r = int(rip) + 1
        else:
            r = 1
        i = 1
        p = 1
        ###print 'r = %i<br>' % r

    return rip, r, i, p        

def get_region_extension(params):

    paramsDict = params.__dict__

    if params.FORM_region == 'srex':
        region_extension = params.FORM_srex
    if params.FORM_region == 'countries':
        region_extension = params.FORM_country
    elif params.FORM_region == 'point':
        region_extension = "%(FORM_lat)sN_%(FORM_lon)sE" % paramsDict
    elif params.FORM_region in ['box', 'mask']:
        if params.FORM_masktype.find('sea') >= 0:
            lsext = "_sea"
        elif params.FORM_masktype.find('lan') >= 0:
            lsext = "_land"
        else:
            lsext = ""
        region_extension = "{FORM_lat1}-{FORM_lat2}N_{FORM_lon1}-{FORM_lon2}E{lsext}".format(lsext=lsext, **paramsDict)
    else:
        # TODO: raise an exception
#        echo "error: unknown region %(FORM_region)s" % paramsDict
#        exit -1
        pass

    return region_extension

def define_dataset(dataset,field):

    if dataset in ['CMIP5','CMIP5ext']:
        datasetname = 'full CMIP5 ensemble'
    elif dataset in 'CMIP5one':
        datasetname = 'AR5 CMIP5 subset'
    elif dataset in 'CMIP5extone':
        datasetname = 'CMIP5 one member'
    elif dataset == 'CMIP3':
        datasetname = 'CMIP3'
    elif dataset == 'ERAi':
        datasetname = 'ERA-interim'
    elif dataset == '20CR':
        datasetname = '20CR'
    elif dataset == 'obs':
        names = [ el[1] for el in obs_tas_values + obs_tasmin_values + obs_tasmax_values + obs_pr_values + obs_psl_values if el[0] == field ]
        datasetname = names[0]
    else:
        datasetname = dataset

    return datasetname

def getboxfrompolygon(polyRegionFile):

    cmd = "bin/polygon2box {polyRegionFile} | tr -d ' '".format(polyRegionFile=polyRegionFile)
    ###print "getboxfrompolygon: cmd = %s<br>" % cmd
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    xmin = re.search(r"xmin=(.*)\s", output).groups()[0]
    xmax = re.search(r"xmax=(.*)\s", output).groups()[0]
    ymin = re.search(r"ymin=(.*)\s", output).groups()[0]
    ymax = re.search(r"ymax=(.*)\s", output).groups()[0]

    return xmin, xmax, ymin, ymax

