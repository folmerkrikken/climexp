#!/bin/sh
# sourced from other scripts, just for nice colouring in emacs...
#
# show a selection of time series with this e-mail address and nperyear

. ./nperyear2timescale.cgi

###echo "<div class=\"formbody\">"
echo "<table class=\"realtable\" width=451 border=0 cellpadding=0 cellspacing=0>"
echo "<tr><th><a href=\"javascript:pop_page('help/systemseries.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>System-defined ${timescale}timeseries</th></tr><tr><td>"
if [ -z "$NPERYEAR" -o "$NPERYEAR" = 12 ]; then
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"nino12\">NINO1+2"
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"nino3\">NINO3"
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"nino34\">NINO3.4"
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"nino4\">NINO4"
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"soi\">SOI"
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"nao\">NAO"
fi
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"time\">time"
echo "</td></tr><tr><th><a href=\"javascript:pop_page('help/userseries.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>User-defined ${timescale}timeseries</th></tr><tr><td>"
forbidden='!`;&|'
i=0
for file in ./data/*$NPERYEAR.$EMAIL.inf
do
    # if no match it loops once with the unexpanded *.inf...
    if [ -s "$file" ]; then
	let i=$i+1
	datfile=`head -1 $file | tr $forbidden '?'`
	st=`head -2 $file | tail -1 | tr '_' ' '`
	wm=`tail -1 $file`
	ty=`basename $datfile .dat`
	ty=`basename $ty $wm`
	echo "<input type=\"checkbox\" class=\"formcheck\" name=\"myindex$i\" value=\"$file\">$st ($ty$wm)<br>"
    fi
done
echo "</td></tr></table>"
###echo "</div>"
