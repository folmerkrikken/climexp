#!/bin/sh
if [ "$FORM_type" != attribute ]; then
    export DIR=`pwd`
    . ./getargs.cgi
    NPERYEAR=$FORM_NPERYEAR
    echo 'Content-Type: text/html'
    . ./expires.cgi
    echo
    echo
fi
export EMAIL

if [ -z "$FORM_NPERYEAR" ]; then
    echo "internal error: NPERYEAR not set"
    NPERYEAR=12
fi

# check email address
. ./checkemail.cgi

if [ "$EMAIL" = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

# real work
if [ $EMAIL != someone@somewhere ]; then
    if [ "$FORM_type" = plot ]; then
      . ./save_plotfieldoptions.cgi
    else
      . ./save_commonoptions.cgi
    fi
    if [ -n "$FORM_var" ]; then
        if [ "$FORM_type" = histogram ]; then
            . ./save_statistical.cgi
        elif [ "$FORM_type" != attribute ]; then
            . ./save_variable.cgi
        fi
    fi
fi

if [ "$FORM_type" = histogram ]; then
    if [ ${FORM_var%r} != $FORM_var -o ${FORM_var%R} != $FORM_var ]; then
        # return time
        if [ -z "$FORM_year" -o ${FORM_year:-0} -lt -2000 -o ${FORM_year:-0} -gt 2300 ]; then
            . ./myvinkhead.cgi "Map of stations" "Error"
            echo "Cannot compute the return time without the year being defined"
            . ./myvinkfoot.cgi
            exit
        fi
    fi
fi

# common options
forbidden='!`;|&'

if [ -n "$FORM_timeseries" ]; then
  case "$FORM_timeseries" in
  "")        index="station $FORM_climate";;
  #echo "<html><head><title>error</title><body bgcolor=\"#ffffff\">Please select a predictor (index)</body></html>";exit;;
  nino12)    index="NINO12";sfile="$DIR/NCDCData/ersst_nino12a.dat";;
  nino3)     index="NINO3";sfile="$DIR/NCDCData/ersst_nino3a.dat";;
  nino34)    index="NINO3.4";sfile="$DIR/NCDCData/ersst_nino3.4a.dat";;
  nino4)     index="NINO4";sfile="$DIR/NCDCData/ersst_nino4a.dat";;
  soi)       index="SOI";sfile="$DIR/CRUData/soi.dat";;
  nao)       index="NAO-Gibraltar";sfile="$DIR/CRUData/nao.dat";;
  sunspots)  index="sunspots";sfile="$DIR/SIDCData/sunspots.dat";;
  co2)       index="CO2"
             if [ ${NPERYEAR:-12} = 12 ]; then
                sfile="$DIR/CDIACData/co2_monthly.dat"
             elif [ $NPERYEAR = 1 -o $NOERYEAR = -1 ]; then
                sfile="$DIR/CDIACData/co2_annual.dat"
             fi;;
  gmst)      index="GMST"
             if [ ${NPERYEAR:-12} = 12 ]; then
                sfile="$DIR/NASAData/giss_al_gl_m_4yrlo.dat"
             elif [ $NPERYEAR = 1 -o $NPERYEAR = -1 ]; then
                sfile="$DIR/NASAData/giss_al_gl_a_4yrlo.dat"
             else
                echo 
                . ./myvinkhead.cgi "Not yet ready" ""
                . ./nperyear2timescale.cgi
                echo "I am afraid this routine cannot yet handle $timescale data."
                . ./myvinkfoot.cgi
                exit
             fi;;
  time)      index="time";sfile="$DIR/KNMIData/time$NPERYEAR.dat";;
  *)         sfile=$DIR/`head -1 $FORM_timeseries | tr $forbidden '?'`
	     TYPE=`basename $sfile | cut -b 1`
	     case $TYPE in
  	     t) iclim="temperature";;
	     p) iclim="precipitation";;
	     s) iclim="pressure";;
	     l) iclim="sealevel";;
	     r) iclim="runoff";;
	     c) iclim="correlation";;
             *) iclim="index";;
             esac
	     index="`head -2 $FORM_timeseries | tail -1 | tr '_' ' '` $iclim"
             ;;
  esac
elif [ -n "$FORM_field" ]; then
  . ./queryfield.cgi
fi

if [ "$FORM_var" = "zdif" -a "$FORM_runvar" = "regression" ]; then
  FORM_var=bdif
fi

plotlist=$DIR/data/plotcorr$$.txt
if [ -n "$FORM_extraargs" ]; then
  fullprog="${FORM_prog}_${FORM_extraargs}"
else
  fullprog=$FORM_prog
fi
FORM_listname=`echo "$FORM_listname" | tr -d '\\'`

if [ "$FORM_type" = 'plot' -o "$FORM_type" = 'histogram' -o "$FORM_type" = attribute ]; then
  corrargs="$FORM_listname $plotlist $fullprog $FORM_var"
elif [ -z "$FORM_timeseries" -a -n "$FORM_field" ]; then
  if [ "$FORM_intertype" = "nearest" ]; then
    corrargs="$FORM_listname $plotlist $fullprog field$FORM_var $file"
  else
    corrargs="$FORM_listname $plotlist $fullprog ifield$FORM_var $file"
  fi
elif [ "$index" = time ]; then
  corrargs="$FORM_listname $plotlist $fullprog $FORM_var time"
elif [ -z "$FORM_timeseries" -a -z "$FORM_field" ]; then
  corrargs="$FORM_listname $plotlist $fullprog au$FORM_var"
elif [ "$FORM_type" != attribute ]; then
  corrargs="$FORM_listname $plotlist $fullprog $FORM_var file $sfile"
fi

# prevent getopts from switching to running correlations
# if these have not been selected explicitly
FORM_num=$$
if [ "$FORM_var" != 'runc' -a "$FORM_var" != 'zdif' -a "$FORM_var" != 'bdif' ]; then
  FORM_runwindow=""
fi
if [ "$FORM_type" != attribute ]; then # for attribute this has been done in attribute.cgi
    . ./getopts.cgi
    [ -n "$FORM_year" ] && corrargs="$corrargs end2 $FORM_year"
fi
FORM_threshold=$FORM_dgt
FORM_dgt=""

echo `date` "$FORM_email ($REMOTE_ADDR) correlatebox $corrargs" | sed -e  "s:$DIR/::g" >> log/log
if [ $NPERYEAR -ge 12 ]; then
  eval `./bin/month2string "$FORM_month" "$sumstring" "$FORM_lag" "$FORM_operation" $FORM_fix`
elif [ $NPERYEAR -eq 4 ]; then
  eval `./bin/season2string "$FORM_month" "$sumstring" "$FORM_lag" "$FORM_operation" $FORM_fix`
fi
###title="Correlations of $seriesmonth $FORM_climate stations\with $indexmonth $index"

email="$FORM_email"
oper="$FORM_var"
CLIM="$FORM_climate"
if [ -z "$climfield" ]; then
  if [ -z "$index" ] ; then
    climfield="station $FORM_climate"
  else
    climfield="$index"
  fi
else
  if [ "$FORM_intertype" = "interpolated" ]; then
    kindname="interpolated $kindname"
  else
    kindname="nearest point $kindname"
  fi
fi
FORM_STATION="station"
station="station"
if [ -n "$FORM_month" -a -n "$FORM_year" ]; then
  endmonth=$((${FORM_sum:-1} * 12 / $NPERYEAR + $FORM_month - 1))
  if [ $endmonth -gt 12 ]; then
    plotyear="$(($FORM_year + 1))\\"
  elif [ $NPERYEAR -eq 4 -a $FORM_month -eq 1 ]; then
    plotyear="$(($FORM_year + 1))\\"
  else
    plotyear="$FORM_year\\"
  fi
fi
. ./title.cgi
if [ "$FORM_type" = 'plot' ]; then
title=`echo $title | sed -e 's/\\\\with.*//' \
 -e 's/day //' \
 -e 's/val /value of /' \
 -e 's/frac /fractional anomaly of /'`
fi
# significance really is log10(sign)
title=`echo $title | sed -e 's/^sign/Log10(sign)/'`
# I cannot seem to get rid of the '\'... another two slashes did the trick.
htmltitle=`echo "$title" | sed -e 's/^corr /Correlation of /' -e 's/\\\\/ /'`

backupfile="data/correlatebox_$$.html"
. $DIR/restofcorrelatebox.cgi |tee $backupfile
sed -e 's:plotstations.cgi:../plotstations.cgi:' $backupfile > $backupfile.new
mv $backupfile.new $backupfile
