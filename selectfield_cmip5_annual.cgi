#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select an annual field" "CMIP5 extremes" "index,nofollow"

cat <<EOF
<div class="inhoudsopgave">
<div class="inhoudlink"><a href="#mix">Periods, days above/below thresholds</a></div>
<div class="inhoudlink"><a href="#prcp">Precipitation extremes</a></div>
<div class="inhoudlink"><a href="#temp">Temperature extrems</a></div>
</div>

<div class="kalelink">
Tne annual extremes of the daily CMIP5 data have been obtained from the <a href="http://www.cccma.ec.gc.ca/data/climdex/climdex.shtml" target=_new>ETCCDI extremes indices archive</a> at the <a href="http://www.ec.gc.ca/ccmac-cccma/default.asp?lang=En" target=_new>Canadian Centre for Climate Modelling and Analysis</a>.
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="11"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

sed -e "s/EMAIL/$EMAIL/" ./selectfield_cmip5_annual.html
echo '</table>'

. ./myvinkfoot.cgi
