#!/bin/bash

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchenginewithheader.cgi
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
        if [ $i = $FORM_month ]; then
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
	        if [ $i = "$FORM_day" ]; then
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
        ###echo "<br>average over"
        echo "<select class=forminput name=operation>"
        echo "<option>averaging<option>summing</select> over"
    fi
    if [ $NPERYEAR -eq 12 ]; then
        echo "<select class=\"forminput\" name=\"sum\">"
        for sum in 1 2 3 4 5 6 7 8 9 10 11 12 18 24 60
        do
            if [ "$sum" = "$FORM_sum" ]; then
                echo "<option selected>$sum"
            else
                echo "<option>$sum"
            fi
        done
        echo "</select>months"
    elif [ $NPERYEAR -ge 360 -a $NPERYEAR -le 366 ]; then
        echo "<select class=\"forminput\" name=\"sum\">"
        for sum in 1 2 3 4 5 6 7 10 9 10 11 12 13 14 15 18 20 21 25 30 60 90 120 180 365
        do
            if [ "$sum" = "$FORM_sum" ]; then
                echo "<option selected>$sum"
            else
                echo "<option>$sum"
            fi
        done
        echo "</select>days"
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
