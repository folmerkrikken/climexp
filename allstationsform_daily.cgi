#!/bin/sh

echo "Content-Type:text/html"
echo
echo

. ./init.cgi
. ./getargs.cgi
. ./searchengine.cgi

. ./myvinkhead.cgi "Select all daily time series" "Historical observations" "index,follow"

cat <<EOF
These links will give <b>long</b> lists of all stations in the
databases.  They will take a few minutes to generate and even longer
to transmit and display.  Alternatively, you can <a
href="selectdailyseries.cgi?id=$EMAIL">search for stations</a> by name,
coordinates, elevation, and number of years with data.

<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr>
<th>
<a href="javascript:pop_page('help/ghcnd.shtml',568,450)">GHCN-D v2</a>
</th><th>
<a href="javascript:pop_page('help/ecad.shtml',568,450)">pure ECA&amp;D</a>
</th><th>
<a href="javascript:pop_page('help/ecad.shtml',568,450)">blended ECA&amp;D</a>
</th><th>
<a href="http://water.usgs.gov/pubs/wri/wri934076/1st_page.html"
target="_new">HCDN</a>
</th></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=gdcnprcp&n=366">precipitation<br>
<a href="allstations.cgi?id=$EMAIL&climate=gdcnprcpall&n=366">precip+GTS
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=ecaprcp&n=366">precipitation 
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=becaprcp&n=366">precipitation 
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=streamflowdaily&n=366">US runoff
</td></tr><tr><td>
&nbsp;</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=ecatemp&n=366">mean temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=becatemp&n=366">mean temperature
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=gdcntmin&n=366">minimum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=ecatmin&n=366">minimum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=becatmin&n=366">minimum temperature
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=gdcntmax&n=366">maximum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=ecatmax&n=366">maximum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=becatmax&n=366">maximum temperature
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=gdcnsnow&n=366">snow fall
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=ecapres&n=366">pressure
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=becapres&n=366">pressure
</td><td>
&nbsp;
</td></tr><tr><td>
 <a href="allstations.cgi?id=$EMAIL&climate=gdcnsnwd&n=366">snow depth
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=ecasnow&n=366">snow depth
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=becasnow&n=366">snow depth
</td><td>
&nbsp;
</td></tr><tr><td>
&nbsp;
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=ecaclou&n=366">cloud cover
</td><td>
 <a href="allstations.cgi?id=$EMAIL&climate=becaclou&n=366">cloud cover
</td><td>
&nbsp;
</td></tr>
</table>
EOF

. ./myvinkfoot.cgi
