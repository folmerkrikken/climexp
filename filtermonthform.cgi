#!/bin/sh
if [ $EMAIL != someone@somewhere ]; then
   def=./prefs/$EMAIL.filtermonthoptions
   if [ -f $def ]; then
      eval `egrep '^FORM_[a-z]*=[-0-9a-zA-Z]*;$' $def`
   fi
   case "$FORM_hilo" in
       high-pass) hi_selected=selected;;
       low-pass) lo_selected=selected;;
       *)  lo_selected=selected;;
   esac
   case "$FORM_filtertype" in
       loess1) loess1_selected=selected;;
       loess2) loess2_selected=selected;;
       box) box_selected=selected;;
       *) loess1_selected=selected;;
   esac
   case "$FORM_nfilter" in
       1) m1=selected;;
       2) m2=selected;;
       3) m3=selected;;
       4) m4=selected;;
       5) m5=selected;;
       6) m6=selected;;
       7) m7=selected;;
       8) m8=selected;;
       9) m9=selected;;
       10) m10=selected;;
       11) m11=selected;;
       12) m12=selected;;
       13) m13=selected;;
       14) m14=selected;;
       15) m15=selected;;
       18) m18=selected;;
       24) m24=selected;;
       30) m30=selected;;
       36) m36=selected;;
       48) m48=selected;;
       60) m60=selected;;
       72) m72=selected;;
       84) m84=selected;;
       96) m96=selected;;
       108) m108=selected;;
       120) m120=selected;;
       144) m144=selected;;
       180) m180=selected;;
       240) m240=selected;;
       300) m300=selected;;
       360) m360=selected;;
       480) m480=selected;;
       600) m600=selected;;
       720) m720=selected;;
       840) m840=selected;;
       960) m960=selected;;
       1080) m1080=selected;;
       1200) m1200=selected;;
       *) m12=selected;;
   esac
fi

if [ $NPERYEAR = 4 ]; then
  month="season"
elif [ $NPERYEAR = 12 ]; then
  month="month"
elif [ $NPERYEAR = 360 -o $NPERYEAR -eq 365 -o $NPERYEAR -eq 366 ]; then
  month="day"
else
  month="period"
fi
if [ -z "$FORM_field" ]; then
  echo "<tr valign=\"top\"><td>Filter adjacent ${month}s</td><td>"
fi

cat <<EOF
<form action="filtermonthseries.cgi" method="POST">
<input type="hidden" name="field"   value="$FORM_field">
<input type="hidden" name="wmo"     value="$WMO">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="email"   value="$EMAIL">
<input type="hidden" name="type"    value="$TYPE">
<input type="hidden" name="name"    value="$NAME">
<input type="hidden" name="nperyear" value="$NPERYEAR">
<input type="hidden" name="file"    value="$TYPE$WMO.dat">
<select class="forminput" name="hilo">
<option $hi_selected>high-pass
<option $lo_selected>low-pass
</select>
<select class="forminput" name="filtertype">
<option $box_selected value=box>running-mean
<option $loess1_selected value="loess1">1st order LOESS
<option $loess2_selected value="loess2">2nd order LOESS
</select>
filter<br>cut-off value  
<select class="forminput" name="nfilter">
<option $m1>1
<option $m2>2
<option $m3>3
<option $m4>4
<option $m5>5
<option $m6>6
<option $m7>7
<option $m8>8
<option $m9>9
<option $m10>10
<option $m11>11
<option $m12>12
<option $m13>13
<option $m14>14
<option $m15>15
<option $m18>18
<option $m24>24
<option $m30>30
<option $m36>36
<option $m48>48
<option $m60>60
<option $m72>72
<option $m84>84
<option $m96>96
<option $m108>108
<option $m120>120
<option $m144>144
<option $m180>180
<option $m240>240
<option $m300>300
<option $m360>360
<option $m480>480
<option $m600>600
<option $m720>720
<option $m840>840
<option $m960>960
<option $m1080>1080
<option $m1200>1200
</select>${month}s
<br>requiring at least <input type="$number" min=0 max=100 step=1 class="forminput" name="minfac" $textsize2 value="${FORM_minfac:-75}">% valid data
<br><input type="submit" class="formbutton" value="Filter consecutive ${month}s">
</form>
EOF
