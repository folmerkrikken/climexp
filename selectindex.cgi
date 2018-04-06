#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./init.cgi
. ./getargs.cgi
# check if a search engine, if so set user to anonymous
. ./searchengine.cgi

. ./myvinkhead.cgi "Select a monthly time series" "Climate indices"

cat <<EOF
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3">Select a time series by clicking on the name
<tr><td>ENSO<td><div class="kalelink">absolute <a href="getindices.cgi?WMO=NCDCData/ersst_nino12a&STATION=NINO12&TYPE=i&id=$EMAIL">NINO12</a>,
<a href="getindices.cgi?WMO=NCDCData/ersst_nino3a&STATION=NINO3&TYPE=i&id=$EMAIL">NINO3</a>,
<a href="getindices.cgi?WMO=NCDCData/ersst_nino3.4a&STATION=NINO3.4&TYPE=i&id=$EMAIL">NINO3.4</a>,  
<a href="getindices.cgi?WMO=NCDCData/ersst_nino4a&STATION=NINO4&TYPE=i&id=$EMAIL">NINO4</a>, relative 
<a href="getindices.cgi?WMO=NCDCData/ersst_nino12a_rel&STATION=NINO12_rel&TYPE=i&id=$EMAIL">NINO12</a>,
<a href="getindices.cgi?WMO=NCDCData/ersst_nino3a_rel&STATION=NINO3_rel&TYPE=i&id=$EMAIL">NINO3</a>,
<a href="getindices.cgi?WMO=NCDCData/ersst_nino3.4a_rel&STATION=NINO3.4_rel&TYPE=i&id=$EMAIL">NINO3.4</a>,
<a href="getindices.cgi?WMO=NCDCData/ersst_nino4a_rel&STATION=NINO4_rel&TYPE=i&id=$EMAIL">NINO4</a>
(1880-now, ERSST v5, relative is relative to 20S-20N, i.e., without global warming, recommended)</div>
<td><a
href="https://www.ncdc.noaa.gov/data-access/marineocean-data/extended-reconstructed-sea-surface-temperature-ersst-v4" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/hadisst1_nino12a&STATION=NINO12&TYPE=i&id=$EMAIL">NINO12</a>,
<a href="getindices.cgi?WMO=UKMOData/hadisst1_nino3a&STATION=NINO3&TYPE=i&id=$EMAIL">NINO3</a>,
<a href="getindices.cgi?WMO=UKMOData/hadisst1_nino3.4a&STATION=NINO3.4&TYPE=i&id=$EMAIL">NINO3.4</a>,
<a href="getindices.cgi?WMO=UKMOData/hadisst1_nino4a&STATION=NINO4&TYPE=i&id=$EMAIL">NINO4</a>
(1870-now, HadISST1)</div>
<td><a
href="http://hadobs.metoffice.gov.uk/hadisst/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/nino2&STATION=NINO12&TYPE=i&id=$EMAIL">NINO12</a>,
<a href="getindices.cgi?WMO=NCEPData/nino3&STATION=NINO3&TYPE=i&id=$EMAIL">NINO3</a>,
<a href="getindices.cgi?WMO=NCEPData/nino5&STATION=NINO3.4&TYPE=i&id=$EMAIL">NINO3.4</a>,
<a href="getindices.cgi?WMO=NCEPData/nino4&STATION=NINO4&TYPE=i&id=$EMAIL">NINO4</a>
(1856-1981 Kaplan, 1982-now NCEP OISSTv2)</div>
<td><a href="http://www.cpc.noaa.gov/data/indices/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CRUData/soi&STATION=SOI&TYPE=i&id=$EMAIL">SOI</a>
(1866-now, Jones)</div>
<td><a href="http://www.cru.uea.ac.uk/cru/data/soi.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_soi&STATION=SOI&TYPE=i&id=$EMAIL">SOI</a>
(1882-now, NCEP)</div>
<td><a href="http://www.cpc.noaa.gov/data/indices/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Precipitation Ni&ntilde;o indices:  <a href="getindices.cgi?WMO=GPCCData/telecon_nino34_gpcc&STATION=Nino34_prcp_land&TYPE=i&id=$EMAIL">GPCC land </a>, <a href="getindices.cgi?WMO=NCEPData/telecon_nino34_cmorph&STATION=Nino34_prcp_sat&TYPE=i&id=$EMAIL">CMORPH satellite</a></div>
<td><a href="help/prcp_nino_indices.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NOAAData/mei&STATION=MEI&TYPE=i&id=$EMAIL">MEI</a>
(1950-now, NOAA/ESRL/PSD)</div>
<td><a href="http://www.cdc.noaa.gov/people/klaus.wolter/MEI/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=TAOData/tao_wwv&STATION=WWV&TYPE=i&id=$EMAIL">Warm Water Volume</a>
(5&deg;S-5&deg;N, 120&deg;E-80&deg;W, 1980-now, PMEL/TAO)</div>
<td><a href="http://www.pmel.noaa.gov/tao/elnino/wwv/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=BMRCData/wwv_poama&STATION=WWV&TYPE=i&id=$EMAIL">WWV</a>
(5&deg;S-5&deg;N, 120&deg;E-80&deg;W, 1960-now, POAMA/PEODAS)</div>
<td><a href="http://poama.bom.gov.au/ocean_monitoring.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_eq_heat300&STATION=eq_heat300&TYPE=i&id=$EMAIL">temperature averaged to 300m</a>
(130&deg;E-80&deg;W, 1979-now, GODAS)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ocean/index/heat_content_index.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>NAO<td><div class="kalelink"><a href="getindices.cgi?WMO=CRUData/nao&STATION=NAO-Gibraltar&TYPE=i&id=$EMAIL">NAO Gibraltar-Stykkisholmur</a> (1821-now, Jones)</div>
<td><a href="http://www.cru.uea.ac.uk/cru/data/nao/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CRUData/nao_ijs_azo&STATION=NAO-Azores&TYPE=i&id=$EMAIL">NAO Azores-Stykkisholmur</a> (1865-2002, data from Jones)</div>
<td><a href="http://www.cru.uea.ac.uk/cru/data/nao.htm"
target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_nao&STATION=CPC_NAO&TYPE=i&id=$EMAIL">NAO</a> (pattern-based, 1950-now, CPC)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/nao.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>SNAO<td><div class="kalelink">Summer NAO from <a href="getindices.cgi?WMO=NCEPNCAR40/snao_ncepncar&STATION=SNAO_ncepncar&TYPE=i&id=$EMAIL">NCEP/NCAR</a> (1948-now), <a href="getindices.cgi?WMO=UCARData/snao_ucar&STATION=SNAO_ucar&TYPE=i&id=$EMAIL">UCAR</a> (1899-now), <a href="getindices.cgi?WMO=20C/snao_20c&STATION=SNAO_20C&TYPE=i&id=$EMAIL">20C</a> (1871-2008) SLP</div>
<td><a href="javascript:pop_page('help/snao.shtml',568,450)" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>AO<td><div class="kalelink"><a href="getindices.cgi?WMO=ColostateData/ao_slp_ext&STATION=AO_SLP&TYPE=i&id=$EMAIL">Arctic Oscillation derived from SLP</a> (1899-2002, Thompson, Colorado State)</div>
<td><a href="http://www.atmos.colostate.edu/ao/Data/ao_index.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_ao&STATION=AO_CPC&TYPE=i&id=$EMAIL">Arctic Oscillation</a> (1950-now, NCEP/CPC)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/ao.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>AMO<td><div class="kalelink">Atlantic Multidecadal Oscillation <a href="getindices.cgi?WMO=UKMOData/amo_hadsst&STATION=AMO_hadsst&TYPE=i&id=$EMAIL">derived from HadSST</a> (1850-now) and <a href="getindices.cgi?WMO=NCDCData/amo_ersst&STATION=AMO_ersst&TYPE=i&id=$EMAIL">derived from ERSST</a> (1880-now) SST 25&deg;-60&deg;N, 7&deg;-75&deg;W minus regression on Tglobal</div>
<td><a href="amo.cgi?id=$EMAIL"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Atlantic Multidecadal Oscillation <a href="getindices.cgi?WMO=UKMOData/amo_hadsst_ts&STATION=AMO_hadsst&TYPE=i&id=$EMAIL">derived from HadSST</a> (1850-now) and <a href="getindices.cgi?WMO=NCDCData/amo_ersst_ts&STATION=AMO_ersst&TYPE=i&id=$EMAIL">derived from ERSST</a> (1880-now) SST EQ-60&deg;N, 0&deg;-80&deg;W minus SST 60&deg;S-60&deg;N </div>
<td><a href="amo.cgi?id=$EMAIL"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Teleconnection patterns<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_ea&STATION=CPC_EA&TYPE=i&id=$EMAIL">East Atlantic</a>, 
<a href="getindices.cgi?WMO=NCEPData/cpc_ea_wr&STATION=CPC_EA/WR&TYPE=i&id=$EMAIL">East
Atlantic/Western Russia</a>,
<a href="getindices.cgi?WMO=NCEPData/cpc_sca&STATION=CPC_SCA&TYPE=i&id=$EMAIL">Scandinavia</a>
and
<a href="getindices.cgi?WMO=NCEPData/cpc_pol&STATION=CPC_POL&TYPE=i&id=$EMAIL">Polar/Eurasia</a>
patterns (1950-now, CPC)</div>
<td> <a
href="http://www.cpc.noaa.gov/data/teledoc/telecontents.shtml"
target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_wp&STATION=CPC_WP&TYPE=i&id=$EMAIL">West
Pacific</a>,
<a href="getindices.cgi?WMO=NCEPData/cpc_epnp&STATION=CPC_EP/NP&TYPE=i&id=$EMAIL">East Pacific/North Pacific</a> patterns (1950-now, CPC)</div>
<td> <a href="http://www.cpc.noaa.gov/data/teledoc/telecontents.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_pna&STATION=CPC_PNA&TYPE=i&id=$EMAIL">Pacific
North American index</a> and <a
href="getindices.cgi?WMO=NCEPData/cpc_tnh&STATION=CPC_TNH&TYPE=i&id=$EMAIL">Tropical/Northern
Hemisphere index</a>, (1950-now, CPC)</div>
<td><a
href="http://www.cpc.noaa.gov/data/teledoc/telecontents.shtml"
target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>IPO<td><div class="kalelink">4-yr time scale, based on <a href="getindices.cgi?WMO=UKMOData/eof_pac_hadsst3_4_01&STATION=IPO_HadSST3_4&TYPE=i&id=$EMAIL">HadSST3</a>, <a href="getindices.cgi?WMO=UKMOData/eof_pac_hadisst1_4_01&STATION=IPO_HadISST1_4&TYPE=i&id=$EMAIL">HadISST1</a>, <a href="getindices.cgi?WMO=NCDCData/eof_pac_ersstv5_4_01&STATION=IPO_HadERSSTv5_4&TYPE=i&id=$EMAIL">ERSSTv5</a></div>
<td><a href="javascript:pop_page('help/ipo.shtml',568,450)" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>PDO<td><div class="kalelink"><a href="getindices.cgi?WMO=UWData/pdo&STATION=PDO&TYPE=i&id=$EMAIL">Pacific Decadal  Oscillation</a> (1900-now, Mantua, U. Washington)</div>
<td><a
href="http://www.atmos.washington.edu/~mantua/abst.PDO.html"
target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UWData/pdo_hadsst3&STATION=PDO_HadSST3&TYPE=i&id=$EMAIL">based on HadSST3</a> (1850-now), <a href="getindices.cgi?WMO=UWData/pdo_ersst&STATION=PDO_ERSST&TYPE=i&id=$EMAIL">based on ERSST</a> (1880-now)</div>
<td>&nbsp;

<!--
<tr><td>IOD/IOZM<td><div class="kalelink"><a href="getindices.cgi?WMO=FRCGCData/dmi_hadisst&STATION=DMI_HadISST&TYPE=i&id=$EMAIL">DMI</a> based on HadISST (1958-2008)</div>
<td><a href="http://www.jamstec.go.jp/frcgc/research/d1/iod/e/iod/about_iod.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
-->
<tr><td>DMI<td><div class="kalelink"><a href="getindices.cgi?WMO=JAMSTECData/dmi&STATION=DMI&TYPE=i&id=$EMAIL">DMI</a>, <a href="getindices.cgi?WMO=JAMSTECData/seio&STATION=SEIO&TYPE=i&id=$EMAIL">SEIO</a>, <a href="getindices.cgi?WMO=JAMSTECData/wio&STATION=WIO&TYPE=i&id=$EMAIL">WIO</a> based on HadISST (1870-now)<!--, home-computed: <a href="getindices.cgi?WMO=UKMOData/hadisst1_siod&STATION=HadISST1_SIOD&TYPE=i&id=$EMAIL">DMI from HadISST1</a>, <a href="getindices.cgi?WMO=NCDCData/siod_ersst&STATION=ERSST_SIOD&TYPE=i&id=$EMAIL">DMI from ERSST</a>--><td><a href="http://www.jamstec.go.jp/frcgc/research/d1/iod/e/iod/about_iod.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/hadisst1_dmi&STATION=DMI_HadISST1&TYPE=i&id=$EMAIL">DMI</a>, <a href="getindices.cgi?WMO=UKMOData/hadisst1_seio&STATION=SEIO_HadISST1&TYPE=i&id=$EMAIL">SEIO</a>, <a href="getindices.cgi?WMO=UKMOData/hadisst1_wtio&STATION=WTIO_HadISST1&TYPE=i&id=$EMAIL">WTIO</a> based on HadISST1</a> (1870-now), <a href="getindices.cgi?WMO=NCDCData/dmi_ersst&STATION=DMI_ERSST&TYPE=i&id=$EMAIL">DMI</a>, <a href="getindices.cgi?WMO=NCDCData/seio_ersst&STATION=SEIO_ERSST&TYPE=i&id=$EMAIL">SEIO</a>, <a href="getindices.cgi?WMO=NCDCData/wtio_ersst&STATION=WTIO_ERSST&TYPE=i&id=$EMAIL">WTIO</a> based on ERSST</a> (1880-now)</div>
<td><a href="http://ioc-goos-oopc.org/state_of_the_ocean/sur/ind/dmi.php" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>MJO<td><div class="kalelink">
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo01_mean12&STATION=MJO_01&TYPE=i&id=$EMAIL">1</a> (80&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo02_mean12&STATION=MJO_02&TYPE=i&id=$EMAIL">2</a> (100&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo03_mean12&STATION=MJO_03&TYPE=i&id=$EMAIL">3</a> (120&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo04_mean12&STATION=MJO_04&TYPE=i&id=$EMAIL">4</a> (140&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo05_mean12&STATION=MJO_05&TYPE=i&id=$EMAIL">5</a> (160&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo06_mean12&STATION=MJO_06&TYPE=i&id=$EMAIL">6</a> (120&deg;W),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo07_mean12&STATION=MJO_07&TYPE=i&id=$EMAIL">7</a> (40&deg;W),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo08_mean12&STATION=MJO_08&TYPE=i&id=$EMAIL">8</a> (10&deg;W),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo09_mean12&STATION=MJO_09&TYPE=i&id=$EMAIL">9</a> (20&deg;E),
<a href="getindices.cgi?WMO=NCEPData/cpc_mjo10_mean12&STATION=MJO_10&TYPE=i&id=$EMAIL">10</a> (70&deg;E)
(1978-now, CPC)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_mjo_index/mjo_index.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>QBO<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPNCAR40/nqbo&STATION=CDC_QBO&TYPE=i&id=$EMAIL">QBO</a> (1958-now, Cathy Smith, CDC)</div>
<td><a href="http://www.cdc.noaa.gov/ClimateIndices/List/#QBO" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">reconstruction at <a href="getindices.cgi?WMO=BernData/qbo_3&STATION=QBO_3&TYPE=i&id=$EMAIL">3</a>, <a href="getindices.cgi?WMO=BernData/qbo_5&STATION=QBO_5&TYPE=i&id=$EMAIL">5</a>, <a href="getindices.cgi?WMO=BernData/qbo_10&STATION=QBO_10&TYPE=i&id=$EMAIL">10</a>, <a href="getindices.cgi?WMO=BernData/qbo_30&STATION=QBO_30&TYPE=i&id=$EMAIL">30</a>, <a href="getindices.cgi?WMO=BernData/qbo_50&STATION=QBO_50&TYPE=i&id=$EMAIL">50</a>, <a href="getindices.cgi?WMO=BernData/qbo_90&STATION=QBO_90&TYPE=i&id=$EMAIL">90</a> hPa (Stefan Br&ouml;nnimann)</div>
<td><a href="http://onlinelibrary.wiley.com/doi/10.1029/2007GL031354/abstract" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>AAO<td><div class="kalelink"><a href="getindices.cgi?WMO=NCEPData/cpc_aao&STATION=CPC_AAO&TYPE=i&id=$EMAIL">Antarctic Oscillation</a> (1979-now, CPC/NCEP)</div>
<td><a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao.shtml" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>SAM<td><div class="kalelink"><a href="getindices.cgi?WMO=BASData/bas_sam&STATION=BAS_SAM&TYPE=i&id=$EMAIL">Southern Annular Mode index</a> (1957-now, BAS)</div>
<tr><td>Mset<td><div class="kalelink"><a href="getindices.cgi?WMO=MBARIData/M1&STATION=M1&TYPE=i&id=$EMAIL">M1</a>, <a href="getindices.cgi?WMO=MBARIData/M2&STATION=M2&TYPE=i&id=$EMAIL">M2</a>, <a href="getindices.cgi?WMO=MBARIData/M3&STATION=M3&TYPE=i&id=$EMAIL">M3</a>, <a href="getindices.cgi?WMO=MBARIData/M4&STATION=M4&TYPE=i&id=$EMAIL">M4</a>, <a href="getindices.cgi?WMO=MBARIData/M5&STATION=M5&TYPE=i&id=$EMAIL">M5</a>, <a href="getindices.cgi?WMO=MBARIData/M6&STATION=M6&TYPE=i&id=$EMAIL">M6</a> 
<td><a href="http://www.mbari.org/bog/GlobalModes/Indices.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Global temperature<td><div class="kalelink">HadCRUT4 <a href="getindices.cgi?WMO=UKMOData/hadcrut4_ns_avg&STATION=HadCRUT4_global_temperature&TYPE=i&id=$EMAIL">Global average temperature</a> (<a href="getindices.cgi?WMO=UKMOData/HadSST3_monthly_globe_ts&STATION=HadSST3_global&TYPE=i&id=$EMAIL">ocean only</a>), <a href="getindices.cgi?WMO=UKMOData/hadcrut4_nh&STATION=HadCRUT4_NH&TYPE=i&id=$EMAIL">northern hemisphere</a> (<a href="getindices.cgi?WMO=UKMOData/HadSST3_monthly_nh_ts&STATION=HadSST3_nh&TYPE=i&id=$EMAIL">ocean only</a>), <a href="getindices.cgi?WMO=UKMOData/hadcrut4_sh&STATION=HadCRUT4_SH&TYPE=i&id=$EMAIL">southern hemisphere</a> (<a href="getindices.cgi?WMO=UKMOData/HadSST3_monthly_sh_ts&STATION=HadSST3_sh&TYPE=i&id=$EMAIL">ocean only</a>), <a href="getindices.cgi?WMO=UKMOData/hadcrut4_30S_30N&STATION=HadCRUT4_30S-30N&TYPE=i&id=$EMAIL">tropics</a> (<a href="getindices.cgi?WMO=UKMOData/HadSST3_monthly_tropics_ts&STATION=HadSST3_tropics&TYPE=i&id=$EMAIL">ocean only</a>) (1850-now Hadley Centre)</div>
<td><a href="http://www.metoffice.gov.uk/hadobs/hadcrut4/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><td><div class="kalelink">CRUTEM4 <a href="getindices.cgi?WMO=UKMOData/crutem4_ns&STATION=CRUTEM4_land_temperature&TYPE=i&id=$EMAIL">global land temperature</a> (1850-now CRU / Hadley Centre)</div>
<td><a href="http://www.metoffice.gov.uk/hadobs/crutem4/data/diagnostics/global/nh+sh/index.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">HadCRUT4 <a href="getindices.cgi?WMO=UKMOData/hadcrut4_ns_avg_%%&STATION=HadCRUT4_global_temperature&TYPE=i&id=$EMAIL">Global average temperature ensemble</a>, <a href="getindices.cgi?WMO=UKMOData/hadcrut4_nh_%%&STATION=HadCRUT4_NH&TYPE=i&id=$EMAIL">northern hemisphere ensemble</a>, <a href="getindices.cgi?WMO=UKMOData/hadcrut4_sh_%%&STATION=HadCRUT4_SH&TYPE=i&id=$EMAIL">southern hemisphere ensemble</a>, <a href="getindices.cgi?WMO=UKMOData/hadcrut4_30S_30N_%%&STATION=HadCRUT4_30S-30N&TYPE=i&id=$EMAIL">tropics ensemble</a> (1850-now Hadley Centre)</div>
<td><a href="http://www.metoffice.gov.uk/hadobs/hadcrut4/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NASAData/giss_al_gl_m&STATION=GISS_global_temperature&TYPE=i&id=$EMAIL">Land-Ocean average temperature</a> (<a href="getindices.cgi?WMO=NASAData/giss_sea&STATION=GISS_ocean_temperature&TYPE=i&id=$EMAIL">ocean only</a>), <a href="getindices.cgi?WMO=NASAData/giss_al_nh_m&STATION=GISS_NH_temperature&TYPE=i&id=$EMAIL">northern hemisphere</a>, <a href="getindices.cgi?WMO=NASAData/giss_al_sh_m&STATION=GISS_SH_temperature&TYPE=i&id=$EMAIL">southern hemisphere</a> (1880-now, NASA/GISS Ts+dSST)</div>
<td><a href="http://data.giss.nasa.gov/gistemp/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NCDCData/ncdc_gl&STATION=NCDC_global_temperature&TYPE=i&id=$EMAIL">Global average temperature</a> (<a href="getindices.cgi?WMO=NCDCData/ncdc_gl_land&STATION=NCDC_global_land_temperature&TYPE=i&id=$EMAIL">land</a>, <a href="getindices.cgi?WMO=NCDCData/ncdc_gl_ocean&STATION=NCDC_global_ocean_temperature&TYPE=i&id=$EMAIL">ocean</a>), (1880-now, NOAA/NCEI)</div>
<td><a href="https://www.ncdc.noaa.gov/cag/global/time-series" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<!--
<tr><td>&nbsp;<td><div class="kalelink">ERA-interim T2m <a href="getindices.cgi?WMO=ERA-interim/erai_t2m_gl&STATION=ERA_global_t2m&TYPE=i&id=$EMAIL">global</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2m_land&STATION=ERA_land_t2m&TYPE=i&id=$EMAIL">land</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2m_sea&STATION=ERA_sea_t2m&TYPE=i&id=$EMAIL">sea</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2m_nh&STATION=ERA_nh_t2m&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2m_sh&STATION=ERA_sh_t2m&TYPE=i&id=$EMAIL">SH</a> T2m  (1979-now)</div>
<td><a href="http://apps.ecmwf.int/datasets/data/interim_full_moda/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
-->

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=YorkData/had4_krig_v2_0_0&STATION=CowtanWay_global_temperature&TYPE=i&id=$EMAIL">HadCRUT4 filled in with kriging</a> (1850-now, Cowtan and Way)</div>
<td><a href="http://www-users.york.ac.uk/~kdc3/papers/coverage2013/series.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">1850-now <a href="getindices.cgi?WMO=BerkeleyData/t2m_land_ocean_best&STATION=Berkeley_land_ocean_temperature&TYPE=i&id=$EMAIL">Land-ocean temperature</a>, 1750-now <a href="getindices.cgi?WMO=BerkeleyData/t2m_land_best&STATION=Berkeley_land_temperature&TYPE=i&id=$EMAIL">land temperature</a> Berkeley</div>
<td><a href="http://www.berkeleyearth.org" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<!--
<tr><td>&nbsp;<td><div class="kalelink">ERA-interim T2m/SST <a href="getindices.cgi?WMO=ERA-interim/erai_t2msst_gl&STATION=ERA_global_t2msst&TYPE=i&id=$EMAIL">global</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2msst_land&STATION=ERA_land_t2msst&TYPE=i&id=$EMAIL">land</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2msst_sea&STATION=ERA_sea_t2msst&TYPE=i&id=$EMAIL">sea</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2msst_nh&STATION=ERA_nh_t2msst&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=ERA-interim/erai_t2msst_sh&STATION=ERA_sh_t2msst&TYPE=i&id=$EMAIL">SH</a> T2m  (1979-now)</div>
<td><a href="http://apps.ecmwf.int/datasets/data/interim_full_moda/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
-->

<tr><td>Lower troposphere temperature<td><div class="kalelink"><a href="getindices.cgi?WMO=UAHData/tlt_gl&STATION=TLT&TYPE=i&id=$EMAIL">Global</a>, <a href="getindices.cgi?WMO=UAHData/tlt_nh&STATION=TLT_NH&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=UAHData/tlt_sh&STATION=TLT_SH&TYPE=i&id=$EMAIL">SH</a>, <a href="getindices.cgi?WMO=UAHData/tlt_land&STATION=TLT_land&TYPE=i&id=$EMAIL">land</a>, <a href="getindices.cgi?WMO=UAHData/tlt_sea&STATION=TLT_sea&TYPE=i&id=$EMAIL">sea</a> anomalies (1979-now, UAH v6.0beta3)</div>
<td><a href="http://www.atmos.uah.edu/data/msu/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Ocean heat content<td><div class="kalelink">0-700m: <a href="getindices.cgi?WMO=NODCData/heat700_global&STATION=global_upper_ocean_heat_content&TYPE=i&id=$EMAIL">Global upper ocean</a> (<a href="getindices.cgi?WMO=NODCData/heat700_nh&STATION=NH_upper_ocean_heat_content&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=NODCData/heat700_sh&STATION=SH_upper_ocean_heat_content&TYPE=i&id=$EMAIL">SH</a>),
<a href="getindices.cgi?WMO=NODCData/heat700_Atlantic&STATION=Atlantic_Ocean_heat_content&TYPE=i&id=$EMAIL">Atlantic</a> (<a href="getindices.cgi?WMO=NODCData/heat700_North_Atlantic&STATION=North_Atlantic_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat700_South_Atlantic&STATION=South_Atlantic_heat_content&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/heat700_Indian&STATION=Indian_Ocean_heat_content&TYPE=i&id=$EMAIL">Indian</a> (<a href="getindices.cgi?WMO=NODCData/heat700_North_Indian&STATION=North_Indian_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat700_South_Indian&STATION=South_Indian_heat_content&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/heat700_Pacific&STATION=Pacific_Ocean_heat_content&TYPE=i&id=$EMAIL">Pacific</a> (<a href="getindices.cgi?WMO=NODCData/heat700_North_Pacific&STATION=North_Pacific_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat700_South_Pacific&STATION=South_Pacific_heat_content&TYPE=i&id=$EMAIL">S</a>),
(1955-now, NODC)<br>
0-2000m: <a href="getindices.cgi?WMO=NODCData/heat2000_global&STATION=global_upper_ocean_heat_content&TYPE=i&id=$EMAIL">Global upper ocean</a> (<a href="getindices.cgi?WMO=NODCData/heat2000_nh&STATION=NH_upper_ocean_heat_content&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=NODCData/heat2000_sh&STATION=SH_upper_ocean_heat_content&TYPE=i&id=$EMAIL">SH</a>),
<a href="getindices.cgi?WMO=NODCData/heat2000_Atlantic&STATION=Atlantic_Ocean_heat_content&TYPE=i&id=$EMAIL">Atlantic</a> (<a href="getindices.cgi?WMO=NODCData/heat2000_North_Atlantic&STATION=North_Atlantic_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat2000_South_Atlantic&STATION=South_Atlantic_heat_content&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/heat2000_Indian&STATION=Indian_Ocean_heat_content&TYPE=i&id=$EMAIL">Indian</a> (<a href="getindices.cgi?WMO=NODCData/heat2000_North_Indian&STATION=North_Indian_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat2000_South_Indian&STATION=South_Indian_heat_content&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/heat2000_Pacific&STATION=Pacific_Ocean_heat_content&TYPE=i&id=$EMAIL">Pacific</a> (<a href="getindices.cgi?WMO=NODCData/heat2000_North_Pacific&STATION=North_Pacific_heat_content&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/heat2000_South_Pacific&STATION=South_Pacific_heat_content&TYPE=i&id=$EMAIL">S</a>),
(2005-now, NODC)</div>
<td><a href="http://www.nodc.noaa.gov/OC5/3M%5fHEAT%5fCONTENT/basin%5fdata.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--Ocean heat content--><td><div class="kalelink"><a href="getindices.cgi?WMO=TAOData/pmel_ohc700&STATION=PMEL_global_upper_ocean_heat_content&TYPE=i&id=$EMAIL&NPERYEAR=1">global upper ocean heat content</a> (0-700m, 1993-now, PMEL)</div>
<td><a href="http://oceans.pmel.noaa.gov/Data/OHCA_700.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Ocean mean temperature<td><div class="kalelink">0-100m: <a href="getindices.cgi?WMO=NODCData/temp100_global&STATION=global_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">Global upper ocean</a> (<a href="getindices.cgi?WMO=NODCData/temp100_nh&STATION=NH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=NODCData/temp100_sh&STATION=SH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">SH</a>),
<a href="getindices.cgi?WMO=NODCData/temp100_Atlantic&STATION=Atlantic_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Atlantic</a> (<a href="getindices.cgi?WMO=NODCData/temp100_North_Atlantic&STATION=North_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp100_South_Atlantic&STATION=South_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp100_Indian&STATION=Indian_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Indian</a> (<a href="getindices.cgi?WMO=NODCData/temp100_North_Indian&STATION=North_Indian_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp100_South_Indian&STATION=South_Indian_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp100_Pacific&STATION=Pacific_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Pacific</a> (<a href="getindices.cgi?WMO=NODCData/temp100_North_Pacific&STATION=North_Pacific_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp100_South_Pacific&STATION=South_Pacific_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
(1955-now, NODC)<br>
0-700m: <a href="getindices.cgi?WMO=NODCData/temp700_global&STATION=global_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">Global upper ocean</a> (<a href="getindices.cgi?WMO=NODCData/temp700_nh&STATION=NH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=NODCData/temp700_sh&STATION=SH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">SH</a>),
<a href="getindices.cgi?WMO=NODCData/temp700_Atlantic&STATION=Atlantic_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Atlantic</a> (<a href="getindices.cgi?WMO=NODCData/temp700_North_Atlantic&STATION=North_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp700_South_Atlantic&STATION=South_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp700_Indian&STATION=Indian_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Indian</a> (<a href="getindices.cgi?WMO=NODCData/temp700_North_Indian&STATION=North_Indian_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp700_South_Indian&STATION=South_Indian_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp700_Pacific&STATION=Pacific_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Pacific</a> (<a href="getindices.cgi?WMO=NODCData/temp700_North_Pacific&STATION=North_Pacific_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp700_South_Pacific&STATION=South_Pacific_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
(1955-now, NODC)<br>
0-2000m: <a href="getindices.cgi?WMO=NODCData/temp2000_global&STATION=global_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">Global upper ocean</a> (<a href="getindices.cgi?WMO=NODCData/temp2000_nh&STATION=NH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">NH</a>, <a href="getindices.cgi?WMO=NODCData/temp2000_sh&STATION=SH_upper_ocean_mean_temperature&TYPE=i&id=$EMAIL">SH</a>),
<a href="getindices.cgi?WMO=NODCData/temp2000_Atlantic&STATION=Atlantic_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Atlantic</a> (<a href="getindices.cgi?WMO=NODCData/temp2000_North_Atlantic&STATION=North_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp2000_South_Atlantic&STATION=South_Atlantic_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp2000_Indian&STATION=Indian_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Indian</a> (<a href="getindices.cgi?WMO=NODCData/temp2000_North_Indian&STATION=North_Indian_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp2000_South_Indian&STATION=South_Indian_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
<a href="getindices.cgi?WMO=NODCData/temp2000_Pacific&STATION=Pacific_Ocean_mean_temperature&TYPE=i&id=$EMAIL">Pacific</a> (<a href="getindices.cgi?WMO=NODCData/temp2000_North_Pacific&STATION=North_Pacific_mean_temperature&TYPE=i&id=$EMAIL">N</a>, <a href="getindices.cgi?WMO=NODCData/temp2000_South_Pacific&STATION=South_Pacific_mean_temperature&TYPE=i&id=$EMAIL">S</a>),
(2005-now, NODC)</div>
<td><a href="http://www.nodc.noaa.gov/OC5/3M%5ftemp%5fCONTENT/basin%5fdata.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sea level<td><div class="kalelink"><a href="getindices.cgi?WMO=AVISOData/ssh_aviso&STATION=global_sea_level&TYPE=i&id=$EMAIL">Global sea level</a> from altimetry. (1993-now, AVISO)</div></a>
<td><a href="https://www.aviso.altimetry.fr/en/data/products/ocean-indicators-products/mean-sea-level/products-images.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--Sea level--><td><div class="kalelink"><a href="getindices.cgi?WMO=SiegenData/ssh_dangendorf&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">Global sea level reconstruction</a> (1902-2012, Dangendorf et al, <a href="getindices.cgi?WMO=SiegenData/dssh_dangendorf&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">uncertainty</a>), <a href="getindices.cgi?WMO=SiegenData/ssh_dangendorf_extended&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">extended with AVISO</a></div></a>
<td><a href="http://www.pnas.org/content/114/23/5946.abstract" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<!--
<tr><td><td><div class="kalelink"><a href="getindices.cgi?WMO=HarvardData/ssh_hay&STATION=global_sea_level&TYPE=i&id=$EMAIL">Global sea level reconstruction</a> (1900-2012, Hay et al), <a href="getindices.cgi?WMO=HarvardData/ssh_hay_extended&STATION=global_sea_level&TYPE=i&id=$EMAIL">extended with AVISO</a> (1900-now)</div></a>
<td><a href="http://www.nature.com/nature/journal/v517/n7535/full/nature14093.html?foxtrotcallback=true" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
-->

<tr><td><!--Sea level--><td><div class="kalelink"><a href="getindices.cgi?WMO=CSIROData/ssh_church&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">Global sea level reconstruction</a> (1880-2013, Church and White, <a href="getindices.cgi?WMO=CSIROData/dssh_church&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">uncertainty</a>), <a href="getindices.cgi?WMO=CSIROData/ssh_church_extended&STATION=global_sea_level&TYPE=i&NPERYEAR=1&id=$EMAIL">extended with AVISO</a></div></a>
<td><a href="https://link.springer.com/article/10.1007/s10712-011-9119-1" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--
Sea level--><td><div class="kalelink"><a href="getindices.cgi?WMO=CUData/sl_global&STATION=global_sea_level&TYPE=i&id=$EMAIL">Global sea level</a>, <a href="getsealevelave.cgi?id=$EMAIL&WHERE=ocean">oceans</a>, <a href="getsealevelave.cgi?id=$EMAIL&WHERE=sea">seas</a> from altimetry. Same with inverse barometer correction: <a href="getindices.cgi?WMO=CUData/sl_ib_global&STATION=global_sea_level&TYPE=i&id=$EMAIL">global sea level</a>, <a href="getsealevelave.cgi?id=$EMAIL&WHERE=ocean_ib">oceans</a>, <a href="getsealevelave.cgi?id=$EMAIL&WHERE=sea_ib">seas</a> (1993-now, University of Colorado)</div><a name="cudata"></a>
<td><a href="http://sealevel.colorado.edu/results.php" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--Sea level--><td><div class="kalelink"><a href="getindices.cgi?WMO=PSMSLData/gsl&STATION=global_coastal_sea_level&TYPE=i&id=$EMAIL">Global coastal sea level</a> (<a href="getindices.cgi?WMO=PSMSLData/gsl_err&STATION=global_sea_level_error&TYPE=i&id=$EMAIL">error</a>), <a href="getindices.cgi?WMO=PSMSLData/gsl_rate&STATION=global_sea_level_rate&TYPE=i&id=$EMAIL">rate of change</a> (<a href="getindices.cgi?WMO=PSMSLData/gsl_rate_err&STATION=global_sea_level_rate_error&TYPE=i&id=$EMAIL">error</a>) (1807-2002, PSMSL)</div>
<td><a href="http://www.pol.ac.uk/psmsl/author_archive/jevrejeva_etal_gsl//" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Radiation<td><div class="kalelink"><a href="getindices.cgi?WMO=CDIACData/maunaloa_f&STATION=Mauna_Loa_CO2&TYPE=i&id=$EMAIL">Mauna Loa CO<sub>2</sub> concentrations</a> (1958-now, NOAA), <a href="getindices.cgi?WMO=CDIACData/maunaloa_log&STATION=log_Mauna_Loa_CO2&TYPE=i&id=$EMAIL">logarithm</a></div>
<td><a href="http://www.esrl.noaa.gov/gmd/ccgg/trends/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CDIACData/co2&STATION=CO2&TYPE=i&id=$EMAIL">Global marine CO<sub>2</sub> concentrations</a> (1980-now, NOAA), <a href="getindices.cgi?WMO=CDIACData/co2_monthly&STATION=CO2&TYPE=i&id=$EMAIL">annual mean 0001-now</a>, <a href="getindices.cgi?WMO=CDIACData/co2_log&STATION=log_CO2&TYPE=i&id=$EMAIL">logarithm</a></div>
<td><a href="http://www.esrl.noaa.gov/gmd/ccgg/trends/index.html#global" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CDIACData/ch4_monthly&STATION=CH4&TYPE=i&id=$EMAIL">Global marine CH<sub>4</sub> concentrations</a> (1983-now, NOAA), <a href="getindices.cgi?WMO=CDIACData/ch4_annual&STATION=CH4&TYPE=i&id=$EMAIL&NPERYEAR=1">annual mean 0001-now</a></div>
<td><a href="http://www.esrl.noaa.gov/gmd/ccgg/trends/index.html#global" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">CMIP5 historical &amp; RCP2.6 <a href="getindices.cgi?WMO=CDIACData/RCP3PD_CO2&STATION=historical/RCP3PD_CO2&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP3PD_CH4&STATION=historical/RCP3PD_CH4&TYPE=i&&NPERYEAR=1&id=$EMAIL">CH<sub>4</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP3PD_KYOTO-CO2EQ&STATION=historical/RCP3PD_KYOTO-CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP3PD_CO2EQ&STATION=historical/RCP3PD_CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>, logarithm of <a href="getindices.cgi?WMO=CDIACData/RCP3PD_CO2_log&STATION=historical/RCP3PD_CO2_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP3PD_KYOTO-CO2EQ_log&STATION=historical/RCP3PD_KYOTO-CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP3PD_CO2EQ_log&STATION=historical/RCP3PD_CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>  (1765-2300, IIASA)</div>
<td><a href="http://www.iiasa.ac.at/web-apps/tnt/RcpDb/dsd?Action=htmlpage&page=download" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">CMIP5 historical &amp; RCP4.5 <a href="getindices.cgi?WMO=CDIACData/RCP45_CO2&STATION=historical/RCP45_CO2&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP45_CH4&STATION=historical/RCP45_CH4&TYPE=i&&NPERYEAR=1&id=$EMAIL">CH<sub>4</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP45_KYOTO-CO2EQ&STATION=historical/RCP45_KYOTO-CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP45_CO2EQ&STATION=historical/RCP45_CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>, logarithm of <a href="getindices.cgi?WMO=CDIACData/RCP45_CO2_log&STATION=historical/RCP45_CO2_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP45_KYOTO-CO2EQ_log&STATION=historical/RCP45_KYOTO-CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP45_CO2EQ_log&STATION=historical/RCP45_CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>  (1765-2300, IIASA)</div>
<td><a href="http://www.iiasa.ac.at/web-apps/tnt/RcpDb/dsd?Action=htmlpage&page=download" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">CMIP5 historical &amp; RCP6.0 <a href="getindices.cgi?WMO=CDIACData/RCP6_CO2&STATION=historical/RCP6_CO2&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP6_CH4&STATION=historical/RCP6_CH4&TYPE=i&&NPERYEAR=1&id=$EMAIL">CH<sub>4</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP6_KYOTO-CO2EQ&STATION=historical/RCP6_KYOTO-CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP6_CO2EQ&STATION=historical/RCP6_CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>, logarithm of <a href="getindices.cgi?WMO=CDIACData/RCP6_CO2_log&STATION=historical/RCP6_CO2_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP6_KYOTO-CO2EQ_log&STATION=historical/RCP6_KYOTO-CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP6_CO2EQ_log&STATION=historical/RCP6_CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>  (1765-2300, IIASA)</div>
<td><a href="http://www.iiasa.ac.at/web-apps/tnt/RcpDb/dsd?Action=htmlpage&page=download" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">CMIP5 historical &amp; RCP8.5 <a href="getindices.cgi?WMO=CDIACData/RCP85_CO2&STATION=historical/RCP85_CO2&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP85_CH4&STATION=historical/RCP85_CH4&TYPE=i&&NPERYEAR=1&id=$EMAIL">CH<sub>4</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP85_KYOTO-CO2EQ&STATION=historical/RCP85_KYOTO-CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP85_CO2EQ&STATION=historical/RCP85_CO2EQ&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>, logarithm of <a href="getindices.cgi?WMO=CDIACData/RCP85_CO2_log&STATION=historical/RCP85_CO2_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">CO<sub>2</sub></a>, <a href="getindices.cgi?WMO=CDIACData/RCP85_KYOTO-CO2EQ_log&STATION=historical/RCP85_KYOTO-CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG</a>, <a href="getindices.cgi?WMO=CDIACData/RCP85_CO2EQ_log&STATION=historical/RCP85_CO2EQ_log&TYPE=i&&NPERYEAR=1&id=$EMAIL">GHG+aerosols</a>  (1765-2300, IIASA)</div>
<td><a href="http://www.iiasa.ac.at/web-apps/tnt/RcpDb/dsd?Action=htmlpage&page=download" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">SRES <a href="getindices.cgi?WMO=CDIACData/A1B&STATION=A1B&TYPE=i&id=$EMAIL&NPERYEAR=1">A1B</a>, <a href="getindices.cgi?WMO=CDIACData/A1B&STATION=A1B&TYPE=i&id=$EMAIL&NPERYEAR=1">A1B</a>, <a href="getindices.cgi?WMO=CDIACData/A1FI&STATION=A1FI&TYPE=i&id=$EMAIL&NPERYEAR=1">A1FI</a>, <a href="getindices.cgi?WMO=CDIACData/A2&STATION=A2&TYPE=i&id=$EMAIL&NPERYEAR=1">A2</a>, <a href="getindices.cgi?WMO=CDIACData/B1&STATION=B1&TYPE=i&id=$EMAIL&NPERYEAR=1">B1</a>, <a href="getindices.cgi?WMO=CDIACData/B2&STATION=B2&TYPE=i&id=$EMAIL&NPERYEAR=1">B2</a>, <a href="getindices.cgi?WMO=CDIACData/sres%%&STATION=SRES&TYPE=i&id=$EMAIL&NPERYEAR=1">combined</a> scenarios (1850-2100, IPCC)</div>
<td><a href="http://www.ipcc-data.org/ancilliary/tar-isam.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Global <a href="getindices.cgi?WMO=CDIACData/global_co2_fossil&STATION=CO2_fossil&TYPE=i&NPERYEAR=1&id=$EMAIL">fossil fuel</a>, <a href="getindices.cgi?WMO=CDIACData/global_co2_landuse&STATION=CO2_landuse&TYPE=i&NPERYEAR=1&id=$EMAIL">land use</a>, <a href="getindices.cgi?WMO=CDIACData/global_co2_emissions&STATION=CO2_emissions&TYPE=i&NPERYEAR=1&id=$EMAIL">total CO2 emissions</a>, <a href="getindices.cgi?WMO=CDIACData/cum_global_co2_emissions&STATION=cum_CO2_emissions&TYPE=i&NPERYEAR=1&id=$EMAIL">cumulative</a></div>
<td><a href="http://www.globalcarbonproject.org/carbonbudget/17/data.htm" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>


<tr><td>&nbsp;<td><div class="kalelink">Global <a href="getindices.cgi?WMO=NASAData/saod_gl&STATION=stratospheric_AOD&TYPE=i&id=$EMAIL">stratospheric aerosol optical depth</a> due to volcanic eruptions, <a href="getindices.cgi?WMO=NASAData/saod_nh&STATION=stratospheric_AOD_NH&TYPE=i&id=$EMAIL">NH</a>,<a href="getindices.cgi?WMO=NASAData/saod_sh&STATION=stratospheric_AOD_SH&TYPE=i&id=$EMAIL">SH</a> (1850-now, NASA/GISS)</div>
<td><a href="http://data.giss.nasa.gov/modelforce/strataer/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sun<td><div class="kalelink"><a href="getindices.cgi?WMO=PMODData/tsi&STATION=measured_total_solar_irradiance&TYPE=i&id=$EMAIL">Measured total solar irradiance</a> (1978-now, WRC/PMOD)</div>
<td><a href="http://www.pmodwrc.ch/pmod.php?topic=tsi/composite/SolarConstant" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<!--
<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/solarconstanths&STATION=Hoyt&Schatten_reconstructed_solar_constant&TYPE=i&id=$EMAIL">Reconstructed solar constant</a> (1680-1992 yearly, Hoyt and Schatten)</div>
<td>&nbsp;
-->

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CUData/TSI_TIM_Reconstruction&STATION=reconstructed_solar_constant&TYPE=i&id=$EMAIL&NPERYEAR=1">Annual reconstructed solar constant</a> (1610-2013) 
<td><a href="http://lasp.colorado.edu/home/sorce/data/tsi-data/#historical_TSI" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Lean <a href="getindices.cgi?WMO=NCDCData/tsi_ncdc_yearly&STATION=reconstructed_tsi&TYPE=i&id=$EMAIL&NPERYEAR=1">annual</a> (1610-now), <a href="getindices.cgi?WMO=NCDCData/tsi_ncdc_monthly&STATION=reconstructed_tsi&TYPE=i&id=$EMAIL">monthly</a> (1882-now) reconstructed total solar irradiance</a>
<td><a href="https://www.ncdc.noaa.gov/cdr/atmospheric/total-solar-irradiance" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=SIDCData/sunspots&STATION=sunspots&TYPE=i&id=$EMAIL">Sunspots</a> (1749-now, SIDC)</a></div>
<td><a href="http://sidc.oma.be/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=SRMPData/solarradioflux&STATION=solar_radio_flux&TYPE=i&id=$EMAIL">Solar radio flux</a> (1947-now, DRAO)</div>
<td><a href="http://www.drao-ofr.hia-iha.nrc-cnrc.gc.ca/icarus/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Annual <a href="getindices.cgi?WMO=RALData/osf&STATION=open_solar_flux&TYPE=i&id=$EMAIL&NPERYEAR=1">reconstructed open solar flux</a> (1675-2010),  <a href="getindices.cgi?WMO=RALData/osf_obs&STATION=open_solar_flux&TYPE=i&id=$EMAIL&NPERYEAR=1">observed open solar flux</a> (1967-2010), Lockwood</div>
<td><a href="http://www.eiscat.rl.ac.uk/Members/mike/Open%20solar%20flux%20data/openflux1675to2010.txt" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Rotation<td><div class="kalelink"><a href="getindices.cgi?WMO=IERSData/lod_12&STATION=length_of_day&TYPE=i&id=$EMAIL">Length Of Day</a> (1962-now, IERS)</div>
<td><a href="http://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<!--
<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=ASUData/mld&STATION=maximum_lunar_declination&TYPE=i&id=$EMAIL">Maximum Lunar Declination</a>
(1900-1996, Randall. S. Cerveny)</div>
-->

<tr><td>Tropical cyclones<td><div class="kalelink">Number of <a href="getindices.cgi?WMO=AOMLData/landsea_ns&STATION=Number_of_named_storms_(Atl)&TYPE=i&id=$EMAIL">named storms</a>, <a href="getindices.cgi?WMO=AOMLData/landsea_ih&STATION=Number_of_intense_hurricanes_(Atl)&TYPE=i&id=$EMAIL">intense hurricanes</a> per season over the North Atlantic (1944-2008, Landsea plus FAQ</a>)</div>
<td><a href="http://www.aoml.noaa.gov/hrd/Landsea/predAtl/table.html#table1" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a><br><a href="http://www.aoml.noaa.gov/hrd/tcfaq/tcfaqF.html#F3" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<a name="hurricanes"></a>
<tr><td>&nbsp;<td><div class="kalelink">Annual number of hurricanes over the Atlantic
<a href="getindices.cgi?WMO=GFDLData/hurdat_count&STATION=N.Atlantic_hurricanes&TYPE=i&id=$EMAIL&NPERYEAR=1">observed</a>,
<a href="getindices.cgi?WMO=GFDLData/hurdat_count_adj&STATION=adjusted_N.Atlantic_hurricanes&TYPE=i&id=$EMAIL&NPERYEAR=1">adjusted</a>
(1878-2008, Gabe Vecchi)</div>
<td><a href="http://www.gfdl.noaa.gov/cms-filesystem-action/user_files/gav/publications/vk10_hurrrecount.pdf" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>
<tr><td>&nbsp;<td><div class="kalelink">Annual hurricane days over the Atlantic
<a href="getindices.cgi?WMO=GFDLData/hurdat_hurday&STATION=N.Atlantic_hurricane_days&TYPE=i&id=$EMAIL&NPERYEAR=1">observed</a>,
<a href="getindices.cgi?WMO=GFDLData/hurdat_hurday_adj&STATION=adjusted_N.Atlantic_hurricane_days&TYPE=i&id=$EMAIL&NPERYEAR=1">adjusted</a>
(1878-2008, Gabe Vecchi)</div>
<td><a href="http://www.gfdl.noaa.gov/cms-filesystem-action/user_files/gav/publications/vk10_hurrrecount.pdf" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Number of tropical storms over the
<a href="getindices.cgi?WMO=MITData/tsat&STATION=TS_Atlantic&TYPE=i&id=$EMAIL">Atlantic</a>,
<a href="getindices.cgi?WMO=MITData/tswp&STATION=TS_West_Pacific&TYPE=i&id=$EMAIL">West Pacific</a>,
<a href="getindices.cgi?WMO=MITData/tsep&STATION=TS_East_Pacific&TYPE=i&id=$EMAIL">East Pacific</a>,
<a href="getindices.cgi?WMO=MITData/tsio&STATION=TS_Indian&TYPE=i&id=$EMAIL">Indian</a> Ocean, 
<a href="getindices.cgi?WMO=MITData/tssh&STATION=TS_Southern_Hemisphere&TYPE=i&id=$EMAIL">Southern Hemisphere</a> and
<a href="getindices.cgi?WMO=MITData/ts&STATION=TS_world&TYPE=i&id=$EMAIL">whole world</a>
(1851-2008, Kerry Emanual)</div>
<td><a href="http://wind.mit.edu/~emanuel/home.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Number of tropical cyclones (cat 1-5) over the
<a href="getindices.cgi?WMO=MITData/tcat&STATION=TC_Atlantic&TYPE=i&id=$EMAIL">Atlantic</a>,
<a href="getindices.cgi?WMO=MITData/tcwp&STATION=TC_West_Pacific&TYPE=i&id=$EMAIL">West Pacific</a>,
<a href="getindices.cgi?WMO=MITData/tcep&STATION=TC_East_Pacific&TYPE=i&id=$EMAIL">East Pacific</a>,
<a href="getindices.cgi?WMO=MITData/tcio&STATION=TC_Indian&TYPE=i&id=$EMAIL">Indian</a> Ocean,
<a href="getindices.cgi?WMO=MITData/tcsh&STATION=TC_Southern_Hemisphere&TYPE=i&id=$EMAIL">Southern Hemisphere</a> and
<a href="getindices.cgi?WMO=MITData/tc&STATION=TC_world&TYPE=i&id=$EMAIL">whole world</a>
(1851-2008, Kerry Emanual)</div>
<td><a href="http://wind.mit.edu/~emanuel/home.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Number of severe tropical cyclones (cat 3-5) over the
<a href="getindices.cgi?WMO=MITData/ssat&STATION=cat3-5_Atlantic&TYPE=i&id=$EMAIL">Atlantic</a>,
<a href="getindices.cgi?WMO=MITData/sswp&STATION=cat3-5_West_Pacific&TYPE=i&id=$EMAIL">West Pacific</a>,
<a href="getindices.cgi?WMO=MITData/ssep&STATION=cat3-5_East_Pacific&TYPE=i&id=$EMAIL">East Pacific</a>,
<a href="getindices.cgi?WMO=MITData/ssio&STATION=cat3-5_Indian&TYPE=i&id=$EMAIL">Indian</a> Ocean,
<a href="getindices.cgi?WMO=MITData/sssh&STATION=cat3-5_Southern_Hemisphere&TYPE=i&id=$EMAIL">Southern Hemisphere</a> and
<a href="getindices.cgi?WMO=MITData/ss&STATION=cat3-5_world&TYPE=i&id=$EMAIL">whole world</a>
(1851-2008, Kerry Emanual)</div>
<td><a href="http://wind.mit.edu/~emanuel/home.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Number of very severe tropical cyclones (cat 4-5) over the
<a href="getindices.cgi?WMO=MITData/vsat&STATION=cat45_Atlantic&TYPE=i&id=$EMAIL">Atlantic</a>,
<a href="getindices.cgi?WMO=MITData/vswp&STATION=cat45_West_Pacific&TYPE=i&id=$EMAIL">West Pacific</a>,
<a href="getindices.cgi?WMO=MITData/vsep&STATION=cat45_East_Pacific&TYPE=i&id=$EMAIL">East Pacific</a>,
<a href="getindices.cgi?WMO=MITData/vsio&STATION=cat45_Indian&TYPE=i&id=$EMAIL">Indian</a> Ocean,
<a href="getindices.cgi?WMO=MITData/vssh&STATION=cat45_Southern_Hemisphere&TYPE=i&id=$EMAIL">Southern Hemisphere</a> and
<a href="getindices.cgi?WMO=MITData/vs&STATION=cat45_world&TYPE=i&id=$EMAIL">whole world</a>
(1851-2008, Kerry Emanual)</div>
<td><a href="http://wind.mit.edu/~emanuel/home.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Tropical Accumulated Cyclone Energy (ACE): <a href="getindices.cgi?WMO=WXData/ace_natl&STATION=ace_atl&TYPE=i&id=$EMAIL">North Atlantic</a>, <a href="getindices.cgi?WMO=WXData/ace_wpac&STATION=ace_wpac&TYPE=i&id=$EMAIL">West Pacific</a>, <a href="getindices.cgi?WMO=WXData/ace_nepac&STATION=ace_nepac&TYPE=i&id=$EMAIL">Northeast Pacific</a>, <a href="getindices.cgi?WMO=WXData/ace_nio&STATION=ace_nio&TYPE=i&id=$EMAIL">North Indian Ocean</a>, <a href="getindices.cgi?WMO=WXData/ace_nh&STATION=ace_nh&TYPE=i&id=$EMAIL">Northern Hemisphere</a>, <a href="getindices.cgi?WMO=WXData/ace_sh&STATION=ace_sh&TYPE=i&id=$EMAIL">Southern Hemisphere</a>, <a href="getindices.cgi?WMO=WXData/ace_global&STATION=ace_global&TYPE=i&id=$EMAIL">Global</a> (1970-now, Ryan Maue)</div>
<td><a href="http://wx.graphics/tropical/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">Atlantic basin monthly <a href="getindices.cgi?WMO=CSUData/atlantic_monthly_ace&STATION=atl_ace&TYPE=i&id=$EMAIL">Accumulated Cyclone Energy Index</a>, <a href="getindices.cgi?WMO=CSUData/atlantic_monthly_ntc&STATION=atl_ntc&TYPE=i&id=$EMAIL">Net Tropical Cyclone Activity</a>, annual <a href="getindices.cgi?WMO=CSUData/atlantic_annual_ace&STATION=annual_atl_ace&TYPE=i&id=$EMAIL">ACE</a>, <a href="getindices.cgi?WMO=CSUData/atlantic_annual_ntc&STATION=annual_atl_ntc&TYPE=i&id=$EMAIL">NTC</a> (1851-2016, Phil Klotzbach)</div>
<td>&nbsp;

<tr><td>Snow cover</td><td><div class="kalelink"><a href="getindices.cgi?WMO=RutgersData/nh_snow&STATION=NH_snow_cover&TYPE=i&id=$EMAIL">Northern Hemisphere</a>, <a href="getindices.cgi?WMO=RutgersData/eurasia_snow&STATION=Eurasia_snow_cover&TYPE=i&id=$EMAIL">Eurasia</a>, <a href="getindices.cgi?WMO=RutgersData/namerica_snow&STATION=North_America_snow_cover&TYPE=i&id=$EMAIL">North America</a>, <a href="getindices.cgi?WMO=RutgersData/namerica2_snow&STATION=North_America_without_Greenland_snow_cover&TYPE=i&id=$EMAIL">North America without Greenland</a> snow cover (1966-now, Rutgers University)</td><td><a href="http://climate.rutgers.edu/snowcover/table_area.php?ui_set=2" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sea ice</td><td><div class="kalelink"><a href="getindices.cgi?WMO=NSIDCData/N_ice_area&STATION=NH_seaice_area&TYPE=i&id=$EMAIL">NH area</a>, <a href="getindices.cgi?WMO=NSIDCData/N_ice_extent&STATION=NH_seaice_extent&TYPE=i&id=$EMAIL">NH extent</a>, <a href="getindices.cgi?WMO=NSIDCData/S_ice_area&STATION=SH_seaice_area&TYPE=i&id=$EMAIL">SH area</a>, <a href="getindices.cgi?WMO=NSIDCData/S_ice_extent&STATION=SH_seaice_extent&TYPE=i&id=$EMAIL">SH extent</a> (1978-now, NSIDC)</td><td><a href="http://nsidc.org/data/g02135.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;</td><td><div class="kalelink">PIOMAS <a href="getindices.cgi?WMO=UWData/piomas_mo&STATION=NH_seaice_volume&TYPE=i&id=$EMAIL">NH volume</a> (1979-now, U Washington PSC)</td><td><a href="http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Land ice</td><td><div class="kalelink">GRACE <a href="getindices.cgi?WMO=GRACEData/data_grs&STATION=Greenland_mass&TYPE=i&id=$EMAIL">Greenland</a>, <a href="getindices.cgi?WMO=GRACEData/data_ant&STATION=Antarctica_mass&TYPE=i&id=$EMAIL">Antarctica</a> mass changes,  (2003-2013, TU Delft)</td><td>&nbsp;</a>

<tr><td>India<td><div class="kalelink"><a href="getindices.cgi?WMO=IITMData/ALLIN&STATION=All-India_Rainfall&TYPE=p&id=$EMAIL">All-India Rainfall</a> (1871-2014, 29 subdivision, 2880000 km2, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=IITMData/HOMIN&STATION=Homogeneous_India_RAINFALL&TYPE=p&id=$EMAIL">Homogeneous India Rainfall</a> (1871-2014, 14 subdivisions, 1596970 km2, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=IITMData/CORIN&STATION=Core-Monsoon_India_Rainfall&TYPE=p&id=$EMAIL">Core-Monsoon India Rainfall</a> (1871-1999, 7 subdivisions, 776942 km2, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindia.cgi?id=$EMAIL&where=region&type=p">Indian rainfall per region</a> (<a href="IITMData/ismreg.png" target="_new">map</a>, 1871-2014, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindia.cgi?id=$EMAIL&where=subdiv&type=p">Indian rainfall per subdivision</a> (<a href="IITMData/india-subdiv-rev1.png" target="_new">map</a>, 1871-2014, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindia.cgi?id=$EMAIL&where=region&type=n">Indian minimum temperature per region</a> (1871-2007, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindia.cgi?id=$EMAIL&where=region&type=x">Indian maximum temperature per region</a> (1871-2007, IITM)</div>
<td><a href="http://www.tropmet.res.in" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink">yearly <a href="getindices.cgi?WMO=LDGOData/AIR&STATION=All_India_Rainfall&TYPE=p&id=$EMAIL">All India Rainfall</a> (1813-1998, LDGO archive)</div>
<td><a href="http://ingrid.ldgo.columbia.edu/SOURCES/.Indices/.india/rainfall/?help&STATION=datafiles" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Indonesia<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/Konnen/jakarta_raindays&STATION=Jakarta_Raindays&TYPE=p&id=$EMAIL">Jakarta Rain Days</a> (1829-1997, KNMI)</div>
<td><a href="http://www.knmi.nl/publicaties/abstract.php?id=744" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Switzerland<td><div class="kalelink"><a href="getindices.cgi?WMO=BernData/ch_temp&STATION=Swiss_reconstruction&TYPE=t&id=$EMAIL">Temperature</a>, <a href="getindices.cgi?WMO=BernData/ch_prec&STATION=Swiss_reconstruction&TYPE=p&id=$EMAIL">precipitation</a> reconstruction (1525-1989, Pfister)</div>
<td><a href="http://www.ncdc.noaa.gov/paleo/historical.html" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=MeteoSwissData/swiss_swiss&STATION=Swissmean&TYPE=t&id=$EMAIL">Swissmean</a>, <a href="getindices.cgi?WMO=MeteoSwissData/swiss_north.low&STATION=Swiss_north_low&TYPE=t&id=$EMAIL">North low</a>, <a href="getindices.cgi?WMO=MeteoSwissData/swiss_north.high&STATION=Swiss_north_high&TYPE=t&id=$EMAIL">North high</a>, <a href="getindices.cgi?WMO=MeteoSwissData/swiss_south&STATION=Swiss_south&TYPE=t&id=$EMAIL">South</a>, (1864-now, MeteoSwiss) (<a href="getindices.cgi?WMO=KNMIData/cnt&STATION=CNT_v1.0&TYPE=t&id=$EMAIL">v1.0</a>)</div>
<td><a href="http://www.meteoswiss.admin.ch/home/climate/present-day/climate-trends/data-on-the-swiss-temperature-mean-since-1864.html"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>United Kingdom<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/cet&STATION=Central_England_Temperature&TYPE=t&id=$EMAIL">Central England Temperature</a> (1659-now),
<a href="getindices.cgi?WMO=UKMOData/cet_min&STATION=Central_England_min_temperature&TYPE=t&id=$EMAIL">minimum</a> (1878-now),
<a href="getindices.cgi?WMO=UKMOData/cet_max&STATION=Central_England_max_temperature&TYPE=t&id=$EMAIL">maximum</a> (1878-now,
Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadcet" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/HadEWP_monthly_qc&STATION=England-Wales&TYPE=p&id=$EMAIL">England &amp; Wales Precipitation</a> (1766-now),
<a href="getindices.cgi?WMO=UKMOData/HadSP_monthly_qc&STATION=Scotland&TYPE=p&id=$EMAIL">Scotland Precipitation</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNIP_monthly_qc&STATION=Northern_Ireland&TYPE=p&id=$EMAIL">Northern Ireland Precipitation</a> (1931-now, Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadukp" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=UKMOData/HadSEEP_monthly_qc&STATION=SE_England&TYPE=p&id=$EMAIL">Southeast England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadSWEP_monthly_qc&STATION=SW_England&TYPE=p&id=$EMAIL">Southwest England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadCEP_monthly_qc&STATION=Central_England&TYPE=p&id=$EMAIL">Central England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNEEP_monthly_qc&STATION=NE_England&TYPE=p&id=$EMAIL">Northeast England</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNWEP_monthly_qc&STATION=NW_England&TYPE=p&id=$EMAIL">Northwest England</a> (1873-now),
<a href="getindices.cgi?WMO=UKMOData/HadSSP_monthly_qc&STATION=S_Scotland&TYPE=p&id=$EMAIL">Southern Scotland</a>,
<a href="getindices.cgi?WMO=UKMOData/HadESP_monthly_qc&STATION=E_Scotland&TYPE=p&id=$EMAIL">Eastern Scotland</a>,
<a href="getindices.cgi?WMO=UKMOData/HadNSP_monthly_qc&STATION=N_Scotland&TYPE=p&id=$EMAIL">Northern Scotland</a> precipitation</a> (1931-now, Hadley Centre)</div>
<td><a href="http://hadobs.metoffice.gov.uk/hadukp" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Island of Ireland<td><div class="kalelink"><a href="getindices.cgi?WMO=MUData/prcp_ireland&STATION=Island_of_Ireland_rainfall&TYPE=p&id=$EMAIL">Island of Ireland rainfall</a> (1711-now, Maynooth University)</div><td><a href="https://doi.pangaea.de/10.1594/PANGAEA.887593"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Sweden<td><div class="kalelink">Haparanda homogenised <a href="getindices.cgi?WMO=MainzData/Haparanda_MeanTemperature_corr_ext&STATION=TG_Haparanda&TYPE=t&id=$EMAIL">mean</a>, <a href="getindices.cgi?WMO=MainzData/Haparanda_MinimumTemperature_corr_ext&STATION=TN_Haparanda&TYPE=t&id=$EMAIL">minimum</a>, <a href="getindices.cgi?WMO=MainzData/Haparanda_MaximumTemperature_corr_ext&STATION=TX_Haparanda&TYPE=t&id=$EMAIL">maximum</a> temperature (1859-2014 U Mainz, 2015-now ECAD)</div><td><a href="MainzData/Dienst_et_al-2017-International_Journal_of_Climatology.pdf"><img src="images/info-i.gif" alt="more information" border="0"></a>


<tr><td>Netherlands<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/cnt_v11&STATION=CNT&TYPE=t&id=$EMAIL">Central Netherlands Temperature</a> (1906-now, KNMI) (<a href="getindices.cgi?WMO=KNMIData/cnt&STATION=CNT_v1.0&TYPE=t&id=$EMAIL">v1.0</a>)</div>
<td><a href="http://www.knmi.nl/publications/fulltexts/CNT.pdf"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getdutchstations.cgi?id=$EMAIL&TYPE=temp_hom">Homogenised Dutch temperatures</a> (10 stations, 1906-now, KNMI)</div>
<td><a href="http://www.knmi.nl/publications/fulltexts/CNT.pdf"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/Tdebilt_hom&STATION=Tg_Debilt_homogenized&TYPE=t&id=$EMAIL">Homogenized monthly mean temperature in De Bilt</a> (1901-now, KNMI)</div>
<td><a href="KNMIData/Tg_De_Bilt_homogenized.html"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/labrijn&STATION=Tdebilt&TYPE=i&id=$EMAIL">Temperature in De Bilt, the Netherlands</a> (1706-now, van Engelen &amp; Nellestijn)</div>
<td><a href="http://www.knmi.nl/klimatologie/daggegevens/antieke_wrn/index.html"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/elfsteden&STATION=Elfstedentochten&TYPE=i&id=$EMAIL">Elfstedentochten</a> (1901-2008, KNMI)</div>
<td><a href="http://www.knmi.nl/voorl/nader/icefrl.htm"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=WURData/BVnootjes&STATION=beechnuts&TYPE=i&id=$EMAIL">beech nuts</a> (1930-1967), <a href="getindices.cgi?WMO=WURData/HPnootjes&STATION=beechcrop&TYPE=i&id=$EMAIL">beech crop</a> (1930-1996)</div>
<td>&nbsp;

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=CBSData/windex&STATION=windex&TYPE=i&id=$EMAIL&NPERYEAR=4">Windex</a> (2002-now) index for wind energy</div>
<td><a href="http://statline.cbs.nl/StatWeb/publication/default.aspx?DM=SLNL&PA=70802ned&D1=5&D2=1&D3=3%2c7%2c11%2c15%2c20%2c24%2c28%2c32%2c37%2c41%2c45%2c49%2c54%2c58%2c62%2c66%2c71%2c75%2c79%2c83%2c88%2c92%2c96%2c100%2c105%2c109%2c113%2c117-118%2c122%2c126%2c130%2c134-152%2c156%2c160%2c164%2c168-169%2c173%2c177%2c181%2c185-186%2cl&HDR=T%2cG1&STB=G2&CHARTTYPE=1&VW=D"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Currents<td><div class="kalelink"><a href="getindices.cgi?WMO=AOMLData/FC_monthly&STATION=Florida_Current&TYPE=i&id=$EMAIL">Strength of the Florida Current</a> (1982-now, Florida Current Project)</div>
<td><a href="http://www.aoml.noaa.gov/phod/floridacurrent/"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td><!--Currents-->&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=NOCData/moc_mar_hc10_mon&STATION=AMOC_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">AMOC transport at 26.5&deg;N</a>, <a href="getindices.cgi?WMO=NOCData/t_umo10_mon&STATION=Upper_Mid-Ocean_Transport_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">upper mid-ocean transport</a>, <a href="getindices.cgi?WMO=NOCData/t_gs10_mon&STATION=Florida_Straits_Transport&TYPE=i&id=$EMAIL&NPERYEAR=366">Florida Straits transport</a>, <a href="getindices.cgi?WMO=NOCData/t_ek10_mon&STATION=Ekman_Transport_26N&TYPE=i&id=$EMAIL&NPERYEAR=366">Ekman transport</a> (2004-now, Rapid)</div>
<td><a href="http://www.rapid.ac.uk/rapidmoc" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Time<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/time12&STATION=time&TYPE=i&id=$EMAIL">Time</a> (to investigate the time-behaviour of fields)</div>
<td><a href="http://http://en.wikipedia.org/wiki/Coordinated_Universal_Time"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="getindices.cgi?WMO=KNMIData/leap&STATION=leap&TYPE=i&id=$EMAIL">difference between civic date and tropical date</a> (spurious trends in spring and autumn)</div>
<td><a href="http://http://en.wikipedia.org/wiki/Coordinated_Universal_Time"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>Noise<td><div class="kalelink"><form action="ar1.cgi" method="POST">Red noise: 
<input type="hidden" name="email" value="$EMAIL">
<input type="hidden" name="NPERYEAR" value="12">
Y(mo,yr) = white gaussian noise + 
<input type="text" class="forminput" name="a1" size="6" value="0.0">Y(mo-1,yr) +
<input type="text" class="forminput" name="a2" size="6" value="0.0">Y(mo,yr-1)
<input type="submit" class="formbutton" value="make noise">
</form>
<td>

<tr><td>Models<td><div class="kalelink"><a href="ecmwf_indices.cgi?id=$EMAIL">ENSO, NAO indices</a> (1981-about now, operational seasonal forecasts)</div>
<td>&nbsp;

<tr><td>&nbsp;<td><div class="kalelink"><a href="demeter_nino.cgi?id=$EMAIL">ENSO indices</a> (1958-2001, DEMETER seasonal hindcasts)</div>
<td><a href="http://www.ecmwf.int/research/demeter/" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="essence_indices.cgi?id=$EMAIL">ENSO, global mean temperature, MOC Indices</a> (1950-2100, ESSENCE climate change experiments)</div>
<td><a href="http://www.knmi.nl/~sterl/Essence/"><img src="images/info-i.gif" alt="more information" border="0"></a>

<tr><td>&nbsp;<td><div class="kalelink"><a href="cmip5_indices.cgi?id=$EMAIL">CMIP5 global mean temperature</a></div>
<td><a href="?http://cmip-pcmdi.llnl.gov/cmip5/data_getting_started.html"><img src="images/info-i.gif" alt="more information" border="0"></a>

</table>
If you have time series that you would like to add to the list contact <a href="mailto:oldenborgh@knmi.nl">me</a>.
EOF

. ./myvinkfoot.cgi

