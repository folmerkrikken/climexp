#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a field" "Attribution runs" "index,nofollow"

cat <<EOF
<div class="kalelink">
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="14"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
<tr><th>EC-Earth 2.3<br>T159 coupled 1860-2100
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
<th>wspd
<th>max<br>wspd
<th>psl
<tr><td>16 daily
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
<td><input type=radio class=formradio name=field value=knmi14_sfcWind_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_sfcWindmax_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_psl_Aday_ECEARTH23_rcp85>
<tr><td>16 monthly
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
<td><input type=radio class=formradio name=field value=knmi14_sfcWind_Amon_ECEARTH23_rcp85>
<td>&nbsp;
<td><input type=radio class=formradio name=field value=knmi14_psl_Amon_ECEARTH23_rcp85>
<tr><td>&nbsp;
<td>RCP8.5
<td colspan=12>
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_su_%%&STATION=Tglobal_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">Global mean temperature</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_5lan_su_%%&STATION=Tland_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">land only</a>;
<a href="getindices.cgi?WMO=KNMI14Data/Nino/nino34_%%%&STATION=EC-Earth23_Nino3.4&TYPE=i&NPERYEAR=12&id=$EMAIL">Ni&ntilde;o3.4 (detrended)</a>.
<tr><th>&nbsp;
<th>&nbsp;
<th>Rx1day
<th>Rx3day
<th>Rx5day
<th>Txx
<th>Tx3x
<th>Txn
<th>Tnx
<th>Tnn
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<tr><td>annual
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_rx1day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_rx3day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_rx5day_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_txx_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tx3x_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_txn_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tnx_yr_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_tnn_yr_ECEARTH23_rcp85>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
EOF
if [   $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 \
    -o $EMAIL = e279dd4de035b5fd9edc95ba4df755f7 \
    -o $EMAIL = bd113ded9265e569c369d53ff59bf69a \
    -o $EMAIL = f9646e78b5dbcaee3d001eb713252e3e ]; then
    cat << EOF
<tr><th>EC-Earth 2.3<br>T159 coupled time slices
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
<th>wspd
<th>max<br>wspd
<th>psl
<tr><td>400 daily 5yr
<td>present
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=hiwaves3_pr_Aday_ECEarth_PD>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><td>400 daily 5yr
<td>2&deg;C
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=hiwaves3_pr_Aday_ECEarth_2C>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><th>PCR-GLOBWB S Asia
<th>input
<th colspan=2>discharge
<th colspan=2>runoff
<th colspan=2>snowmelt
<th colspan=2>satdeglow
<th colspan=2>satdegupp
<th>&nbsp;
<th>&nbsp;
<tr><td>1979-2017
<td>CPC
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_discharge_Aday_CPC_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_runoff_Aday_CPC_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_snowMelt_Aday_CPC_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_satDegLow_Aday_CPC_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_satDegUpp_Aday_CPC_hist>
<td>&nbsp;
<td>&nbsp;
<tr><td>1979-2017
<td>ERA-interim
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_discharge_Aday_ERA_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_runoff_Aday_ERA_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_snowMelt_Aday_ERA_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_satDegLow_Aday_ERA_hist>
<td colspan=2><input type=radio class=formradio name=field value=hiwaves3_satDegUpp_Aday_ERA_hist>
<td>&nbsp;
<td>&nbsp;
EOF
fi
cat <<EOF
<tr><th>EC-Earth 2.3<br>T799 SST-forced
<th>period
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
<tr><td>6 daily
<td>together
<td><input type=radio class=formradio name=field value=futureweather_tas_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_pr_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_pme_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_uas_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_vas_Aday_ECEARTH23_alldays>
<td><input type=radio class=formradio name=field value=futureweather_psl_Aday_ECEARTH23_alldays>
<tr><td>&nbsp;
<td>1850-1854
<td><input type=radio class=formradio name=field value=futureweather_tas_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_pr_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_pme_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_uas_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_vas_Aday_ECEARTH23_18500101-18541231>
<td><input type=radio class=formradio name=field value=futureweather_psl_Aday_ECEARTH23_18500101-18541231>
<tr><td>&nbsp;
<td>2002-2006
<td><input type=radio class=formradio name=field value=futureweather_tas_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_pr_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_pme_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_uas_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_vas_Aday_ECEARTH23_20020101-20061231>
<td><input type=radio class=formradio name=field value=futureweather_psl_Aday_ECEARTH23_20020101-20061231>
<tr><td>&nbsp;
<td>2030-2034
<td><input type=radio class=formradio name=field value=futureweather_tas_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_pr_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_pme_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_uas_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_vas_Aday_ECEARTH23_20300101-20341231>
<td><input type=radio class=formradio name=field value=futureweather_psl_Aday_ECEARTH23_20300101-20341231>
<tr><td>&nbsp;
<td>2094-2098
<td><input type=radio class=formradio name=field value=futureweather_tas_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_pr_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_pme_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_uas_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_vas_Aday_ECEARTH23_20940101-20981231>
<td><input type=radio class=formradio name=field value=futureweather_psl_Aday_ECEARTH23_20940101-20981231>
<tr><td>6 monthly
<td>together
<td><input type=radio class=formradio name=field value=futureweather_tas_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_pr_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_pme_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_uas_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_vas_Amon_ECEARTH23_allmonths>
<td><input type=radio class=formradio name=field value=futureweather_psl_Amon_ECEARTH23_allmonths>
<tr><td>&nbsp;
<td>1850-1854
<td><input type=radio class=formradio name=field value=futureweather_tas_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_pr_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_pme_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_uas_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_vas_Amon_ECEARTH23_185001-185412>
<td><input type=radio class=formradio name=field value=futureweather_psl_Amon_ECEARTH23_185001-185412>
<tr><td>&nbsp;
<td>2002-2006
<td><input type=radio class=formradio name=field value=futureweather_tas_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_pr_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_pme_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_uas_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_vas_Amon_ECEARTH23_200201-200612>
<td><input type=radio class=formradio name=field value=futureweather_psl_Amon_ECEARTH23_200201-200612>
<tr><td>&nbsp;
<td>2030-2034
<td><input type=radio class=formradio name=field value=futureweather_tas_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_pr_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_pme_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_uas_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_vas_Amon_ECEARTH23_203001-203412>
<td><input type=radio class=formradio name=field value=futureweather_psl_Amon_ECEARTH23_203001-203412>
<tr><td>&nbsp;
<td>2094-2098
<td><input type=radio class=formradio name=field value=futureweather_tas_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_tasmin_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_tasmax_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_pr_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_evspsbl_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_pme_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_ssr_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_uas_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_vas_Amon_ECEARTH23_209401-209812>
<td><input type=radio class=formradio name=field value=futureweather_psl_Amon_ECEARTH23_209401-209812>
<tr><th>HadGEM3A N216 1960-2015<br><a href="EUCLEIA/HadGEM3-A-N216/eucleia_conditions.pdf">conditions of use</a>
<th>SST forcing
<th>tas
<th>tas<br>min
<th>tas<br>max
<th>pr
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>psl
<tr><td>15/105 daily
<td>historical
<td><input type=radio class=formradio name=field value=eucleia_tas_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Aday_HadGEM3-A-N216_historical>
<tr><td>15/105 daily
<td>historicalNat
<td><input type=radio class=formradio name=field value=eucleia_tas_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Aday_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_pr_Aday_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Aday_HadGEM3-A-N216_historicalNat>
<tr><td>15/105 monthly
<td>historical
<td><input type=radio class=formradio name=field value=eucleia_tas_Amon_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Amon_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Amon_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_pr_Amon_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Amon_HadGEM3-A-N216_historical>
<tr><td>15/105 monthly
<td>historicalNat
<td><input type=radio class=formradio name=field value=eucleia_tas_Amon_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmin_Amon_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tasmax_Amon_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_pr_Amon_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=eucleia_psl_Amon_HadGEM3-A-N216_historicalNat>
<tr><th>&nbsp;
<th>&nbsp;
<th>Rx1day
<th>Rx3day
<th>Rx5day
<th>Txx
<th>Tx3x
<th>Txn
<th>Tnx
<th>Tnn
<th>&nbsp;
<th>&nbsp;
<tr><td>15/105 annual
<td>historical
<td><input type=radio class=formradio name=field value=eucleia_rx1day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txx_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tx3x_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_txn_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnx_yr_HadGEM3-A-N216_historical>
<td><input type=radio class=formradio name=field value=eucleia_tnn_yr_HadGEM3-A-N216_historical>
<td>&nbsp;
<td>&nbsp;
<tr><td>15/105 annual
<td>historicalNat
<td><input type=radio class=formradio name=field value=eucleia_rx1day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx3day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_rx5day_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txx_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tx3x_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_txn_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnx_yr_HadGEM3-A-N216_historicalNat>
<td><input type=radio class=formradio name=field value=eucleia_tnn_yr_HadGEM3-A-N216_historicalNat>
<td>&nbsp;
<td>&nbsp;
<tr><th>RACMO 12km<br>/EC-EARTH2.3 1950-2100
<th>scenario
<th>tas
<th>tas<br>min
<th>tas<br>max
<th>pr
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>&nbsp;
<th>psl
<tr><td>16 daily
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_t2m_day_RACMO22E_rcp85>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><td>16 monthly
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_t2m_mon_RACMO22E_rcp85>
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<td>&nbsp;
<tr><th>&nbsp;
<th>&nbsp;
<th>RX1day
<th>RX2day
<th>RX3day
<th>RX5day
<th>TXx
<th>TX3x
<th>TXn
<th>TX3n
<th>TNx
<th>TN3x
<th>TNn
<th>TN3n
<tr><td>16 annual
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_RX1day_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_RX2day_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_RX3day_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_RX5day_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TXx_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TX3x_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TXn_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TX3n_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TNx_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TN3x_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TNn_yr_RACMO22E_rcp85_year>
<td><input type=radio class=formradio name=field value=knmi14_TN3n_yr_RACMO22E_rcp85_year>
<tr><td>16 Oct-Mar
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_RX1day_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_RX2day_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_RX3day_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_RX5day_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TXx_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TX3x_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TXn_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TX3n_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TNx_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TN3x_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TNn_yr_RACMO22E_rcp85_ONDJFM>
<td><input type=radio class=formradio name=field value=knmi14_TN3n_yr_RACMO22E_rcp85_ONDJFM>
<tr><td>16 Apr-Sep
<td>RCP8.5
<td><input type=radio class=formradio name=field value=knmi14_RX1day_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_RX2day_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_RX3day_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_RX5day_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TXx_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TX3x_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TXn_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TX3n_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TNx_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TN3x_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TNn_yr_RACMO22E_rcp85_AMJJAS>
<td><input type=radio class=formradio name=field value=knmi14_TN3n_yr_RACMO22E_rcp85_AMJJAS>
</table>
</form>

<p>Observations and model output used in attribution studies are listed below per project.
Resources not listed are either easily accessible through  other Climate Explorer pages
or available from the authors (except for non-public data such as the IMD analyses).

<div class=alineakop>Kenya flooding Long Rains 2018: 2&deg;S-4&deg;N, 37-40&deg;E average</div>
Monthly <a href="get_index.cgi?field=gpccall_10&lat1=-2&lat2=4&lon1=37&lon2=40&standardunits=standardunits&id=$EMAIL">GPCC analyses</a>, 
<a href="get_index.cgi?field=CenTrendsChirps&lat1=-2&lat2=4&lon1=37&lon2=40&standardunits=standardunits&id=$EMAIL">CenTrends/CHIRPS analyses</a>.<br>
Monthly <a href="getindices.cgi?WMO=KNMI14Data/Pkenya/knmi14_pr_Amon_ECEARTH23_rcp85_37-40E_-2-4N_n_su_%%&STATION=ECEARTH23_rcp85_pr_37-40E_-2-4N_ensemble&TYPE=i&id=$EMAIL&NPERYEAR=12">EC-Earth 2.3 transient runs</a>,<br>
Monthly FLOR 50km time series <a href="getindices.cgi?WMO=PrincetonData/PIctl_CMIP6volc.precip_ce_mo_-2_4N_37_40E&STATION=FLOR_preindustrial_2S-4N_37-40E&TYPE=i&id=$EMAIL&NPERYEAR=12">pre-industrial</a>, 
<a href="getindices.cgi?WMO=PrincetonData/Control_2000.precip_ce_mo_-2_4N_37_40E&STATION=FLOR_2000_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">2000</a> control runs, 
<a href="getindices.cgi?WMO=PrincetonData/nudgelongalle.%%_5dy_tigerx86_64.intel16_512PE.precip_ce_mo_-2_4N_37_40E&STATION=FLOR_transient_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">5 SST-forced 1871-2016</a> runs<br>
Monthly FLOR 50km fields <a href="select.cgi?field=pr_flor_kenya_preindustrial&id=$EMAIL">pre-industrial</a>, 
<a href="select.cgi?field=pr_flor_kenya_2000&id=$EMAIL">2000</a> control ,
<a href="select.cgi?field=pr_flor_kenya_nudged&id=$EMAIL">5 SST-forced 1871-2016</a> runs.<br>
Monthly HadGEM3-A N216 time series <a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pkenya/eucleia_pr_Amon_HadGEM3-A-N216_historical_37-40E_-2-4N_n_su_%%%&STATION=HadGEM3A_historical_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">historical</a>, 
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pkenya/eucleia_pr_Amon_HadGEM3-A-N216_historicalNat_37-40E_-2-4N_n_su_%%%&STATION=HadGEM3A_historicalNat_2S-4N_37-40E&TYPE=i&id=$EMAIL&NPERYEAR=12">historicalNat</a>.<br>
Monthly weather@home time series
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_ACTUAL_monthly_2S-4N_37-40E_longrains_@@@&STATION=wah_actual_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">actual</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_NATURAL_monthly_2S-4N_37-40E_longrains_@@@&STATION=wah_natural_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">natural</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_ACTUALCLIM_monthly_2S-4N_37-40E_longrains_@@@&STATION=wah_actualclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">actualclim</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_NATURALCLIM_monthly_2S-4N_37-40E_longrains_@@@&STATION=wah_naturalclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">naturalclim</a>.<br>
Monthly MIROC5 time series
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_miroc5_ACTUALCLIM_monthly_2S-4N_37-40E_@@@&STATION=miroc5_actualclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">actualclim</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_miroc5_NATURALCLIM_monthly_2S-4N_37-40E_@@@&STATION=miroc5_naturalclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=12">naturalclim</a>.<br> 
Daily <a href="get_index.cgi?field=prcp_cpc_daily&NPERYEAR=366&lat1=-2&lat2=4&lon1=37&lon2=40&standardunits=standardunits&intertype=nearest&id=$EMAIL">CPC analyses</a>, 
<a href="get_index.cgi?field=cmorph_daily_05&NPERYEAR=366&lat1=-2&lat2=4&lon1=37&lon2=40&standardunits=standardunits&&intertype=nearestid=$EMAIL">CMORPH analyses</a>, 
<a href="get_index.cgi?field=chirps_20_25&NPERYEAR=366&lat1=-2&lat2=4&lon1=37&lon2=40&standardunits=standardunits&intertype=nearest&id=$EMAIL">CHIRPS analyses</a>.<br> 
Daily <a href="getindices.cgi?WMO=KNMI14Data/Pkenya/knmi14_pr_Aday_ECEARTH23_rcp85_37-40E_-2-4N_n_su_%%&STATION=ECEARTH23_rcp85_pr_37-40E_-2-4N_ensemble&TYPE=i&id=$EMAIL&NPERYEAR=12">EC-Earth 2.3 transient runs</a>,<br>
Daily FLOR 50km time series <a href="getindices.cgi?WMO=PrincetonData/PIctl_CMIP6volc.precip_ce_-2_4N_37_40E&TYPE=i&id=$EMAIL&NPERYEAR=12">pre-industrial</a>, 
<a href="getindices.cgi?WMO=PrincetonData/Control_2000.precip_ce_-2_4N_37_40E&TYPE=i&id=$EMAIL&NPERYEAR=12">2000</a> control runs, 
<a href="getindices.cgi?WMO=PrincetonData/nudgelongalle.%%_5dy_tigerx86_64.intel16_512PE.precip_ce_-2_4N_37_40E&TYPE=i&id=$EMAIL&NPERYEAR=12">5 SST-forced 1871-2016</a> runs<br>
Daily FLOR 50km fields <a href="select.cgi?field=pr_flor_kenya_preindustrial_daily&id=$EMAIL&NPERYEAR=366">pre-industrial</a>, 
<a href="select.cgi?field=pr_flor_kenya_2000_daily&id=$EMAIL">2000</a> control ,
<a href="select.cgi?field=pr_flor_kenya_nudged_daily&id=$EMAIL">5 SST-forced 1871-2016</a> runs.<br>
Daily HadGEM3-A N216 time series <a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pkenya/eucleia_pr_Aday_HadGEM3-A-N216_historical_37-40E_-2-4N_n_su_%%%&STATION=HadGEM3A_historical_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=366">historical</a>, 
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pkenya/eucleia_pr_Aday_HadGEM3-A-N216_historicalNat_37-40E_-2-4N_n_su_%%%&STATION=HadGEM3A_historicalNat_2S-4N_37-40E&TYPE=i&id=$EMAIL&NPERYEAR=366">historicalNat</a>.<br>
Daily weather@home time series
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_ACTUAL_daily_2S-4N_37-40E_longrains_@@@&STATION=wah_actual_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">actual</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_NATURAL_daily_2S-4N_37-40E_longrains_@@@&STATION=wah_natural_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">natural</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_ACTUALCLIM_daily_2S-4N_37-40E_longrains_@@@&STATION=wah_actualclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">actualclim</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_wah_NATURALCLIM_daily_2S-4N_37-40E_longrains_@@@&STATION=wah_naturalclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">naturalclim</a><br> 
Annual weather@home climatology field 
<a href="select.cgi?field=pr_wah_kenya_actualclim_clim&id=$EMAIL">actualclim</a>.<br>
Daily MIROC5 time series
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_miroc5_ACTUALCLIM_daily_2S-4N_37-40E_@@@&STATION=miroc5_actualclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">actualclim</a>, 
<a href="getindices.cgi?WMO=Weather@Home/Kenya/pr_miroc5_NATURALCLIM_daily_2S-4N_37-40E_@@@&STATION=miroc5_naturalclim_2S-4N_37-40E&TYPE=i&TYPE=i&id=$EMAIL&NPERYEAR=360">naturalclim</a><br> 
Annual MIROC5 climatology field 
<a href="select.cgi?field=pr_miroc5_kenya_actualclim_clim&id=$EMAIL">actualclim</a>, 

<div class=alineakop>Western Cape drought 2015-2017: 35-31&deg;S, 18-21&deg;E land average</div>
Monthly <a href="get_index.cgi?field=gpccall_10&lat1=-35&lat2=-31&lon1=18&lon2=21&standardunits=standardunits&id=$EMAIL">GPCC analyses</a>, <br>
Monthly <a href="getindices.cgi?WMO=KNMI14Data/Pwesterncape/knmi14_pr_Amon_ECEARTH23_rcp85_18-21E_-35--31N_n_5lan_su_%%&STATION=ECEARTH23_rcp85_pr_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">EC-Earth 2.3 transient runs</a>,<br>
Monthly HadGEM3-A N216 <a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pwesterncape/eucleia_pr_Amon_HadGEM3-A-N216_historical_18-21E_-35--31N_n_5lan_su_%%%&STATION=HadGEM3A_historical_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">historical</a>, 
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Pwesterncape/eucleia_pr_Amon_HadGEM3-A-N216_historicalNat_18-21E_-35--31N_n_5lan_su_%%%&STATION=HadGEM3A_historicalNat_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">historicalNat</a>,<br>
Monthly CESM <a href="getindices.cgi?WMO=CESMData/Pwesterncape/pr_Amon_CESM-LENS_rcp85_18-21E_-35--31N_land_%%&STATION=CESM_historical-rcp85_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">RCP8.5 large ensemble</a>
(<a href="getindices.cgi?WMO=CESMData/Pwesterncape/tas_Amon_CESM-LENS_rcp85_global_%%&STATION=Tglobal_CESM_historical-rcp85&TYPE=i&id=$EMAIL&NPERYEAR=12">Tglobal</a>), 
<a href="getindices.cgi?WMO=CESMData/Pwesterncape/pr_Amon_CESM-ME_rcp45_18-21E_-35--31N_land_%%&STATION=CESM_historical-rcp45_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">RCP4.5 medium ensemble</a>
(<a href="getindices.cgi?WMO=CESMData/Pwesterncape/tas_Amon_CESM-ME_rcp45_global_%%&STATION=Tglobal_CESM_historical-rcp45&TYPE=i&id=$EMAIL&NPERYEAR=12">Tglobal</a>),<br>
Monthly <a href="getindices.cgi?WMO=CMIP5/Pwesterncape/pr_Amon_cmip5one_-35--31N_18-21E_land_%%%&STATION=CMIP5_rcp45_pr_18-21E_35-31S&TYPE=i&id=$EMAIL&NPERYEAR=12">CMIP5 historical/RCP4.5 transient runs</a> (one ensemble member per model).<br>
(make annual mean at the bottom of the page)
EOF
if [   $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 \
    -o $EMAIL = e279dd4de035b5fd9edc95ba4df755f7 \
    -o $EMAIL = bd113ded9265e569c369d53ff59bf69a \
    -o $EMAIL = f9646e78b5dbcaee3d001eb713252e3e ]; then
    cat << EOF
<div class=alineakop>Bangladesh flooding 2017</div>
Observed precipitation in the Brahmaputra basin: 
<a href="getindices.cgi?WMO=Bangladesh2017Data/iprcp_cpc_daily_mask0_su&STATION=pr_CPC_Brahmaputra&TYPE=p&NPERYEAR=366&id=$EMAIL">CPC</a>, 
<a href="getindices.cgi?WMO=Bangladesh2017Data/igpcc_daily_mask0_su&STATION=pr_GPCC_Brahmaputra&TYPE=p&NPERYEAR=366&id=$EMAIL">GPCC</a>, 
<a href="getindices.cgi?WMO=Bangladesh2017Data/ierai_prcp_daily_mask0_su&STATION=pr_ERAi_Brahmaputra&TYPE=p&NPERYEAR=366&id=$EMAIL">ERA-interim</a>, 
<br>HIWAVES precipitation in Bangladesh:
<a href="getindices.cgi?WMO=Bangladesh2017Data/iknmi14_pr_Aday_ECEARTH23_rcp85_mask20_su_%%&STATION=pr_ECEarth_rcp85_Bangladesh&TYPE=p&NPERYEAR=366&id=$EMAIL">HIWAVES_rcp85</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/ihiwaves3_pr_Aday_ECEarth_PD_mask20_su_%%%&STATION=pr_ECEarth_PD_Bangladesh&TYPE=p&NPERYEAR=366&id=$EMAIL">HIWAVES_PD</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/ihiwaves3_pr_Aday_ECEarth_2C_mask20_su_%%%&STATION=pr_ECEarth_2C_Bangladesh&TYPE=p&NPERYEAR=366&id=$EMAIL">HIWAVES_2C</a>
<br>Modelled discharge at Bahadurabad
<a href="getindices.cgi?WMO=Bangladesh2017Data/CPC_discharge_Bahadurabad&STATION=discharge_PCR_GLOBWB_CPC_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">PCR_GLOBWB_CPC</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/ERA_discharge_Bahadurabad&STATION=discharge_PCR_GLOBWB_ERA_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">PCR_GLOBWB_ERA</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/discharge_hiwaves_monthMax_rcp85_%%&STATION=discharge_PCR_GLOBWB_ECEarth_rcp85_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">PCR_GLOBWB_HIWAVES_rcp85</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/discharge_hiwaves_monthMax_PD_%%%&STATION=discharge_PCR_GLOBWB_ECEarth_PD_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">PCR_GLOBWB_HIWAVES_PD</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/discharge_hiwaves_monthMax_2C_%%%&STATION=discharge_PCR_GLOBWB_ECEarth_2C_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">PCR_GLOBWB_HIWAVES_2C</a>,
<a href="getindices.cgi?WMO=Bangladesh2017Data/discharge_SWAT_ECEarth_rcp85_%%&STATION=discharge_SWAT_ECEarth_rcp85_Bahadurabad&TYPE=i&NPERYEAR=366&id=$EMAIL">SWAT_ECEARTH_rcp85</a>.
EOF
fi
cat << EOF
<div class=alineakop>European storms January 2018 </div>
ISD-lite station average 1976-2017 <a href="getindices.cgi?WMO=ISDData/Storms/isdlite_eleanor&STATION=u10max_Eleanor_ISDlite&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max 3-hourly instantaneous wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=ISDData/Storms/isdlite_friederike&STATION=u10max_Friederike_ISDlite&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<br>EuroCODEX runs (LSCE bias-corrected) 1971-2069 <a href="getindices.cgi?WMO=CORDEX/Storms/u10max_eurocordex_rcp85_eleanor_1971-2070_%%&STATION=u10max_Eleanor_EuroCORDEX&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=CORDEX/Storms/u10max_eurocordex_rcp85_friederike_1971-2070_%%&STATION=u10max_Friederike_EuroCORDEX&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<br>EC-Earth/RACMO 12km runs (KNMI) 1971-2070 <a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_eleanor_1971-2070_%%&STATION=u10max_Eleanor_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_friederike_1971-2070_%%&STATION=u10max_Friederike_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<!--
<br>EC-Earth/RACMO 12km runs (KNMI) 1971-2000 <a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_eleanor_1971-2000_%%&STATION=u10max_Eleanor_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_friederike_1971-2000_%%&STATION=u10max_Friederike_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<br>EC-Earth/RACMO 12km runs (KNMI) 2001-2030 <a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_eleanor_2001-2030_%%&STATION=u10max_Eleanor_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_friederike_2001-2030_%%&STATION=u10max_Friederike_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<br>EC-Earth/RACMO 12km runs (KNMI) 2021-2050 <a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_eleanor_2021-2050_%%&STATION=u10max_Eleanor_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_friederike_2021-2050_%%&STATION=u10max_Friederike_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
<br>EC-Earth/RACMO 12km runs (KNMI) 2041-2070 <a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_eleanor_2041-2070_%%&STATION=u10max_Eleanor_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">annual max hourly wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/u10max_racmo_rcp85_friederike_2041-2070_%%&STATION=u10max_Friederike_RACMO&TYPE=i&NPERYEAR=1&id=$EMAIL">Friederike region</a>.
-->
<br>EC-Earth 2.3 T159 (KNMI) 1861-2100 <a href="getindices.cgi?WMO=KNMI14Data/Storms/sfcWindmax_Aday_ECEARTH23_rcp85_Eleanor_n_5lan_%%&STATION=u10max_Eleanor_ECEARTH&TYPE=i&NPERYEAR=366&id=$EMAIL">daily max of 3-hr instantaneous wind in Eleanor region</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Storms/sfcWindmax_Aday_ECEARTH23_rcp85_Friederike_n_5lan_%%&STATION=u10max_Friederike_ECEARTH&TYPE=i&NPERYEAR3661&id=$EMAIL">Friederike region</a>


<div class=alineakop>India heat waves <a href="https://doi.org/10.5194/nhess-18-365-2018">2015, 2016</a></div>
ERA-interim daily <a href="select.cgi?id=$EMAIL&field=erai_tmax_daily">TX</a>, <a href="select.cgi?id=$EMAIL&field=erai_tmin_daily">TN</a>,
<a href="select.cgi?id=$EMAIL&field=erai_twet_daily">max daily Twetbulb</a>, <a href="select.cgi?id=$EMAIL&field=erai_tdew_daily">daily mean Tdew</a>
<br>ERA-interim annual <a href="select.cgi?id=$EMAIL&field=erai_txx">TXx</a>, <a href="select.cgi?id=$EMAIL&field=erai_tnx">TNx</a>.
<br>GHCN-D TX <a href="gdcntmax.cgi?id=$EMAIL8&WMO=IN019070100&STATION=BIKANER&extraargs=">Bikaner</a>, 
<a href="gdcntmax.cgi?id=$EMAIL8&WMO=IN019180500&STATION=JODHPUR&extraargs=">Jodhpur</a>, 
<a href="gdcntmax.cgi?id=$EMAIL8&WMO=IN001111200&STATION=MACHILIPATNAM&extraargs=">Machilipatnam</a>.
<br>weather@home HadAM3P May TXx fields <a href="select.cgi?field=wh_txx_india">Climatology</a>
(cannot yet be fully analysed in the Climate Explorer).
<br>weather@home HadAM3P May TXx at grid point Phalodi <a href="Weather@Home/India/phalodi_TXx_may_Actual_2016.nc">Actual</a>, 
<a href="Weather@Home/India/phalodi_TXx_may_Natural_2016.nc">Natural</a> and <a href="Weather@Home/India/phalodi_TXx_may_Climatology_1986-2014.nc">Climatology</a>
(cannot yet be analysed in the Climate Explorer).
<br>CAMS-Interim EAC3 AOD at 550 nm 2003-2015 <a href="select.cgi?field=eac3_aod550_day&id=$EMAIL">daily</a>, <a href="select.cgi?field=eac3_aod550&id=$EMAIL">monthly</a>.

<div class=alineakop>US Gulf coast extreme precipitation <a href="https://doi.org/10.5194/hess-21-897-2017">2016</a>, <a href="https://doi.org/10.1088/1748-9326/aa9ef2">2017</a></div>
CPC analysis
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">0.25&deg;</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_05_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">0.50&deg;</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_10_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">1.0&deg;</a> series
FLOR transient runs 1861-2100: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long.18610101-21001231.precip_LA_all_ce_%%%&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=366&id=$EMAIL">all grid points</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long-E%%.18610101-21001231.precip_LA_all_ce_3dymax&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long-E%%.18610101-21001231.precip_LA_all_ce_3dymax_mo&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=12&id=$EMAIL">spatial and monthly max of 3-day means</a>,
<br>FLOR transient runs 1861-2100:  
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.long-E%%.1861-2100.t_ref_all_gm_ce&STATION=GMST_FLOR_transient&TYPE=i&NPERYEAR=1&id=$EMAIL">global mean surface temperature</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.long-ave.1861-2100.t_ref_all_gm_ce&STATION=GMST_FLOR_transient&TYPE=i&NPERYEAR=1&id=$EMAIL">ensemble mean</a>.
<br>FLOR 1860 control run
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_flor_control_1max3ave_max_%%&STATION=pr_LA_FLOR_control&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<br>FLOR 1860 control run
<a href="getindices.cgi?WMO=GFDLData/Louisiana/Tglobal_flor_control_%%&STATION=GMST_FLOR_control&TYPE=i&NPERYEAR=1&id=$EMAIL">global mean surface temperature</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34_flor_control_%%&STATION=Nino34_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">Ni&ntilde;o3.4</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_flor_control_%%&STATION=Nino34detrended_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">Ni&ntilde;o3.4 detrended</a>,
<br>FLOR 1860 control run
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_30ns_flor_control_%%&STATION=SST_30S30N_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">SST 30&deg;S-30&deg;N</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_gulf_flor_control_%%&STATION=SST_Gulf_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">SST Gulf</a>.
<br>HiFLOR grid boxes
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1860-Ctl.00010101-02001231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1860&TYPE=p&NPERYEAR=366&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1940-Ctl.00010101-00761231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1940&TYPE=p&NPERYEAR=366&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1990-Ctl.00010101-03011231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1990&TYPE=p&NPERYEAR=366&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.2015-Ctl.00010101-00701231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_2015&TYPE=p&NPERYEAR=366&id=$EMAIL">2015</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_conc_%%%&STATION=pr_LA_hiFLOR_conc&TYPE=p&NPERYEAR=366&id=$EMAIL">concatenated</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_conc_%%%_max1_3v&STATION=pr_LA_hiFLOR_conc_max1_3v&TYPE=p&NPERYEAR=1&id=$EMAIL">concatenated annual max of 3-day precip</a>.
<br>HiFLOR 2&times;2 grid boxes
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1860-Ctl.00010101-02001231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1860&TYPE=p&NPERYEAR=366&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1940-Ctl.00010101-00761231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1940&TYPE=p&NPERYEAR=366&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1990-Ctl.00010101-03011231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1990&TYPE=p&NPERYEAR=366&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.2015-Ctl.00010101-00701231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_2015&TYPE=p&NPERYEAR=366&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_05_conc_%%%&STATION=pr_LA_hiFLOR_05_conc_1max3ave&TYPE=p&NPERYEAR=1&id=$EMAIL">concatenated</a>.
<br>HiFLOR global mean surface temperature 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1860-Ctl.0001-0200.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1860&TYPE=i&NPERYEAR=1&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1940-Ctl.0001-0075.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1940&TYPE=i&NPERYEAR=1&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1990-Ctl.0001-0301.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1990&TYPE=i&NPERYEAR=1&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.2015-Ctl.0001-0070.t_ref_all_gm_ce&STATION=GMST_hiFLOR_2015&TYPE=i&NPERYEAR=1&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/Tglobal_hiflor_conc&STATION=GMST_hiFLOR_conc&TYPE=i&NPERYEAR=1&id=$EMAIL">concatenated</a>.
<br>HiFLOR Ni&ntilde;o3.4 (detrended)  
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1860&STATION=N34d_hiFLOR_1860&TYPE=i&NPERYEAR=12&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1940&STATION=N34d_hiFLOR_1940&TYPE=i&NPERYEAR=12&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1990&STATION=N34d_hiFLOR_1990&TYPE=i&NPERYEAR=12&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_2015&STATION=N34d_hiFLOR_2015&TYPE=i&NPERYEAR=12&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_conc&STATION=N34d_hiFLOR_conc&TYPE=i&NPERYEAR=12&id=$EMAIL">concatenated</a>.
<br>HiFLOR Gulf SST  
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1860-Ctl.000101-020012.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1860&TYPE=i&NPERYEAR=12&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1940-Ctl.000101-007512.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1940&TYPE=i&NPERYEAR=12&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1990-Ctl.000101-030112.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1990&TYPE=i&NPERYEAR=12&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.2015-Ctl.000101-007012.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_2015&TYPE=i&NPERYEAR=12&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_gulf_hiflor_conc&STATION=30S30N_hiFLOR_conc&TYPE=i&NPERYEAR=12&id=$EMAIL">concatenated</a>.
<br>HiFLOR transient runs 1971-2015
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_05_sst_%%%&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=366&id=$EMAIL">all 2&times;2 averaged grid points</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.sst-E%%.19710101-20151231.precip_LA_all_ce_3dymax&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.sst-E%%.19710101-20151231.precip_LA_all_ce_3dymax_mo&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=12&id=$EMAIL">spatial and monthly max of 3-day means</a>.
<br>EC-Earth 2.3 T799
<a href="select.cgi?field=pr_futureweather_gulfcoast&id=$EMAIL">precipitation along the Gulf Coast</a>.

<div class=alineakop>European summer heat <a href="https://wwa.climatecentral.org/analyses/euro-mediterranean-heat-summer-2017/">2017</a></div>
Portugal CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_Portugal_without_islands&STATION=Tmax_Portugal&TYPE=t&id=$EMAIL">Tmax</a>, 
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_t2m_Portugal_without_islands&STATION=T2m_Portugal&TYPE=t&id=$EMAIL">T2m</a>
<br>Spain CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_Spain_Europe&STATION=Tmax_Spain&TYPE=t&id=$EMAIL">Tmax</a>,
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_t2m_Spain_Europe&STATION=T2m_Spain&TYPE=t&id=$EMAIL">T2m</a>
<br>France CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_France_metropolitan&STATION=Tmax_France&TYPE=t&id=$EMAIL">Tmax</a>,
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_t2m_France_metropolitan&STATION=T2m_France&TYPE=t&id=$EMAIL">T2m</a>
<br>Switzerland  CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_Switzerland&STATION=Tmax_Switzerland&TYPE=t&id=$EMAIL">Tmax</a>, Swissmean 
<a href="getindices.cgi?WMO=Event_EuropeJune2017/swiss_swiss&STATION=Swissmean&TYPE=t&id=$EMAIL">T2m</a>
<br>Belgium CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_Belgium&STATION=Tmax_Belgium&TYPE=t&id=$EMAIL">Tmax</a>,
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_t2m_Belgium&STATION=T2m_Belgium&TYPE=t&id=$EMAIL">T2m</a>
<br>Netherlands CRU TS 4.00
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_Netherlands_without_Caribbean&STATION=Tmax_Netherlands&TYPE=t&id=$EMAIL">Tmax</a>, CNT
<a href="getindices.cgi?WMO=KNMIData/cnt_v11&STATION=CNT&TYPE=t&id=$EMAIL">T2m</a>
<br>Central England
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_tmax_-3-0E_54-57N_n&STATION=Tmax_-3-0E_54-57N&TYPE=t&id=$EMAIL">Tmax</a>, CET
<a href="getindices.cgi?WMO=Event_EuropeJune2017/cru_t2m_-3-0E_54-57N_n&STATION=CET&TYPE=t&id=$EMAIL">T2m</a>
<br>EC-Earth 2.3 T159 
<a href="getindices.cgi?WMO=KNMI14Data/Tmed/tasmax_8-24E_36-48N_muladdcorr_ydrun_retrend_%%&STATION=EC-EARTH_biascorr_Tmax_8-24E_36-48N&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmax 36-48&deg;N, 8-24&deg;E, bias-corrected (mean and variance)</a>


<div class=alineakop>Spring/summer rains in France <a href="https://doi.org/10.5194/hess-2016-308">2016</a></div>
EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Loire_su_%%&STATION=P_Loire_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Loire basin</a>.
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Seine_su_%%&STATION=P_Seine_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Seine basin</a>.
<br>HadGEM3A N216 historical <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Loire_su_%%%&STATION=P_Loire_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Seine_su_%%%&STATION=P_Seine_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Seine basin</a>,
<br>HadGEM3A N216 historicalNat <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historicalNat_Loire_su_%%%&STATION=P_Loire_HadGEM3A_historicalNat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historicalNat_Seine_su_%%%&STATION=P_Seine_HadGEM3A_historicalNat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Seine basin</a>,
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/rx3day_cordex_LOIRE_%%&STATION=Rx3day_Loire_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">max of 3-day ave precipitation in Loire basin</a>,
<br>CORDEX EUR-11 (LCSE) <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/rx3day_cordex_SEINE_%%&STATION=Rx3day_Seine_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">max of 3-day ave precipitation in Seine basin</a>.
<br>CORDEX EUR-11 (LCSE) <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_cordex_germany_%%&STATION=prmax_germany_CORDEX&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>.
<br>EC-Earth/RACMO 12km runs (KNMI) <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/pr_racmo_Loire_%%&STATION=pr_Loire_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/pr_racmo_Seine_%%&STATION=pr_Seine_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Seine basin</a>
<br>EC-Earth/RACMO 12km runs (KNMI) <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_racmo_germany_%%&STATION=prmax_Germany_RACMO&TYPE=p&NPERYEAR=366&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>
<br>HadGEM2-ES/RACMO 12km runs (KNMI) <a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/prmax_racmo_hadgem_germany_%%&STATION=prmax_Germany_HadGEM2_RACMO&TYPE=p&NPERYEAR=360&id=$EMAIL">spatial maximum of precipitation in Central/South Germany</a>


<div class=alineakop>Winter rains in the UK <a href="https://doi.org/10.1088/1748-9326/aa9663">2015</a></div>
EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=KNMI14Data/Pcumbria/pr_day_ECEARTH23_rcp85_%%_18600101-21001231_NEngland&STATION=P_NEngland_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Northern England</a>.


<div class=alineakop>The Netherlands</div>
EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tas_muladdcorr_ydrun_retrend_%%&STATION=Tmean_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmean De Bilt bias-corrected</a>, <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_muladdcorr_ydrun_retrend_%%&STATION=Tmax_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmax De Bilt bias-corrected</a>, <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmin_muladdcorr_ydrun_retrend_%%&STATION=Tmin_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmin De Bilt bias-corrected</a>,
<br>EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tas_day_ECEARTH23_rcp85_%%_18600101-21001231_52N_5E&STATION=Tdebilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">temperature at 52&deg;N, 5&deg;E</a>, <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5.2E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5.2&deg;E</a>,
<br>EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/pr_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Pdebilt_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>,
<br>EC-Earth 2.3 T159 <a href="getindices.cgi?WMO=KNMI14Data/Tglobal/tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_su_mean_mean1&STATION=Tglobal_EC-Earth23&TYPE=i&NPERYEAR=1&id=$EMAIL">annual mean ensemble mean global mean temperature</a>,
<br>HadGEM3A N216 historical <a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historical_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_obs&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>, 
<a href="select.cgi?field=EUCLEIA/HadGEM3-A-N216/Tdebilt/pr_day_HadGEM3-A-N216_historical__%%%_Netherlands_without_Caribbean_su.info&NPERYEAR=360&id=$EMAIL">precipitation in the Netherlands (w/o Caribbean)</a>
<br>HadGEM3A N216 historicalNat <a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historicalNat_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_nat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>,
<a href="select.cgi?field=EUCLEIA/HadGEM3-A-N216/Tdebilt/pr_day_HadGEM3-A-N216_historicalNat__%%%_Netherlands_without_Caribbean_su.info&NPERYEAR=360&id=$EMAIL">precipitation in the Netherlands (w/o Caribbean)</a>


EOF

. ./myvinkfoot.cgi
