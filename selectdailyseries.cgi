#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./searchengine.cgi

DIR=`pwd`
tmpfile=/tmp/selectseries$$.html
if [ -z "$EMAIL" ]; then
  EMAIL=someone@somewhere
fi
base_url=`dirname $SCRIPT_NAME`

. ./read_getstations.cgi

. ./myvinkhead.cgi "Select a daily time series" "Historical observations" "index,follow"

cat <<EOF
<form action="getstations.cgi" method="POST">
<div class="kalelink">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr>
<th>
<a href="javascript:pop_page('help/ghcnd.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>GHCN-D v2
</th><th>
<a href="javascript:pop_page('help/ecad.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>pure ECA&amp;D
</th><th>
<a href="javascript:pop_page('help/ecad.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>blended ECA&amp;D
</th><th>
<a href="javascript:pop_page('help/hcdn.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>HCDN
</th></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="gdcnprcp" $climate_gdcnprcp>precipitation<br>
<input type="radio" class="formradio" name="climate" value="gdcnprcpall" $climate_gdcnprcp_all>precip+GTS
</td><td>
<input type="radio" class="formradio" name="climate" value="ecaprcp" $climate_ecaprcp>precipitation 
</td><td>
<input type="radio" class="formradio" name="climate" value="becaprcp" $climate_becaprcp>precipitation 
</td><td>
<input type="radio" class="formradio" name="climate" value="streamflowdaily" $climate_streamflowdaily>US runoff
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="gdcntave" $climate_gdcntave>average temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="ecatemp" $climate_ecatemp>mean temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="becatemp" $climate_becatemp>mean temperature
</td><td>
&nbsp;
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="gdcntmin" $climate_gdcntmin>minimum temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="ecatmin" $climate_ecatmin>minimum temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="becatmin" $climate_becatmin>minimum temperature
</td><td>
&nbsp;
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="gdcntmax" $climate_gdcntmax>maximum temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="ecatmax" $climate_ecatmax>maximum temperature
</td><td>
<input type="radio" class="formradio" name="climate" value="becatmax" $climate_becatmax>maximum temperature
</td><td>
&nbsp;
</td></tr><tr><td>
<!--
&nbsp;
</td><td>
<input type="radio" class="formradio" name="climate" value="ecatave" $climate_ecatave>mean temperature, if unavailable (tmin+tmax)/2
</td></tr><tr><td>
&nbsp;
</td><td>
 <input type="radio" class="formradio" name="climate" value="ecatdif" $climate_ecatdif>daily temperature range
</td></tr><tr><td>
-->
<input type="radio" class="formradio" name="climate" value="gdcnsnow" $climate_gdcnsnow>snowfall
</td><td>
 <input type="radio" class="formradio" name="climate" value="ecapres" $climate_ecapres>pressure
</td><td>
 <input type="radio" class="formradio" name="climate" value="becapres" $climate_becapres>pressure
</td><td>
&nbsp;
</td></tr><tr><td>
 <input type="radio" class="formradio" name="climate" value="gdcnsnwd" $climate_gdcnsnwd>snow depth
</td><td>
 <input type="radio" class="formradio" name="climate" value="ecasnow" $climate_ecasnow>snow depth
</td><td>
 <input type="radio" class="formradio" name="climate" value="becasnow" $climate_becasnow>snow depth
</td><td>
&nbsp;
</td></tr><tr><td>
(<a href="allstationsform_daily.cgi?id=$EMAIL">full lists</a>)
</td><td>
 <input type="radio" class="formradio" name="climate" value="ecaclou" $climate_ecaclou>cloud cover
</td><td>
 <input type="radio" class="formradio" name="climate" value="becaclou" $climate_becaclou>cloud cover
</td><td>
&nbsp;
</td></tr><tr><th colspan="4">
<a href="javascript:pop_page('help/selectstation.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0">Select</a>
</th></tr><tr><td colspan="4">
<ul><li>stations with a name containing <input type="text" class="forminput" name="name" size=10 value="$FORM_name"></ul>
</td></tr><tr><td colspan="4">
<ul><li><input type="$number" class="forminput" name="num" $textsize3 value="${FORM_num:-10}"> stations near 
<input type="$number" step=any class="forminput" name="lat" $textsize4 value="$FORM_lat">&deg;N, 
<input type="$number" step=any class="forminput" name="lon" $textsize4 value="$FORM_lon">&deg;E (<a href="showmap.cgi?id=$EMAIL&scale=daily">world map</a>)</ul>
</td></tr><tr><td colspan="4">
<ul><li>all stations in the region 
<input type="$number" step=any class="forminput" name="lat1" $textsize4 value="$FORM_lat1">&deg;N -
<input type="$number" step=any class="forminput" name="lat2" $textsize4 value="$FORM_lat2">&deg;N, 
<input type="$number" step=any class="forminput" name="lon1" $textsize4 value="$FORM_lon1">&deg;E - 
<input type="$number" step=any class="forminput" name="lon2" $textsize4 value="$FORM_lon2">&deg;E</ul>
</td></tr><tr><td colspan="4">
<ul><li>the stations with station numbers <br>
 <textarea name="list" rows="2" cols="35" class="forminput">
# lon1 lon2 lat1 lat2 (optional)
station number (one per line)</textarea></ul>
</td></tr><tr><th colspan="4">
<a href="javascript:pop_page('help/timedistance.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0">Time, distance</a>
</th></tr><tr><td colspan=4>
At least <input type="$number" class="forminput" name="min" $textsize3 value="${FORM_min:-10}">years of data
</td></tr><tr><td colspan=4>
At least <input type="$number" step=any class="forminput" name="dist" $textsize4 value="$FORM_dist">&deg; apart and with 
<input type="$number" step=any class="forminput" name="elevmin" $textsize4 value="$FORM_elevmin">m
&lt; elevation &lt;
<input type="$number" step=any class="forminput" name="elevmax" $textsize4 value="$FORM_elevmax">
</td></tr><tr><td colspan=4>
<input type="submit" class="formbutton" value="Get stations">
<input type="reset" class="formbutton" value="Clear Form" align="right">
</td><tr>
</table>
</div>
</form>

<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr><th colspan="3"><a href="javascript:pop_page('help/dutchdailydata.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0">Dutch daily data</th></tr>
<tr><td colspan="3">1901-now, <a
href="http://www.knmi.nl/klimatologie/daggegevens/download.cgi?language=eng">KNMI Climatological Service</a>.  These series have not
yet been homogenised. Homogenised daily precipitation series are available <a href="/PhomNL.cgi?id=$EMAIL">here</a> and monthly homogenised mean temperature series <a href="getdutchstations.cgi?id=$EMAIL&TYPE=temp_hom">here</a></td><tr>
<tr><td>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=tg">mean temperature</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=tn">minimum temperature</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=tx">maximum temperature</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=t1">min 10cm temperature</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=tw">max wet bulb temp</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=dr">precipitation duration</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=rh">precipitation (0-24)</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=rr">precipitation (8-8)</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=preciphom1910">precip (8-8) 1910- hom</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=preciphom1951">precip (8-8) 1951- hom</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=rx">max hourly precip (0-24)</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=ev">Makking evaporation</a><br>
</td><td>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=pg">mean surface pressure</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=pn">minimum surface pressure</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=px">maximum surface pressure</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=dd">prevailing wind direction</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=fg">daily mean windspeed</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=fh">maximum hourly windspeed</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=fn">minimum hourly windspeed</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=upx">maximum hourly potential wind</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<a href="getdutchstations.cgi?id=$EMAIL&TYPE=upx_land">land</a>,
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=upx_coast">coast</a>,
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=upx_sea">sea</a>)<br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=fx">maximum wind gust</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=dx">zonal wind direction</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=dy">meridional wind direction</a><br>
</td><td>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=td">max dew point temp</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=ug">mean relative humidity</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=un">minimum relative humidity</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=ux">maximum relative humidity</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=ng">cloud cover</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sq">sunshine duration</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sp">sunshine fraction</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=qq">global radiation</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=vn">minimum visibility</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=vx">maximum visibility</a><br>
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sd">snow depth (8-8)</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sdhom">(somewhat homogenised)</a><br>
</td></tr></table>
EOF
if [ ${EMAIL%knmi.nl} != $EMAIL ]; then
  cat <<EOF
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sw">global shortwave radiation</a>
(<a href="getdutchstations.cgi?id=$EMAIL&TYPE=sr">circulation-dependent</a>,
<a href="getdutchstations.cgi?id=$EMAIL&TYPE=si">-independent part</a>)
<br>
EOF
fi
. ./myvinkfoot.cgi
