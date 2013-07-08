#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`

. ./getargs.cgi
# check email address
. ./checkemail.cgi
# no robots
. ./nosearchengine.cgi

echo `date` "$EMAIL ($REMOTE_ADDR) difffieldform $FORM_field" >> log/log

# start real work
. ./queryfield.cgi

. ./myvinkhead.cgi "Plot difference with another field" "$kindname $climfield" "noindex,nofollow"

eval `bin/getunits.sh $file`

if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname $climfield from $UNITS to $NEWUNITS"
fi

. ./getfieldtype.cgi

echo '<form action="difffield.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"NPERYEAR\" value=\"$NPERYEAR\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"
echo "<input type=\"hidden\" name=\"field_type\" value=\"$field_type\">"

echo "<table class=realtable border=0 width=451 cellspacing=0 cellpadding=0>"
echo "<tr><th colspan="4">Select a second $field_type field</th></tr>"
fgrep "$field_type" selectfield_obs.html | sed -e "s/EMAIL/$EMAIL/"
fgrep "$field_type" selectfield_rea1.html
fgrep -i "value=\"${VAR}_" selectfield_ipcc.html \
  | sed -e "s:^:<tr><td align=right>$VAR</td>:" \
        -e 's:align="center":align="left" colspan=3:' \
        -e 's:value="\([^"]*\)"></td>:value="\1">\1</td>:' \
        -e "s:$:</tr>:"
userdefined=`. ./selectuserfield.cgi | tail -n +2`
if [ -n "$userdefined" ]; then
  echo "<tr><td align=right>user<br>defined<td colspan=3>"
  echo "$userdefined"
fi
echo "<tr><td align="right">$VAR</td><td colspan=3><input type=\"radio\" name=\"field\" value=\"$FORM_field\">$kindname $climfield</td></tr>"
echo "</table>"

cat <<EOF

<p><div class="formheader">Area</div>
<div class="formbody">
<table width=451>
EOF

lsmask=yes
probmask=true
intable=true
. ./plotoptions.cgi
echo '</table></div>'

timeseries="field1"
index="field2"
###justonemonth="T"
. ./diffoptions.cgi

. ./myvinkfoot.cgi
