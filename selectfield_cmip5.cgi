#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "CMIP5 scenario runs" "index,nofollow"

cat <<EOF
<div class="inhoudsopgave">
<div class="inhoudlink"><a href="#surface">Surface variables</a></div>
<div class="inhoudlink"><a href="#radiation">Radiation variables</a></div>
<div class="inhoudlink"><a href="#ocean">Ocean, ice &amp; upper air variables</a></div>
<div class="inhoudlink"><a href="#emissions">Emissions</a></div>
</div>

<div class="kalelink">
EOF
cat CMIP5_disclaimer.html
cat <<EOF
Global mean temperatures can be <a href="cmip5_indices.cgi?id=$EMAIL">analysed</a> or <a href="CMIP5/Tglobal/index.cgi?email=$EMAIL">downloaded</a> separately.
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

sed -e "s/EMAIL/$EMAIL/" ./selectfield_cmip5.html
echo '</table>'
cat selectfield_rcp.html | sed -e "s/EMAIL/$EMAIL/g"

. ./myvinkfoot.cgi
