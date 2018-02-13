#!/bin/sh

. ./httpheaders_nocache.cgi

DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
# check email address
. ./checkemail.cgi
# off limits for search engines
. ./nosearchengine.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) svdform $FORM_field" >> log/log

if [ $EMAIL != somone@somewhere ]; then
  def=./prefs/$EMAIL.svds
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z]*=[0-9a-zA-Z]*;$' $def`
  fi
fi

if [ -n "$FORM_normsd" ]; then
  normsd_checked=checked
fi
case "${FORM_normalization:-maxspace}" in
varspace) varspace_checked=checked;;
maxtime)  maxtime_checked=checked;;
vartime)  vartime_checked=checked;;
*)        maxspace_checked=checked;;
esac

# start real work
. ./queryfield.cgi

myname=`basename $0 .cgi`
if [ "$myname" = "svdform_obs" ]; then
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_CMIP5=true
  NO_USE=true
  anotherfield="an observation field"
elif [ "$myname" = "svdform_rea" ]; then
  NO_OBS=true
  NO_SEA=true
  NO_CO2=true
  NO_CMIP5=true
  NO_USE=true
  anotherfield="a reanalysis field"
elif [ "$myname" = "svdform_sea" ]; then
  NO_OBS=true
  NO_REA=true
  NO_CO2=true
  NO_CMIP5=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "svdform_co2" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_CMIP5=true
  NO_USE=true
  anotherfield="a CMIP3+ scenario field"
elif [ "$myname" = "svdform_cmip5" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_USE=true
  anotherfield="a CMIP5 scenario field"
elif [ "$myname" = "svdform_use" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_CMIP5=true
  anotherfield="a user-defined field"
else
  anotherfield="another field"
fi

. ./myvinkhead.cgi "SVD with $anotherfield" "$kindname $climfield" "noindex,nofollow"

echo "<font color=\"#FF0000\">SVDs are new and have not yet been tested well.  Please report any problems to <a href=\"http://www.knmi.nl/\">me</a></font><p>"

echo '<form action="svd.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"

if [ -z "$NO_OBS" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="3">Observations</th></tr>'
  sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
  echo '</table>'
fi
if [ -z "$NO_REA" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="8">Reanalyses</th></tr>'
  cat selectfield_rea.html
  echo '</table>'
fi
if [ -z "$NO_SEA" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
  cat selectfield_sea.html
  echo '</table>'
fi
if [ -z "$NO_CO2" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="15">CMIP3+ scenario runs</th></tr>'
  fgrep -v getindices selectfield_ipcc.html
  echo '</table>'
fi
if [ -z "$NO_CMIP5" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="15">CMIP5 scenario runs</th></tr>'
  fgrep -v getindices selectfield_cmip5.html
  echo '</table>'
fi
if [ -z "$NO_USE" ]; then 
 . selectuserfield.cgi
fi
cat <<EOF
<div class="formheader">Choose how to compute the SVDs</div>
<div class="formbody">
<table width="100%">
<tr><td>Compute:<td>first <input type="$number" style="width: 4em;" min=1 max=13 step=1 name="nsvd" size="2" value="${FORM_nsvd:-4}"> SVDs (<input type="checkbox" class="formcheck" name="normsd" $normsd_checked>normalized to s.d.)<td><a href="javascript:pop_page('help/svdnormalise.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Average:<td><input type="$number" min=1 step=1 class="forminput" name="avex" $textsize2 value="${FORM_avex:-1}">lon &times;<input type="$number" min=1 step=1 class="forminput" name="avey" $textsize2 value="${FORM_avey:-1}">lat grid points of the first field
<tr><td>&nbsp;<td><input type="$number" min=1 step=1 class="forminput" name="altavex" $textsize2 value="${FORM_altavex:-1}">lon &times;<input type="$number" min=1 step=1 class="forminput" name="altavey" $textsize2 value="${FORM_altavey:-1}">lat grid points of second field
<tr><td>Demand:<td>at least <input type="$number" class="forminput" name="minfac" $textsize value="${FORM_minfac}">% valid points<td><a href="javascript:pop_page('help/svdaverage.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Normalize:<td><input type="radio" class="formradio" name="normalization" value="maxspace" $maxspace_checked>spatial maximum <input type="radio" class="formradio" name="normalization" value="varspace" "$varspace_checked">spatial variance<br><input type="radio" class="formradio" name="normalization"value="maxtime" $maxtime_checked">time series maximum <input type="radio" class="formradio" name="normalization" value="vartime" "$vartime_checked">time series variance<td><a href="javascript:pop_page('help/svdnormaliseoutput.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
EOF
latlononly="true"
tworegions=true
intable=true
. ./plotoptions.cgi
echo "</table><p>"
NAME=field
station="$kindname $climfield"
timeseries="selected field"
index="second field"
norun=true
SUBMIT="Compute SVDs"
. ./commonoptions.cgi | egrep -v 'option.*[^a-z]:' | fgrep -v fix2

. ./myvinkfoot.cgi

