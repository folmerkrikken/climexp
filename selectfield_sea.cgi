#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Seasonal forecasts" "index,nofollow"
cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realTable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

echo '<tr><th colspan=13>FULL ENSEMBLES</th>'
cat ./selectfield_seaens.html
echo '<tr><th colspan=13>ENSEMBLES MEANS</th>'
cat ./selectfield_sea.html
echo '</table>'

. ./myvinkfoot.cgi
