#!/usr/bin/env python

"""
script to produce maps and time series analogous
to the IPCC WG1 AR3 Annex I "Atlas" but much more general.
The follwoing choices have to be made by the user
1) region: a rectangle or a predefined (uploaded?) mask
2) season: starting month, number of months
3) dataset: CMIP3, CMIP3, ENSEMBLES RCM, ...; maybe observational as well
4) variable (list depends on the above)
3) map or time series
map:
6m) scenario (if model)
7m) measure of change, time period(s)
8m) measure of PDF
9m) measure of natural variability
time series:
6t) time period
7t) scenario(s)
8t) include observations, which ones
"""

# Only for debugging
import cgitb
cgitb.enable()

import os
import cgi
import sys
import datetime
import logging
import util
from jinja2 import Environment, FileSystemLoader


class AtlasParams:
    """Contains all paramaters from the plot_atlas_form webpage."""

    def __init__(self, form, logLevel=logging.DEBUG):
        """Initialize the object."""

        # Create a logger
        self.log = logging.getLogger('AtlasParam')
        self.log.setLevel(logLevel)

        # Configure the logger to log in the HTML page
        self.hdlr = logging.StreamHandler(sys.stdout)
        self.hdlr.setFormatter(util.JavascriptFormatter())
        self.log.addHandler(self.hdlr)

        self.EMAIL = cgi.escape(form.getfirst('EMAIL', 'someone@somewhere'))
        self.FORM_region = cgi.escape(form.getfirst('region', 'srex'))
        self.FORM_srex = cgi.escape(form.getfirst('srex', 'world'))
        self.FORM_lon1 = cgi.escape(form.getfirst('lon1', ''))
        self.FORM_lon2 = cgi.escape(form.getfirst('lon2', ''))
        self.FORM_lat1 = cgi.escape(form.getfirst('lat1', ''))
        self.FORM_lat2 = cgi.escape(form.getfirst('lat2', ''))
        self.FORM_masktype = cgi.escape(form.getfirst('masktype', 'all'))
        self.FORM_mon = cgi.escape(form.getfirst('mon', '1'))
        self.FORM_sum = cgi.escape(form.getfirst('sum', '12'))
        self.FORM_dataset = cgi.escape(form.getfirst('dataset', 'CMIP5'))
        self.FORM_var = cgi.escape(form.getfirst('var', 'tas'))
        self.FORM_normsd = cgi.escape(form.getfirst('normsd', ''))
        self.FORM_output = cgi.escape(form.getfirst('output', 'map'))
        self.FORM_scenario_cmip5 = cgi.escape(form.getfirst('scenario_cmip5', 'rcp45'))
        self.FORM_scenario_cmip3 = cgi.escape(form.getfirst('scenario_cmip3', ''))
        self.FORM_scenario_rt2b = cgi.escape(form.getfirst('scenario_rt2b', ''))
        self.FORM_measure = cgi.escape(form.getfirst('measure', 'diff'))
        self.FORM_regr = cgi.escape(form.getfirst('regr', 'time'))
        self.FORM_plotvar = cgi.escape(form.getfirst('plotvar', ''))
        self.FORM_obs_tas = cgi.escape(form.getfirst('obs_tas', 'giss_temp_1200'))
        self.FORM_obs_pr = cgi.escape(form.getfirst('obs_pr', 'hadcrut4110'))
        self.FORM_obs_psl = cgi.escape(form.getfirst('obs_psl', 'hadlslp2r'))
        self.FORM_rcp26 = cgi.escape(form.getfirst('rcp26', ''))
        self.FORM_rcp45 = cgi.escape(form.getfirst('rcp45', ''))
        self.FORM_rcp60 = cgi.escape(form.getfirst('rcp60', ''))
        self.FORM_rcp85 = cgi.escape(form.getfirst('rcp85', ''))
        self.FORM_anomaly = cgi.escape(form.getfirst('anomaly', ''))
        self.FORM_anom1 = cgi.escape(form.getfirst('anom1', ''))
        self.FORM_anom2 = cgi.escape(form.getfirst('anom2', ''))

        self.FORM_lon = cgi.escape(form.getfirst('lon', ''))
        self.FORM_lat = cgi.escape(form.getfirst('lat', ''))

        self.var_ok = False
        self.dataset_ok = False

        self.yr1 = 0
        self.yr2 = 0
        self.FORM_begin = None
        self.FORM_end = None
        self.FORM_begin2 = None
        self.FORM_end2 = None

        self.log.info("Init.")

    def calculateDate(self, form):
        """Calculate dates."""

        self.log.debug('CalculateDate')

        # Find yr1 and yr2
        thisYear = datetime.date.today() - datetime.timedelta(days=31)
        thisYear = thisYear.year

        dumptypes, endhistory = '0', thisYear

        if self.FORM_dataset in ['CMIP5', 'CMIP5one']:
            self.yr1, self.yr2 = 1861, 2100
            dumptypes, endhistory = '0 1', 2005
        elif self.FORM_dataset == 'CMIP3':
            self.yr1, self.yr2 = 1900, 2099
            dumptypes, endhistory = '0 1', 2000
        elif self.FORM_dataset == 'RT2b':
            self.yr1, self.yr2 = 1950, 2100
            dumptypes, endhistory = '0 1', 2000
        elif self.FORM_dataset == 'RT3':
            self.yr1, self.yr2 = 1960, 2000
        elif self.FORM_dataset == '20CR':
            self.yr1, self.yr2 = 1878, 2010
        elif self.FORM_dataset == 'obs':
            if self.FORM_var == 'tas':
                self.yr1 = 1880
            else:
                self.yr1 = 1901
            self.yr2 = thisYear

        self.log.info('Find yr1 = %s and yr2 = %s' % (str(self.yr1), str(self.yr2)))

        self.FORM_begin = cgi.escape(form.getfirst('begin', str(self.yr1)))
        self.FORM_end = cgi.escape(form.getfirst('end', '2005'))
        self.FORM_begin2 = cgi.escape(form.getfirst('begin2', '2006'))
        self.FORM_end2 = cgi.escape(form.getfirst('end2', str(self.yr2)))

        log.info('before self.FORM_begin   = %s', self.FORM_begin)
        log.info('before self.FORM_end     = %s', self.FORM_end)
        log.info('before self.FORM_begin2  = %s', self.FORM_begin2)
        log.info('before self.FORM_end2    = %s', self.FORM_end2)

        if self.FORM_end > self.yr2:
            self.FORM_begin = str(int(self.yr2) - int(self.FORM_end) + int(self.FORM_begin))
            if self.FORM_begin < self.yr1:
                self.FORM_begin = self.yr1
            self.FORM_end = self.yr2

        if self.FORM_begin < self.yr1:
            self.FORM_end = str(int(self.yr1) + int(self.FORM_end) - int(self.FORM_begin))
            if self.FORM_end > self.yr2:
                self.FORM_end = self.yr2
            self.FORM_begin = self.yr1

        if self.FORM_end2 > self.yr2:
            self.FORM_begin2 = str(int(self.yr2) - int(self.FORM_end2) + int(self.FORM_begin2))
            if self.FORM_begin2 < self.yr1:
                self.FORM_begin2 = self.yr1
            self.FORM_end2 = self.yr2

        if self.FORM_begin2 < self.FORM_end:
            self.FORM_end2 = str(int(self.FORM_end) + 1 + int(self.FORM_end2) - int(self.FORM_begin2))
            if self.FORM_end2 > self.yr2:
                self.FORM_end2 = self.yr2
            self.FORM_begin2 = str(int(self.FORM_end) + 1)

        log.info('AFTER self.FORM_begin   = %s', self.FORM_begin)
        log.info('AFTER self.FORM_end     = %s', self.FORM_end)
        log.info('AFTER self.FORM_begin2  = %s', self.FORM_begin2)
        log.info('AFTER self.FORM_end2    = %s', self.FORM_end2)

        if self.FORM_dataset in ['ERAi']:
            self.yr1 = 1979
            self.yr2 = thisYear
            self.log.debug('FORM_dataset == ERAi, yr1=%i, yr2=%i', self.yr1, self.yr2)

        if self.FORM_dataset == 'obs':
            self.dataset_ok = True
            self.var_ok = False
            self.log.debug('--- 1')     # TEMP

            if self.FORM_var in ['tas', 'pr', 'psl']:
                self.var_ok = True
                self.log.debug('--- 2')     # TEMP

        if self.FORM_measure == 'regr':
            if self.FORM_end > self.yr2:
                self.FORM_end = self.yr2

            if self.FORM_begin < self.yr1:
                self.FORM_begin = self.yr1
            self.log.debug('FORM_measure == regr, yr1=%i, yr2=%i', self.yr1, self.yr2)
                

    def display(self):
        """Display all parameters."""

        disp = [["EMAIL                 = %s" % self.EMAIL],
                ["FORM_region           = %s" % self.FORM_region],
                ["FORM_srex             = %s" % self.FORM_srex],
                ["FORM_lon1             = %s" % self.FORM_lon1],
                ["FORM_lon2             = %s" % self.FORM_lon2],
                ["FORM_lat1             = %s" % self.FORM_lat1],
                ["FORM_lat2             = %s" % self.FORM_lat2],
                ["FORM_masktype         = %s" % self.FORM_masktype],
                ["FORM_mon              = %s" % self.FORM_mon],
                ["FORM_sum              = %s" % self.FORM_sum],
                ["FORM_dataset          = %s" % self.FORM_dataset],
                ["FORM_var              = %s" % self.FORM_var],
                ["FORM_normsd           = %s" % self.FORM_normsd],
                ["FORM_output           = %s" % self.FORM_output],
                ["FORM_scenario_cmip5   = %s" % self.FORM_scenario_cmip5],
                ["FORM_scenario_cmip3    = %s" % self.FORM_scenario_cmip3],
                ["FORM_scenario_rt2b    = %s" % self.FORM_scenario_rt2b],
                ["FORM_measure          = %s" % self.FORM_measure],
                ["FORM_regr             = %s" % self.FORM_regr],
                ["FORM_plotvar          = %s" % self.FORM_plotvar],
                ["FORM_obs_tas          = %s" % self.FORM_obs_tas],
                ["FORM_obs_pr           = %s" % self.FORM_obs_pr],
                ["FORM_obs_psl          = %s" % self.FORM_obs_psl],
                ["FORM_rcp26            = %s" % self.FORM_rcp26],
                ["FORM_rcp45            = %s" % self.FORM_rcp45],
                ["FORM_rcp60            = %s" % self.FORM_rcp60],
                ["FORM_rcp85            = %s" % self.FORM_rcp85],
                ["FORM_anomaly          = %s" % self.FORM_anomaly],
                ["FORM_anom1            = %s" % self.FORM_anom1],
                ["FORM_anom2            = %s" % self.FORM_anom2],

                ["FORM_lon              = %s" % self.FORM_lon],
                ["FORM_lat              = %s" % self.FORM_lat],

                ["yr1                   = %s" % self.yr1],
                ["yr2                   = %s" % self.yr2],
                ["FORM_begin            = %s" % self.FORM_begin],
                ["FORM_end              = %s" % self.FORM_end],
                ["FORM_begin2           = %s" % self.FORM_begin2],
                ["FORM_end2             = %s" % self.FORM_end2]]

        self.log.debug("Display parameters")
        for el in disp:
            self.log.debug(el)

# Load HTML template
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('plot_atlas_form.htm')

# Get variables from the HTML formular
form = cgi.FieldStorage()

# Create a logger
log = logging.getLogger('plot_atlas')
log.setLevel(logging.DEBUG)

# Configure the logger to log in the HTML page
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(util.JavascriptFormatter())
log.addHandler(hdlr)

print 'Content-Type: text/html'
print

# if the script does not call itself load saved values
###echo "EMAIL=$EMAIL, FORM_resubmitted=$FORM_resubmitted<br>"
#if [ $EMAIL != someone@somewhere ]; then
#	if [ "$FORM_resubmitted" != true ]; then
#  		def=prefs/$EMAIL.plot_atlas.$NPERYEAR
#  		if [ -f $def ]; then
#    		eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
#  		fi
#  	else
#  		. ./plot_atlas_defaults_write.cgi
#	fi
#fi

# Display variables from the HTML webpage
for val in form.value:
    log.debug('==> %s', str(val))


# Initialize variables from formular
params = AtlasParams(form)
params.calculateDate(form)
params.display()

log.debug('%s plot_atlas_form', os.getenv('REMOTE_ADDR'))
#util.headerScript('Plot %s %s %s' % (params.FORM_dataset, params.FORM_var, params.FORM_output))
util.headerScript()

httpUserAgent = os.getenv('HTTP_USER_AGENT').lower()    
if ('mobile' in httpUserAgent) or ('opera' in httpUserAgent):
    number = "number"
    textsize2 = "style=\"width: 4em;\""
    textsize3 = "style=\"width: 5em;\""
    textsize4 = "style=\"width: 6em;\""
    textsize6 = "style=\"width: 7em;\""
    textsize10 = "style=\"width: 13em;\""
else:
    number = "text"
    textsize2 = "size=2"
    textsize3 = "size=3"
    textsize4 = "size=4"
    textsize6 = "size=6"
    textsize10 = "size=10"
    
# Region: Predefined (srex)
region_values = [['srex', 'predefined'],
                 ['point', 'place'],
                 ['box', 'box'],
                 ['mask', 'mask']]

srex_values = [['world', 'World'],
               ['worldland', 'World (land)'],
               ['worldsea_selected', 'World (sea)'],
               ['NAmerica', 'North America'],
               ['SAmerica', 'South America'],
               ['Europe', 'Europe'],
               ['Africa', 'Africa'],
               ['Asia', 'Asia'],
               ['Australia', 'Australia'],
               ['Arcticland', 'Arctic (land)'],
               ['Arcticsea', 'Arctic (sea)'],
               ['CGI', 'SREX Canada/Greenland/Iceland'],
               ['NAS', 'SREX North Asia'],
               ['ALA', 'SREX Alaska'],
               ['WNA', 'SREX West North America'],
               ['CNA', 'SREX Central North America'],
               ['ENA', 'SREX Eastern North America'],
               ['CAM', 'SREX Central America'],
               ['Caribbean', 'Caribbean'],
               ['AMZ', 'SREX Amazon'],
               ['NEB', 'SREX North-East Brazil'],
               ['WSA', 'SREX West Coast South America'],
               ['SSA', 'SREX Southeastern South America'],
               ['NEU', 'SREX North Europe'],
               ['CEU', 'SREX Central Europe'],
               ['MED', 'SREX South Europe/Mediterranean'],
               ['SAH', 'SREX Sahara'],
               ['WAF', 'SREX west Africa'],
               ['EAF', 'SREX East Africa'],
               ['SAF', 'SREX Southern Africa'],
               ['WIndian', 'West Indian Ocean'],
               ['WAS', 'SREX West Asia'],
               ['CAS', 'SREX Central Asia'],
               ['TIB', 'SREX Tibetan Plateau'],
               ['EAS', 'SREX Eastern Asia'],
               ['SAS', 'SREX South Asia'],
               ['NIndian', 'North Indian Ocean'],
               ['SEA', 'SREX Southeast Asia (land)'],
               ['SEAsia_sea', 'Southeast Asia (sea)'],
               ['NAU', 'SREX North Australia'],
               ['SAU', 'SREX South Australia/New Zealand'],
               ['NTPacific', 'Northern Tropical Pacific'],
               ['EQPacific', 'Equatorial Pacific'],
               ['STPacific', 'Southern Tropical Pacific'],
               ['Antarcticland', 'Antarctic (land)'],
               ['Antarcticsea', 'Antarctic (sea)']]

mon_values = [['1', 'Jan'],
              ['2', 'Feb'],
              ['3', 'Mar'],
              ['4', 'Apr'],
              ['3', 'May'],
              ['6', 'Jun'],
              ['7', 'Jul'],
              ['8', 'Aug'],
              ['9', 'Sep'],
              ['10', 'Oct'],
              ['11', 'Nov'],
              ['12', 'Dec']]

dataset_values = [['CMIP5', 'GCM: CMIP5 (full set)'],
                  ['CMIP5one', 'GCM: CMIP5 (one member per model)'],
                  ['CMIP3', 'GCM: CMIP3'],
                  ['RT2b', 'RCM: ENSEMBLES (Europe) GCM-driven'],
                  ['RT3', 'RCM: ENSEMBLES (Europe) ERA40-driven'],
                  ['ERAi', 'ERA-interim reanalysis'],
                  ['20CR', '20C reanalysis'],
                  ['obs', 'Observations']]

var_values = [['tas', 'near-surface temperature'],
              ['tasmin', 'minimum near-surface temperature'],
              ['tasmin', 'maximum near-surface temperature'],
              ['pr', 'precipitation'],
              ['evspsbl', 'evaporation, transpiration, sublimation'],
              ['pme', 'P-E, net water flux'],
              ['huss', 'specific humidity near the surface'],
              ['rsds', 'downward solar radiation at the surface'],
              ['psl', 'air pressure at sea-level']]

output_values = [['map', 'map'],
                 ['series', 'time series'],
                 ['histogram', 'histogram']]
#                ['scatter', 'scatter plots']

sum_values = [str(el) for el in range(1, 13)]    # ['1', '2', ..., '12']

regr_values = [['time', 'Linear trend in time'],
               ['co2eq', 'Proportional to effective CO2 concentration'],
               ['obstglobal', 'Proportional to observed Tglobal'],
               ['modtglobal', 'Proportional to modelled Tglobal']]

scenario_cmip5_values = [['rcp26', 'Historical + RCP2.6'],
                         ['rcp45', 'Historical + RCP4.5'],
                         ['rcp60', 'Historical + RCP6.0'],
                         ['rcp83', 'Historical + RCP8.5']]

obs_tas_values = [['giss_temp_1200', 'GISTEMP 1200'],
                  ['ncdc_temp', 'NCDC MOST'],
                  ['hadcrut4110', 'HadCRUT4.1.1.0']]

obs_pr_values = [['gpcc_25', 'GPCC v6'],
                 ['prca', 'NCDC anomalies'],
                 ['cru311_pre_25', 'CRU TS 3.10.01']]

obs_psl_values = [['trenberthslp', 'UCAR ds010 (NH only)'],
                  ['hadslp2r', 'HadSLP2r']]

measure_values = [['diff', 'Difference of two periods'],
                  ['regr', 'Linear or non-linear trend']]

plotvar_values = [['mean', 'mean'],
                  ['p025', '2.5%'],
                  ['p05', '5%'],
                  ['p10', '10%'],
                  ['p17', '17%'],
                  ['p25', '25%'],
                  ['p50', '50%'],
                  ['p75', '75%'],
                  ['p83', '83%'],
                  ['p90', '90%'],
                  ['p95', '95%'],
                  ['p975', '97.5%']]

# Generate template
print template.render(EMAIL=params.EMAIL,
                      FORM_region=params.FORM_region,
                      FORM_srex=params.FORM_srex,
                      FORM_lat1=params.FORM_lat1,
                      FORM_lat2=params.FORM_lat2,
                      FORM_lon1=params.FORM_lon1,
                      FORM_lon2=params.FORM_lon2,
                      FORM_masktype=params.FORM_masktype,
                      FORM_lon=params.FORM_lon,
                      FORM_lat=params.FORM_lat,
                      FORM_mon=params.FORM_mon,
                      FORM_sum=params.FORM_sum,
                      FORM_normsd=params.FORM_normsd,
                      FORM_dataset=params.FORM_dataset,
                      FORM_var=params.FORM_var,
                      FORM_output=params.FORM_output,
                      FORM_measure=params.FORM_measure,
                      FORM_begin=params.FORM_begin,
                      FORM_end=params.FORM_end,
                      FORM_begin2=params.FORM_begin2,
                      FORM_end2=params.FORM_end2,
                      FORM_scenario_cmip5=params.FORM_scenario_cmip5,
                      FORM_scenario_cmip3=params.FORM_scenario_cmip3,
                      FORM_obs_tas=params.FORM_obs_tas,
                      FORM_obs_pr=params.FORM_obs_pr,
                      FORM_obs_psl=params.FORM_obs_psl,
                      FORM_regr=params.FORM_regr,
                      FORM_plotvar=params.FORM_plotvar,
                      yr1=params.yr1,
                      yr2=params.yr2,
                      var_ok=params.var_ok,
                      dataset_ok=params.dataset_ok,
                      region_values=region_values,
                      srex_values=srex_values,
                      mon_values=mon_values,
                      sum_values=sum_values,
                      output_values=output_values,
                      dataset_values=dataset_values,
                      var_values=var_values,
                      scenario_cmip5_values=scenario_cmip5_values,
                      obs_tas_values=obs_tas_values,
                      obs_pr_values=obs_pr_values,
                      obs_psl_values=obs_psl_values,
                      measure_values=measure_values,
                      regr_values=regr_values,
                      plotvar_values=plotvar_values,
                      number=number,
                      textsize2=textsize2,
                      textsize3=textsize3,
                      textsize4=textsize4,
                      textsize6=textsize6,
                      textsize10=textsize10
                      )

#if params.FORM_region == params.FORM_region_old and params.FORM_dataset == params.FORM_dataset_old and params.FORM_var == params.FORM_var_old and params.FORM_measure == params.FORM_measure_old and params.FORM_output == params.FORM_output_old:
if params.FORM_output == 'map':
    log.debug('map')
    # plot_atlas_map.cgi
elif params.FORM_output == 'series':
    log.debug('series')
    # plot_atlas_series.cgi
elif params.FORM_output == 'histogram':
    print " A WONDERFUL TIME SERIES PLOT WILL APPEAR HERE"
elif params.FORM_output == 'scatter':
    print " A WONDERFUL TIME SCATTER PLOT WILL APPEAR HERE"
else:
    print "Error: do not know how to make a %s plot" % params.FORM_output


util.footerScript()
