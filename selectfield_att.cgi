#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Attribution runs" "index,nofollow"

cat <<EOF
<div class="kalelink">
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="14"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
<tr><th>EC-Earth 2.3
<th>scenario
<th>tas
<th>tas<br>min
<th>tas<br>max
<th>pr
<th>evsp<br>sbl
<th>pme
<th>ssr
<th>uas
<th>vas
<th>psl
<tr><td>daily
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_tas_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tasmin_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tasmax_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_pr_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_evspsbl_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_pme_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_ssr_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_uas_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_vas_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_psl_Aday_ECEARTH23_rcp85>
<tr><td>monthly
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_tas_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tasmin_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tasmax_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_pr_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_evspsbl_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_pme_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_ssr_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_uas_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_vas_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_psl_Amon_ECEARTH23_rcp85>
<tr><th>&nbsp;
<th>&nbsp;
<th>Rx1day
<th>Rx3day
<th>Rx5day
<th>Txx
<th>Txn
<th>Tnx
<th>Tnn
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<tr><td>annual
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_rx1day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_rx3day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_rx5day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_txx_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_txn_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tnx_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tnn_yr_ECEARTH23_rcp85>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><th>HadGEM3A N216<br><a href="EUCLEIA/HadGEM3-A-N216/eucleia_conditions.pdf">conditions</a>
<th>SST forcing
<th>&nbsp;
<th>tas<br>min
<th>tas<br>max
<th>pr
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>psl
<tr><td>daily
<td>historical
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Aday_HadGEM3-A-N216_historical>
<tr><td>daily
<td>historicalNat
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Aday_HadGEM3-A-N216_historicalNat>
<tr><th>&nbsp;
<th>&nbsp;
<th>Rx1day
<th>Rx3day
<th>Rx5day
<th>Txx
<th>Txn
<th>Tnx
<th>Tnn
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<tr><td>annual
<td>historical
<td><input type=radio class=formradio name=field value=eucleia_rx1day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txx_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txn_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnx_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnn_yr_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><td>annual
<td>historicalNat
<td><input type=radio class=formradio name=field value=eucleia_rx1day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txx_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txn_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnx_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnn_yr_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
</table>
</form>
<div class=alineakop>EC-Earth 2.3 monthly series</div>
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_su_%%&STATION=Tglobal_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">Global mean temperature</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_5lan_su_%%&STATION=Tland_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">land only</a>.
<br><a href="getindices.cgi?WMO=KNMI14Data/Nino/nino34_%%%&STATION=EC-Earth23_Nino3.4&TYPE=i&NPERYEAR=12&id=$EMAIL">Ni&ntilde;o3.4 (detrended)</a>,

<div class=alineakop>EC-Earth 2.3 daily series</div>
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tas_day_ECEARTH23_rcp85_%%_18600101-21001231_52N_5E&STATION=Tdebilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/ttasmax_muladdcorr_ydrun_retrend_%%&STATION=Tmax_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmax De Bilt bias-corrected</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5.2E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5.2&deg;E</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Pcumbria/pr_day_ECEARTH23_rcp85_%%_18600101-21001231_NEngland&STATION=P_NEngland_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Northern England</a>,
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Loire_su_%%&STATION=P_Loire_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Loire basin</a>.
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Seine_su_%%&STATION=P_Seine_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Seine basin</a>.

<div class=alineakop>HadGEM3A N216 historical daily series</div>
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historical_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_obs&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>,
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Loire_su_%%%&STATION=P_Loire_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Seine_su_%%%&STATION=P_Seine_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Seine basin</a>,

<div class=alineakop>HadGEM3A N216 historicalNat daily series</div>
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historicalNat_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_nat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>.
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historicalNat_Loire_su_%%%&STATION=P_Loire_HadGEM3A_historicalNat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historicalNat_Seine_su_%%%&STATION=P_Seine_HadGEM3A_historicalNat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Seine basin</a>,

<div class=alineakop>CORDEX EUR-11 (LCSE)</div>
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/rx3day_cordex_LOIRE_%%&STATION=Rx3day_Loire_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">max of 3-day ave precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/rx3day_cordex_SEINE_%%&STATION=Rx3day_Seine_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">max of 3-day ave precipitation in Seine basin</a>.
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_cordex_germany_%%&STATION=prmax_germany_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>.

<div class=alineakop>EC-Earth/RACMO 12km runs (KNMI)</div>
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/pr_racmo_Loire_%%&STATION=pr_Loire_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/pr_racmo_Seine_%%&STATION=pr_Seine_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Seine basin</a>
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_racmo_germany_%%&STATION=prmax_Germany_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>

<div class=alineakop>HadGEM2-ES/RACMO 12km runs (KNMI)</div>
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_racmo_hadgem_germany_%%&STATION=prmax_Germany_HadGEM2_RACMO&TYPE=p&NPERYEAR=360&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>

<div class=alineakop>hiFLOR daily series</div>
Precipitation along the Gulf Coast in hiFlOR control runs 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1860-Ctl.00010101-02001231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1860&TYPE=p&NPERYEAR=366&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1940-Ctl.00010101-00761231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1940&TYPE=p&NPERYEAR=366&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1990-Ctl.00010101-03011231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1990&TYPE=p&NPERYEAR=366&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.2015-Ctl.00010101-00701231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_2015&TYPE=p&NPERYEAR=366&id=$EMAIL">2015</a>.

<div class=alineakop>FLOR daily series</div>
Precipitation along the Gulf Coast in FlOR transient runs 1861-2100: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long.18610101-21001231.precip_LA_all_ce_%%%&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=366&id=$EMAIL">all grid points</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long-E%%.18610101-21001231.precip_LA_all_ce_3dymax&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=366&id=$EMAIL">spatial and annual max of 3-day means</a>,



EOF

. ./myvinkfoot.cgi
