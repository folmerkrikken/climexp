#!/bin/bash
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

if [   $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 \
    -o $EMAIL = e279dd4de035b5fd9edc95ba4df755f7 \
    -o $EMAIL = bd113ded9265e569c369d53ff59bf69a \
    -o $EMAIL = f9646e78b5dbcaee3d001eb713252e3e ]; then
    sed -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL\&field=\1">/g' \
        -e 's:,:</a>,:g' \
        -e 's:</td><td><a href=":</a></td><td><a href=":g' \
        -e "s/EMAIL/$EMAIL/g" \
        ./selectfield_obs_hidden.html
fi

cat <<EOF
</table>
The date "now" means that I update the field whenever I need it or someone requests it.
EOF

. ./myvinkfoot.cgi
