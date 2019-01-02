#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Scenario runs" "index,nofollow"
cat <<EOF
<div class="kalelink">
These are the model runs made public after publication of the <a href="https://www.ipcc.ch/report/ar3/wg1/">IPCC WG1 Third Assessment Report</a> in 2001. The links on this page may no longer work.
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

cat ./selectfield_co2.html

. ./myvinkfoot.cgi
