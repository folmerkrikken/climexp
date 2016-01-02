#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi

. ./queryfield.cgi
if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12
fi

cat <<EOF
Content-Type: text/html


EOF
. ./myvinkhead.cgi "Project $FORM_variable on another field" "$kindname $climfield" "noindex,nofollow"

cat <<EOF
<form action="patternfield.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="patfile" value="$FORM_patfile">
<input type="hidden" name="variable" value="$FORM_variable">
<input type="hidden" name="month" value="$FORM_month">
<input type="hidden" name="field2" value="$FORM_field">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th><input class=formbutton type="submit" value="Project">
<th colspan=3>Select a field from the long list below and press this button
<tr><td>Valid points:<td colspan=3><input type="$number" name="minfac" $textsize2 value="50">%
EOF
echo '<tr><th colspan="4">Observations</th></tr>'
sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="8">Reanalyses</th></tr>'
cat selectfield_rea.html
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
cat selectfield_sea.html
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="13">Seasonal forecasts full ensembles</th></tr>'
cat selectfield_seaens.html
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="15">Scenario runs</th></tr>'
fgrep -v getindices selectfield_ipcc.html
echo '</table>'

. $DIR/selectuserfield.cgi

. ./myvinkfoot.cgi
