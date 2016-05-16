#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "CORDEX scenario runs" "index,nofollow"

cat <<EOF

<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

sed -e "s/EMAIL/$EMAIL/" ./selectfield_cordex.html
echo '</table>'

. ./myvinkfoot.cgi
