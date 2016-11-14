#!/bin/sh
. ./init.cgi
. ./getargs.cgi
lwrite=false
if [ "$EMAIL" = oldenborgh@knmi.nl ]; then
    lwrite=false # true
fi
if [ -z "$myvinkhead" ]; then
    echo 'Content-Type: text/html'
    echo
    echo

    # check if search engine
    . ./searchengine.cgi

    # check email address
    . ./checkemail.cgi

    # start real work
    if [ -z "$NPERYEAR" ]; then
      NPERYEAR=12
    fi
    TYPE=$FORM_TYPE
    WMO=$FORM_WMO
    STATION=$FORM_STATION
    NAME=$FORM_NAME

    . ./nperyear2timescale.cgi
    station=`echo "$STATION" | tr '_' ' '`
    if [ -z "$ROBOT" ]; then
        echo `date` "$EMAIL ($REMOTE_ADDR) count_missing $NAME $STATION ($WMO)" >> log/log
    fi
    . ./myvinkhead.cgi "Fraction missing data" "$timescale $station $NAME" "index,nofollow"
    call_vinkfoot=true
fi
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
    if [ -s ./prefs/$EMAIL.count_missing ]; then
        if [ -z "$FORM_month" ]; then
            FORM_month=`fgrep 'FORM_month=' ./prefs/$EMAIL.count_missing | sed -e 's/^.*=//' -e 's/;.*$//'`
        fi
        if [ -z "$FORM_sel" ]; then
            FORM_sel=`fgrep 'FORM_sel=' ./prefs/$EMAIL.count_missing | sed -e 's/^.*=//' -e 's/;.*$//'`
        fi
    fi
    cat > ./prefs/$EMAIL.count_missing <<EOF
FORM_month=$FORM_month;
FORM_sel=$FORM_sel;
EOF
fi

case ${FORM_month:--1} in
    1) month_1_selected="selected";;
    2) month_2_selected="selected";;
    3) month_3_selected="selected";;
    4) month_4_selected="selected";;
    5) month_5_selected="selected";;
    6) month_6_selected="selected";;
    7) month_7_selected="selected";;
    8) month_8_selected="selected";;
    9) month_9_selected="selected";;
    10) month_10_selected="selected";;
    11) month_11_selected="selected";;
    12) month_12_selected="selected";;
esac
case ${FORM_sel:-1} in
    2) sel_2_selected="selected";;
    3) sel_3_selected="selected";;
    4) sel_4_selected="selected";;
    5) sel_5_selected="selected";;
    6) sel_6_selected="selected";;
    7) sel_7_selected="selected";;
    8) sel_8_selected="selected";;
    9) sel_9_selected="selected";;
    10) sel_10_selected="selected";;
    11) sel_11_selected="selected";;
    12) sel_12_selected="selected";;
    *) sel_1_selected="selected";;
esac

base=./data/$TYPE$WMO
missbase=`echo ${base}_missing | sed -e 's/+++//' -e 's/++//'`
if [ -n "$FORM_month" ]; then
    missbase=${missbase}_${FORM_sum}_${FORM_sel}
fi
if [ ! -s ${missbase}.txt -o ${missbase}.plt -ot $base.dat ]; then
    if [ -n "$FORM_month" ]; then
        args="mon $FORM_month sel $FORM_sel"
    fi
    [ "$lwrite" = true ] && echo "./bin/count_missing $args $base.dat"
    ( ./bin/count_missing $base.dat $args > ${missbase}.txt ) 2>&1
fi
c=`cat ${missbase}.txt | wc -l`
if [ $c -le 2 ]; then
    echo "No missing data<br>"
else
    if [ ! -s ./${missbase}.plt -o ./${missbase}.plt -ot ./${missbase}.txt ]; then
        ( ./bin/plotdat ${missbase}.txt > ./${missbase}.plt ) 2>&1
    fi
    if [ ! -s ${missbase}.png -o ${missbase}.png -ot ${missbase}.plt ]; then
        title=`echo $NAME $station | tr "_" " "`
        if [ -n "$args" ]; then
            if [ $NPERYEAR = 2 ]; then
                eval `bin/halfyear2string $FORM_month 1 0`
            elif [ $NPERYEAR = 4 ]; then
                eval `bin/season2string $FORM_month 1 0`
            elif [ $NPERYEAR -ge 12 ]; then
                eval `bin/month2string $FORM_month $FORM_sel 0`
            fi
            title="$indexmonth $title"
        fi
        ./bin/gnuplot << EOF
$gnuplot_init
set size .7057,.4
set ylabel "fraction missing [1]"
set term postscript epsf color solid
set zeroaxis
set output "${missbase}.eps"
plot "./${missbase}.plt" title "$title" with steps
set term png $gnuplot_png_font_hires
set out "./${missbase}.png"
replot
quit
EOF
    fi
    pngfile=${missbase}.png
    getpngwidth
    datafile=`echo ${missbase}.txt | tr '+' '%'`
    cat << EOF 
<div class="bijschrift">Fraction missing data
(<a href="${missbase}.eps">eps</a>, <a href="ps2pdf.cgi?file=${missbase}.eps">pdf</a>,
<a href="${missbase}.txt">raw data</a>, 
<a href="dat2nc.cgi?datafile=${missbase}.txt&type=i&station=missing_$STATION&id=$EMAIL">netcdf</a>, 
<a href="analyse_anomaly.cgi?datafile=$datafile&STATION=${STATION}_missing&TYPE=$TYPE&id=$EMAIL">analyse this time series)</div>
<center>
<img src="${missbase}.png" alt="fraction missing data" width="$halfwidth" border=0 class="realimage" hspace=0 vspace=0>
</center>
EOF

    if [ $NPERYEAR -gt 1 ]; then
        cat << EOF
<form action="count_missing.cgi" method="post">
<input type="hidden" name="WMO"     value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="EMAIL"   value="$EMAIL">
<input type="hidden" name="TYPE"    value="$TYPE">
<input type="hidden" name="NAME"    value="$NAME">
EOF
        if [ $NPERYEAR = 2 ]; then
            cat <<EOF
Replot using half year
<select class="forminput" name="month">
<option value="1" $month_1_selected>Oct-Mar
<option value="2" $month_2_selected>Apr-Sep
</select>
<input type="hidden" name="sum" value="1">
EOF
        elif [ $NPOERYEAR = 4 ]; then
            cat <<EOF
Replot using season 
<select class="forminput" name="month">
<option value="1" $month_1_selected>DJF
<option value="2" $month_2_selected>MAM
<option value="3" $month_3_selected>JJA
<option value="4" $month_4_selected>SON
</select>
<input type="hidden" name="sum" value="1">
EOF
        elif [ $NPERYEAR -ge 12 ]; then
            cat <<EOF
Replot using starting month
<select class="forminput" name="month">
<option value="1" $month_1_selected>Jan
<option value="2" $month_2_selected>Feb
<option value="3" $month_3_selected>Mar
<option value="4" $month_4_selected>Apr
<option value="5" $month_5_selected>May
<option value="6" $month_6_selected>Jun
<option value="7" $month_7_selected>Jul
<option value="8" $month_8_selected>Aug
<option value="9" $month_9_selected>Sep
<option value="10" $month_10_selected>Oct
<option value="11" $month_11_selected>Nov
<option value="12" $month_12_selected>Dec
</select>length of season 
<select class="forminput" name="sel">
<option $sel_1_selected>1
<option $sel_2_selected>2
<option $sel_3_selected>3
<option $sel_4_selected>4
<option $sel_5_selected>5
<option $sel_6_selected>6
<option $sel_7_selected>7
<option $sel_8_selected>8
<option $sel_9_selected>9
<option $sel_10_selected>10
<option $sel_11_selected>11
<option $sel_12_selected>12
</select> months
EOF
        else
            echo "unknown timescale $NPERYEAR"
        fi
        cat << EOF
<input type="submit" class="formbutton" value="Select season">
</form>
EOF
    fi # NPERYEAR -gt 1
fi # there is missing data


if [ "$call_vinkfoot" = true ]; then
    . ./myvinkfoot.cgi
fi
