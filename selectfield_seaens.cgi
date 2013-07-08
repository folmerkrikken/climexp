#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Seasonal forecasts full ensembles" "index,nofollow"
cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realTable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select ensemble">
Choose an ensemble and press this button</td></tr>
EOF

cat ./selectfield_seaens.html
echo '</table>'

. ./myvinkfoot.cgi
