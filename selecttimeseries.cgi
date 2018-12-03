#!/bin/bash
# sourced from other scripts, just for nice colouring in emacs...
#
# show a selection of time series with this e-mail address and nperyear

. ./nperyear2timescale.cgi

###echo "<div class=\"formbody\">"
echo "<table class=\"realtable\" width=\"100%\" border=0 cellpadding=0 cellspacing=0>"
echo "<tr><th><a href=\"javascript:pop_page('help/systemseries.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>System-defined ${timescale}timeseries</th></tr><tr><td>"
if [ -z "$NPERYEAR" -o "$NPERYEAR" = 12 ]; then
    cat <<EOF  # coordinate links with 
<input type="checkbox" class="formcheck" name="nino3"><a href="getindices.cgi?WMO=NCDCData/ersst_nino3a&STATION=NINO3&TYPE=i&id=$EMAIL">NINO3</a>
<input type="checkbox" class="formcheck" name="nino34"><a href="getindices.cgi?WMO=NCDCData/ersst_nino3.4a&STATION=NINO3.4&TYPE=i&id=$EMAIL">NINO3.4</a>
<input type="checkbox" class="formcheck" name="nino4"><a href="getindices.cgi?WMO=NCDCData/ersst_nino4a&STATION=NINO4&TYPE=i&id=$EMAIL">NINO4</a>
<input type="checkbox" class="formcheck" name="soi"><a href="getindices.cgi?WMO=CRUData/soi&STATION=SOI&TYPE=i&id=$EMAIL">SOI</a>
<input type="checkbox" class="formcheck" name="nao"><a href="getindices.cgi?WMO=CRUData/nao&STATION=NAO-Gibraltar&TYPE=i&id=$EMAIL">NAO</a>
<input type="checkbox" class="formcheck" name="co2"><a href="getindices.cgi?WMO=CDIACData/co2_monthly&STATION=CO2&TYPE=i&id=$EMAIL">CO2</a>
<input type="checkbox" class="formcheck" name="gmst"><a href="getindices.cgi?WMO=NASAData/giss_al_gl_m&STATION=GMST&TYPE=i&id=$EMAIL">smoothed GMST</a>
EOF
elif [ $NPERYEAR = 1 -o $NPERYEAR = -1 ]; then
    cat <<EOF
<input type="checkbox" class="formcheck" name="co2"><a href="getindices.cgi?WMO=CDIACData/co2_monthly&STATION=CO2&TYPE=i&id=$EMAIL">CO2</a>
<input type="checkbox" class="formcheck" name="gmst"><a href="getindices.cgi?WMO=NASAData/giss_al_gl_a_4yrlo&STATION=smoothed_GMST&TYPE=i&id=$EMAIL">smoothed GMST</a>
EOF
fi
echo "<input type=\"checkbox\" class=\"formcheck\" name=\"time\">time"
[ "$show_none" = true -a \( $NPERYEAR = 1 -o $NPERYEAR = -1 \) ] && echo "<input type=\"checkbox\" class=\"formcheck\" name=\"none\">none"
echo "</td></tr><tr><th><a href=\"javascript:pop_page('help/userseries.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>User-defined ${timescale}timeseries</th></tr><tr><td>"
forbidden='!`;&|'
i=0
for file in ./data/*${NPERYEAR#-}.$EMAIL.inf
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
