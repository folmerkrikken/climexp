#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
if [ -z "$EMAIL" ]; then
  EMAIL=someone@somewhere
fi

. ./myvinkhead.cgi "KNMI ERS scatterometer re-analysis" "Data" "index,follow"

cat <<EOF
<div class="kalelink">

<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<div class="alineakop">Monthly gridded fields</div>
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="4">Straight averages (no interpolation)</th></tr>
EOF

fgrep sos ./selectfield_obs.html | sed -e "s/EMAIL/$EMAIL/"

cat <<EOF
<tr><td colspan="4"><input type="submit" class="formbutton" value="Select field"></td></tr>
</table>
</form>

<div class="alineakop">6-hourly gridded fields</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
EOF

. ./select6hourlyfield_sos.cgi
cat <<EOF
<tr><td colspan="11"><input type="submit" class="formbutton" value="Select field"></td>
</tr>
</table>

</form>

</div>

<div class="alineakop">Along-track data</div>
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr><th colspan="3">ASCII data per year</th></tr>
EOF
for file in SOS/ers_stress/*.txt.bz2
do
  yr=`basename $file .txt.bz2 | cut -b 4-`
  size=`wc -c $file | awk '{print $1}'`
  echo "<tr><td>$yr</td><td><a href=\"$file\" title=\"wind and wind stress for $yr\"><img src=/images/download.gif border=0 alt=\"wind and wind stress for $yr\"></a></td><td>$(($size / 1048576)) MB</td></tr>"
done
echo '</table>'
echo 'NB. In 1995 (20 and 24 april) there are duplicates that have not yet been removed.'
echo '<p>This work was supported by the <a href="http://www.cmsaf.eu/" target="_new">EUMETSAT Climate Monitoring-SAF</a>'
. ./myvinkfoot.cgi
