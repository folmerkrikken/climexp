#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "RCM runs" "index,nofollow"
cat <<EOF
<div class="kalelink">
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="9"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
<tr><td colspan="9">ENSEMBLES RT2b Europe with GCM boundary conditions 1950-2100<a href="wipefeet.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" align="right" alt="more information" border="0"></a></td><tr>
EOF

cat ENSEMBLES_RCM/rt2b.html

cat <<EOF
<tr><th colspan=9>&nbsp;</th></tr>
<tr><td colspan="9">ENSEMBLES RT3 Europe with ERA-40 boundary conditions 1960-2000 <a href="wipefeet.cgi?http://ensemblesrt3.dmi.dk" target="_new"><img src="images/info-i.gif" align="right" alt="more information" border="0"></a></td><tr>
EOF
cat ENSEMBLES_RCM/rt3.html
echo '</table>'
###cat selectfield_co2.html
###sed -e "s/EMAIL/$EMAIL/" selectfield_challenge.html
###cat selectfield_rcp.html

. ./myvinkfoot.cgi
