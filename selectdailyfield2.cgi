#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

. ./myvinkhead.cgi "Select a daily field" "" "index,follow"

cat <<EOF
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr><th colspan="3">Select a field by following its link (<a href="selectdailyfield.cgi?id=$EMAIL">alternative</a>)</td></tr>
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id='$EMAIL'\&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id='$EMAIL'\&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href=":</a></td><td><a href=":g' \
    selectdailyfield_obs.html
cat <<EOF
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id='$EMAIL'\&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id='$EMAIL'\&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href=":</a></td><td><a href=":g' \
    selectdailyfield_rea.html
cat <<EOF
</table>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr><th colspan=13>Note that these are vintage CMIP3 models from circa 2004. More modern daily climate model data is available under <a href="selectfield_att.cgi?id=$EMAIL">Attribution runs</> 
EOF
sed -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"><a:<a href="select.cgi?id='$EMAIL'\&field=\1">x</a>,<a:g' \
    -e 's:<input type="radio" class="formradio" name="field" value="\([^"]*\)"></td>:<a href="select.cgi?id='$EMAIL'\&field=\1">x</a>:g' \
    -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id='$EMAIL'\&field=\1">/g' \
    -e 's:,:</a>,:g' \
    -e 's:</td><td><a href=":</a></td><td><a href=":g' \
    selectdailyfield_ipcc.html
cat <<EOF
</table>
EOF

. ./myvinkfoot.cgi
