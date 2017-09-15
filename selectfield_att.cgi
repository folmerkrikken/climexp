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
<tr><th>EC-Earth 2.3<br>T159 coupled
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
<td><input type=radio class=formradio name=field value=knmi14_sfcWind_Aday_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_sfcWindmax_Aday_ECEARTH23_rcp85>
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
<td><input type=radio class=formradio name=field value=knmi14_sfcWind_Amon_ECEARTH23_rcp85>
<td>&nbsp;
<td><input type=radio class=formradio name=field value=knmi14_psl_Amon_ECEARTH23_rcp85>
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
<tr><td>daily
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
<tr><td>monthly
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
<tr><th>HadGEM3A N216<br><a href="EUCLEIA/HadGEM3-A-N216/eucleia_conditions.pdf">conditions of use</a>
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
<tr><td>daily
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
<tr><td>daily
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
<tr><td>monthly
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
<tr><td>monthly
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
<tr><th>RACMO 12km<br>/EC-EARTH2.3
<th>scenario
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
<tr><td>annual
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
<tr><td>Oct-Mar
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
<tr><td>Apr-Sep
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
<div class=alineakop>EC-Earth 2.3 monthly series</div>
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_su_%%&STATION=Tglobal_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">Global mean temperature</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tglobal/iknmi14_tas_Amon_ECEARTH23_rcp85_0-360E_-90-90N_n_5lan_su_%%&STATION=Tland_EC-Earth23&TYPE=t&NPERYEAR=12&id=$EMAIL">land only</a>.
<br><a href="getindices.cgi?WMO=KNMI14Data/Nino/nino34_%%%&STATION=EC-Earth23_Nino3.4&TYPE=i&NPERYEAR=12&id=$EMAIL">Ni&ntilde;o3.4 (detrended)</a>,

<div class=alineakop>EC-Earth 2.3 daily series</div>
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tas_day_ECEARTH23_rcp85_%%_18600101-21001231_52N_5E&STATION=Tdebilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_muladdcorr_ydrun_retrend_%%&STATION=Tmax_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmax De Bilt bias-corrected</a>, <a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmin_muladdcorr_ydrun_retrend_%%&STATION=Tmin_debilt_EC-Earth23_debias&TYPE=t&NPERYEAR=366&id=$EMAIL">Tmin De Bilt bias-corrected</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5&deg;E</a>,
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/tasmax_Aday_ECEARTH23_rcp85_5.2E_52N_n_su_%%&STATION=Tmax_debilt_EC-Earth23&TYPE=t&NPERYEAR=366&id=$EMAIL">maximum temperature at 52&deg;N, 5.2&deg;E</a>,<br>
<a href="getindices.cgi?WMO=KNMI14Data/Tdebilt/pr_Aday_ECEARTH23_rcp85_5E_52N_n_su_%%&STATION=Pdebilt_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>,
<br><a href="getindices.cgi?WMO=KNMI14Data/Pcumbria/pr_day_ECEARTH23_rcp85_%%_18600101-21001231_NEngland&STATION=P_NEngland_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Northern England</a>,
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Loire_su_%%&STATION=P_Loire_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Loire basin</a>.
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/knmi14_pr_Aday_ECEARTH23_rcp85_Seine_su_%%&STATION=P_Seine_EC-Earth23&TYPE=p&NPERYEAR=366&id=$EMAIL">precipitation in Seine basin</a>.

<div class=alineakop>HadGEM3A N216 historical daily series</div>
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historical_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_obs&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>
<br><a href="select.cgi?field=EUCLEIA/HadGEM3-A-N216/Tdebilt/pr_day_HadGEM3-A-N216_historical__%%%_Netherlands_without_Caribbean_su.info&NPERYEAR=360&id=$EMAIL">precipitation in the Netherlands (w/o Caribbean)</a>
<br><a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Loire_su_%%%&STATION=P_Loire_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Loire basin</a>,
<a href="getindices.cgi?WMO=Event_FloodsEuropeMay2016/eucleia_pr_Aday_HadGEM3-A-N216_historical_Seine_su_%%%&STATION=P_Seine_HadGEM3A_historical&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation in Seine basin</a>,

<div class=alineakop>HadGEM3A N216 historicalNat daily series</div>
<a href="getindices.cgi?WMO=EUCLEIA/HadGEM3-A-N216/Tdebilt/ieucleia_pr_Aday_HadGEM3-A-N216_historicalNat_5E_52N_n_su_%%%&STATION=Pdebilt_HadGEM3A_nat&TYPE=p&NPERYEAR=360&id=$EMAIL">precipitation at 52&deg;N, 5&deg;E</a>.
<br><a href="select.cgi?field=EUCLEIA/HadGEM3-A-N216/Tdebilt/pr_day_HadGEM3-A-N216_historicalNat__%%%_Netherlands_without_Caribbean_su.info&NPERYEAR=360&id=$EMAIL">precipitation in the Netherlands (w/o Caribbean)</a>
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

<div class=alineakop>CPC analysis daily precipitation along the central Gulf Coast</div>
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">0.25&deg;</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_05_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">0.50&deg;</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/gridprcp_cpc_daily_us_10_%%%&STATION=pr_LA_cpc&TYPE=p&NPERYEAR=366&id=$EMAIL">1.0&deg;</a> series

<div class=alineakop>FLOR daily series</div>
Precipitation along the Gulf Coast in FLOR transient runs 1861-2100: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long.18610101-21001231.precip_LA_all_ce_%%%&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=366&id=$EMAIL">all grid points</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long-E%%.18610101-21001231.precip_LA_all_ce_3dymax&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.long-E%%.18610101-21001231.precip_LA_all_ce_3dymax_mo&STATION=pr_LA_FLOR_transient&TYPE=p&NPERYEAR=12&id=$EMAIL">spatial and monthly max of 3-day means</a>,
<br>Global mean temperature in these runs: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.long-E%%.1861-2100.t_ref_all_gm_ce&STATION=GMST_FLOR_transient&TYPE=i&NPERYEAR=1&id=$EMAIL">ensemble</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.long-ave.1861-2100.t_ref_all_gm_ce&STATION=GMST_FLOR_transient&TYPE=i&NPERYEAR=1&id=$EMAIL">mean</a>.
<br>
Same in the long 1860 conditions control run (chopped in pieces): 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_flor_control_1max3ave_max_%%&STATION=pr_LA_FLOR_control&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<br>Global mean temperature in these runs: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/Tglobal_flor_control_%%&STATION=GMST_FLOR_control&TYPE=i&NPERYEAR=1&id=$EMAIL">ensemble</a>,
<br>Ni&ntilde;o3.4 in these runs: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34_flor_control_%%&STATION=Nino34_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">ensemble</a>,
detrended: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_flor_control_%%&STATION=Nino34detrended_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">ensemble</a>,
<br>SST 30&deg;S-30&deg;N: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_30ns_flor_control_%%&STATION=SST_30S30N_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">ensemble</a>,
<br>Gulf: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_gulf_flor_control_%%&STATION=SST_Gulf_FLOR_control&TYPE=i&NPERYEAR=12&id=$EMAIL">ensemble</a>,

<div class=alineakop>HiFLOR daily series</div>
Daily precipitation along the Gulf Coast in hiFLOR control runs per grid box:
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1860-Ctl.00010101-02001231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1860&TYPE=p&NPERYEAR=366&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1940-Ctl.00010101-00761231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1940&TYPE=p&NPERYEAR=366&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1990-Ctl.00010101-03011231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_1990&TYPE=p&NPERYEAR=366&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.2015-Ctl.00010101-00701231.precip_LA_all_ce_%%%&STATION=pr_LA_hiFLOR_2015&TYPE=p&NPERYEAR=366&id=$EMAIL">2015</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_conc_%%%&STATION=pr_LA_hiFLOR_conc&TYPE=p&NPERYEAR=366&id=$EMAIL">concatenated</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_conc_%%%_max1_3v&STATION=pr_LA_hiFLOR_conc_max1_3v&TYPE=p&NPERYEAR=1&id=$EMAIL">concatenated annual max of 3-day precip</a>.
<br>
Annual max of 3-day precip of HiFLOR spatially averaged over 2x2 grid boxes 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1860-Ctl.00010101-02001231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1860&TYPE=p&NPERYEAR=366&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1940-Ctl.00010101-00761231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1940&TYPE=p&NPERYEAR=366&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.1990-Ctl.00010101-03011231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_1990&TYPE=p&NPERYEAR=366&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.2015-Ctl.00010101-00701231.precip_LA_all_ce_05_%%%&STATION=pr_LA_hiFLOR_2015&TYPE=p&NPERYEAR=366&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_05_conc_%%%&STATION=pr_LA_hiFLOR_05_conc_1max3ave&TYPE=p&NPERYEAR=1&id=$EMAIL">concatenated</a>.
<br>
Global mean temperature in 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1860-Ctl.0001-0200.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1860&TYPE=i&NPERYEAR=1&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1940-Ctl.0001-0075.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1940&TYPE=i&NPERYEAR=1&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1990-Ctl.0001-0301.t_ref_all_gm_ce&STATION=GMST_hiFLOR_1990&TYPE=i&NPERYEAR=1&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.2015-Ctl.0001-0070.t_ref_all_gm_ce&STATION=GMST_hiFLOR_2015&TYPE=i&NPERYEAR=1&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/Tglobal_hiflor_conc&STATION=GMST_hiFLOR_conc&TYPE=i&NPERYEAR=1&id=$EMAIL">concatenated</a>.
<br>
Ni&ntilde;o3.4 (detrended) in  
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1860&STATION=N34d_hiFLOR_1860&TYPE=i&NPERYEAR=12&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1940&STATION=N34d_hiFLOR_1940&TYPE=i&NPERYEAR=12&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_1990&STATION=N34d_hiFLOR_1990&TYPE=i&NPERYEAR=12&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_2015&STATION=N34d_hiFLOR_2015&TYPE=i&NPERYEAR=12&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_n34d_hiflor_conc&STATION=N34d_hiFLOR_conc&TYPE=i&NPERYEAR=12&id=$EMAIL">concatenated</a>.
<br>
SST Gulf in  
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1860-Ctl.000101-020012.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1860&TYPE=i&NPERYEAR=12&id=$EMAIL">1860</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1940-Ctl.000101-007512.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1940&TYPE=i&NPERYEAR=12&id=$EMAIL">1940</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.1990-Ctl.000101-030112.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_1990&TYPE=i&NPERYEAR=12&id=$EMAIL">1990</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos.2015-Ctl.000101-007012.t_surf_all_gulf_ce&STATION=30S30N_hiFLOR_2015&TYPE=i&NPERYEAR=12&id=$EMAIL">2015</a>.
<a href="getindices.cgi?WMO=GFDLData/Louisiana/sst_gulf_hiflor_conc&STATION=30S30N_hiFLOR_conc&TYPE=i&NPERYEAR=12&id=$EMAIL">concatenated</a>.

<div class=alineakop>HiFLOR daily series</div>
Precipitation along the Gulf Coast in HiFLOR transient runs 1971-2015 nudged to observed SST: 
<a href="getindices.cgi?WMO=GFDLData/Louisiana/prcp_hiflor_05_sst_%%%&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=366&id=$EMAIL">all 2&times;2 averaged grid points</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.sst-E%%.19710101-20151231.precip_LA_all_ce_3dymax&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=1&id=$EMAIL">spatial and annual max of 3-day means</a>,
<a href="getindices.cgi?WMO=GFDLData/Louisiana/atmos_daily.sst-E%%.19710101-20151231.precip_LA_all_ce_3dymax_mo&STATION=pr_LA_HiFLOR_sst&TYPE=p&NPERYEAR=12&id=$EMAIL">spatial and monthly max of 3-day means</a>.

<div class=alineakop>EC-Earth 2.3 T799 daily series</div>
Precipitation along the Gulf Coast in FutureWeather runs: 
<a href="select.cgi?field=pr_futureweather_gulfcoast&id=$EMAIL">gridded daily data</a>,

<div class=alineakop>2017 Europe June heat series</div>
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
<p>
<a href="getindices.cgi?WMO=KNMI14Data/Tmed/tasmax_8-24E_36-48N_muladdcorr_ydrun_retrend_%%&STATION=EC-EARTH_biascorr_Tmax_8-24E_36-48N&TYPE=t&NPERYEAR=366&id=$EMAIL">EC-Earth 2.3 T159 Tmax 36-48&deg;N, 8-24&deg;E, bias-corrected (mean and variance)</a>

EOF

. ./myvinkfoot.cgi
