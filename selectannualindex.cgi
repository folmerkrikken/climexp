#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
# check if a search engine, if so set user to anonymous
. ./searchengine.cgi

. ./myvinkhead.cgi "Select an annual time series" "Annual climate reconstructions"

cat <<EOF
Please note that many of these time series have been derived from (very) indirect data and have large uncertainties. The Climate Explorer cannot currently represent the uncertainty margins, please consult the documentation of the time series to obtain these. You are encouraged to compare a few reconstructions of the same quantity and compare with instrumental data on the overlap period.
<p>
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3">Select a time series by clicking on the name

<tr><td>ENSO<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/enso_li&STATION=Li_ENSO&TYPE=i&id=$EMAIL&NPERYEAR=1">1,100 Year El Ni&ntilde;o/Southern Oscillation (ENSO) Index Reconstruction</a> (900-2002, Li et al 2011)</div>
<td><a href="ftp://ftp.ncdc.noaa.gov/pub/data/paleo/treering/reconstructions/enso-li2011.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/nino3_mann&STATION=Mann_Nino3&TYPE=i&id=$EMAIL&NPERYEAR=1">Ni&ntilde;o3 Reconstruction</a> (500-2006, Mann et al 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/mann2009b/mann2009b.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>NAO<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/nao_trouet&STATION=Trouet_NAO&TYPE=i&id=$EMAIL&NPERYEAR=1">Multidecadal winter NAO reconstruction</a> (1049-1995, Trouet 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/trouet2009/trouet2009.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>PDO<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/pdo_macdonald&STATION=MacDonald_PDO&TYPE=i&id=$EMAIL&NPERYEAR=1">Pacific Decadal Oscillation Reconstruction for the Past Millennium</a> (993-1996, MacDonald&amp;Case 2005)</div>
<td><a href="ftp://ftp.ncdc.noaa.gov/pub/data/paleo/treering/reconstructions/pdo-macdonald2005.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/pdo_mann&STATION=Mann_PDO&TYPE=i&id=$EMAIL&NPERYEAR=1">PDO Reconstruction</a> (500-2006, Mann et al 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/mann2009b/mann2009b.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>AMO<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/amo_mann&STATION=Mann_AMO&TYPE=i&id=$EMAIL&NPERYEAR=1">AMO Reconstruction</a> (500-2006, Mann et al 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/mann2009b/mann2009b.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Temperature<td><div class="kalelink"><a href="getindices.cgi?WMO=WDCPData/moberg2005&STATION=Moberg_NH_temp&TYPE=i&id=$EMAIL&NPERYEAR=1">Moberg Northern Hemsiphere temperature</a> (1-1979, Moberg 2005)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/moberg2005/moberg2005.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/nh_mann&STATION=Mann_NH_temperature&TYPE=i&id=$EMAIL&NPERYEAR=1">NH Temperature Reconstruction</a> (500-2006, Mann et al 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/mann2009b/mann2009b.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/sst_mann&STATION=Mann_global_SST&TYPE=i&id=$EMAIL&NPERYEAR=1">Global SST Reconstruction</a> (500-2006, Mann et al 2009)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/pubs/mann2009b/mann2009b.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<a name="buisman"></a><td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/nederland_djf&STATION=Tnetherlands_DJF&TYPE=i&id=$EMAIL&NPERYEAR=1">Winter</a>, <a  href="getindices.cgi?WMO=KNMIData/nederland_jja&STATION=Tnetherlands_JJA&TYPE=i&id=$EMAIL&NPERYEAR=1">summer</a> and <a href="getindices.cgi?WMO=KNMIData/nederland_yr&STATION=Tnetherlands&TYPE=i&id=$EMAIL&NPERYEAR=1">annual mean</a> temperature in the Netherlands</a> (753-2000, v. Engelen, Buisman, IJnsen)</div>
<td><a href="http://www.knmi.nl/klimatologie/daggegevens/antieke_wrn/index.html"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>Sea level<td><div class="kalelink"><a href="getindices.cgi?WMO=PSMSLData/gsl_ann&STATION=global_sea_level&TYPE=i&id=$EMAIL&NPERYEAR=1">Global sea level</a> (<a href="getindices.cgi?WMO=PSMSLData/gsl_ann_err&STATION=global_sea_level_error&TYPE=i&id=$EMAIL&NPERYEAR=1">error</a>) (1700-2002, PSMSL)</div>
<td><a href="http://www.pol.ac.uk/psmsl/author_archive/jevrejeva_etal_1700/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Radiation<td><div class="kalelink"><a href="getindices.cgi?WMO=CDIACData/co2_annual&STATION=CO2&TYPE=i&id=$EMAIL&NPERYEAR=1">CO<sub>2</sub> concentration 1000-now</a>, <a href="getindices.cgi?WMO=CDIACData/co2_log&STATION=log_CO2&TYPE=i&id=$EMAIL&NPERYEAR=1">logarithm</a></div>
<td><a href="http://www.esrl.noaa.gov/gmd/ccgg/trends/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sun<td><div class="kalelink"><a href="getindices.cgi?WMO=FUBData/tsi_wls_ann&STATION=reconstructed_solar_constant&TYPE=i&id=$EMAIL&NPERYEAR=1">Reconstructed solar constant</a> (1610-2008, FUB) 
<td><a href="http://www.geo.fu-berlin.de/en/met/ag/strat/forschung/SOLARIS/Input_data/CMIP5_solar_irradiance.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=RALData/osf&STATION=open_solar_flux&TYPE=i&id=$EMAIL&NPERYEAR=1">Reconstructed open solar flux</a> (1675-2010, Lockwood)</div>
<td><a href="http://www.eiscat.rl.ac.uk/Members/mike/Open%20solar%20flux%20data/openflux1675to2010.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Drought<td><div class="kalelink"><a href="getindices.cgi?WMO=RapidData/dai&STATION=Western_US_Drought_Index&TYPE=i&id=$EMAIL&NPERYEAR=1">Western US Drought Index</a> (800-2003, Cook et al, 2004)</div>
<td><a href="ftp://ftp.ncdc.noaa.gov/pub/data/paleo/drought/pdsi2004/readme-pdsi-na2004.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>


</table>
If you have time series that you would like to add to the list contact <a href="mailto:oldenborgh@knmi.nl">me</a>.
EOF

. ./myvinkfoot.cgi

