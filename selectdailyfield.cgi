#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

. ./myvinkhead.cgi "Select a daily field" "" "index,follow"

cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">

<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr><td colspan="10"><input type="submit" class="formbutton" value="Select field"> Choose a field and press this button (<a href="selectdailyfield2.cgi?id=$EMAIL">alternative</a>)</td></tr>
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
cat selectdailyfield_obs.html
cat <<EOF
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
cat selectdailyfield_rea.html
cat <<EOF
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
cat selectdailyfield_ipcc.html
cat <<EOF
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
cat selectdailyfield_rcm.html
cat <<EOF
</table>
</form>
EOF

. ./myvinkfoot.cgi
