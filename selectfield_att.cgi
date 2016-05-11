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
<th>&nbsp;
<tr><td>daily
<td>observed
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><td>daily
<td>counterfactual
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
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
<td>observed
<td><input type=radio class=formradio name=field value=eucleia_rx1day_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txx_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txn_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnx_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnn_Aday_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><td>annual
<td>counterfactual
<td><input type=radio class=formradio name=field value=eucleia_rx1day_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txx_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txn_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnx_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnn_Aday_HadGEM3-A-N216_historicalNat>
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
<br><a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5.2E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5.2&deg;E</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Pcumbria/pr_day_ECEARTH23_rcp85_%%_18600101-21001231_NEngland&STATION=P_NEngland_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Northern England</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Pboulder/pr_day_ECEARTH23_rcp85_%%_18600101-21001231_Boulder&STATION=P_Boulder_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Boulder, Colorado, USA</a>.

EOF

. ./myvinkfoot.cgi
