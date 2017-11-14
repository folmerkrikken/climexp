#!/bin/sh
if [ $EMAIL != someone@somewhere ]; then
   def=./prefs/$EMAIL.filteryearoptions
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
       *) box_selected=selected;;
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
       18) m18=selected;;
       24) m24=selected;;
       25) m25=selected;;
       30) m30=selected;;
       35) m35=selected;;
       40) m40=selected;;
       45) m45=selected;;
       50) m50=selected;;
       60) m60=selected;;
       70) m70=selected;;
       80) m80=selected;;
       90) m90=selected;;
       100) m100=selected;;
       120) m120=selected;;
       150) m150=selected;;
       200) m200=selected;;
       *) m2=selected;;
   esac
fi

cat << EOF
<form action="filteryearseries.cgi" method="POST">
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
<option value="box" $box_selected>running-mean
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
<option $m16>16
<option $m17>17
<option $m18>18
<option $m19>19
<option $m20>20
<option $m21>21
<option $m22>22
<option $m23>23
<option $m24>24
<option $m25>25
<option $m30>30
<option $m35>35
<option $m40>40
<option $m45>45
<option $m50>50
<option $m60>60
<option $m70>70
<option $m80>80
<option $m90>90
<option $m100>100
<option $m120>120
<option $m150>150
<option $m200>200
</select> years<br>
requiring at least <input type="$number" min=0 max=100 step=1 class="forminput" name="minfac" $textsize2 value="${FORM_minfac:-75}">% valid data
<br><input type="submit" class="formbutton" value="Filter consecutive years">
</form>
EOF
