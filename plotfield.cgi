#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
. ./checkemail.cgi

. ./queryfield.cgi

. ./myvinkhead.cgi "Plot field" "$kindname $climfield" "noindex,nofollow"

eval `bin/getunits.sh $file`
# better hack
FORM_var=`./bin/describefield.sh $file | tail -1 | awk '{print $2}' | cut -b 1-15`
if [ "${FORM_field#erai}" != "$FORM_field" -o "${FORM_field#data/erai}" != "$FORM_field" -o \
    "${FORM_field#ct}" != "$FORM_field" -o "${FORM_field#data/ct}" != "$FORM_field" ]; then
    if [ -z "$FORM_plotanomaly" -a \( "$UNITS" = "K" -o "$UNITS" = degK \) -a "$NEWUNITS" = "Celsius" ]; then
        FORM_var="$FORM_var-273.15"
    fi
fi
if [ -n "$FORM_year2" ]; then
# some sanity checking
  if [ -z "$FORM_lon2" ]; then
    if [ -z "$FORM_lon1" ]; then
      if [ -z "$FORM_lat2" ]; then
        if [ -z "$FORM_lat1" ]; then
          echo "Error: specifiy at least one latitude or longitude"
          . ./myvinkfoot.cgi
          exit
        fi
        plotyear="${FORM_lat1}N"
      elif [ "$FORM_lat1" != "$FORM_lat2" ]; then
        FORM_var="ave($FORM_var,lat=$FORM_lat1,lat=$FORM_lat2)"
        FORM_lat2=$FORM_lat1
        plotyear="${FORM_lat1}-${FORM_lat2}N"
      else
        plotyear="${FORM_lat1}N"
      fi
    else
      plotyear="${FORM_lon1}E"
    fi
  else
    if [ "$FORM_lon1" != "$FORM_lon2" ]; then
      if [ -z "$FORM_lat2" ]; then
        if [ -z "$FORM_lat1" ]; then
          FORM_var="ave($FORM_var,lat=$FORM_lon1,lat=$FORM_lon2)"
          FORM_lon2=$FORM_lon1
          plotyear="${FORM_lon1}-${FORM_lon2}E"
        else
          plotyear="${FORM_lat1}N"
        fi
      elif [ "$FORM_lat1" != "$FORM_lat2" ]; then
        echo "Error: specifiy at most 3 latitudes and longitudes"
        . ./myvinkfoot.cgi
        exit
      else
        ploytear="${FORM_lat1}N"
      fi
    fi
  fi
fi
. $DIR/getfieldopts.cgi

if [ $EMAIL != someone@somewhere ]; then
  cat > prefs/$EMAIL.plotfield.$NPERYEAR <<EOF
FORM_year=$FORM_year;
FORM_month=$FORM_month;
FORM_year2=$FORM_year2;
FORM_month2=$FORM_month2;
FORM_day=$FORM_day;
FORM_hour=$FORM_hour;
FORM_plotsum=$FORM_plotsum;
FORM_plotanomaly=$FORM_plotanomaly;
FORM_plotanomalykind=$FORM_plotanomalykind;
FORM_climyear1=$FORM_climyear1;
FORM_climyear2=$FORM_climyear2;
EOF
fi

if [ "$FORM_movie" = "yes" ]; then
  FORM_year="$FORM_year1"
  FORM_month="$FORM_month1"
fi
if [ $NPERYEAR != 0 ]; then
    if [ -z "$FORM_year" -o -z "$FORM_month" -a ${NPERYEAR:-12} -gt 1 ]; then
        echo "Error: please specify year and month to plot"
        . ./myvinkfoot.cgi
        exit
    fi
fi 

if [ "$NPERYEAR" = 1 ]; then
  m=jan
  [ -n "$FORM_year2" ] && m2=dec
elif [ "$NPERYEAR" = 4 ]; then
  case $FORM_month in 
  1 ) m=jan;;
  2 ) m=apr;;
  3 ) m=jul;;
  4 ) m=oct;;
  esac
  case $FORM_month2 in 
  1 ) m2=jan;;
  2 ) m2=apr;;
  3 ) m2=jul;;
  4 ) m2=oct;;
  esac  
else
  case $FORM_month in 
  1 ) m=jan;;
  2 ) m=feb;;
  3 ) m=mar;;
  4 ) m=apr;;
  5 ) m=may;;
  6 ) m=jun;;
  7 ) m=jul;;
  8 ) m=aug;;
  9 ) m=sep;;
  10) m=oct;;
  11) m=nov;;
  12) m=dec;;
  esac
  case $FORM_month2 in 
  1 ) m2=jan;;
  2 ) m2=feb;;
  3 ) m2=mar;;
  4 ) m2=apr;;
  5 ) m2=may;;
  6 ) m2=jun;;
  7 ) m2=jul;;
  8 ) m2=aug;;
  9 ) m2=sep;;
  10) m2=oct;;
  11) m2=nov;;
  12) m2=dec;;
  esac
fi
echo `date` "$EMAIL ($REMOTE_ADDR) plot $kindname $climfield" $m$FORM_year >> log/log

if [ $NPERYEAR = 0 ]; then
    NPERYEAR=1 # otherwise grads.cgi gets confused
    FORM_year=0001 # grads puts netcdf files without date on 1:1:1:0
    m=jan
fi
if [ -z "$FORM_hour" ]; then
    date=${FORM_day:-1}$m$FORM_year
else
    date=${FORM_hour}Z$FORM_day$m$FORM_year
fi
date2=$m2$FORM_year2
if [ "$NPERYEAR" = 12 ]; then
    endmonth=$(($FORM_month + $FORM_plotsum - 1))
fi
if [ -z "$FORM_year2" ]; then
    if [ $endmonth -gt 12 ]; then
        plotyear="$(($FORM_year + 1))\\"
    else
        plotyear="$FORM_year\\"
    fi
fi
if [ $NPERYEAR -le 12 ]; then
    sumstring=${FORM_plotsum},${FORM_plotsum}
fi
echo "date = $date $date2<br>"
station=$kindname
CLIM=$climfield

. ./grads.cgi

. ./myvinkfoot.cgi
