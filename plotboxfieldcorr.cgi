#!/bin/sh

echo "Content-Type:text/html"
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi

# check email address
. ./checkemail.cgi

myname=`basename $0 .cgi`
if [ "$myname" = "plotboxfieldcorr_obs" ]; then
  NO_REA=true
  NO_SEA=true
  NO_USE=true
  anotherfield="an observation field"
elif [ "$myname" = "plotboxfieldcorr_rea" ]; then
  NO_OBS=true
  NO_SEA=true
  NO_USE=true
  anotherfield="a reanalysis field"
elif [ "$myname" = "plotboxfieldcorr_sea" ]; then
  NO_OBS=true
  NO_REA=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "plotboxfieldcorr_use" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  anotherfield="a user-defined field"
else
  anotherfield="a field"
fi

. ./myvinkhead.cgi "Plot of correlations with $anotherfield" "$timescale $extraname$climate stations" "noindex,nofollow"

echo '<form action="correlatebox.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"email\" value=\"$email\">"
echo "<input type=\"hidden\" name=\"climate\" value=\"$timescale $extraname$climate\">"
echo "<input type=\"hidden\" name=\"prog\" value=\"$prog\">"
echo "<input type=\"hidden\" name=\"extraargs\" value=\"$extraargs\">"
echo "<input type=\"hidden\" name=\"listname\" value=\"$listname\">"

. ./selectfieldform.cgi

cat <<EOF
<div class="formheader">Choose variable</div>
<div class="formbody">
EOF
. ./choosevariable.cgi
cat <<EOF
at points with at least <input type="$number" name="minnum" $textsize3> valid 
years/months (or <input type=\"$number\" name=\"minfac\" value=\"$FORM_minfac\" $textsize2>%)<br>
Take 
<select name="intertype">
<option value="nearest">nearest grid point</option>
<option value="interpolated">interpolated</option>
</select> field value
</div>
EOF

timeseries="timeseries"
index="index"
justonemonth="true"
NAME=$climate
station="stations"
. $DIR/commonoptions.cgi

. ./myvinkfoot.cgi
