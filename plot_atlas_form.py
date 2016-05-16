#!/usr/bin/python

"""
script to produce maps and time series analogous
to the IPCC WG1 AR3 Annex I "Atlas" but much more general.
The following choices have to be made by the user
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
#import cgitb
#cgitb.enable()

import os
import cgi
import sys
import logging
import util
import settings
###from urlparse import parse_qs
from subprocess import CalledProcessError
from formparameters import FormParameters, region_values, \
    srex_values, country_values, ipbes_values, mon_values, dataset_values, \
    cmip5_var_values, cmip5_extreme_values, cordex_var_values, cmip3_var_values, erai_var_values, era20c_var_values, c20cr_var_values, obs_var_values, \
    output_values, sum_values, regr_values, \
    scenario_cmip5_values, scenario_cordex_values, obs_tas_values, obs_tasmax_values, obs_tasmin_values, obs_pr_values, \
    obs_psl_values, measure_values, plotvar_values 
from plot_atlas_map import PlotAtlasMap, PlotMapError
from plot_atlas_series import PlotAtlasSeries, PlotSeriesError
from more_functions_atlas import GetModelError
from jinja2 import Environment, FileSystemLoader

# Load HTML template
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('plot_atlas_form.htm')

# Get variables from the HTML formular
form = cgi.FieldStorage()

# Create a logger
log = logging.getLogger('plot_atlas')
log.setLevel(logging.ERROR)

# Configure the logger to log in the HTML page
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(util.JavascriptFormatter())
log.addHandler(hdlr)

print 'Content-Type: text/html'
print

# Initialize variables from formular
params = FormParameters(form)
#params = FormParameters(form, logLevel=logging.DEBUG)
params.calculateDate(form)

if 0:
    dumpParams = params.dump()
    for el in dumpParams:
        log.error(el)

lwrite = False
if params.EMAIL == 'oldenbor@knmi.nl':
    lwrite = False

#util.headerScript('Plot %s %s %s' % (params.FORM_dataset, params.FORM_var, params.FORM_output))
util.headerScript(params)

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
    
# Generate template
print template.render(params.__dict__,
                      region_values=region_values,
                      srex_values=srex_values,
                      country_values=country_values,
                      ipbes_values=ipbes_values,
                      mon_values=mon_values,
                      sum_values=sum_values,
                      output_values=output_values,
                      dataset_values=dataset_values,
                      cmip5_var_values=cmip5_var_values,
                      cmip5_extreme_values=cmip5_extreme_values,
                      cordex_var_values=cordex_var_values,
                      cmip3_var_values=cmip3_var_values,
                      erai_var_values=erai_var_values,
                      era20c_var_values=era20c_var_values,
                      c20cr_var_values=c20cr_var_values,
                      obs_var_values=obs_var_values,
                      scenario_cmip5_values=scenario_cmip5_values,
                      scenario_cordex_values=scenario_cordex_values,
                      obs_tas_values=obs_tas_values,
                      obs_tasmin_values=obs_tasmin_values,
                      obs_tasmax_values=obs_tasmax_values,
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

try:                      
    if params.DO_ACTION:

        # if nominous, save in defaults file for next visit
        if params.EMAIL != "someone@somewhere" and params.EMAIL != "":
            prefs = "prefs/" + params.EMAIL + ".atlas"
            with open(prefs, 'w') as f:
                for v in vars(params):
                    if v[:5] == "FORM_":
                        if v == "FORM_normsd":
                            f.write(v+' = "absolute";\n')
                        else:
                            w = str(eval("params."+v))
                            f.write(v+' = "'+w+'";\n')

        ###print "Processing ...<p>"

        if params.FORM_output == 'map':
            log.debug('map')
            plotMap = PlotAtlasMap(params)
#            plotMap = PlotAtlasMap(params, logLevel=logging.DEBUG)
            plotMap.process()

        elif params.FORM_output == 'series':

            # Do some sanity check
            if ( params.FORM_dataset in ['CMIP5','CMIP5one'] and
                params.FORM_rcp26 == '' and params.FORM_rcp45 == '' and
                params.FORM_rcp60 == '' and params.FORM_rcp85 == ''):
                print 'Error. Select at least one scenario in Time series options.<br>'
            else:
                ###print "<font color=#ff2222>plot_atlas_series: CONTAINS MANY BUGS, ONLY FOR INTERNAL TESTING AT KNMI</font><br>"
                
                ###log.debug('series')
                plotSeries = PlotAtlasSeries(params)
#                plotSeries = PlotAtlasSeries(params, logLevel=logging.DEBUG)
                plotSeries.process()
                plotSeries.doPlot()
        elif params.FORM_output == 'histogram':
            print " A WONDERFUL TIME SERIES PLOT WILL APPEAR HERE"
        elif params.FORM_output == 'scatter':
            print " A WONDERFUL TIME SCATTER PLOT WILL APPEAR HERE"
        else:
            print "Error: do not know how to make a %s plot" % params.FORM_output
    else:
        # some news to the user
        f = open("atlas_news.html", "r")
        text = f.read()
        print text
        f.close()

except (PlotMapError, PlotSeriesError) as e:
    print '<br><b>Error: %s</b></br>' % e
    util.generateReport(params, e)
except CalledProcessError as e:
    print '<br><b>Error in %s</b><br>' % e.cmd
    if e.output:
        print '<br>Output:<br><b>%s</b><br>' % cgi.escape(e.output).replace('\n', '<br />')
    print '<br>Return code: <b>%s</b><br>' % e.returncode
    util.generateReport(params, e)
except GetModelError as e:
    print 'GetModelError: %s' % e
    util.generateReport(params, e)

os.chdir(settings.WORKING_DIR)
util.footerScript()

