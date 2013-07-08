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

<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>
<tr><th colspan="3">Select a field by following its link</td></tr>
</table>
<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id=EMAIL&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href="wipefeet:</a></td><td><a href="wipefeet:g' \
    -e "s/EMAIL/$EMAIL/" \
    selectdailyfield_obs.html
cat <<EOF
</table>
<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id=EMAIL&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href="wipefeet:</a></td><td><a href="wipefeet:g' \
    -e "s/EMAIL/$EMAIL/" \
    selectdailyfield_rea.html
cat <<EOF
</table>
<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"><a:<a href="select.cgi?id=EMAIL&field=\1">x</a>,<a:g' \
    -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id=EMAIL&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href="wipefeet:</a></td><td><a href="wipefeet:g' \
    -e "s/EMAIL/$EMAIL/" \
    selectdailyfield_ipcc.html
cat <<EOF
</table>
</form>
EOF

. ./myvinkfoot.cgi
