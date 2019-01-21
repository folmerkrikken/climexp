#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "WMO-assessed data sets" "Observations" "index,follow"
cat <<EOF
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="3">Temperature and Precipitation (ECVs) and Climate Indices: fields</td></tr>
EOF

for string in hadcrut4 noaa_temp giss_temp_1200 gpcc cocorahs hadex2
do
    fgrep -i $string selectfield_obs.html | fgrep -v filled |
        sed -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL\&field=\1">/g' \
            -e 's:,:</a>,:g' \
            -e 's:</td><td><a href=":</a></td><td><a href=":g' \
            -e "s/EMAIL/$EMAIL/g" \
            -e 's/<!--GPCC-->/Precipitation/' \
            -e 's/<!--HADEX2-->/Extreme indices/' \
            -e 's/<!--ICOADS-->/Ocean surface/'
done
cat <<EOF
<tr><th colspan="3">Temperature and Precipitation (ECVs) and Climate Indices: time series</td></tr>
EOF
for string in hadcrut4 NOAA/NCEI "Ts+dSST"
do
    fgrep -i $string selectindex.cgi | fgrep -v filled |
        sed -e "s/EMAIL/$EMAIL/g" 
done

cat <<EOF
<tr><th colspan="3">Hydrology and Marine</td></tr>
<tr><td align=right>Run-off time series</td><td>GRDC (not yet available here)</td></td><td><a href="https://www.bafg.de/GRDC/EN/01_GRDC/13_dtbse/database_node.html</a>" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a></td></tr>
EOF
for string in coads
do
    fgrep -i $string selectfield_obs.html | fgrep -v filled |
        sed -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL\&field=\1">/g' \
            -e 's:,:</a>,:g' \
            -e 's:</td><td><a href=":</a></td><td><a href=":g' \
            -e "s/EMAIL/$EMAIL/g" \
            -e 's/<!--GPCC-->/Precipitation/' \
            -e 's/<!--HADEX2-->/Extreme indices/' \
            -e 's/<!--ICOADS-->/Ocean surface/'
done
cat <<EOF
<tr><td align=right>Subsurface ocean</td><td>WOD13 (not yet available here)</td></td><td><a href="https://www.nodc.noaa.gov/OC5/WOD13/</a>" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a></td></tr>
<tr><th colspan="3">Sea Level ECVs</td></tr>
<tr><td align=right>Sea level</td><td>(not yet available)</td></tr>
<tr><th colspan="3">Sea Ice & Ice Sheets & Glacier ECVs: fields</td></tr>
EOF
for string in ice_index grace
do
    fgrep -i $string selectfield_obs.html | fgrep -v filled |
        sed -e 's/<input type="radio" class="formradio" name="field" value="\([^"]*\)">/<a href="select.cgi?id=EMAIL\&field=\1">/g' \
            -e 's:,:</a>,:g' \
            -e 's:</td><td><a href=":</a></td><td><a href=":g' \
            -e "s/EMAIL/$EMAIL/g" \
            -e 's/<!--GPCC-->/Precipitation/' \
            -e 's/<!--HADEX2-->/Extreme indices/' \
            -e 's/<!--ICOADS-->/Ocean surface/'
done
cat <<EOF
<tr><th colspan="3">Sea Ice & Ice Sheets & Glacier ECVs: indices</td></tr>
EOF
for string in ice_area GRACE
do
    fgrep -i $string selectindex.cgi  |
        sed -e "s/EMAIL/$EMAIL/g"
done

cat <<EOF
</table>
EOF

. ./myvinkfoot.cgi
