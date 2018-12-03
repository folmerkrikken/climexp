#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

# check if a search engine, if so set user to anonymous
. ./searchengine.cgi

. ./read_getstations.cgi
[ -n "$lon" ] && FORM_lon=$lon
[ -n "$lat" ] && FORM_lat=$lat

. ./myvinkhead.cgi "Select a monthly time series" "Historical observations" "index,follow"

###cat news.html
cat <<EOF
<form action="getstations.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<a name="get"></a>
<div class="kalelink">
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr>
<th align="left">GHCN-M (adjusted)</th>
<th align="left">GHCN-M (all)</th>
<th align="left">other</th>
</tr><tr>
<td>
<input type="radio" class="formradio" name="climate" value="precipitation" $climate_precipitation>precipitation <a href="http://www.ncdc.noaa.gov/ghcnm/v2.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="precipitation_all" $climate_precipitation_all>precipitation <a href="http://www.ncdc.noaa.gov/ghcnm/v2.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<a href="javascript:pop_page('help/psmsl.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a><input type="radio" class="formradio" name="climate" value="sealev" $climate_sealev>PSMSL sealevel
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="temperature" $climate_temperature>mean temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="temperature_all" $climate_temperature_all>mean temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="sealevel" $climate_sealevel>sealevel (<a href="http://ilikai.soest.hawaii.edu/UHSLC/jasl.html"
target="_new">JASL</a>)
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="min_temperature" $climate_min_temperature>minimum temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="min_temperature_all" $climate_min_temperature_all>minimum temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="runoff" $climate_runoff>world river discharge (<a href="http://www.RiVDis.sr.unh.edu/">RivDis</a>)
</td></tr><tr><td>
<input type="radio" class="formradio" name="climate" value="max_temperature" $climate_max_temperature>maximum temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="max_temperature_all" $climate_max_temperature_all>maximum temperature <a href="http://www.ncdc.noaa.gov/ghcnm/v3.php" target=_new><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
</td><td>
<input type="radio" class="formradio" name="climate" value="streamflow" $climate_streamflow>USA river discharge (<a href="http://water.usgs.gov/pubs/wri/wri934076/1st_page.html"
target="_new">HCDN</a>)
</td></tr><tr><td>
&nbsp;
</td><td>
<input type="radio" class="formradio" name="climate" value="sealevel_pressure" $climate_sealevel_pressure>sealevel pressure
</td><td>
<input type="radio" class="formradio" name="climate" value="eu_sealevel_pressure" $climate_eu_sealevel_pressure>european SLP (<a href="advice.cgi?id=$EMAIL" target="_new">ADVICE</a>)
</td></tr><tr><td>
(<a href="allstationsform.cgi?id=$EMAIL">full lists</a>)
</td><td>
&nbsp;
</td><td>
<input type="radio" class="formradio" name="climate" value="snow" $climate_snow>N-America snowcourses (<a href="http://www.wcc.nrcs.usda.gov/snowcourse/" target="_new">NRCS</a>)
</td></tr><tr><th colspan="3"><a href="javascript:pop_page('help/selectstation.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>Select stations
</th></tr><tr><td colspan="3">
<ul><li>stations with a name containing <input type="text" class="forminput" name="name" size=10 value="$FORM_NAME"></ul>
</td></tr><tr><td colspan="3">
<ul><li><input type="$number" min=1 class="forminput" name="num" $textsize3 value="${FORM_num:-10}"> stations near 
<input type="$number" step=any class="forminput" name="lat" $textsize4 value="$FORM_lat">&deg;N, 
<input type="$number" step=any class="forminput" name="lon" $textsize4 value="$FORM_lon">&deg;E (<a href="showmap.cgi?id=$EMAIL&scale=monthly">select on world map</a>)</ul>
</td></tr><tr><td colspan="3">
<ul><li>all stations in the region 
<input type="$number" step=any class="forminput" name="lat1" $textsize4 value="$FORM_lat1">&deg;N -
<input type="$number" step=any class="forminput" name="lat2" $textsize4 value="$FORM_lat2">&deg;N, 
<input type="$number" step=any class="forminput" name="lon1" $textsize4 value="$FORM_lon1">&deg;E - 
<input type="$number" step=any class="forminput" name="lon2" $textsize4 value="$FORM_lon2">&deg;E</ul>
</td></tr><tr><td colspan="3">
<ul><li>the stations with station numbers <br>
 <textarea class="forminput" name="list" rows="2" cols="35">
# lon1 lon2 lat1 lat2 (optional)
station number (one per line)</textarea></ul>
</td></tr><tr><th colspan="3">
<a href="javascript:pop_page('help/timedistance.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>Time, distance
</th></tr><tr><td colspan=3>
At least <input type="$number" class="forminput" name="min" $textsize3 value="${FORM_min:-10}">years of data in the
<select name="sum" class="forminput">
<option value="1" $sum_1>monthly
<option value="2" $sum_2>2 month
<option value="3" $sum_3>3 month
<option value="4" $sum_4>4 month
</select>
season starting in
<select name="month" class="forminput">
<option value="-1" $month_m1>any month
<option value="0" $month_0>all months
<option value="1" $month_1>Jan
<option value="2" $month_2>Feb
<option value="3" $month_3>Mar
<option value="4" $month_4>Apr
<option value="5" $month_5>May
<option value="6" $month_6>Jun
<option value="7" $month_7>Jul
<option value="8" $month_8>Aug
<option value="9" $month_9>Sep
<option value="10" $month_10>Oct
<option value="11" $month_11>Nov
<option value="12" $month_12>Dec
</select> in years
<input type="$number" class="forminput" name="yr1" $textsize4 value="${FORM_yr1}">-<input type="$number" class="forminput" name="yr2" $textsize4 value="${FORM_yr2}">
</td></tr><tr><td colspan=3>
At least <input type="$number" step=any class="forminput" name="dist" $textsize4 value="$FORM_dist">&deg; apart and with 
<input type="$number" step=any class="forminput" name="elevmin" $textsize4 value="$FORM_elevmin">m
&lt; elevation &lt;
<input type="$number" step=any class="forminput" name="elevmax" $textsize4 value="$FORM_elevmax">
</td></tr><tr><td colspan=3>
<input type="submit" class="formbutton" value="Get stations">
<input type="reset" class="formbutton" value="Clear Form" align="right">
</td><tr>
</table>
</div>
</form>
EOF

. ./myvinkfoot.cgi

