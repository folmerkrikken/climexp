"""PlotAtlasSeries class"""

import os
import re
import logging
import sys
import resource
import subprocess
import tempfile
from time import gmtime, strftime
import settings
from more_functions_atlas import *
from define_functions_atlas import *
from define_functions import *
from defineregion import DefineRegion
from util import month2string

class PlotSeriesError(Exception):
    """Raised when a error occured in PlotSeries."""
    pass


class PlotAtlasSeries:

    def __init__(self, params=None, logLevel=logging.INFO, isLogFormatHTML=True):
        """Initialize the object."""

        # Create a logger
        self.log = logging.getLogger('PlotAtlasSeries')
        self.log.setLevel(logLevel)

        if not isLogFormatHTML:
#            hdlr = logging.NullHandler(sys.stdout)
            self.hdlr = logging.StreamHandler(sys.stdout)
            self.hdlr.setFormatter(logging.Formatter('\033[1;31m%(name)s(%(lineno)s):\033[1;0m \033[1;1m%(message)s\033[1;0m'))
            self.log.addHandler(self.hdlr)
        else:
            self.hdlr = logging.StreamHandler(sys.stdout)
            self.hdlr.setFormatter(logging.Formatter('<b>%(name)s(%(lineno)s)</b>: <i>%(message)s</i><br>'))
            self.log.addHandler(self.hdlr)

        self.logOut = logging.getLogger('htmlOutput')
        self.logOut.setLevel(logLevel)
        self.hdlrOut = logging.StreamHandler(sys.stdout)
        self.hdlrOut.setFormatter(logging.Formatter('%(message)s'))
        self.logOut.addHandler(self.hdlrOut)

        params.dump()
        self.params = params
        self.typeVar = None
        self.ensemble = False

        # increase the stack size
        try:
            resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        except ValueError as e:
            self.log.warning("Cannot increase stack size")

        # Set temporary folder
        self.tempDir = tempfile.mkdtemp()
        self.log.debug('Use temporary folder: %s' % self.tempDir)
        
        self.maskfile = None

        # set flag for ensembles
        if self.params.FORM_dataset.split('-')[0] in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone', 'CMIP3', 'CORDEX']:
            self.ensemble = True


    def __del__(self):

        self.log.removeHandler(self.hdlr)

    def set_dirs(self, dir, paramsDict):
        """ make directory names """
        monthlydir = 'atlas/series/{dir}/monthly/{region_extension}'.format(dir=dir, region_extension=self.region_extension)
        anomdir = 'atlas/series/{dir}/monthly_anom_{FORM_anom1}_{FORM_anom2}_mon{FORM_mon}_ave{FORM_sum}/{region_extension}'.format(dir=dir, region_extension=self.region_extension, **paramsDict)
        if self.params.FORM_anomaly != 'on':
            dump0dir = 'atlas/series/{dir}/monthly_dump0/{region_extension}'.format(dir=dir, region_extension=self.region_extension)
            dump1dir = 'atlas/series/{dir}/monthly_dump1/{region_extension}'.format(dir=dir, region_extension=self.region_extension)
        else:
            dump0dir = 'atlas/series/{dir}/monthly_dump0_{FORM_anom1}_{FORM_anom2}_mon{FORM_mon}_ave{FORM_sum}/{region_extension}'.format(dir=dir, region_extension=self.region_extension, **paramsDict)
            dump1dir = 'atlas/series/{dir}/monthly_dump1_{FORM_anom1}_{FORM_anom2}_mon{FORM_mon}_ave{FORM_sum}/{region_extension}'.format(dir=dir, region_extension=self.region_extension, **paramsDict)
        return monthlydir, anomdir, dump0dir, dump1dir

    def get_series_name(self, monthlydir, basename, region_extension):
        """ construct the name of the time series """
        series = '{monthlydir}/time_{basename}_{region_extension}.dat'.format(monthlydir=monthlydir, basename=basename, region_extension=self.region_extension)
        return series

    def get_aseries_name(self, anomdir, series, paramsDict):
        """ construct the name of the anomaly series """
        if not self.params.FORM_normsd:
            aseries = '{anomdir}/{abasename}_anom_{FORM_anom1}_{FORM_anom2}.txt'.format(abasename=os.path.splitext(os.path.basename(series))[0], anomdir=anomdir, **paramsDict)
        else:
            abasename = os.path.splitext(os.path.basename(series))[0]
            abasename = abasename.replace('_'+self.params.FORM_var+'_','_'+self.params.FORM_var+'rel_')
            aseries = '{anomdir}/{abasename}_anom_{FORM_anom1}_{FORM_anom2}_mon{FORM_mon}_ave{FORM_sum}.txt'.format(abasename=abasename, anomdir=anomdir, **paramsDict)
        return aseries

    def get_dumpfile_name(self, dumpdir, aseries, ext, paramsDict):
        """ construct name of dumpfile either historical (0) or RCP (1) """
        dumpfile = '{dumpdir}/{basename}_mon{FORM_mon}_ave{FORM_sum}_dump{ext}.txt'.format(dumpdir=dumpdir, basename=os.path.splitext(os.path.basename(aseries))[0], ext=ext, **paramsDict)
        return dumpfile

    def get_dumpfile_names(self, aseries, dir, exts, paramsDict):
        """ construct name of both dumpfiles, historical (0) or RCP (1) """
        dumpfile0 = ""
        dumpfile1 = ""
        for ext in exts:
            (monthlydir, anomdir, dump0dir, dump1dir) = self.set_dirs(dir, paramsDict)
            if ext == 0:
                dumpfile0 = self.get_dumpfile_name(dump0dir, aseries, ext, paramsDict)
            elif ext == 1:
                dumpfile1 = self.get_dumpfile_name(dump1dir, aseries, ext, paramsDict)
        return dumpfile0, dumpfile1


    def process(self, lwrite=False):
        """ main routine """

        paramsDict = self.params.__dict__
        
        if self.params.FORM_normsd == 'normsd' and self.params.FORM_anomaly != 'on':
            self.logOut.info("Error: a reference period is needed for relative changes")
            return None

        for dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone', self.params.FORM_dataset]:
            dir = 'atlas/series/{dataset}'.format(dataset=dataset)
            if not os.path.isdir(dir):
                os.makedirs(dir)
        # First find files for all experiments requested
        if self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
            # params.FORM_rcp26, _rcp45, _rcp60, _rcp85
            lstExps = [(self.params.FORM_rcp26, 'rcp26'), (self.params.FORM_rcp45, 'rcp45'),
                       (self.params.FORM_rcp60, 'rcp60'), (self.params.FORM_rcp85, 'rcp85')]
            # Create a list of experiments
            exps = [el[1] for el in lstExps if el[0]]
        elif self.params.FORM_dataset.split('-')[0] in ['CORDEX']:
            # params.FORM_rcp26, _rcp45, _rcp85
            lstExps = [(self.params.FORM_rcp26, 'rcp26'), (self.params.FORM_rcp45, 'rcp45'),
                       (self.params.FORM_rcp85, 'rcp85')]
            # Create a list of experiments
            exps = [el[1] for el in lstExps if el[0]]
        elif self.params.FORM_dataset == 'CMIP3':
            exps = ['sresa1b']
        elif self.params.FORM_dataset in ['ERAi', 'ERA20C', '20CR']:
            exps = ['reanalysis']
        elif self.params.FORM_dataset == 'obs':
            exps = ['observations']

        if self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
            for exp in exps:
                dirall = 'atlas/series/CMIP5/{exp}'.format(exp=exp)
                if not os.path.isdir(dirall):
                    os.makedirs(dirall)
        if self.params.FORM_dataset == 'CMIP5one':
            # share all time series with CMIP5    
            for exp in exps:
                dirone = 'atlas/series/CMIP5one/{exp}'.format(exp=exp)
                if not os.path.islink(dirone):
                    os.symlink('../CMIP5/{exp}'.format(exp=exp), dirone)
                dir = 'atlas/series/CMIP5/{exp}'.format(exp=exp)
                if not os.path.isdir(dir):
                    os.makedirs(dir)
        if self.params.FORM_dataset == 'CMIP5extone':
            # share all time series with CMIP5ext  
            for exp in exps:
                dirone = 'atlas/series/CMIP5extone/{exp}'.format(exp=exp)
                if not os.path.islink(dirone):
                    os.symlink('../CMIP5ext/{exp}'.format(exp=exp), dirone)
                dir = 'atlas/series/CMIP5ext/{exp}'.format(exp=exp)
                if not os.path.isdir(dir):
                    os.makedirs(dir)
        if self.params.FORM_dataset.split('-')[0] == 'CORDEX':
            for exp in exps:
                dir = 'atlas/series/{dataset}/{exp}'.format(dataset=self.params.FORM_dataset, exp=exp)
                if not os.path.isdir(dir):
                    os.makedirs(dir)

        varObj = DefineVar(self.params.FORM_var, self.params.FORM_normsd)
        save_plotvar = self.params.FORM_plotvar
        partfiles = []
        for exp in exps:
            printexp = True
            files = []
            self.params.FORM_plotvar = 'something'
            (self.typeVar, dir, partfiles) = get_file_list(exp, self.params)
            files += partfiles
            if self.ensemble:
                # also compute the mean
                self.params.FORM_plotvar = 'mean'
                (self.typeVar, dir, partfiles) = get_file_list(exp, self.params)
                files += partfiles
            self.params.FORM_plotvar = save_plotvar

            if not files:
                raise PlotSeriesError('No available input files for the time series.')

            # Next compute monthly time series
            self.region_extension = get_region_extension(self.params)
    
            if self.params.FORM_normsd and varObj.norelative == True:
                self.params.FORM_normsd = ""
                self.logOut.info("Ignoring request for relative changes for this variable.<br>")

            if self.params.FORM_anomaly == 'on':
                if not self.params.FORM_anom1:
                    self.params.FORM_anom1 = 1986
                if not self.params.FORM_anom2:
                    self.params.FORM_anom2 = 2005
                if self.params.FORM_anom1 > self.params.FORM_anom2:
                    raise PlotSeriesError("error: anomalies from {FORM_anom1} to {FORM_anom2} are not defined".format(**paramsDict))

            for idxFilename, filename in enumerate(files):            
                # deduce model from 'filename' and get path to 'lsmask'
                model, LSMASK = get_model(self.params, filename, self.typeVar)

                if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                    # the following routines use the averaging period, set it to annual
                    # they were already written to the form and saved to the defaults file
                    self.params.FORM_mon = 1
                    self.params.FORM_sum = 12
                if self.params.FORM_dataset == '20CR':
                    basename = "c{var}".format(var=self.params.FORM_var)
                elif self.params.FORM_dataset == 'obs':
                    basename = "{model}".format(model=model)
                else:
                    basename = os.path.splitext(os.path.basename(filename))[0]
                (monthlydir, anomdir, dump0dir, dump1dir) = self.set_dirs(dir, paramsDict)
                ###print "exp = %s<br>" % exp
                ###print "dir = %s<br>" % dir
                ###print "monthlydir = %s<br>" % monthlydir
                ###print "basename = %s<br>" % basename
                series = self.get_series_name(monthlydir, basename, self.region_extension)
                for d in [ monthlydir, anomdir, dump0dir, dump1dir ]:
                    if not os.path.exists(d):
                        os.makedirs(d)

                if self.params.FORM_region == 'point':
                    args = "{FORM_lon} {FORM_lon} {FORM_lat} {FORM_lat} interpolate".format(**paramsDict)
                    self.regionname = "{FORM_lat}N, {FORM_lon}E".format(**paramsDict)

                elif self.params.FORM_region == 'box':
                    if self.params.FORM_masktype == 'all':
                        lsargs = ""
                        lsext = ""
                        lsname = ""
                    else:
                        lsargs = "lsmask {LSMASK} {FORM_masktype}".format(LSMASK=LSMASK, **paramsDict)
                        if self.params.FORM_masktype.find('sea') >= 0:
                            lsext = "_sea"
                            lsname = " (sea)"
                        if self.params.FORM_masktype.find('lan') >= 0:
                            lsext = "_land"
                            lsname = " (land)"
                
                    args = "{FORM_lon1} {FORM_lon2} {FORM_lat1} {FORM_lat2} {lsargs} nearest".format(lsargs=lsargs, **paramsDict)
                    self.regionname = "{FORM_lat1}-{FORM_lat2}N, {FORM_lon1}-{FORM_lon2}E{lsname}".format(lsname=lsname, **paramsDict)
         
                elif self.params.FORM_region == 'srex':
                    region, subregion = lookup_region(self.params)
                
                    reg = DefineRegion(region)
                    self.regionname = reg.name[subregion]

                    if reg.abbr[subregion]:
                        # the region is defined by a mask
                        maskfile = 'srex_masks/{abbr_subregion}/mask_{model}_{abbr_subregion}.nc'.format(abbr_subregion=reg.abbr[subregion], model=model)
                        self.maskfile = maskfile

                        if not os.path.exists(maskfile) or os.path.getsize(maskfile) == 0:
                            raise PlotSeriesError("error: cannot locate maskfile {maskfile}".format(maskfile=maskfile))

                        args = "mask {maskfile}".format(maskfile=maskfile)
                    else:
                        if LSMASK:
                            args = "{lon1_subregion} {lon2_subregion} {lat1_subregion}  {lat2_subregion} lsmask {LSMASK} {lsmask_subregion}".format(lon1_subregion=reg.lon1[subregion],
                                    lon2_subregion=reg.lon2[subregion],lat1_subregion=reg.lat1[subregion],lat2_subregion=reg.lat2[subregion], LSMASK=LSMASK, lsmask_subregion=reg.lsmask[subregion])
                        else:
                            args = "{lon1_subregion} {lon2_subregion} {lat1_subregion}  {lat2_subregion}".format(lon1_subregion=reg.lon1[subregion],
                                    lon2_subregion=reg.lon2[subregion],lat1_subregion=reg.lat1[subregion],lat2_subregion=reg.lat2[subregion], LSMASK=LSMASK, lsmask_subregion=reg.lsmask[subregion])

                elif self.params.FORM_region in ['countries','ipbes']:

                    if self.params.FORM_region == 'countries':
                        country = self.params.FORM_country
                        countries = 'countries'
                    else:
                        country = self.params.FORM_ipbes
                        countries = 'IPBES'
                    self.regionname = country
                    maskfile = 'country_masks/{country}/mask_{model}_{country}.nc'.format(country=country, model=model)
                    self.maskfile = maskfile

                    if not os.path.exists(maskfile) or os.path.getsize(maskfile) == 0:
                        countrydir = "country_masks/{country}".format(country=country)
                        if not os.path.isdir(countrydir):
                            os.makedirs(countrydir)
                        command = "polygon2mask {filename} {countries}/{country}.txt {maskfile}".format(filename=filename, countries=countries, country=country, maskfile=maskfile)
                        ###self.logOut.info(command)
                        subprocess.call(command, shell=True, stderr=subprocess.STDOUT)
                        if not os.path.exists(maskfile) or os.path.getsize(maskfile) == 0:
                            # most likely there were no grid points in the polygons - skip
                            print "Cannot make mask for {country}, skipping {model}<br>".format(country=country, model=model)
                            print command
                            continue

                    args = "mask {maskfile}".format(maskfile=maskfile)

                elif self.params.FORM_region == 'mask':
                    # TODO: fix this. Ask geert jan
#                    save_uploaded_mask

                    if not os.path.exists(maskfile) or os.path.getsize(maskfile) == 0:
                        raise PlotSeriesError("error: cannot locate uploaded maskfile {maskfile}".format(maskfile=maskfile))
                    self.maskfile = maskfile
                
                    args = "mask {maskfile}".format(maskfile=maskfile)
                else:
                    raise PlotSeriesError("error: unknown value for region: {FORM_region}".format(**paramsDict))

                if not os.path.exists(series) or (os.path.getsize(series) == 0) or (os.path.getmtime(series) < os.path.getmtime(filename)):
                
                    cmd = 'get_index {file} {args} > {series}'.format(file=filename, args=args, series=series)
                    ###self.logOut.info(cmd)
                    if printexp:
                        self.logOut.info('<p>%s<br>' % exp)
                        printexp = False
                    self.logOut.info('Averaging {i}/{n} {infile} over {regionname}<br>'.format(i=str(idxFilename), n=str(len(files) - 1), infile=os.path.splitext(os.path.basename(filename))[0], regionname=self.regionname))

                    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        
                    if not os.path.exists(series) or os.path.getsize(series) == 0:
                        raise PlotSeriesError("Command failed: '%s'" % cmd)
            
                # take anomalies if requested
                ###self.logOut.info('self.params.FORM_anomaly = %s<br>' % self.params.FORM_anomaly)
                if self.params.FORM_anomaly != "on":
                    aseries = series
                else:
                    if self.params.FORM_normsd == "normsd":
                        if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                            rel = "normsd"    
                        else:
                            rel = "normsd mon {FORM_mon} ave {FORM_sum}".format(**paramsDict)
                        relative = "relative"
                    else:
                        rel = ""
                        relative = ""
                
                    aseries = self.get_aseries_name(anomdir, series, paramsDict)

                    if not os.path.exists(aseries) or os.path.getsize(aseries) == 0 or (os.path.getmtime(aseries) < os.path.getmtime(series)):
                        if int(self.params.FORM_anom1) < int(self.params.yr1):
                            raise PlotSeriesError("beginning of anomaly range {FORM_anom1} is before beginning of data {yr1}".format(**paramsDict))
                        # ensanom here means "compute anomalies relative to the ensemble mean"
                        # normsd here means "take relative anomalies"
                
                        cmd = "plotdat anom {FORM_anom1} {FORM_anom2} ensanom {rel} {series} | fgrep -v repeat > {aseries}".format(rel=rel, series=series, aseries=aseries, **paramsDict)
                        if printexp:
                            self.logOut.info('<p>%s<br>' % exp)
                            printexp = False
                        ###self.logOut.info('Taking {relative} anomalies {i}/{n} {series} w.r.t. {anom1}-{anom2}<br>'.format(relative=relative, series=os.path.splitext(os.path.basename(series))[0], i=str(idxFilename), n=str(len(files) - 1), anom1=self.params.FORM_anom1, anom2=self.params.FORM_anom2))
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
                        c = subprocess.check_output('cat {aseries} | wc -l'.format(aseries=aseries), shell=True, stderr=subprocess.STDOUT)
                        c = int(c)

                        if c < 100:
                            rsp = subprocess.check_output('cat {aseries}'.format(aseries=aseries), shell=True, stderr=subprocess.STDOUT)
                            self.logOut.info(rsp)

                            os.remove(aseries)
                            raise PlotSeriesError("something went wrong in making {aseries}".format(aseries=aseries))

                # make plot files summing over the correct season
                for ext in self.params.dumptypes:
                    if ext == 0:
                        times = 'end {endhistory}'.format(endhistory=self.params.endhistory)
                        dumpdir = dump0dir
                    elif ext == 1:
                        times = 'begin {endhistory2}'.format(endhistory2=self.params.endhistory+1)
                        dumpdir = dump1dir
                    else:
                        raise PlotSeriesError("error: unknown ext {ext}".format(ext=ext))
               

                    dumpfile = self.get_dumpfile_name(dumpdir, aseries, ext, paramsDict)
                

                    # always plot standard units
                    # TODO: fix this
                    standardunits = 'standardunits'
                
                    if not os.path.exists(dumpfile) or (os.path.getsize(dumpfile) == 0) or (os.path.getmtime(dumpfile) < os.path.getmtime(aseries)):
                        if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                            season = ""
                        else:
                            season = "mon %(FORM_mon)s ave %(FORM_sum)s" % paramsDict
                        cmd = 'correlate {aseries} time {season} {times} {standardunits} dump {dumpfile}'.format(aseries=aseries, season=season, times=times, standardunits=standardunits, dumpfile=dumpfile, **paramsDict)

                        if ext == 0:
                            if printexp:
                                self.logOut.info('%s<p>' % exp)
                                printexp = False
                            if self.params.FORM_dataset in ['CMIP5ext','CMIP5extone']:
                                self.logOut.info('Converting {i}/{n} {aseries}<br>'.format(i=str(idxFilename), n=str(len(files) - 1), aseries=os.path.splitext(os.path.basename(series))[0], times=times, **paramsDict))
                            else:
                                self.logOut.info('Averaging {i}/{n} {aseries} over season starting month {FORM_mon}, length {FORM_sum}<br>'.format(i=str(idxFilename), n=str(len(files) - 1), aseries=os.path.splitext(os.path.basename(series))[0], times=times, **paramsDict))
                    
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                        # Get number of lines in file 'dumpfile'
                        nLines = subprocess.check_output('cat {dumpfile} | wc -l'.format(dumpfile=dumpfile), shell=True, stderr=subprocess.STDOUT)
                        nLines = int(nLines)

                        # TODO: check if c is 'int'
                        if nLines < 30:
                            rsp = subprocess.check_output('cat {dumpfile}'.format(dumpfile=dumpfile), shell=True, stderr=subprocess.STDOUT)
                            self.logOut.info(rsp)

                            os.remove(dumpfile)
                            raise PlotSeriesError("something went wrong in making {dumpfile}. nLines={nLines}".format(dumpfile=dumpfile, nLines=nLines))
                        # nlines
                    # make dumpfile if not exists
                # loop over dump0, dump1
            # endfor files
        # endfor exps
           
    def doPlot(self):
        """
        inputs:
            transparency (bool)
            exps (list)
            rangeVal (int) ??
            season (str)
            mon (int)
            ave (int)
        """

        paramsDict = self.params.__dict__
        timeSeries = {}
        if self.params.FORM_transparency == 'off':
            transparency = False
        else:
            transparency = True

        rangeVal = 50
        startMonth = int(self.params.FORM_mon)
        lenAverage = int(self.params.FORM_sum)
        season = 'mon%02i_ave%02i' % (startMonth, lenAverage)

        if self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
            # params.FORM_rcp26, _rcp45, _rcp60, _rcp85
            lstExps = [(self.params.FORM_rcp26, 'rcp26'), (self.params.FORM_rcp45, 'rcp45'),
                   (self.params.FORM_rcp60, 'rcp60'), (self.params.FORM_rcp85, 'rcp85')]
        elif self.params.FORM_dataset.split('-')[0] in ['CORDEX']:
            # params.FORM_rcp26, _rcp45, _rcp85
            lstExps = [(self.params.FORM_rcp26, 'rcp26'), (self.params.FORM_rcp45, 'rcp45'),
                   (self.params.FORM_rcp85, 'rcp85')]
        elif self.params.FORM_dataset == 'CMIP3':
            lstExps = [('on', 'sresa1b')]
        elif self.params.FORM_dataset in ['ERAi', 'ERA20C', '20CR']:
            lstExps = [('on', 'reanalysis')]
        elif self.params.FORM_dataset == 'obs':
            lstExps = [('on', 'observations')]
        else:
            lstExps = [('on', 're-analaysis boundaries')]

        # Create a list of experiments
        exps = [el[1] for el in lstExps if el[0]]
        ###print 'exps = {exps}<br>'.format(exps=exps)

        if transparency:
            suffix = '_transparency'
        else:
            suffix = ''

        mkpngfile = True

        # TODO: create a temporary file
        # TSU-proposed colours for SOD (here so that the file does not get lost)
        adjustColoursFilename = os.path.join(self.tempDir, 'adjust_colours.sed')
        adjustColoursFilename = '/tmp/adjust_colours.sed'

        with open(adjustColoursFilename, 'w') as f:
            fileContent = """s@/LC0 {1 0 0} def@/LC0 {0 0 1} def@
s@/LC1 {0 1 0} def@/LC1 {0.4745 0.7373 1} def@
s@/LC2 {0 0 1} def@/LC2 {1 0.5098 0.1765} def@
s@/LC3 {1 0 1} def@/LC3 {1 0 0} def@\n"""
            f.write(fileContent)

            if transparency:
                fileContent = """s/0.250 UL/0.250 UL 0.35 .setopacityalpha/
s/5.000 UL/5.000 UL 1 .setopacityalpha/"""
                f.write(fileContent)

        lo, hi = define_range(rangeVal)


        region, subregion = lookup_region(self.params)

        defRegion = DefineRegion(region)
        subregions = defRegion.subregions
        var = self.params.FORM_var

        defVar = DefineVar(var, self.params.FORM_normsd)


        mon = int(self.params.FORM_mon)
        ave = int(self.params.FORM_sum)
        if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
            sname = ''
        else:
            sname = ' ' + month2string(mon) + '-' + month2string(((mon+ave-2)%12)+1)
        s3 = adjust_winter(mon, ave)

        if self.params.FORM_anomaly == 'on':
            anom1 = self.params.FORM_anom1
            anom2 = self.params.FORM_anom2
            yr2s = self.params.FORM_end
            yr1s = str(int(yr2s) - (int(anom2)-int(anom1)))
        else:
            anom1 = '0'
            anom2 = '0'
            yr2s = self.params.FORM_end
            yr1s = str(int(yr2s)-19) # IPCC standard...

        if self.params.FORM_normsd:
            rel = "rel"
            relative = "Relative "
        else:
            rel = ""
            relative = ""
        if self.params.FORM_dataset in ['CMIP5one', 'CMIP5extone']:
            allone = 'one'
        else:
            allone = 'all'

        scenarios = '_'.join(exps)
        folder = 'atlas/series/{FORM_dataset}'.format(scenarios=scenarios, **paramsDict)
        epsfolder = '{folder}/eps{suffix}/{region_extension}'.format(folder=folder, suffix=suffix, region_extension=self.region_extension)
        if not os.path.isdir(epsfolder):
            os.makedirs(epsfolder)
        quantfolder = '{folder}/quantiles/{region_extension}'.format(folder=folder, region_extension=self.region_extension)
        if not os.path.isdir(quantfolder):
            os.makedirs(quantfolder)
        plotfolder = '{folder}/plotfiles/{region_extension}'.format(folder=folder, region_extension=self.region_extension)
        FORM_field = ""
        if not os.path.isdir(plotfolder):
            os.makedirs(plotfolder)
        if self.params.FORM_dataset.split('-')[0] in ['CMIP5','CMIP5one','CMIP5ext','CMIP5extone','CMIP3', 'CORDEX']:
            lastbit = self.params.FORM_dataset + '_' + scenarios
        elif self.params.FORM_dataset in ['ERAi','ERA20C','20CR']:
            lastbit = self.params.FORM_dataset
        elif self.params.FORM_dataset == 'obs':
            if var in [el[0] for el in obs_var_values]: # make sure it is trusted input
                variable = 'self.params.FORM_obs_{var}'.format(var=var)
                FORM_field = eval(variable)
            else:
                print 'process: unknown value for var %s<br>' % var
            lastbit = self.params.FORM_dataset + '_' + FORM_field
        else:
            raise PlotSeriesError("error: unknown dataset5 %s<br>") % self.params.FORM_dataset
        epsfile = '{epsfolder}/time_{var}{rel}_{region_extension}_mon{FORM_mon}_ave{FORM_sum}_ref{anom1}-{anom2}_{FORM_begin}-{FORM_end}_{lastbit}.eps'.format(epsfolder=epsfolder, 
var=var, rel=rel, region_extension=self.region_extension, anom1=anom1, anom2=anom2, lastbit=lastbit, **paramsDict)
        quantfile = '{quantfolder}/quant_{var}{rel}_{region_extension}_mon{FORM_mon}_ave{FORM_sum}_all_ref{anom1}-{anom2}_{yr1s}-{yr2s}_{lastbit}.txt'.format(quantfolder=quantfolder, var=var, rel=rel, region_extension=self.region_extension, anom1=anom1, anom2=anom2, yr1s=yr1s, yr2s=yr2s, lastbit=lastbit, **paramsDict)
        plotfile = '{plotfolder}/plot_time_{var}{rel}_{region_extension}_mon{FORM_mon}_ave{FORM_sum}_ref{anom1}-{anom2}_{FORM_begin}-{FORM_end}_{lastbit}.gnuplot'.format(plotfolder=plotfolder, 
var=var, rel=rel, region_extension=self.region_extension, anom1=anom1, anom2=anom2, lastbit=lastbit, **paramsDict)

        if self.params.FORM_anomaly == 'on':
            change = "change "
        else:
            change = ""

        plottitle = "{relative}{Varname} {change}{regionname}{sname}".format(relative=relative, Varname=defVar.Varname, regionname=self.regionname, change=change, sname=sname)
        plottitle = plottitle.replace('_',' ') # also avoids subscripts in gnuplot 5
        if anom1 != '0':
            plottitle += ' wrt {anom1}-{anom2}'.format(anom1=anom1, anom2=anom2)
        datasetname = define_dataset(self.params.FORM_dataset,FORM_field)
        plottitle += " {datasetname}".format(datasetname=datasetname)
        dt = self.params.FORM_end - self.params.FORM_begin
        if dt > 100:
            xtics = 50
        elif dt > 60:
            xtics = 20
        elif dt > 20:
            xtics = 10
        else:
            xtics = 5
        # log to Climate Explorer log file
        with open('log/log', 'a') as f:
            f.write('{datetime} {EMAIL} ({REMOTE_ADDR}) plot_atlas_series {title} {FORM_begin}:{FORM_end}\n'.format(datetime=strftime("%a %b %d %H:%M:%S %Z %Y", gmtime()), title=plottitle, **paramsDict))
        if not os.path.exists(epsfile) or os.path.getsize(epsfile) == 0:
            # update when gnuplot is upgraded to gnuplot 5 on linux...
            if sys.platform == 'darwin':
                gnuplot_init = 'set colors classic'
            else:
                gnuplot_init = ''
            plotFileStr = """#!/usr/bin/env gnuplot
# {region_extension} {var} {sname} ref{anom1}-{anom2} {scenarios}
{gnuplot_init}
set size 0.75,0.6
set term postscript epsf color solid "Helvetica" 13
set out "{epsfile}"
set title "{plottitle}"
set multiplot
set origin 0,0
set size 0.6,0.6
set xrange [{FORM_begin}:{FORM_end}]
set yrange [] writeback
set key left Right
set xtics {xtics}
set ytics nomirror
set y2tics out
set xzeroaxis lw 4
set ylabel "{units}"
###set style fill solid
plot \\\n""".format(range=rangeVal, region_extension=self.region_extension, var=var, sname=sname, scenarios=scenarios, anom1=anom1, anom2=anom2, gnuplot_init=gnuplot_init, plottitle=plottitle,
     epsfile=epsfile, Varname=defVar.Varname,
     units=defVar.units, xtics=xtics, **paramsDict)

            with open(plotfile, 'w') as f:
                f.write(plotFileStr)

    		# all RCPs plume
            if not exps:
                raise PlotSeriesError("No experiments selected")

            save_plotvar = self.params.FORM_plotvar
            for exp in exps:
                self.params.FORM_plotvar = 'something but not mean'
                expname, iexp, lt, lw = define_exp(exp)
                (self.typeVar, dir, files) = get_file_list(exp, self.params)
                idx = 1
                nIndex = len(files)
                ###print files
                self.params.FORM_plotvar = save_plotvar

                idx = 0
                for file in files:
                    model, LSMASK = get_model(self.params, file, self.typeVar)

                    idx += 1

                    if self.params.FORM_dataset in ['CMIP5','CMIP5one','CMIP5ext','CMIP5extone']:
                        # one ensemble member per model - choose the same ones as in CMIP5one
                        rip, r, i, p = get_rip(self.params, file)
                        ###print "model = {model}, rip = {rip}<br>".format(model=model,rip=rip)
                        if model == 'EC-EARTH':
                            if r != 8:
                                continue
                        elif model == 'HadGEM2-ES':
                            if r != 2:
                                continue
                        else:
                            if r != 1:
                                continue

                    basename = os.path.splitext(os.path.basename(file))[0]
                    (monthlydir, anomdir, dump0dir, dump1dir) = self.set_dirs(dir, paramsDict)
                    ###print 'basename = %s<br>' % basename
                    series = self.get_series_name(monthlydir, basename, self.region_extension)
                    ###print 'series = %s<br>' % series
                    if self.params.FORM_anomaly == 'on':
                        aseries = self.get_aseries_name(anomdir, series, paramsDict)
                    else:
                        aseries = series
                    ###print 'aseries = %s<br>' % aseries
                    dumpfile0, dumpfile1 = self.get_dumpfile_names(aseries, dir, self.params.dumptypes, paramsDict)
                    ###self.logOut.info('dumpfile0 = {dumpfile0}<br>'.format(dumpfile0=dumpfile0))
                    with open(plotfile, 'a') as f:
                        f.write("\"{dumpfile0}\" u {s3}:{s2} notitle with lines lt 9 lw 0.25,\\\n".format(dumpfile0=dumpfile0, s3=s3, s2=defVar.s2))
                        if dumpfile1 != "":
                            f.write("\"{dumpfile1}\" u {s3}:{s2} notitle with lines lt {lt} lw 0.25,\\\n".format(dumpfile1=dumpfile1, s3=s3, s2=defVar.s2, lt=lt))
                # endfor file
            # endfor exp

            # all model means
            for idxExp, exp in enumerate(exps):
                expname, iexp, lt, lw = define_exp(exp)
                if self.params.FORM_dataset in ['ERAi', 'ERA20C', '20CR', 'obs']:
                    dir = '{FORM_dataset}'.format(**paramsDict)
                else:
                    dir = '{FORM_dataset}/{exp}'.format(exp=exp, **paramsDict)
                (monthlydir, anomdir, dump0dir, dump1dir) = self.set_dirs(dir, paramsDict)
                if self.params.FORM_dataset in ['CMIP5one', 'CMIP5','CMIP5extone', 'CMIP5ext']:
                    if allone == 'one':
                        modone = 'one'
                    else:
                        modone = 'mod'
                    series = '{monthlydir}/time_{var}_{typeVar}_{modone}mean_{exp}_000_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, typeVar=self.typeVar, modone=modone, exp=exp, region_extension=self.region_extension)
                elif self.params.FORM_dataset.split('-')[0] == 'CORDEX':
                    domain = self.params.FORM_dataset.split('-')[1]
                    domain = domain[:-2] + '-' + domain[-2:]
                    series = '{monthlydir}/time_{var}_{domain}_cordex_{exp}_mon_ave_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, domain=domain, exp=exp, region_extension=self.region_extension)
                elif self.params.FORM_dataset == 'CMIP3':
                    series = '{monthlydir}/time_{var}_cmip3_ave_mean_144_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, region_extension=self.region_extension)
                elif self.params.FORM_dataset == 'ERAi':
                    series = '{monthlydir}/time_erai_{var}_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, region_extension=self.region_extension)
                elif self.params.FORM_dataset == 'ERA20C':
                    series = '{monthlydir}/time_era20c_{var}_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, region_extension=self.region_extension)
                elif self.params.FORM_dataset == '20CR':
                    series = '{monthlydir}/time_c{var}_{region_extension}.dat'.format(monthlydir=monthlydir, var=var, region_extension=self.region_extension)                
                elif self.params.FORM_dataset == 'obs':
                    series = '{monthlydir}/time_{field}_{region_extension}.dat'.format(monthlydir=monthlydir, field=model, region_extension=self.region_extension)                
                else:
                    raise PlotSeriesError("Unknown dataset1 %s" % self.params.FORM_dataset)
                    
                if not os.path.exists(series):
                    raise PlotSeriesError('Cannot find series {series}.'.format(series=series))
                else:
                    if self.params.FORM_anomaly == 'on':
                        aseries = self.get_aseries_name(anomdir, series, paramsDict)
                    else:
                        aseries = series
                    dumpfile0, dumpfile1 = self.get_dumpfile_names(aseries, dir, self.params.dumptypes, paramsDict)
                    ###print 'dumpfile0 = %s<br>' % dumpfile0
                    title = expname

                    if dumpfile1 != "":
                        # black line underneath to offset the model mean from the thin lines for all ensemble members. 0=grey, 9=grey, -1=black
                        with open(plotfile, 'a') as f:
                            if not transparency:
                                f.write("\"{dumpfile1}\" u {s3}:{s2} notitle with lines lt 9 lw {lw2},\\\n".format(dumpfile1=dumpfile1, s3=s3, s2=defVar.s2, lw2=lw+4))
                            f.write( "\"{dumpfile1}\" u {s3}:{s2} title \"{title}\" with lines lt {lt} lw {lw},\\\n".format(dumpfile1=dumpfile1, s3=s3, s2=defVar.s2, lt=lt, lw=lw, title=title))

            # and the same for historical - take RCP4.5 as this has the largest number of runs
            if self.params.FORM_dataset.split('-')[0] in ['CMIP5', 'CMIP5one','CMIP5ext', 'CMIP5extone','CORDEX']:
                exp = 'rcp45'
                title = 'historical'
            elif self.params.FORM_dataset == 'CMIP3':
                exp = 'sresa1b'
                title = '20c3m'
            else:
                title = exp

            with open(plotfile, 'a') as f:
                f.write("\"{dumpfile0}\" u {s3}:{s2} title \"{title}\" with lines lt 7 lw {lw}\n".format(dumpfile0=dumpfile0, s3=s3, s2=defVar.s2, title=title, lw=lw))

            if self.ensemble:
                # box and whisker plots
                plotfileStr = """set origin 0.55,0
set size 0.2,0.6
set title " "
set xrange [20:90]
set yrange restore
set xtics ("{yr1s}-{yr2s} mean" 57.5)
set xtics scale 0
unset ytics
unset y2tics
unset border
unset ylabel
set boxwidth 6
plot \\\n""".format(yr1s=yr1s, yr2s=yr2s)

                with open(plotfile, 'a') as f:
                    f.write(plotfileStr)

                findFilesFilter = ""
                ###for exp in exps:
                exp = exps[0]
                self.params.FORM_scenario_cmip5 = exp
                expname, iexp, lt, lw = define_exp(exp)

                if self.params.FORM_dataset in ['CMIP5one', 'CMIP5', 'CMIP5extone', 'CMIP5ext']:
                    findFilesFilter += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_{typeVar}_{modone}mean_{exp}_000_{region_extension}.dat'.format(dataset=self.params.FORM_dataset, exp=exp, region_extension=self.region_extension, var=var, typeVar=self.typeVar, modone=modone)
                elif self.params.FORM_dataset.split('-')[0] == 'CORDEX':
                    domain = self.params.FORM_dataset.split('-')[1]
                    domain = domain[:-2] + '-' + domain[-2:]
                    findFilesFilter += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_{domain}_cordex_{exp}_mon_ave_{region_extension}.dat'.format(dataset=self.params.FORM_dataset, domain=domain, exp=exp, region_extension=self.region_extension, var=var)
                elif self.params.FORM_dataset == 'CMIP3':
                    findFilesFilter += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_cmip3_ave_mean_144_{region_extension}.dat'.format(dataset=self.params.FORM_dataset, exp=exp, region_extension=self.region_extension, var=var)
                else:
                    raise PlotSeriesError("Unknown dataset %s" % self.params.FORM_dataset)

                findFiles = glob.glob(findFilesFilter)
                if findFiles:
                    firstfile = findFiles[0]
                else:
                    raise PlotSeriesError('Cannot find files {findFilesFilter}.'.format(findFilesFilter=findFilesFilter))

                if firstfile and (not os.path.exists(quantfile) or (os.path.getsize(quantfile) == 0) or (os.path.getmtime(quantfile) < os.path.getmtime(firstfile))):
                    inpattern = "\'"
                    for exp in exps:
                        if exp == 'sresa1b':
                            inpattern += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_{typeVar}_*_{region_extension}.dat '.format(dataset=self.params.FORM_dataset, exp=exp, var=var, typeVar=self.typeVar, region_extension=self.region_extension)
                        elif  self.params.FORM_dataset.split('-')[0] == 'CORDEX':
                            inpattern += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_{domain}_*_{exp}_*_{region_extension}.dat '.format(dataset=self.params.FORM_dataset, exp=exp, var=var, domain=domain, region_extension=self.region_extension)
                        else:
                            inpattern += 'atlas/series/{dataset}/{exp}/monthly/{region_extension}/time_{var}_{typeVar}_*_{exp}_*_{region_extension}.dat '.format(dataset=self.params.FORM_dataset, exp=exp, var=var, typeVar=self.typeVar, region_extension=self.region_extension)

                    inpattern += "\'"
                    if self.params.FORM_normsd == "normsd":
                        rel = "rel"
                    else:
                        rel = ""
                    if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                        season = "mon 1 ave 1"
                    else:
                        season = "mon %(FORM_mon)s ave %(FORM_sum)s" % paramsDict
                    cmd = "quantiles_series {var}{rel} '{region_extension}' {allone} {season} {anom1} {anom2} {yr1s} {yr2s} {rcplist} {inpattern} {quantfile} 2> /dev/null".format(var=var, season=season, rel=rel, region_extension=self.region_extension, allone=allone, mon=mon, ave=ave, anom1=anom1, anom2=anom2, yr1s=yr1s, yr2s=yr2s, rcplist=scenarios, inpattern=inpattern, quantfile=quantfile)
                    ###self.logOut.info("cmd = '%s<br>" % cmd)
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                    self.logOut.info(output)

                with open(plotfile, 'a') as f:
                    for exp in exps:
                        if exp == 'sresa1b':
                            exp_without_rcp = '50'
                        else:
                            exp_without_rcp = exp.strip('rcp')
                        expname, iexp, lt, lw = define_exp(exp)
                        f.write("\"{quantfile}\" index {iexp} using ({exp_without_rcp}):{s8}:{s5}:{s15}:{s12} notitle with candlesticks whiskerbars lt {lt} lw {lw},\\\n".format(quantfile=quantfile, iexp=iexp, s8=defVar.s8, s5=defVar.s5, s15=defVar.s15, s12=defVar.s12, lt=lt, lw=lw, exp_without_rcp=exp_without_rcp))
                        # last exp in list?
                        if scenarios.find(exp+'_') >= 0:
                            f.write("\"{quantfile}\" index {iexp} using ({exp_without_rcp}):{s10}:{s10}:{s10}:{s10} notitle with candlesticks whiskerbars 2 lt {lt} lw {lw},\\\n".format(quantfile=quantfile, iexp=iexp, s10=defVar.s10, lt=lt, lw=lw, exp_without_rcp=exp_without_rcp))
                        else:
                            f.write("\"{quantfile}\" index {iexp} using ({exp_without_rcp}):{s10}:{s10}:{s10}:{s10} notitle with candlesticks whiskerbars 2 lt {lt} lw {lw}\n".format(quantfile=quantfile, iexp=iexp, s10=defVar.s10, lt=lt, lw=lw, exp_without_rcp=exp_without_rcp))

            with open(plotfile, 'a') as f:
                f.write('unset multiplot\n')

            # and plot it all

            if self.params.FORM_var in ['r95p','r99p','rx1day','rx5day','r10mm','r20mm','sdii']:
                if self.ensemble or self.params.FORM_dataset == '20CR':
                    self.logOut.info("Please note that tropical cyclones (hurricanes, typhoons) are not well-simulated by these models. In areas where these occur the time series are not reliable.<p>")

            self.logOut.info("Plotting ...<p>")

            cmd = 'gnuplot < {plotfile}'.format(plotfile=plotfile)
            subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

            if os.path.exists(epsfile):
                cmd = 'cat {epsfile} | wc -l'.format(epsfile=epsfile)
                c = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                c = int(c)
            else:
                c = 0

            if c < 500:
                raise ValueError("Something went wrong in plotting {plotfile}, {epsfile} is only {c} lines long".format(plotfile=plotfile, epsfile=epsfile,
                                                                                                                        c=c))
            epsfile_temp = epsfile + '.tmp'

            os.rename(epsfile,epsfile_temp)
            cmd = 'sed -f {adjustColoursFilename} {epsfile_temp} > {epsfile}'.format(adjustColoursFilename=adjustColoursFilename, epsfile=epsfile, epsfile_temp=epsfile_temp)
            ###self.logOut.info('cmd = %s<br>' % cmd)
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            os.remove(epsfile_temp)

            ###self.logOut.info("generating %s.pdf" % epsfile.rstrip('.eps'))
            cmd = 'epstopdf {epsfile}'.format(epsfile=epsfile)
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        # epsfile already exists ?
        pngfile = epsfile.rstrip('.eps') + '.png'

#       if transparency and mkpngfile and (not os.path.exists(pngfile) or os.path.getsize(pngfile) == 0 or os.path.getmtime(pngfile) < os.path.getmtime(epsfile)):
        if mkpngfile and (not os.path.exists(pngfile) or os.path.getsize(pngfile) == 0 or os.path.getmtime(pngfile) < os.path.getmtime(epsfile)):
            ###self.logOut.info("generating {pngfile}".format(pngfile=pngfile))

            cmd = 'gs -q -r900 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -sDEVICE=ppmraw -sOutputFile=- {epsfile} -c quit | pnmcrop | pnmtopng > {pngfile}'.format(epsfile=epsfile, pngfile=pngfile)
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        # End of processing data

        if self.ensemble:
            ensembletext = "On the left, for each scenario one line per model is shown plus the multi-model mean, on the right percentiles of the whole dataset: the box extends from 25% to 75%, the whiskers from 5% to 95% and the horizontal line denotes the median (50%)."
        else:
            ensembletext = ""

        if self.maskfile:
            masktext = ", <a href='{maskdir}'>masks</a>".format(maskdir=os.path.dirname(self.maskfile))
        else:
            masktext = ""
         
        self.logOut.info("""
<div class='bijschrift'>
{plottitle}. {ensembletext}(<a href='{pngImg}'>png</a>, <a href='{epsImg}'>eps</a>, <a href='{pdfImg}'>pdf</a>, <a href='{plotfile}'>plotscript</a>, <a href='plotfile2zip.cgi?plotfile={plotfile}'>all data</a>, <a href='{quantfile}'>means</a>{masktext})
</div>
<p>
<center><img src='{pngImg}' alt='' width="100%" /></center>'
""".format(plottitle=plottitle, ensembletext=ensembletext, pngImg=pngfile, epsImg=epsfile, pdfImg=epsfile.rstrip('.eps')+'.pdf', plotfile=plotfile, quantfile=quantfile,masktext=masktext))


        return timeSeries

