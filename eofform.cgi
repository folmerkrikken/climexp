#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

# off limits for robots
. ./nosearchengine.cgi
# check email address
. ./checkemail.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) $FORM_field" >> log/log

if [ $EMAIL != somone@somewhere ]; then
  def=./prefs/$EMAIL.eofs
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

. ./myvinkhead.cgi "Compute EOFs" "$kindname $climfield" "noindex,nofollow"

eval `bin/getunits.sh $file`

cat <<EOF
<form action="eof.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<div class="formheader">Choose how to compute the EOFs</div>
<div class="formbody">
<table width="100%">
<tr><td>Compute:<td>first <input type="$number" min=1 max=13 step=1 name="neof" size="2" style="width: 4em;" value="${FORM_neof:-4}"> EOFs (<input type="checkbox" class="formcheck" name="normsd" $normsd_checked>normalized to s.d.)<td><a href="javascript:pop_page('help/eofnormalise.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Average:<td><input type="$number" min=1 step=1 class="forminput" name="avex" $textsize2 value="${FORM_avex:-1}">lon &times;<input type="$number" min=1 step=1 class="forminput" name="avey" $textsize2 value="${FORM_avey:-1}">lat grid points
<br>with at least <input type="$number" class="forminput" name="minfac" $textsize2 value="${FORM_minfac}">% valid points<td><a href="javascript:pop_page('help/eofaverage.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Normalize:<td><input type="radio" class="formradio" name="normalization"value="maxspace" $maxspace_checked">spatial maximum <input type="radio" class="formradio" name="normalization" value="varspace" "$varspace_checked">spatial variance<br><input type="radio" class="formradio" name="normalization"value="maxtime" $maxtime_checked">time series maximum <input type="radio" class="formradio" name="normalization" value="vartime" "$vartime_checked">time series variance<td><a href="javascript:pop_page('help/eofnormaliseoutput.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
EOF
latlononly="true"
intable=true
lsmask=yes
. ./plotoptions.cgi
ONLYONE=true
NAME=field
. ./commonoptions.cgi
echo "<tr><td colspan=2><input type=\"submit\" class=\"formbutton\" value=\"Compute EOFs\">"
###echo "<td align=\"right\"><input type=\"reset\" class=\"formbutton\" value=\"Clear Form\">"
echo "</table>"
echo '</div>'
echo '</form>'

. ./myvinkfoot.cgi
