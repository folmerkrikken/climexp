#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Observations" "index,follow"
cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3"><input type="submit" class="formbutton" value="Select field"> Choose a field and press this button (<a href="selectfield_obs2.cgi?id=$EMAIL">alternative</a>)</td></tr>
EOF

sed -e "s/EMAIL/$EMAIL/" ./selectfield_obs.html

if [   $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 \
    -o $EMAIL = e279dd4de035b5fd9edc95ba4df755f7 \
    -o $EMAIL = bd113ded9265e569c369d53ff59bf69a \
    -o $EMAIL = f9646e78b5dbcaee3d001eb713252e3e ]; then
    sed -e "s/EMAIL/$EMAIL/" ./selectfield_obs_hidden.html
fi

cat <<EOF
</table>
</form>
The date "now" means that I update the field whenever I need it or someone requests it.
EOF

. ./myvinkfoot.cgi
