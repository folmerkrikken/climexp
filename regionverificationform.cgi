#!/bin/bash
. ./httpheaders_nocache.cgi
. ./init.cgi

DIR=`pwd`
. ./getargs.cgi

# check email address
. ./checkemail.cgi
# no robots
. ./nosearchengine.cgi

echo `date` "$EMAIL ($REMOTE_ADDR) region $FORM_field" >> log/log

# start real work
. ./queryfield.cgi
eval `bin/getunits.sh $file`

. ./myvinkhead.cgi "Field verification" "$kindname $climfield" ""

if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname $climfield from $UNITS to $NEWUNITS"
fi

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.field.$NPERYEAR ]; then
      savefield=$FORM_field
      eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' ./prefs/$EMAIL.field.$NPERYEAR`
      oldfield=$FORM_field
      FORM_field=$savefield
  fi
  if [ -f ./prefs/$EMAIL.verification.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' ./prefs/$EMAIL.verification.$NPERYEAR`
  fi
fi

. ./getfieldtype.cgi

echo '<form action="regionverification.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"
echo "<table class=realtable width=\"100%\" border=0 cellspacing=0 cellpadding=0>"
echo "<tr><th colspan="4">Verifying $field_type field</th></tr>"
egrep "[^A-Za-z]$field_type" selectfield_obs.html  | sed -e "s/FORM_EMAIL/$EMAIL/" -e "s/=\"$oldfield\"/=\"$oldfield\" checked/"
fgrep "$field_type" selectfield_rea1.html | sed -e "s/EMAIL/$EMAIL/" -e "s/=\"$oldfield\"/=\"$oldfield\" checked/"
. $DIR/selectuserfield.cgi | sed -e "s/EMAIL/$EMAIL/" -e "s/=\"$oldfield\"/=\"$oldfield\" checked/"
if [ -n "$ENSEMBLE" ]; then
  echo "<tr><td>$field_type</td><td><input type=\"radio\" class=\"formradio\" name=\"field\" value=\"perfectmodel\">perfect model</td><td>&nbsp;</td><td>&nbsp;</td></tr>"
fi
echo "</table>"

. $DIR/choose_mapverification.cgi
. $DIR/choose_verification.cgi
. $DIR/choose_threshold.cgi
cat <<EOF

<p><div class="formheader">Area</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
EOF
intable=true
. ./plotoptions.cgi
if [ -n "$LSMASK" ]; then
  echo "<tr><td>Land-sea mask:<td>one day I\'ll implement a land-sea mask"
else
  echo "<tr><td>Land-sea mask:<td>Land/sea mask not yet available"
fi
cat <<EOF
</table>
<p><div class="formheader">Options</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
EOF
timeseries="forecast"
index="observations"
justonemonth="T"
ONLYONE=true
VERIF=true
NAME="both obs and fcst"
. ./commonoptions.cgi
. $DIR/verifoptions2.cgi
echo '</table></div></form>'

. ./myvinkfoot.cgi
