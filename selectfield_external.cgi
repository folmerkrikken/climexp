#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field or time series" "External data" "index,nofollow"
cat <<EOF
<div class="kalelink">
This page allows access to remotely stored datasets.  Please select a 2D field from one of these datasets.  This will be transferred to the Climate Explorer for further analysis.  The field will be available under <span class=kalelink><a href="selectfield_use.cgi?id=$EMAIL">user-defined fields</a></span> for the next 3 days.
</div>

<form action="selectsectionform.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select dataset">
Choose a dataset and press this button</td></tr>

<tr><td>Seasonal Forecasts
<td><input type="radio" class="formradio" name="CLASS" value="Demeter">DEMETER, 7 models, 9 ensemble members each, hindcasts 1958-2001 (see also <a href="/selectfield_sea.cgi?id=$EMAIL">here</a>)<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/demeter/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_stream_2">ENSEMBLES stream 2, 5 models, 9 ensemble members each, 7-month hindcasts 1960-2005<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_stream_2_daily">ENSEMBLES stream 2 daily data (please only retrieve small areas)<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_stream_1">ENSEMBLES stream 1<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_stream_1_ocean">ENSEMBLES stream 1 ocean data<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_stream_1_daily">ENSEMBLES stream 1 daily data (please only retrieve small areas)<td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>Regional climate models
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_RT3">ENSEMBLES RT3 monthly data, 16 RCMs 1961-2000 with ERA-40 boundaries<td><a href="wipefoot.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_RT2b">ENSEMBLES RT2b monthly data, RCMs 1950-2050/2100 with GCM A1b boundaries<td><a href="wipefoot.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENSEMBLES_AMMA">ENSEMBLES West Africa (AMMA) monthly data, RCMs 1961-2000 with ERA40 boundaries and 1950-2050 with GCM boundaries<td><a href="wipefoot.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="Prudence">Prudeence monthly data, RCM time-slices forced by a variety of GCMs<td><a href="wipefoot.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>Re-analyses
<td><input type="radio" class="formradio" name="CLASS" value="Reanalysis-2_pressure">NCEP/DOE Reanalysis-2 atmospheric data 1979-now (see also <a href="/selectfield_rea.cgi?id=$EMAIL">here</a>)<td><a href="wipefoot.cgi?http://www.cpc.ncep.noaa.gov/products/wesley/reanalysis2/kana/reanl2-1.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="Reanalysis-2_fluxes">NCEP/DOE Reanalysis-2 flux data 1979-now (see also <a href="/selectfield_rea.cgi?id=$EMAIL">here</a>)<td><a href="wipefoot.cgi?http://www.cpc.ncep.noaa.gov/products/wesley/reanalysis2/kana/reanl2-1.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="NCEP_NCAR_reanalysis">NCEP/NCAR Reanalysis-1 atmospheric data 1948-now (see also <a href="/selectfield_rea.cgi?id=$EMAIL">here</a>)<td><a href="wipefoot.cgi?http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="20th_century_reanalysis">20th Century Reanalysis surface data (1908-1958)<td><a href="wipefoot.cgi?http://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2c.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>Ocean re-analyses
<td><input type="radio" class="formradio" name="CLASS" value="SODA">0.5&deg; SODA ocean re-analysis 2.0.2-2.0.3 1958-2004 <td><a href="wipefoot.cgi?http://apdrc.soest.hawaii.edu/datadoc/soda_pop2.0.2.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="SODA_surface">0.5&deg; SODA ocean re-analysis 2.0.2-2.0.3 1958-2004, a few more fields<td><a href="wipefoot.cgi?http://www.imber.info/CLIMECO_Programme.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ENACT">ENACT ocean re-analyses, 5 systems, 1962-2004 <td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENACT/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;
<td><input type="radio" class="formradio" name="CLASS" value="ECMWF_ORA-S3_ocean">1.4&deg; ECMWF System-3 ocean reanalysis (ORA-S3), 1959-2006 <td><a href="wipefoot.cgi?http://www.ecmwf.int/research/EU_projects/ENSEMBLES/data/oras3_disclaimer.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
</table>
</form>
EOF

. ./myvinkfoot.cgi
