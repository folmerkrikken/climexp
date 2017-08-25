#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Observations" "index,follow"
cat <<EOF
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3">Select a field by following its link (<a href="selectfield_obs.cgi?id=$EMAIL">old list</a>)</td></tr>
EOF

sed -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL\&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href=":</a></td><td><a href=":g' \
    -e "s/EMAIL/$EMAIL/g" \
    ./selectfield_obs.html

cat <<EOF
</table>
The date "now" means that I update the field whenever I need it or someone requests it.
EOF

. ./myvinkfoot.cgi
