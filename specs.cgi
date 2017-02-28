#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo
. ./getargs.cgi
. ./myvinkhead.cgi "SPECS empirical seasonal forecasts" ""

cat <<EOF
<p>Past observations are used to deduce significant correlations between the weather 
in the last three months (up to the beginning of the month) and the weather over the next season (from the end of the month). The main predictors are El Ni&ntilde;o / La Ni&ntilde;a and the trends due to global warming. Overfitting is avoided as much as possible. The system has been documented in <a href="http://www.geosci-model-dev.net/8/3947/2015/" target="_new">Eden et al, 2015</a>.

<p>This web page is under construction. Please give feedback if it does not work properly.

EOF

temperature=GCEcom
precipitation=GPCCcom
pressure=20CRslp

case "$FORM_var" in
    prcp) dataset=$precipitation;unis="[%]";prcp_selected=selected;varname="precipitation ";;
    slpa) dataset=$pressure;units="[hPa]";slpa_selected=selected;varname="sea-level pressure ";;
    *) dataset=$temperature;units="[&deg;C]";temp_selected=selected;varname="temperature ";;
esac

prefix=$FORM_prefix
case "$prefix" in
    tercile_) tercile_selected=selected;plotname="Tercile summary plot";units=;;
    correlation_) correlation_selected=selected;plotname="Correlation of ensemble mean";units=;;
    crpss_) crpss_selected=selected;plotname="Probability skill score";units=;;
    rmsess_) rmsess_selected=selected;plotname="Deterministic skill score";units=;;
    *) prefix=forecast_;forecast_selected=selected;plotname="Forecast anomalies";;
esac

firstdate=`ls SPES/plots/$dataset/25/ | tr " " "\n" | tail -1`
firstyear=${firstdate%??}
firstmonth=${firstdate#????}
firstm=${firstmonth#0}
if [ -n "$FORM_date" ]; then
    date="$FORM_date"
else
    date=$firstdate
fi

cat <<EOF
<form action="specs.cgi" method="post">
<input type=hidden name=id value="$EMAIL">
<p><div class="formheader">Options</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Forecast<td>
<select class="forminput" name="date" onChange="this.form.submit()">
EOF
for past in 0 1 2 3 4 5 6 7 8 9 10 11
do
    i=$((firstm-past))
    y=$firstyear
    if [ $i -le 0 ]; then
        i=$((i+12))
        y=$((y-1))
    fi
    ii=`printf %02i $i`
    if [ ${y}${ii} = "$date" ]; then
        selected=selected
        yy=$y
    else
        selected=
    fi
    case $ii in
        01) nextseason=JFM;nextseasonname="January-March";analysismonth=December;;
        02) nextseason=FMA;nextseasonname="February-April";analysismonth=January;;
        03) nextseason=MAM;nextseasonname="March-May";analysismonth=February;;
        04) nextseason=AMJ;nextseasonname="April-June";analysismonth=March;;
        05) nextseason=MJA;nextseasonname="May-July";analysismonth=April;;
        06) nextseason=JJA;nextseasonname="June-August";analysismonth=May;;
        07) nextseason=JAS;nextseasonname="July-September";analysismonth=June;;
        08) nextseason=ASO;nextseasonname="August-October";analysismonth=July;;
        09) nextseason=SON;nextseasonname="September-November";analysismonth=August;;
        10) nextseason=OND;nextseasonname="October-December";analysismonth=September;;
        11) nextseason=NDJ;nextseasonname="November-January";analysismonth=October;;
        12) nextseason=DJF;nextseasonname="December-February";analysismonth=November;;
        *) echo "</table>error: unknown month in past=$past m=$m i=$i ii=$ii"; . ./myvinkfoot.cgi;exit;;
    esac
    echo "<option value=${y}${ii} $selected>$nextseasonname $y from $analysismonth</option>"
done
year=${date%??}
month=${date#????}
case $month in
    01) nextseason=JFM;nextseasonname="January-March";analysismonth=December;;
    02) nextseason=FMA;nextseasonname="February-April";analysismonth=January;;
    03) nextseason=MAM;nextseasonname="March-May";analysismonth=February;;
    04) nextseason=AMJ;nextseasonname="April-June";analysismonth=March;;
    05) nextseason=MJA;nextseasonname="May-July";analysismonth=April;;
    06) nextseason=JJA;nextseasonname="June-August";analysismonth=May;;
    07) nextseason=JAS;nextseasonname="July-September";analysismonth=June;;
    08) nextseason=ASO;nextseasonname="August-October";analysismonth=July;;
    09) nextseason=SON;nextseasonname="September-November";analysismonth=August;;
    10) nextseason=OND;nextseasonname="October-December";analysismonth=September;;
    11) nextseason=NDJ;nextseasonname="November-January";analysismonth=October;;
    12) nextseason=DJF;nextseasonname="December-February";analysismonth=November;;
    *) echo "</table>error: unknown month in ii=$ii"; . ./myvinkfoot.cgi;exit;;
esac

cat <<EOF
</select>
<tr><td>Variable<td>
<select class="forminput" name="var" onChange="this.form.submit()">
<option value="temp" $temp_selected>Temperature</option>
<option value="prcp" $prcp_selected>Precipitation</option>
<option value="slpa" $slpa_selected>Sea-level pressure</option>
</select>

<tr><td>Show<td>
<select class="forminput" name="prefix" onChange="this.form.submit()">
<option value="" $forecast_selected>Forecast anomalies</option>
<option value="tercile_" $tercile_selected>Tercile summery plot</option>
<option value="crpss_" $crpss_selected>Probabilistic skill score (CRPSS)</option>
<option value="rmsess_" $rmsess_selected>Deterministic skill score (RMSESS)</option>
<option value="correlation_" $correlation_selected>Correlation of ensemble mean</option>
</select>
<tr><td span="2"><input type="submit" class="formbutton" value="Plot">
</table>
</div>
</form>
EOF

nobottom=true
. ./myvinkfoot.cgi

cat <<EOF
<table border="0" width="100%" cellspacing="0" cellpadding="0">
   <tr>
      <td width="10%">&nbsp;</td>
      <td width="81.5%" valign=top>
         <div id="printable" name="printable">
<div class=bijschrift id=caption>$plotname $units of $nextseasonname $yy $varname made in early $analysismonth.</div>
<img id="imageToSwap" src="SPES/plots/$dataset/25/$date/${dataset}_${prefix}$date.png" width="100%" />
<p>The development of this forecast system was supported by the EU-project <a href="http://www.specs-fp7.eu">SPECS</a>.
        </div>
      </td>
   </tr>
</table>
EOF

cat ./vinklude/bottom_en.html
cat <<EOF
</body>
</html>
EOF
