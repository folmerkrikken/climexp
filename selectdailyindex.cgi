#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./searchengine.cgi

DIR=`pwd`
base_url=`dirname $SCRIPT_NAME`

. ./myvinkhead.cgi "Select a daily time series" "Climate indices" "index,follow"
cat <<EOF
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3">Select a time series by clicking on the name
<tr><td>ENSO<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/nino12_daily&STATION=NINO12&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO12</a>, <a href="getindices.cgi?WMO=NCEPData/nino3_daily&STATION=NINO3&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO3</a>, <a href="getindices.cgi?WMO=NCEPData/nino34_daily&STATION=NINO3.4&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO3.4</a>, <a href="getindices.cgi?WMO=NCEPData/nino4_daily&STATION=NINO4&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO4</a> (1981-now, from daily SST OI v2)</div>
<td><a href="http://www.cpc.noaa.gov/data/indices/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/nino12_weekly&STATION=NINO12&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO12</a>, <a href="getindices.cgi?WMO=NCEPData/nino3_weekly&STATION=NINO3&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO3</a>, <a href="getindices.cgi?WMO=NCEPData/nino34_weekly&STATION=NINO3.4&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO3.4</a>, <a href="getindices.cgi?WMO=NCEPData/nino4_weekly&STATION=NINO4&TYPE=i&id=$EMAIL&NPERYEAR=366">NINO4</a> (1990-now, from weekly SST OI v2)</div>
<td><a href="http://www.cpc.noaa.gov/data/indices/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Circulation<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_nao_daily&STATION=NAO&TYPE=i&id=$EMAIL&NPERYEAR=366">NAO</a>, <a href="getindices.cgi?WMO=NCEPData/cpc_ao_daily&STATION=AO&TYPE=i&id=$EMAIL&NPERYEAR=366">AO</a>, <a href="getindices.cgi?WMO=NCEPData/cpc_pna_daily&STATION=PNA&TYPE=i&id=$EMAIL&NPERYEAR=366">PNA</a>, <a href="getindices.cgi?WMO=NCEPData/cpc_aao_daily&STATION=AAO&TYPE=i&id=$EMAIL&NPERYEAR=366">AAO</a> (1950-now, CPC)</div>
<td><a href="http://www.cpc.noaa.gov/products/precip/CWlink/daily_ao_index/teleconnections.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>MJO indices<td><div class="kalelink"><a href="getindices.cgi?WMO=BMRCData/rmm1&STATION=RMM1&TYPE=i&id=$EMAIL&NPERYEAR=366">RMM1</a> and <a href="getindices.cgi?WMO=BMRCData/rmm2&STATION=RMM2&TYPE=i&id=$EMAIL&NPERYEAR=366">RMM2</a> (1974-now, BMRC)</div>
<td><a href="http://www.bom.gov.au/bmrc/clfor/cfstaff/matw/maproom/RMM/index.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_mjo01_daily&STATION=MJO_01&TYPE=i&id=$EMAIL&NPERYEAR=366">1</a> (80&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo02_daily&STATION=MJO_02&TYPE=i&id=$EMAIL&NPERYEAR=366">2</a> (100&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo03_daily&STATION=MJO_03&TYPE=i&id=$EMAIL&NPERYEAR=366">3</a> (120&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo04_daily&STATION=MJO_04&TYPE=i&id=$EMAIL&NPERYEAR=366">4</a> (140&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo05_daily&STATION=MJO_05&TYPE=i&id=$EMAIL&NPERYEAR=366">5</a> (160&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo06_daily&STATION=MJO_06&TYPE=i&id=$EMAIL&NPERYEAR=366">6</a> (120&deg;W), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo07_daily&STATION=MJO_07&TYPE=i&id=$EMAIL&NPERYEAR=366">7</a> (40&deg;W), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo08_daily&STATION=MJO_08&TYPE=i&id=$EMAIL&NPERYEAR=366">8</a> (10&deg;W), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo09_daily&STATION=MJO_09&TYPE=i&id=$EMAIL&NPERYEAR=366">9</a> (20&deg;E), <a href="getindices.cgi?WMO=NCEPData/cpc_mjo10_daily&STATION=MJO_10&TYPE=i&id=$EMAIL&NPERYEAR=366">10</a> (70&deg;E) (1978-now, interpolated from 5-daily, NCEP/CPC)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily\_mjo\_index/mjo\_index.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Monsoon<td><div class="kalelink"><a href="getindices.cgi?WMO=SoestData/wnpmidx&STATION=WNPMI&TYPE=i&id=$EMAIL&NPERYEAR=366">Western North Pacific Monsoon Index</a> (1948-2008)</div><td><a href="http://iprc.soest.hawaii.edu/users/ykaji/monsoon/realtime-monidx.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Radiation<td><div class="kalelink"><a href="getindices.cgi?WMO=PMODData/solarconstant_daily&STATION=measured_solar_constant&TYPE=i&id=$EMAIL&NPERYEAR=366">Measured solar constant</a> (1978-now, WRC/PMOD)</div>
<td><a href="http://www.pmodwrc.ch/pmod.php?topic=tsi/composite/SolarConstant" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sun<td><div class="kalelink"><a href="getindices.cgi?WMO=SIDCData/sunspots_daily&STATION=sunspots&TYPE=i&id=$EMAIL&NPERYEAR=366">Sunspot number</a> (1818-now, SIDC)</div>
<td><a href="http://sidc.oma.be/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Weekday<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/week&STATION=week&TYPE=i&id=$EMAIL">(1 on Mon-Fri, 0 on Sat-Sun)</a> or <a href="getindices.cgi?WMO=KNMIData/oldweek&STATION=oldweek&TYPE=i&id=$EMAIL">(1 on Mon-Sat, 0 on Sun)</a>, </div>
<td>

<tr><td>Rotation<td><div class="kalelink"><a href="getindices.cgi?WMO=IERSData/lod&STATION=lenth_of_day&TYPE=i&id=$EMAIL&NPERYEAR=366">Length Of Day</a> (1962-now, IERS)</div>
<td><a href="http://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Currents<td><div class="kalelink"><a href="getindices.cgi?WMO=AOMLData/FC_daily&STATION=Florida_Current&TYPE=i&id=$EMAIL&NPERYEAR=366">Strength of the Florida Current [Sv]</a> (1982-now, Florida  Current Project)</div>
<td><a href="http://www.aoml.noaa.gov/phod/floridacurrent/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--Currents-->&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NOCData/moc_mar_hc10_day&STATION=AMOC_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">AMOC transport at 26.5&deg;N</a>, <a href="getindices.cgi?WMO=NOCData/t_umo10_day&STATION=Upper_Mid-Ocean_Transport_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">upper mid-ocean transport</a>, <a href="getindices.cgi?WMO=NOCData/t_gs10_day&STATION=Florida_Straits_Transport&TYPE=i&id=$EMAIL&NPERYEAR=366">Florida Straits transport</a>, <a href="getindices.cgi?WMO=NOCData/t_ek10_day&STATION=Ekman_Transport_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">Ekman transport</a> (2004-now, Rapid)</div>
<td><a href="http://www.rapid.ac.uk/rapidmoc/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>UK temperatures<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/daily_cet&STATION=Central_England_Temperature&TYPE=t&id=$EMAIL&NPERYEAR=366">Central England Temperature</a> (1772-now),
<a href="getindices.cgi?WMO=UKMOData/daily_cet_min&STATION=Central_England_min_temperature&TYPE=t&id=$EMAIL&NPERYEAR=366">minimum</a> (1878-now),
<a href="getindices.cgi?WMO=UKMOData/daily_cet_max&STATION=Central_England_max_temperature&TYPE=t&id=$EMAIL&NPERYEAR=366">maximum</a> (1878-now, Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadcet" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>


<tr><td>UK precipitation<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/HadEWP_daily_qc&STATION=England-Wales&TYPE=p&id=$EMAIL&NPERYEAR=366">England &amp; Wales Precipitation</a>,
<a href="getindices.cgi?WMO=UKMOData/HadSP_daily_qc&STATION=Scotland&TYPE=p&id=$EMAIL&NPERYEAR=366">Scotland Precipitation</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNIP_daily_qc&STATION=Northern_Ireland&TYPE=p&id=$EMAIL&NPERYEAR=366">Northern Ireland Precipitation</a> (1931-now, Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadukp" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/HadSEEP_daily_qc&STATION=SE_England&TYPE=p&id=$EMAIL&NPERYEAR=366">Southeast England</a>, <a href="getindices.cgi?WMO=UKMOData/HadSWEP_daily_qc&STATION=SW_England&TYPE=p&id=$EMAIL&NPERYEAR=366">Southwest England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadCEP_daily_qc&STATION=Central_England&TYPE=p&id=$EMAIL&NPERYEAR=366">Central England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNEEP_daily_qc&STATION=NE_England&TYPE=p&id=$EMAIL&NPERYEAR=366">Northeast England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNWEP_daily_qc&STATION=NW_England&TYPE=p&id=$EMAIL&NPERYEAR=366">Northwest England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadSSP_daily_qc&STATION=S_Scotland&TYPE=p&id=$EMAIL&NPERYEAR=366">Southern Scotland</a>,
<a href="getindices.cgi?WMO=UKMOData/HadESP_daily_qc&STATION=E_Scotland&TYPE=p&id=$EMAIL&NPERYEAR=366">Eastern Scotland</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNSP_daily_qc&STATION=N_Scotland&TYPE=p&id=$EMAIL&NPERYEAR=366">Northern Scotland</a> precipitation</a> (1931-now, Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadukp" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Netherlands precipitation<td><div class="kalelink"><a href="PhomNL.cgi?id=$EMAIL">Moved to a separate page</a> (1906-now, KNMI)</div>
<td><a href="http://www.knmi.nl/klimatologie/daggegevens/nsl-download.cgi?language=eng" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Noise<td><div class="kalelink"><form action="ar1.cgi" method="POST">Red noise: 
<input type="hidden" name="email" value="$EMAIL">
<input type="hidden" name="NPERYEAR" value="366">
Y(dy,yr) = white gaussian noise + 
<input type="text" class="forminput" name="a1" size="6" value="0.0">Y(dy-1,yr) +
<input type="text" class="forminput" name="a2" size="6" value="0.0">Y(dy,yr-1)
<input type="submit" class="formbutton" value="make noise">
</form>
<td>

</table>
EOF

. ./myvinkfoot.cgi
