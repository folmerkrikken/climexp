#!/bin/bash
. ./httpheaders_nocache.cgi
. ./init.cgi
. ./getargs.cgi
. ./searchengine.cgi

. ./myvinkhead.cgi "Select all monthly time series" "Historical observations" "index,follow"

cat <<EOF
<div class="kalelink">These 
links will give <b>long</b> lists of all stations in the
databases.  They will take a few minutes to generate and even longer
to transmit and display.  Alternatively, you can <a
href="/selectstation.cgi?id=$EMAIL">search for stations</a> by name,
coordinates, elevation, and number of years with data.

<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr>
<th align="left"><a href="javascript:pop_page('help/ghcn.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>GHCN (adjusted)</th><th align="left"><a href="javascript:pop_page('help/ghcn.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>GHCN (all)</th><th align="left">other</th>
</tr><tr>
<td>
<a href="allstations.cgi?id=$EMAIL&climate=precipitation&n=12">precipitation 
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=precipitation_all&n=12">precipitation 
</td><td>
<a href="javascript:pop_page('help/psmsl.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a><a href="allstations.cgi?id=$EMAIL&climate=sealev&n=12">PSMAL sealevel
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=temperature&n=12">mean temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=temperature_all&n=12">mean temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=sealevel&n=12">sealevel (JASL)
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=min_temperature&n=12">minimum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=min_temperature_all&n=12">minimum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=runoff&n=12">world river discharge (RivDis)
</td></tr><tr><td>
<a href="allstations.cgi?id=$EMAIL&climate=max_temperature&n=12">maximum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=max_temperature_all&n=12">maximum temperature
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=streamflow&n=12">USA river discharge (HCDN)
</td></tr><tr><td>
&nbsp;
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=sealevel_pressure&n=12">sealevel pressure
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=eu_sealevel_pressure&n=12">european SLP (ADVICE)
</td></tr><tr><td>
&nbsp;
</td><td>
&nbsp;
</td><td>
<a href="allstations.cgi?id=$EMAIL&climate=snow&n=12">N-American snow course (NRCS)</a>
</td></tr>
</table>
</div>
EOF

. ./myvinkfoot.cgi
