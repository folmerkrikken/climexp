"""PlotAtlasMap class"""

import os
import re
import logging
import sys
import util
import shutil
import subprocess
import tempfile
from time import gmtime, strftime
import settings
from formparameters import get_season_name, obs_var_values
from more_functions_atlas import get_region_extension, \
    get_file_list, lookup_region, define_dataset, getboxfrompolygon
from define_functions_atlas import DefineVar
from defineregion import DefineRegion


class PlotMapError(Exception):
    """Raised when a error occured in PlotAtlasMap."""
    pass


class PlotAtlasMap:

    def __init__(self, params=None, logLevel=logging.INFO, isLogFormatHTML=True):
        """Initialize the object."""

        # Create a logger
        self.log = logging.getLogger('PlotAtlasMap')
        self.log.setLevel(logLevel)

        # Configure the logger to log in the HTML page
#        hdlr = logging.StreamHandler(sys.stdout)
#        hdlr.setFormatter(util.JavascriptFormatter())
#        self.log.addHandler(hdlr)

        if not isLogFormatHTML:
            self.hdlr = logging.StreamHandler(sys.stdout)
            self.hdlr.setFormatter(logging.Formatter('\033[1;31m%(name)s(%(lineno)s):\033[1;0m \033[1;1m%(message)s\033[1;0m'))
            self.log.addHandler(self.hdlr)
        else:
            self.hdlr = logging.StreamHandler(sys.stdout)
            self.hdlr.setFormatter(logging.Formatter('<b>%(name)s(<i>%(lineno)s</i>)</b>: <i>%(message)s</i><br>'))
            self.log.addHandler(self.hdlr)

        self.logOut = logging.getLogger('htmlOutput')
        self.logOut.setLevel(logLevel)
        self.hdlrOut = logging.StreamHandler(sys.stdout)
        self.hdlrOut.setFormatter(logging.Formatter('%(message)s'))
        self.logOut.addHandler(self.hdlrOut)

        self.params = params
        self.typeVar = None
        self.dir = None
        self.files = []
        self.outfiles = []
        self.quantroot = None
        self.quantfile = None
        self.xvar = None
        self.plotfile = None
        self.sdfile = None
        self.uncert = None
        self.normsdmessage = None
        self.ensemble = False

        # Set temporary folder
        self.tempDir = tempfile.mkdtemp()
        self.log.debug('Use temporary folder: %s' % self.tempDir)

        # set flag for ensembles
        if self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone', 'CMIP3']:
            self.ensemble = True

        # Set rel
        if self.params.FORM_normsd:
            self.rel = 'rel'
        else:
            self.rel = ""

        # exception
        varObj = DefineVar(self.params.FORM_var, self.params.FORM_normsd)
        if self.params.FORM_normsd and varObj.norelative == True:
            self.params.FORM_normsd = ""
            self.rel = ""
            self.normsdmessage = True

        # Set the season and season name
        if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
            self.season = ""
            self.sname = ""
        else:
            self.season = 'mon%s_ave%s' % (self.params.FORM_mon, self.params.FORM_sum)
            self.log.debug('season = %s' % self.season)
            self.sname = get_season_name(self.params)
            self.log.debug('get_season_name. sname = %s' % self.sname)

        self.log.debug('__init__')


    def __del__(self):

        self.log.removeHandler(self.hdlr)
        self.log.removeHandler(self.hdlrOut)


    def process(self, lwrite=False):

        paramsDict = self.params.__dict__
        ###self.logOut.info('paramsDict = {paramsDict}'.format(paramsDict=paramsDict))
        self.log.debug('process')

#        self.logOut.info("<font color=#ff2222>plot_atlas_map: UNDER CONSTRUCTION</font>")
        if self.normsdmessage == True:
            self.logOut.info("Ignoring request for relative changes for this variable.<br>")

        # First find files
        save_plotvar = self.params.FORM_plotvar
        save_dataset = self.params.FORM_dataset
        meanfile = ""
        if ( self.params.FORM_measure == 'regr' or self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone'] ) and self.ensemble:
            if self.params.FORM_plotvar == 'mean':
                # make sure we also get the full list, needed for the natural variability
                # note the CMIP3 case does not use the parameter
                (typeVar, dir, meanfile) = get_file_list(self.params.FORM_scenario_cmip5, self.params)
                self.params.FORM_plotvar = 'xmean'
                if self.params.FORM_dataset == 'CMIP5extone':
                    self.params.FORM_dataset = 'CMIP5ext' # to compute the sd of nat. var.
        self.log.debug('get_file_list:')
        (self.typeVar, self.dir, self.files) = get_file_list(self.params.FORM_scenario_cmip5, self.params)
        self.params.FORM_plotvar = save_plotvar
        self.params.FORM_dataset = save_dataset
        if meanfile != "":
            self.files.append(meanfile[0])

        self.log.debug('  self.typeVar = %s', self.typeVar)
        self.log.debug('  self.dir = %s', self.dir)
        self.log.debug('  self.files = %s', self.files)
        self.log.debug('')

        # Next compute difference / regression data
        if self.params.FORM_dataset in ['CMIP5one','CMIP5extone']:
            one = 'one'
        else:
            one = ""

        self.quantroot = 'atlas/diff/{dir}/quant'.format(dir=self.dir)
        self.log.debug('quantroot = %s', self.quantroot)

        if not os.path.exists(self.quantroot):
            self.log.debug('Make dir: %s', self.quantroot)
            os.makedirs(self.quantroot)

        if self.params.FORM_measure == 'diff':
            self.log.debug("## FORM_measure == 'diff'")
            # Compute the difference fields
            self._compute_difference_data(paramsDict, lwrite)

        elif self.params.FORM_measure == 'regr':
            self.log.debug("## FORM_measure == 'regr'")
            # Compute the regression data
            self._compute_regression_data(paramsDict) 

        else:
            raise PlotMapError("unknown measure '%(FORM_measure)s'" % paramsDict)

        # Compute quantiles if needed
        self._set_plotfile_and_compute_quantiles(lwrite)

        # Add sd from pre-industrial runs or from the residuals
        self._add_standard_deviation()

        # Finally plot the map
        (root, title, halfwidth) = self._make_plot(paramsDict, lwrite)

        if self.params.FORM_var in ['r95p','r99p','rx1day','rx5day','r10mm','r20mm','sdii']:
            if self.ensemble or self.params.FORM_dataset == '20CR':
                self.logOut.info("Please note that tropical cyclones (hurricanes, typhoons) are not well-simulated by these models. In areas where these occur the map is not reliable.")
        htmlStr = """
<table width=600 border=0 cellspacing=0 cellpadding=0>
<tr><td>
<div class="bijschrift">{title}. The hatching represents areas where the signal is smaller than one standard deviation of natural variability (<a href="{root}.eps">eps</a>, <a href="{root}.pdf">pdf</a>, <a href="{plotfile}">netcdf</a>)</div>
<center><img src="{root}.png" alt="{title}" width={halfwidth}><br clear=all></center>
</td></tr></table>        
        """.format(root=root, title=title, plotfile=self.plotfile, halfwidth=halfwidth)
        self.logOut.info(htmlStr)

#        self.log.debug('Use temporary folder: %s' % self.tempDir)
        # TODO: delete folder self.tempDir
        return '{root}.png'.format(root=root)


    def _compute_difference_data(self, paramsDict, lwrite):
        """ Compute the difference data. Set the quantfile and xvar """

        # Set number of files
        nfiles = len(self.files)
        ###self.logOut.info('nfiles = %i <br>' % len(self.files))
        varObj = DefineVar(self.params.FORM_var, self.params.FORM_normsd)

        root = 'atlas/diff/{dir}/{season}'.format(dir=self.dir, season=self.season)
        self.log.debug('root = %s', root)

        if not os.path.exists(root):
            self.log.debug('Make dir: %s', root)
            os.makedirs(root)
            
        ifiles = 0
        ###self.logOut.info('self.files = %s<br>' % self.files[:5])
        ###self.logOut.info('len(self.files) = %i<br>' % len(self.files))
        for fileName in self.files:
            self.log.debug('')
            if self.params.FORM_end1 < self.params.FORM_begin1:
                raise PlotMapError("error: end %(FORM_end)s year less then begin year %(FORM_begin)s" % paramsDict)
            if self.params.FORM_end2 < self.params.FORM_begin2:
                raise PlotMapError("error: end %(FORM_end2)s year less then begin year %(FORM_begin2)s" % paramsDict)

            fileName_root = os.path.splitext(os.path.basename(fileName))[0]
            difffile = '{root}/{rel}diff_{basename}_%(FORM_begin2)s-%(FORM_end2)s_minus_%(FORM_begin1)s-%(FORM_end1)s_{season}.nc'.format(root=root, rel=self.rel, fileName=fileName, season=self.season, basename=fileName_root) % paramsDict
            self.outfiles.append(difffile)
            ifiles += 1

            self.log.debug('%i/%i' % (ifiles, nfiles))
            self.log.debug('fileName = %s, .exists = %s' % (fileName, os.path.exists(fileName)))
            self.log.debug('difffile = %s, .exists = %s' % (difffile, os.path.exists(difffile)))

            if not os.path.exists(difffile) or os.path.getsize(difffile) == 0 or (os.path.getmtime(difffile) < os.path.getmtime(fileName)):
                self.logOut.info("Computing difference field {ifiles}/{nfiles} {name} ...<br>".format(ifiles=ifiles, nfiles=nfiles, name=os.path.basename(fileName)))

                # the winter offset :-(
                begin1 = self.params.FORM_begin1 + self.params.offset
                end1 = self.params.FORM_end1 + self.params.offset
                begin2 = self.params.FORM_begin2 + self.params.offset
                end2 = self.params.FORM_end2 + self.params.offset
                if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                    season = ""
                else:
                    season = "mon %(FORM_mon)s ave %(FORM_sum)s" % paramsDict

                # for variables that count the number of days, 
                # do not consider in relative differences denominators < 1
                # and in normal differences points where both fields are < 1
                if self.params.FORM_var in ['fd','id', 'gsl', 'r1mm', 'r10mm', 'r20mm']:
                    mindata = 'dgt 1'
                else:
                    mindata = ''
                    
                cmd = 'difffield {filename} {filename} {season} begin2 {begin1} end2 {end1} begin {begin2} end {end2} %(FORM_normsd)s {mindata} {standardunits} {difffile}'.format(filename=fileName, difffile=difffile, season=season, begin1=begin1, end1=end1, begin2=begin2, end2=end2, standardunits=varObj.standardunits, mindata=mindata) % paramsDict

                if lwrite:
                    self.logOut.info('%s <br>' % cmd)
                   
                self.log.debug("Cmd: '%s'" % cmd)
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                # TODO: check ret and if output file exists
                if not os.path.exists(difffile):
                    raise PlotMapError("Error in command '%s'" % cmd)

                if lwrite:
                    subprocess.check_output('ls -l {difffile}'.format(difffile=difffile), shell=True, stderr=subprocess.STDOUT)

        self.quantfile = '{quantroot}/quant_{rel}diff_%(FORM_var)s_{typeVar}_%(FORM_begin2)s-%(FORM_end2)s_minus_%(FORM_begin1)s-%(FORM_end1)s_{season}.nc'.format(quantroot=self.quantroot, rel=self.rel, typeVar=self.typeVar, season=self.season) % paramsDict
        if self.params.FORM_plotvar != 'mean':
            self.plotfile = self.quantfile
        else:
            self.plotfile = difffile
        
        self.xvar = '{rel}diff'.format(rel=self.rel)


    def _compute_regression_data(self, paramsDict):
        """ Compute the regression data. Set the quantfile and xvar """

        # Set root directory and create it if it does not exist
        root = "atlas/regr/{dir}/{season}".format(dir=self.dir, season=self.season)
        if not os.path.exists(root):
            os.makedirs(root)

        self.quantroot = "{root}/quant".format(root=root)
        if not os.path.exists(self.quantroot):
            os.makedirs(self.quantroot)

        # Select the reference file
        reffile = None
        if self.params.FORM_regr == 'time':
            if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                reffile = 'KNMIData/time1.dat'
            else:
                reffile = "KNMIData/time12.dat"
        elif self.params.FORM_regr == 'co2eq45':
            if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                reffile = "CDIACData/RCP45_CO2EQ.dat"
            else:
                reffile = "CDIACData/RCP45_CO2EQ_mo.dat"                
        elif self.params.FORM_regr == 'co2eq85':
            if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                reffile = "CDIACData/RCP85_CO2EQ.dat"
            else:
                reffile = "CDIACData/RCP85_CO2EQ_mo.dat"
        elif self.params.FORM_regr == 'obstglobal':
            if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                reffile = "NASAData/giss_al_gl_a_4yrlo.dat"
            else:
                reffile = "NASAData/giss_al_gl_m_4yrlo.dat"
        elif self.params.FORM_regr == 'modtglobal':
            raise PlotMapError("Reference 'modtglobal' not yet implemented")
        else:
            raise PlotMapError("Unknown reference '{regr}'".format(regr = self.params.FORM_regr))
      
        # Check if file exists
        if not os.path.exists(reffile):
            raise PlotMapError("Cannot find reference series file {reffile}".format(reffile=reffile))
   
        # Validate the start and end time
        if int(self.params.FORM_end_fit) < int(self.params.FORM_begin_fit):
            raise PlotMapError("end {end_fit} year less then begin year {begin_fit}".format(
        end_fit = self.params.FORM_end_fit, 
        begin_fit = self.params.FORM_begin_fit))

        varObj = DefineVar(self.params.FORM_var, self.params.FORM_normsd)

        nfiles = len(self.files)
        ifiles = 0
        ###self.logOut.info("self.files = {files}<br>".format(files=self.files))
        for filename in self.files:
            # in principle the {rel} is not necessary here, but later on the 
            # error gets the non-unique name "sd". A bit more time wasted for the user.
            regrfile = '{root}/{rel}regr_{basename}_{regr}_{begin_fit}-{end_fit}_{season}.nc'.format(
                rel=self.rel,
                root=root,     
                basename=os.path.splitext(os.path.basename(filename))[0],
                regr=self.params.FORM_regr, 
                begin_fit=self.params.FORM_begin_fit, 
                end_fit=self.params.FORM_end_fit,
                season=self.season)
            self.outfiles.append(regrfile)
            ifiles += 1
            if not os.path.exists(regrfile) or (os.path.getsize(regrfile) == 0) or (os.path.getmtime(regrfile) < os.path.getmtime(filename)):
                self.logOut.info("Computing regression {ifiles}/{nfiles} {filename} ...<br>".format(ifiles=ifiles, nfiles=nfiles, filename=os.path.basename(filename)))
                # TODO: check this. Note that we have introduced new parameters FORM_begin_fit and FORM_end_fit
                # correlatefield $file $reffile mon $FORM_mon ave $FORM_sum begin $FORM_begin end $FORM_end2 $regrfile > /dev/null

                if self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                    season = ""
                else:
                    season = "mon %(FORM_mon)s ave %(FORM_sum)s" % paramsDict
                cmd = 'correlatefield {filename} {reffile} {season} begin {FORM_begin_fit} end {FORM_end_fit} {standardunits} {regrfile} > /dev/null'.format(filename=filename, reffile=reffile, season=season, standardunits=varObj.standardunits, regrfile=regrfile, **paramsDict)

                ###self.logOut.info('cmd = %s<br>' % cmd)
                subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)
                if not self.ensemble:
                    # use dregr/drelregr from fit
                    self.xvar = '{rel}regr'.format(rel=self.rel)
                    cmd = 'ncrename -O -v d{xvar},sd {regrfile}'.format(xvar=self.xvar, regrfile=regrfile)
                    ###self.logOut.info("cmd = '%s'" % cmd)
                    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
        self.quantfile = '{quantroot}/quant_{rel}regr_{basename}_{regr}_{begin_fit}-{end_fit}_{season}.nc'.format(
            quantroot=self.quantroot,
            rel=self.rel, 
            basename=os.path.splitext(os.path.basename(filename))[0],
            regr=self.params.FORM_regr, 
            begin_fit=self.params.FORM_begin_fit, 
            end_fit=self.params.FORM_end_fit,
            season=self.season)
        self.log.debug('quantfile = %s' % self.quantfile)
        if self.params.FORM_plotvar == 'mean':
            self.plotfile = regrfile # the last one of the previous loop
        else:
            self.plotfile = self.quantfile        

        # Set xvar
        self.xvar = '{rel}regr'.format(rel=self.rel)
        self.log.debug('xvar = %s' % self.xvar)


    def _set_plotfile_and_compute_quantiles(self, lwrite):
        """ Set plotfile and compute quantiles """

        # Set number of files
        nfiles = len(self.files)

        ## compute quantiles if needed
        if self.params.FORM_plotvar != 'mean' or self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
            infiles = []
            doit = False

            if not os.path.exists(self.quantfile) or os.path.getsize(self.quantfile) == 0:
                doit = True
            else:
                for outfile in self.outfiles:
                    # TODO: check this
                    if os.path.getmtime(self.quantfile) > os.path.getmtime(outfile):
                        doit = True
        
            if doit or lwrite:      
                # (re)generate quantfile 

                ###self.logOut.info('self.outfiles = %s<br>' % self.outfiles[:5])
                ###self.logOut.info('len(self.outfiles) = %i<br>' % len(self.outfiles))

                for outfile in self.outfiles:
                    self.log.debug('')
                    infile = os.path.join(self.tempDir, '%s_%s' % (self.xvar, os.path.basename(outfile)))
                    self.log.debug('infile = %s, exists = %s' % (infile, os.path.exists(infile)))
                    self.log.debug('outfile = %s, exists = %s' % (outfile, os.path.exists(outfile)))

                    if not os.path.exists(infile) or os.path.getsize(infile) == 0 or (os.path.getmtime(infile) < os.path.getmtime(outfile)):
                        if not os.path.exists(outfile) or os.path.getsize(outfile) == 0:
                            raise PlotMapError("Cannot find {outfile}".format(outfile=outfile))
                        
                        cmd = 'ncks -O -v {xvar} {outfile} {infile}'.format(xvar=self.xvar, outfile=outfile, infile=infile)
                        ###self.log.debug("cmd = '%s'" % cmd)
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                    infiles.append(infile)
                
                infiles.sort()
                self.logOut.info("Generating quantiles of signal ...<br>")

                ###self.logOut.info('infiles = %s<br>' % infiles[:5])
                ###self.logOut.info('len(infiles) = %i<br>' % len(infiles))

                if not infiles:
                    raise PlotMapError("Cannot find data.")

                cmd = "bin/quantiles_field {infiles} {quantfile}".format(infiles=' '.join(infiles), quantfile=self.quantfile)
                ###self.logOut.info("cmd = '%s'" % cmd)
                cmdOutput = subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

                # Remove temporary 'infiles'
                try:
                    for infile in infiles:
                        if os.path.isfile(infile):
                            os.remove(infile)
                except OSError as e:
                    self.log.warning("Cannot remove file %s. %s" % (infile, str(e)))
       
        ###self.logOut.info('plotfile = {plotfile}<br>'.format(plotfile=self.plotfile))


    def _add_standard_deviation(self):
        """ Add sd from pre-industrial runs """

        if self.params.FORM_measure == 'diff' and not self.params.FORM_dataset in ['CMIP5ext','CMIP5extone']:
            period1 = int(self.params.FORM_end1) - int(self.params.FORM_begin1) + 1
            period2 = int(self.params.FORM_end2) - int(self.params.FORM_begin2) + 1
        
            dir = "atlas/diff/CMIP3/sd_{period}".format(period=period1)
            if not os.path.exists(dir):
                self.log.debug('mkdir %s' % dir)
                os.makedirs(dir)

            dir = "atlas/diff/CMIP5/sd_{period}".format(period=period1)
            if not os.path.exists(dir):
                self.log.debug('mkdir %s' % dir)
                os.makedirs(dir)

            dirone = "atlas/diff/CMIP5one/sd_{period}".format(period=period1)
            rdir = "../CMIP5/sd_{period}".format(period=period1)
            if not os.path.islink(dirone):
                self.log.debug('mkdir %s' % dir)
                os.symlink(rdir, dirone)
            
            varObj = DefineVar(self.params.FORM_var, self.params.FORM_normsd)
            # get the s.d. from the CMIP5 piControl run (also for other datasets)
            if period1 == period2:
                self.sdfile = 'atlas/diff/CMIP5/sd_{period}/sd_{var}{rel}_{period}_{season}.nc'.format(dataset=self.params.FORM_dataset, var=varObj.sdvar, period=period1, rel=self.rel, season=self.season)
            else:
                # not elegant, should make function, no time now
                dir = "atlas/diff/CMIP5/sd_{period}".format(period=period2)
                if not os.path.exists(dir):
                    self.log.debug('mkdir %s' % dir)
                    os.makedirs(dir)

                dirone = "atlas/diff/CMIP5one/sd_{period}".format(period=period2)
                rdir = "../CMIP5/sd_{period}".format(period=period2)
                if not os.path.islink(dirone):
                    self.log.debug('mkdir %s' % dir)
                    os.symlink(rdir, dirone)

                dir = "atlas/diff/CMIP5/sd_{period1}_{period2}".format(period1=period1,period2=period2)
                if not os.path.exists(dir):
                    self.log.debug('mkdir %s' % dir)
                    os.makedirs(dir)

                dirone = "atlas/diff/CMIP5one/sd_{period1}_{period2}".format(period1=period1,period2=period2)
                rdir = "../CMIP5/sd_{period1}_{period2}".format(period1=period1,period2=period2)
                if not os.path.islink(dirone):
                    self.log.debug('mkdir %s' % dir)
                    os.symlink(rdir, dirone)

                self.sdfile = 'atlas/diff/CMIP5/sd_{period1}_{period2}/sd_{var}{rel}_{period1}_{period2}_{season}.nc'.format(dataset=self.params.FORM_dataset, var=varObj.sdvar, rel=self.rel, period1=period1, period2=period2, season=self.season)

            self.uncert = 1

            self.logOut.debug("Looking for {file}".format(file=self.sdfile))
            if not os.path.exists(self.sdfile) or os.path.getsize(self.sdfile) == 0:
                # create sd files _ I should write a python function ...
                if self.rel == "rel":
                    rel01 = 1
                else:
                    rel01 = 0
                sd1file = 'atlas/diff/CMIP5/sd_{period}/sd_{var}{rel}_{period}_{season}.nc'.format(dataset=self.params.FORM_dataset, var=varObj.sdvar, period=period1, rel=self.rel, season=self.season)
                if not os.path.exists(sd1file) or os.path.getsize(sd1file) == 0:
                    # generate files for period1
                    self.logOut.info("As you are the first to requests maps of {period}-yr means of the variable {var}, the maps of the standard deviation of natural variability are now being computed. This may take up to half an hour or so, but only once.<p>".format(period=period1,var=varObj.sdvar))

                    if self.params.REMOTE_ADDR != "127.0.0.1":
                        cmd = './makesd.cgi {period} {var} {rel01}'.format(var=varObj.sdvar, rel01=rel01, period=period1)
                        self.log.debug("cmd: '%s'" % cmd)
                        subprocess.call(cmd, shell=True)
                
                if period1 != period2:
                    sd2file = 'atlas/diff/CMIP5/sd_{period}/sd_{var}{rel}_{period}_{season}.nc'.format(dataset=self.params.FORM_dataset, var=varObj.sdvar, period=period2, rel=self.rel, season=self.season)
                    if not os.path.exists(sd2file) or os.path.getsize(sd2file) == 0:
                        # generate files for period1
                        cmd = './makesd.cgi {period} {var} {rel01}'.format(var=varObj.sdvar, rel01=rel01, period=period2)
                        self.log.debug("cmd: '%s'" % cmd)
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                    # and combine the two...
                    cmd = './combinesd.cgi {sd1file} {sd2file} {sdfile}'.format(sd1file=sd1file, sd2file=sd2file, sdfile=self.sdfile)
                    self.log.debug("cmd: '%s'" % cmd)
                    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            mergeit = True

        elif self.params.FORM_measure == 'regr':
        
            if not self.ensemble:
                mergeit = False
            else:
                # get the s.d. from the fits (taking serial correlations into account)
                infiles = []
                for outfile in self.outfiles:
                    if outfile.find('mean_') == -1:
                        infile = os.path.join(self.tempDir, '%s_%s' % ('d'+self.xvar, os.path.basename(outfile)))
                        if not os.path.exists(outfile) or os.path.getsize(outfile) == 0:
                            raise PlotMapError("Cannot find {outfile}".format(outfile=outfile))
                    
                        cmd = 'ncks -O -v d{xvar} {outfile} {infile}'.format(xvar=self.xvar, outfile=outfile, infile=infile)
                        ###self.logOut.info("cmd = '%s'" % cmd)
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                        infiles.append(infile)
            
                self.logOut.info("Generating median of variability...<br>")

                if not infiles:
                    raise PlotMapError("Cannot find data.")

                noisefile = os.path.join(self.tempDir, '%s%s_%s' % ('quant_d',self.xvar, os.path.basename(outfile)))
                cmd = "bin/quantiles_field {infiles} {noisefile}".format(infiles=' '.join(infiles), noisefile=noisefile)
                ###self.log.debug("cmd = '%s'" % cmd)
                cmdOutput = subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

                # Remove temporary 'infiles'
                try:
                    for infile in infiles:
                        if os.path.isfile(infile):
                            os.remove(infile)
                except OSError as e:
                    self.log.warning("Cannot remove file %s. %s" % (infile, str(e)))
        
                # take median to represent to s.d.
                self.sdfile = os.path.join(self.tempDir, '%s%s_%s' % ('sd_',self.xvar, os.path.basename(outfile)))
                cmd = "ncks -v p50 {noisefile} {sdfile}".format(noisefile=noisefile, sdfile=self.sdfile)
                ###self.log.debug("cmd = '%s'" % cmd)
                cmdOutput = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                cmd = "ncrename -v p50,sd {sdfile}".format(noisefile=noisefile, sdfile=self.sdfile)
                self.log.debug("cmd = '%s'" % cmd)
                cmdOutput = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                mergeit = True

        elif self.params.FORM_dataset == 'CMIP5ext':

            if self.params.FORM_plotvar == 'mean':
                # the sd has been computed in quantfile
                mergeit = True
                self.logOut.info("Using intramodel variability to estimate natural variability for the hatching.<br>")
                self.sdfile = os.path.join(self.tempDir, 'sd_var.nc')
                cmd = "ncks -v sd {quantfile} {sdfile}".format(quantfile=self.quantfile, sdfile=self.sdfile)
                ###self.logOut.info(cmd)
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                # the sd has been computed from the intramodel variability by quantiles_field
                self.logOut.info("Using intramodel variability to estimate natural variability for the hatching.<br>")
                mergeit = False

        elif self.params.FORM_dataset == 'CMIP5extone':

            if self.params.FORM_plotvar == 'mean':
                # the sd has been computed in quantfile
                mergeit = True
                self.logOut.info("Using intramodel variability to estimate natural variability for the hatching.<br>")
                self.sdfile = os.path.join(self.tempDir, 'sd_var.nc')
                cmd = "ncks -v sd {quantfile} {sdfile}".format(quantfile=self.quantfile, sdfile=self.sdfile)
                ###self.logOut.info(cmd)
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                # check whether the full ensemble has been run for these parameters
                fullquantfile = self.quantfile.replace('CMIP5extone','CMIP5ext')
                if os.path.exists(fullquantfile):
                    mergeit = True
                    self.logOut.info("Using intramodel variability to estimate natural variability for the hatching.<br>")
                    self.sdfile = os.path.join(self.tempDir, 'sd_var.nc')
                    cmd = "ncks -v sd {fullquantfile} {sdfile}".format(fullquantfile=fullquantfile, sdfile=self.sdfile)
                    ###self.logOut.info(cmd)
                    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                else:
                    mergeit = False
                    self.uncert = 0
                    self.logOut.info("Hatching of regions where the change is small compared to natural variability is only possible when the full ensemble has been run for a percentile.<br>")
                    self.sdfile = 'atlas/diff/CMIP5/sd_20/null.nc'.format(dataset=self.params.FORM_dataset)

        else:
            raise PlotMapError("Unknown measure {measure}".format(measure=self.params.FORM_measure))

        if mergeit:
            if not os.path.exists(self.sdfile) or os.path.getsize(self.sdfile) == 0:
                # no hatching for the time being, this will have to be replaced by a call
                # to a script that generates the sdfile
                # for unequal periods this can usually be done by sqrt(sd1^2+sd2^2)
                # but then of course sd1 and sd2 have to exist...
                self.uncert = 0
                self.logOut.info("Hatching of regions where the change is small compared to natural variability is not yet ready for these choices.<br>")
                # add call to script here.... if successfull, set uncert to 1.
                self.sdfile = 'atlas/diff/CMIP5/sd_20/null.nc'.format(dataset=self.params.FORM_dataset)
            else:
                if self.params.FORM_measure == 'diff' and not self.params.FORM_dataset in ['CMIP5ext', 'CMIP5extone']:
                    self.logOut.info("Using natural variability in the CMIP5 pre-industrial control runs for the hatching.<br>")
        
            newplotfile = self.plotfile[:-3] + "_withsd.nc"
            if not os.path.exists(newplotfile) or (os.path.getmtime(newplotfile) < os.path.getmtime(self.plotfile)):
                tempfile = os.path.join(self.tempDir, os.path.basename(self.sdfile))
                if not self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone', 'CMIP3']:
                    # interpolate to the grid of the data
                    cmd = "cdo remapbil,{plotfile} {sdfile} {tempfile}".format(sdfile=self.sdfile, plotfile=self.plotfile, tempfile=tempfile)
                    ###self.logOut.info("cmd: '%s'" % cmd)
                    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                    self.sdfile = tempfile
                
                if os.path.exists(newplotfile): # cdo does not overwrite...
                    os.remove(newplotfile)
                # and merge in the information from the pre-industrial control run
                cmd = 'cdo -r merge {sdfile} {plotfile} {newplotfile}'.format(sdfile=self.sdfile, plotfile=self.plotfile, newplotfile=newplotfile)
                self.log.debug("cmd: '%s'" % cmd)
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

                if os.path.getsize(newplotfile) == 0:
                    raise PlotMapError("Something went wrong in %s" % cmd)

            self.plotfile = newplotfile

    def _make_plot(self, paramsDict, lwrite):
        """ Plot map """

        lonoverlap = 10
        latoverlap = 5
        if self.params.FORM_region == 'srex':
            if lwrite:
                self.logOut.info("calling lookup_region with FORM_srex=%(FORM_srex)s<br>" % paramsDict)
            
            region, subregion = lookup_region(self.params)
            reg = DefineRegion(region)
            ###print "reg.npoly[subregion] = %s<br>" % reg.npoly[subregion]
            # check
            if self.params.FORM_srex not in (reg.abbr[subregion], reg.shortname[subregion]):
                errMsg = "error: inconsistency in lookup_region: %(FORM_srex)s gives {region} {subregion}".format(region=region, subregion=subregion) % paramsDict 
                errMsg += "but abbr = %s and shortname = %s" % (reg.abbr[subregion], reg.shortname[subregion])
                raise PlotMapError(errMsg)
            
            # make the map larger than the area over which the time series are defined
            if not reg.lon1[subregion]:
                # TODO: test this part
                # polygon region
                polyRegionFile = os.path.join(settings.WORKING_DIR, 'SREX/%(FORM_srex)s.txt' % paramsDict)
                self.log.debug('polyRegionFile = %s', polyRegionFile)

                if not os.path.exists(polyRegionFile) or os.path.getsize(polyRegionFile) == 0:
                    errMsg = "internal error: cannot find file %s " % polyRegionFile
                    errMsg += "region={region}, subregion={subregion}, lon1[{subregion}]={lon1_subregion}".format(region=region, subregion=subregion, lon1_subregion=reg.lon1[subregion])
                    raise PlotMapError(errMsg)
                
                xmin, xmax, ymin, ymax = getboxfrompolygon(polyRegionFile)

                # we assume the region have been encoded sensibly with no wrapping longitudes
                reg.lon1[subregion] = float(xmin)
                reg.lon2[subregion] = float(xmax)
                reg.lat1[subregion] = float(ymin)
                reg.lat2[subregion] = float(ymax)

        elif self.params.FORM_region == 'countries':
            polyRegionFile = "countries/" + self.params.FORM_country + ".txt"
            xmin, xmax, ymin, ymax = getboxfrompolygon(polyRegionFile)
            reg = DefineRegion('world')
            region = self.params.FORM_country
            reg.name[1] = self.params.FORM_country
            reg.country[1] = self.params.FORM_country
            cmd = "cat countries/{country}_nan.txt | fgrep -v '#' | wc -l".format(country=self.params.FORM_country)
            ###print "cmd = %s<br>" % cmd
            string = subprocess.check_output(cmd, shell=True)
            ###print "string = %s<br>" % string
            reg.npoly[1] = int(string) - 1 # convention used for the simple polygons of the IPCC Atlas
            subregion = 1
            reg.lon1[subregion] = float(xmin)
            reg.lon2[subregion] = float(xmax)
            reg.lat1[subregion] = float(ymin)
            reg.lat2[subregion] = float(ymax)

        elif self.params.FORM_region == 'box':
            reg = DefineRegion('world')
            reg.name[1] = "box"
            region = "box"
            subregion = 1
            reg.lon1[subregion] = self.params.FORM_lon1
            reg.lon2[subregion] = self.params.FORM_lon2
            reg.lat1[subregion] = self.params.FORM_lat1
            reg.lat2[subregion] = self.params.FORM_lat2
        elif self.params.FORM_region == 'point':
            reg = DefineRegion('world')
            reg.name[1] = "point"
            region = "point"
            subregion = 1
            reg.lon1[subregion] = self.params.FORM_lon
            reg.lon2[subregion] = self.params.FORM_lon
            reg.lat1[subregion] = self.params.FORM_lat
            reg.lat2[subregion] = self.params.FORM_lat
        elif self.params.FORM_region == 'mask':
            raise PlotMapError("cannot handle maps with masks yet")
        else:
            raise PlotMapError("error: unknown region %(FORM_region)s" % paramsDict)

        if lwrite:
            self.logOut.info("lon1[{subregion}] = {lon1}<br>".format(subregion=subregion, lon1=reg.lon1[subregion]))
            self.logOut.info("lon2[{subregion}] = {lon2}<br>".format(subregion=subregion, lon2=reg.lon2[subregion]))
            self.logOut.info("lat1[{subregion}] = {lat1}<br>".format(subregion=subregion, lat1=reg.lat1[subregion]))
            self.logOut.info("lat2[{subregion}] = {lat2}<br>".format(subregion=subregion, lat2=reg.lat2[subregion]))

        self.log.debug("")
        self.log.debug("lon1[{subregion}] = {lon1}".format(subregion=subregion, lon1=reg.lon1[subregion]))
        self.log.debug("lon2[{subregion}] = {lon2}".format(subregion=subregion, lon2=reg.lon2[subregion]))
        self.log.debug("lat1[{subregion}] = {lat1}".format(subregion=subregion, lat1=reg.lat1[subregion]))
        self.log.debug("lat2[{subregion}] = {lat2}".format(subregion=subregion, lat2=reg.lat2[subregion]))
        self.log.debug('lonoverlap = %i' % lonoverlap)
        self.log.debug('latoverlap = %i' % latoverlap)

        if float(reg.lon1[subregion]) != -170 or float(reg.lon2[subregion]) != 190:
            plotlon1 = float(reg.lon1[subregion]) - lonoverlap
            plotlon2 = float(reg.lon2[subregion]) + lonoverlap
        else:
            plotlon1 = float(reg.lon1[subregion])
            plotlon2 = float(reg.lon2[subregion])

        if float(reg.lat1[subregion]) != -90:
            plotlat1 = float(reg.lat1[subregion]) - latoverlap
        else:
            plotlat1 = float(reg.lat1[subregion])

        if float(reg.lat2[subregion]) != 90:
            plotlat2 = float(reg.lat2[subregion]) + latoverlap
        else:
            plotlat2 = float(reg.lat2[subregion])

        plotlon1 = float(plotlon1)
        plotlon2 = float(plotlon2)
        plotlat1 = float(plotlat1)
        plotlat2 = float(plotlat2)

        if lwrite:
            self.logOut.info("plotlon1,plotlon2={plotlon1},{plotlon2}<br>".format(plotlon1=plotlon1, plotlon2=plotlon2))
            self.logOut.info("plotlat1,plotlat2={plotlat1},{plotlat2}<br>".format(plotlat1=plotlat1, plotlat2=plotlat2))

        self.log.debug("plotlon1,plotlon2 = {plotlon1},{plotlon2}".format(plotlon1=plotlon1, plotlon2=plotlon2))
        self.log.debug("plotlat1,plotlat2 = {plotlat1},{plotlat2}".format(plotlat1=plotlat1, plotlat2=plotlat2))

        # variable
        # Check if 'plotfile' is a NetCDF file
        cmd = "file {plotfile}".format(plotfile=self.plotfile)
        self.log.debug("cmd = '%s'" % cmd)
        resultProcess = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        if 'NetCDF' not in resultProcess:
            raise PlotMapError("Cannot find {plotfile}".format(plotfile=self.plotfile))

        root = 'atlas/maps/{dir}/{rel}{basename}'.format(dir=self.dir, rel=self.rel, basename=os.path.splitext(os.path.basename(self.plotfile))[0])

        folder = os.path.split(root)[0]
        if not os.path.exists(folder):
            self.log.debug('mkdir %s' % folder)
            os.makedirs(folder)

        region_extension = get_region_extension(self.params)
        root = "{root}_{plotvar}_{region_extension}".format(root=root, plotvar=self.params.FORM_plotvar,region_extension=region_extension)
        var = self.params.FORM_var
        normsd = self.params.FORM_normsd

        
        self.log.debug('region_extension = %s' % region_extension)
        self.log.debug('root = %s' % root)
        self.log.debug('var = %s' % var)
        self.log.debug('normsd = %s' % normsd)

        varObj = DefineVar(var, normsd)

        plotvarunits = varObj.units.strip('[]')

        self.log.debug("plotvarunits={plotvarunits}".format(plotvarunits=plotvarunits))

        cnfac = 1 # factor to scale the colour bar with
        if self.params.FORM_measure == 'diff':
            titlebegin = "{varname} %(FORM_begin2)s-%(FORM_end2)s minus %(FORM_begin1)s-%(FORM_end1)s {sname}".format(varname=varObj.varname, sname=self.sname) % paramsDict
        elif self.params.FORM_measure == 'regr':
            self.logOut.info("Using residuals of the fit for the hatching.<br>")
            titlebegin = "regression {varname} on %(FORM_regr)s %(FORM_begin_fit)s-%(FORM_end_fit)s {sname}".format(varname=varObj.varname, sname=self.sname) % paramsDict

            if self.params.FORM_regr == 'time':
                plotvarunits = "{plotvarunits}/100yr".format(plotvarunits=plotvarunits)
                varObj.fac = varObj.fac * 100
            elif self.params.FORM_regr.find('co2eq') >= 0:
                plotvarunits = "{plotvarunits}/100ppm".format(plotvarunits=plotvarunits)
                varObj.fac = varObj.fac * 100
                cnfac = 0.5
            elif self.params.FORM_regr == 'obstglobal' or self.params.FORM_regr == 'modtglobal':
                plotvarunits = "{plotvarunits}/K".format(plotvarunits=plotvarunits)
                cnfac = 0.5
            else:
                raise PlotMapError("internal error: unknow value for FORM_regr=%(FORM_regr)s" % paramsDict)
        else:
            raise PlotMapError("internal error: unknown measure %(FORM_measure)s" % paramsDict)

        if self.params.FORM_dataset == 'obs':
            if var in [el[0] for el in obs_var_values]: # make sure it is trusted input
                variable = 'self.params.FORM_obs_{var}'.format(var=var)
                FORM_field = eval(variable)
            else:
                print 'plot_atlas_map: unknown value for var %s<br>' % var
        else:
            FORM_field = "" # is only required for the obs
        datasetname = define_dataset(self.params.FORM_dataset, FORM_field)
        if self.params.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
            title = "%(FORM_scenario_cmip5)s {titlebegin} {datasetname}".format(titlebegin=titlebegin, datasetname=datasetname) % paramsDict
        elif self.params.FORM_dataset == 'CMIP3':
            title = "%(FORM_scenario_cmip3)s {titlebegin} {datasetname}".format(titlebegin=titlebegin, datasetname=datasetname) % paramsDict
        elif self.params.FORM_dataset == 'RT2b':
            title = "%(FORM_scenario_rt2b)s {titlebegin} {datasetname}".format(titlebegin=titlebegin, datasetname=datasetname) % paramsDict
        elif self.params.FORM_dataset in ('RT3', 'ERAi', '20CR', 'obs'):
            title = "{titlebegin} {datasetname}".format(titlebegin=titlebegin, datasetname=datasetname)
        else:
            raise PlotMapError("Unknown datasetA %(FORM_dataset)s" % paramsDict)

        self.log.debug('')
        self.log.debug('title = %s' % title)
        self.log.debug('titlebegin = %s' % titlebegin)
        self.log.debug("plotvarunits = {plotvarunits}".format(plotvarunits=plotvarunits))

        mycbar = True
        nsd = 1 # change < this number of standard deviations natural variability is hatched
        if self.params.FORM_plotvar != 'mean' :
            plotvar = self.params.FORM_plotvar
        elif self.params.FORM_measure == 'diff':
            plotvar = "{rel}diff".format(rel=self.rel)
        elif self.params.FORM_measure == 'regr':
            plotvar = "{rel}regr".format(rel=self.rel)

        self.log.debug('plotvar = %s' % plotvar)

        pmin = 5
        if pmin != 5:
            raise PlotMapError("Sorry, can only handle pmin = 5 at the moment, not {pmin},{nsd}".format(pmin=pmin, nsd=nsd))

        if plotvar.startswith('p'):
            plotvarname = plotvar.strip('p') + '%'
#            plotvarname = "%s%%" % plotvar[1:]
        else:
            plotvarname = self.params.FORM_plotvar

        self.log.debug('plotvarname = %s' % plotvarname)

        title = "{plotvarname} {title}".format(plotvarname=plotvarname, title=title)
        if plotvar == 'sd':
            uncert = 0
        else:
            uncert = self.uncert # hatching if data available

        force = True # false

        # log to Climate Explorer log file
        with open('log/log', 'a') as f:
            f.write('{datetime} {EMAIL} ({REMOTE_ADDR}) plot_atlas_map {title}\n'.format(datetime=strftime("%a %b %d %H:%M:%S %Z %Y", gmtime()), EMAIL=self.params.EMAIL, REMOTE_ADDR=self.params.REMOTE_ADDR, title=title))

        nclInputName = '{tempDir}/nclinput{pid}.ncl'.format(tempDir=self.tempDir, pid=os.getpid())
        epsFilename = '{root}.eps'.format(root=root)

        ###self.logOut.info('plotfile = %s<br>' % self.plotfile)
        if force or not os.path.exists(epsFilename) or (os.path.getsize(epsFilename) == 0) or (os.path.getmtime(epsFilename) < os.path.getmtime(self.plotfile)):
            if uncert == None:
                uncert = 1
            nclInputDict = { 'plotfile': self.plotfile, 'NCARG_ROOT': os.environ['NCARG_ROOT'], 'plotvar': plotvar,
                             'pmin': pmin, 'nsd': nsd, 'root': root, 'region': region,
                             'plotlon1': plotlon1, 'plotlon2': plotlon2,
                             'plotlat1': plotlat1, 'plotlat2': plotlat2,
                             'plotvarunits': plotvarunits, 'title': title,
                             'mycbar': mycbar, 'uncert': uncert, 'cnfac': cnfac}
            nclInputDict.update(varObj.__dict__)
            nclInputStr = """
            load "%(NCARG_ROOT)s/lib/ncarg/nclscripts/csm/gsn_code.ncl"
            load "%(NCARG_ROOT)s/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
            load "%(NCARG_ROOT)s/lib/ncarg/nclscripts/csm/contributed.ncl"
            load "%(NCARG_ROOT)s/lib/ncarg/nclscripts/csm/shea_util.ncl"
            load "./danoprob.ncl"

            begin

            ; READ DATA
              a = addfile("%(plotfile)s","r")
              ;;;if ( "%(plotvar)s" .eq. "diff" .or. "%(plotvar)s" .eq. "reldiff" ) then
                if (dimsizes(dimsizes(a->%(plotvar)s)) .gt. 3) then
                    plotvar = a->%(plotvar)s(0,0,:,:)
                    plotvar = a->%(plotvar)s(0,0,:,:) * %(fac)s
                    if (dimsizes(dimsizes(a->sd)) .gt. 3) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,0,:,:) / (0.000001 + abs(a->%(plotvar)s(0,0,:,:)))
                    else if (dimsizes(dimsizes(a->sd)) .gt. 2) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,:,:) / (0.000001 + abs(a->%(plotvar)s(0,0,:,:)))
                    else
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(:,:) / (0.000001 + abs(a->%(plotvar)s(0,0,:,:)))
                    end if
                    end if
                else if (dimsizes(dimsizes(a->%(plotvar)s)) .gt. 2) then
                    plotvar = a->%(plotvar)s(0,:,:)
                    plotvar = a->%(plotvar)s(0,:,:) * %(fac)s
                    if (dimsizes(dimsizes(a->sd)) .gt. 3) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,0,:,:) / (0.000001 + abs(a->%(plotvar)s(0,:,:)))
                    else if (dimsizes(dimsizes(a->sd)) .gt. 2) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,:,:) / (0.000001 + abs(a->%(plotvar)s(0,:,:)))
                    else
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(:,:) / (0.000001 + abs(a->%(plotvar)s(0,:,:)))
                    end if
                    end if
                else
                    plotvar = a->%(plotvar)s(:,:)
                    plotvar = a->%(plotvar)s(:,:) * %(fac)s
                    if (dimsizes(dimsizes(a->sd)) .gt. 3) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,0,:,:) / (0.000001 + abs(a->%(plotvar)s(:,:)))
                    else if (dimsizes(dimsizes(a->sd)) .gt. 2) then
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(0,:,:) / (0.000001 + abs(a->%(plotvar)s(:,:)))
                    else
                        prob = ( %(pmin)s / 100. )  * %(nsd)s * a->sd(:,:) / (0.000001 + abs(a->%(plotvar)s(:,:)))
                    end if
                    end if
                end if
                end if
                ; danoprob cuts on this variable; this gives %(pmin)s/100 when plotvar=%(nsd)s * sd

                copy_VarCoords(plotvar,prob)
              ;;;else
                ;;;plotvar = a->%(plotvar)s(0,:,:)
                ;;;plotvar = a->%(plotvar)s(0,:,:) * %(fac)s
                ;;;prob = a->prob(0,:,:)
              ;;;end if
            ; SETUP POSTSCRIPT
              p = new(15000,graphic)
              wks = gsn_open_wks("eps","%(root)s")

            ; RESOURCES FOR PLOT
              res = True
              res@gsnDraw = False
              res@gsnFrame = False
              if ("%(region)s".ne."world") then
               res@mpCenterLonF = (%(plotlon1)s+%(plotlon2)s)/2
              else
               res@mpCenterLonF = 10.
              end if

            ; COLORS
              rgbcbar = "%(rgbcbar)s"
              plotvarunits="%(plotvarunits)s"


            ; CONTOUR INTERVALS
              res@cnLevelSelectionMode = "ExplicitLevels"
              res@cnLevels = %(cnfac)s * %(cnlevels)s

            ; LABELS
              res@gsnCenterString = "%(title)s"
              res@gsnLeftString = ""
              res@gsnRightString = ""
              res@gsnStringFont = 21
              res@lbLabelBarOn = %(mycbar)s
              res@lbTitleString = "["+plotvarunits+"]"
              res@lbTitleFontHeightF = 0.012
              res@lbLabelFont = 21
              res@lbTitleFont = 21
              res@lbTitlePosition = "Right"
              res@lbTitleDirection = "Across"
              res@lbLabelAutoStride = True
              res@lbLabelFontHeightF = 0.012

            ; TO PREVENT AN UNPLOTTED HALF...
             if("%(region)s".eq."pacific") then
               usefieldf = False
             else
               usefieldf = True
             end if

            ; CALL PLOT FUNCTION
              res@mpPerimOn = False
              if("%(region)s".ne."arctic".and."%(region)s".ne."highlatitudes".and."%(region)s".ne."antarctica") then
               res@mpProjection = "Robinson"
               res@mpFillOn = False
               res@mpLimitMode = "LatLon"
               res@mpMinLonF = %(plotlon1)s
               res@mpMaxLonF = %(plotlon2)s
               res@mpMinLatF = %(plotlat1)s
               res@mpMaxLatF = %(plotlat2)s
               plot = danoprob(wks,res,plotvar,"shaded",%(cbar)s,rgbcbar,0,%(pmin)s,%(cmin)s,%(cmax)s,%(cint)s,"latlon",%(uncert)s,prob,usefieldf)
              end if
              if ("%(region)s".eq."arctic".or."%(region)s".eq."highlatitudes") then
               res@mpMinLatF = %(plotlat1)s
               res@gsnTickMarksOn = False
               plot = danoprob(wks,res,plotvar,"shaded",%(cbar)s,rgbcbar,0,%(pmin)s,%(cmin)s,%(cmax)s,%(cint)s,"NH",%(uncert)s,prob,usefieldf)
              end if
              if ("%(region)s".eq."antarctica") then
               res@mpMaxLatF = %(plotlat2)s
               res@gsnTickMarksOn = False
               plot = danoprob(wks,res,plotvar,"shaded",%(cbar)s,rgbcbar,0,%(pmin)s,%(cmin)s,%(cmax)s,%(cint)s,"SH",%(uncert)s,prob,usefieldf)
              end if
              lres = True
        """ % nclInputDict

        self.log.debug('Write data to %s' % nclInputName)
        with open(nclInputName, 'w') as f:
            f.write(nclInputStr)

        if self.params.FORM_region != 'srex' or self.params.FORM_srex != 'world':
            i = subregion
            if self.params.FORM_region == 'box' or self.params.FORM_region == 'point' \
                or ( self.params.FORM_region == 'srex' and reg.abbr[i] == ''):
                if lwrite:
                    self.logOut.info("using lon12,lat12<br>")
                nclInputStr = """
                ; ADD RECTANGLES
                  xpts = (/%(lon1)s,%(lon1)s,%(lon2)s,%(lon2)s,%(lon1)s/)
                  ypts = (/%(lat1)s,%(lat2)s,%(lat2)s,%(lat1)s,%(lat1)s/)
                  do i = 0,3
                   p(i) = gsn_add_polyline(wks,plot,xpts(i:i+1),ypts(i:i+1),lres)
                  end do
                  delete(xpts)
                  delete(ypts)
                """ % {'lon1': reg.lon1[i], 'lon2': reg.lon2[i], 'lat1': reg.lat1[i], 'lat2': reg.lat2[i]}

                self.log.debug('Append data to %s' % nclInputName)
                with open(nclInputName, 'a') as f:
                    f.write(nclInputStr)

            else:
                if self.params.FORM_region == 'srex':
                    polyfile = "SREX/%(abbr)s_kaal.txt" % {'abbr': reg.abbr[i]}
                elif self.params.FORM_region == 'countries':
                    polyfile = "countries/%(country)s_nan.txt" % {'country': reg.country[i]}
                else:
                    raise PlotMapError("NCL code for region %s not yet ready" % self.params.FORM_region)

                # polygon
                nclInputStr = """
                ; ADD POLYGONS - the "kaal" version does not have comments and repeats the first line at the end
                   lonlat = asciiread("%(polyfile)s",(/1+%(npoly)s,2/),"float")
                   do i = 0,%(npoly2)s
                    p(i) = gsn_add_polyline(wks,plot,lonlat(i:i+1,0),lonlat(i:i+1,1),lres)
                   end do
                    delete(lonlat)
                """ % {'polyfile': polyfile, 'npoly': reg.npoly[i], 'npoly2': (reg.npoly[i] - 1)}

                self.log.debug('Append data to %s' % nclInputName)
                with open(nclInputName, 'a') as f:
                    f.write(nclInputStr)

        # TODO: implement this
#        cat >> /tmp/nclinput$$.ncl <<EOF
        nclInputDict = { 'plotvarname': plotvarname }
        nclInputDict.update(reg.__dict__)
        nclInputStr = """
           draw(plot)
          ; ADD PERCENTILE LABEL
          ;txres = True
          ;txres@txFontHeightF = 0.017
          ;txres@txFontColor = 1 ; 0
          ;txres@txBackgroundFillColor = "white" ; "black"
          ;gsn_text_ndc(wks,"%(plotvarname)s",$labelx,$labely,txres)

          frame(wks)
          delete(wks)
        end
        """ % nclInputDict

        self.log.debug('Append data to %s' % nclInputName)
        with open(nclInputName, 'a') as f:
            f.write(nclInputStr)

        ### TEMP
#        with open(nclInputName) as f:
#            nclLines = f.readlines()

#        print '<br>File nclLines<br>'
#        print '----------------<br>'
#        print '<br>'.join(nclLines)
#        print '\n'.join(nclLines)
#        print '----------------<br>'
        ##### TEMP

        cmd = "ncl -Qn < {nclInputName}".format(nclInputName=nclInputName)
        self.log.debug('Launch: %s' % cmd)
        processOutput = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        for el in processOutput.split('\n'):
            if 'EXPLICIT' not in el:
                self.logOut.info(el + '<br>')


        size = os.path.getsize('{root}.eps'.format(root=root))

        if size < 100:

            epsFilename = '{root}.eps'.format(root=root)

            if os.path.exists(epsFilename):
                self.log.debug('rm %s' % epsFilename)
                os.remove(epsFilename)

            self.logOut.info("postscript file too small, {size} bytes.<br>".format(size=size))

            cmd = "cat -n {nclInputName}".format(nclInputName=nclInputName)
            self.log.debug('Launch: %s' % cmd)
            processOutput = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

            # TODO: Instance of 'list' has no 'split' member
            for el in processOutput.split('\n'):
                self.logOut.info(el + '<br>')

            raise PlotMapError("Something went wrong in the script:")

        # TODO: implement this
        cmd = './bin/epstopdf {root}.eps'.format(root=root)
        self.log.debug('Launch: %s' % cmd)
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        cmd = "gs -q -r180 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -sDEVICE=ppmraw -sOutputFile={root}.pnm {root}.eps -c quit".format(root=root)
        self.log.debug('Launch: %s' % cmd)
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        cmd = "pnmcrop {root}.pnm | pnmtopng > {root}.png".format(root=root)
        self.log.debug('Launch: %s' % cmd)
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        os.remove('{root}.pnm'.format(root=root))

        pngfile = '{root}.png'.format(root=root)
        # TODO: check if this is correct. Ask geert-jan
        halfwidth = util.getpngwidth(pngfile)

        return (root, title, halfwidth)

