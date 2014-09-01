#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi
months[1]="Jan"
months[2]="Feb"
months[3]="Mar"
months[4]="Apr"
months[5]="May"
months[6]="Jun"
months[7]="Jul"
months[8]="Aug"
months[9]="Sep"
months[10]="Oct"
months[11]="Nov"
months[12]="Dec"

. ./nperyear2timescale.cgi

cat <<EOF
Content-Type:text/html

EOF
. ./nosearchengine.cgi

. ./myvinkhead.cgi "Plot observations" "$timescale $extraname$climate stations" "noindex,nofollow"

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=prefs/$EMAIL.plotfieldoptions.$NPERYEAR
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
  fi

  case ${FORM_var:-val} in
  anom) var_anom=checked;;
  frac) var_frac=checked;;
  zval) var_zval=checked;;
  *)    var_val=checked;;
  esac

  case ${FORM_sum:-1} in
  2) sum_2=selected;;
  3) sum_3=selected;;
  4) sum_4=selected;;
  5) sum_5=selected;;
  6) sum_6=selected;;
  7) sum_7=selected;;
  8) sum_8=selected;;
  9) sum_9=selected;;
  10) sum_10=selected;;
  11) sum_11=selected;;
  12) sum_12=selected;;
  15) sum_15=selected;;
  18) sum_18=selected;;
  20) sum_20=selected;;
  24) sum_24=selected;;
  30) sum_30=selected;;
  60) sum_60=selected;;
  90) sum_90=selected;;
  120) sum_120=selected;;
  180) sum_180=selected;;
  270) sum_270=selected;;
  365) sum_365=selected;;
  *) sum_1=selected;;
  esac
fi

cat <<EOF
<div class="formheader">Variable and time</div>
<div class="formbody">
<form action="correlatebox.cgi" method="POST">
<input type="hidden" name="email" value="$email">
<input type="hidden" name="climate" value="$timescale $extraname$climate">
<input type="hidden" name="shortclimate" value="$climate">
<input type="hidden" name="prog" value="$prog">
<input type="hidden" name="extraargs" value="$extraargs">
<input type="hidden" name="listname" value="$listname">
<input type="hidden" name="type" value="plot">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">

<input type="radio" class="formradio" name="var" value="val" $var_val>value<br>
<input type="radio" class="formradio" name="var" value="anom" $var_anom>anomaly = val-clim<br>
<input type="radio" class="formradio" name="var" value="frac" $var_frac>fraction = val/clim-1 or<br>
<input type="radio" class="formradio" name="var" value="zval" $var_zval>z-value = (val-clim)/sd
<br>
year: <input type="$number" class="forminput" name="year" $textsize4 value="$FORM_year"> 
EOF
###echo "NPERYEAR = $NPERYEAR"
if [ $NPERYEAR -ge 12 ]; then
  if [ $NPERYEAR = 12 ]; then
      echo "starting month of season:"
  else
      echo "month:"
  fi
  echo "<select class=\"forminput\" name=\"month\">"
  i=0
  while [ $i -lt 12 ]
  do
      i=$((i+1))
      if  $i = $FORM_month ]; then
	  echo "<option value=\"$i\" selected>${months[$i]}"
      else
	  echo "<option value=\"$i\">${months[$i]}"
      fi
  done
  echo "</select>"
  if [ $NPERYEAR -ge 360 ]; then
      if [ $NPERYEAR = 360 ]; then
	  dpm=30
      else
	  dpm=31
      fi
      echo "day: <select class=\"forminput\" name=\"day\">"
      i=0
      while [ $i -lt $dpm ]
      do
	  i=$((i+1))
	  if  $i = $FORM_day ]; then
	      echo "<option value=\"$i\" selected>$i"
	  else
	      echo "<option value=\"$i\">$i"
	  fi
      done
      echo "</select>"
  fi
  if [ $NPERYEAR = 12 ]; then
      echo "<br>length of season"
  else
      echo "<br>average over"
  fi
  if [ $NPERYEAR -eq 12 ]; then
    cat <<EOF
<select class="forminput" name="sum">
<option $sum_1>1
<option $sum_2>2
<option $sum_3>3
<option $sum_4>4
<option $sum_5>5
<option $sum_6>6
<option $sum_7>7
<option $sum_8>8
<option $sum_9>9
<option $sum_10>10
<option $sum_11>11
<option $sum_12>12
<option $sum_18>18
<option $sum_24>24
</select>months
EOF
  elif [ $NPERYEAR -ge 360 -a $NPERYEAR -le 366 ]; then
    cat <<EOF
<select class="forminput" name="sum">
<option $sum_1>1
<option $sum_2>2
<option $sum_7>7
<option $sum_10>10
<option $sum_15>15
<option $sum_20>20
<option $sum_30>30
<option $sum_60>60
<option $sum_90>90
<option $sum_120>120
<option $sum_180>180
<option $sum_270>270
<option $sum_365>365
</select>days
EOF
  else
    cat <<EOF
<input type="text" class="forminput" name="sum" size=4>periods
EOF
  fi
elif [ $NPERYEAR -eq 4 ]; then
cat <<EOF
starting season: <select class="forminput" name="month">
<option value="1">DJF
<option value="2">MAM
<option value="3">JJA
<option value="4">SON
</select>, length of period
<select class="forminput" name="sum">
<option $sum_1>1
<option $sum_2>2
<option $sum_3>3
<option $sum_4>4
</select>seasons
EOF
fi
cat <<EOF
<br><br><input type="submit" class="formbutton" value="Plot">
</form>
</div>
EOF

. ./myvinkfoot.cgi
