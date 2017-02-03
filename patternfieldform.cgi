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
<th colspan=3>Select a field from the long list below and press this button:
monthly
<a href="#observations">observations</a>,
<a href="#reanalyses">reanalyses</a>,
<a href="#seasonal">seasonal forecasts</a>,
<a href="#cmip5">CMIP5 climate runs</a>,
daily
<a href="#daily_obs">observations</a>,
<a href="#daily_rea">reanalyses</a>,
<tr><td>Valid points:<td colspan=3><input type="$number" name="minfac" $textsize2 value="50">%
</table>
EOF
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="3"><a name="observations"></a>Observations</th></tr>'
sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="8"><a name="reanalyses"></a>Reanalyses</th></tr>'
cat selectfield_rea.html
echo '</table>'
###echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
###echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
###cat selectfield_sea.html
e###cho '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="13"><a name="seasonal"></a>Seasonal forecasts full ensembles</th></tr>'
cat selectfield_seaens.html
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="15"><a name="cmip5"></a>CMIP5 scenario runs</th></tr>'
fgrep -v getindices selectfield_ar5.html
echo '</table>'
###echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
###echo '<tr><th colspan="15">CMIP5 scenario runs</th></tr>'
###fgrep -v getindices selectfield_ipcc.html
###echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="9"><a name="daily_obs"></a>Daily observations</th></tr>'
fgrep -v Observations selectdailyfield_obs.html
echo '</table>'
echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
echo '<tr><th colspan="11"><a name="daily_rea"></a>Daily reanalyses</th></tr>'
fgrep -v Reanalyses selectdailyfield_rea.html
echo '</table>'

. ./selectuserfield.cgi

. ./myvinkfoot.cgi
