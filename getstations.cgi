#!/bin/sh
echo "Content-Type:text/html"
. ./expires.cgi
echo
echo

. ./searchengine.cgi

export DIR=`pwd`
# printenv
if [ -z "$EMAIL" ]; then
  . ./getargs.cgi
fi
if [ -z "$EMAIL" ]; then
   echo "getstations: internal error: EMAIL undefined" 1>&2   
   EMAIL=someone@somewhere
fi
if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false
fi
if [ $EMAIL != someone@somewhere ]; then
  if [ -n "$FORM_name" ]; then
    FORM_NAME=`echo "$FORM_name" | tr ' ' '_'`
  fi
  cat > prefs/$EMAIL.getstations <<EOF
FORM_climate=$FORM_climate;
FORM_min=$FORM_min;
FORM_sum=$FORM_sum;
FORM_month=$FORM_month;
FORM_dist=$FORM_dist;
FORM_elevmin=$FORM_elevmin;
FORM_elevmax=$FORM_elevmax;
FORM_num=$FORM_num;
FORM_lat=$FORM_lat;
FORM_lon=$FORM_lon;
FORM_NAME=$FORM_NAME;
FORM_lat1=$FORM_lat1;
FORM_lon1=$FORM_lon1;
FORM_lat2=$FORM_lat2;
FORM_lon2=$FORM_lon2;
FORM_yr1=$FORM_yr1;
FORM_yr2=$FORM_yr2;
FORM_list=$FORM_list;
EOF
fi

if [ -z "$FORM_climate" ]; then
  . ./myvinkhead.cgi "Search station data" ""
  cat <<EOF
<div class="alineakop">Error</div>
Please specify which database to search
EOF
  . ./myvinkfoot.cgi
  exit
fi

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12
  if [ "${FORM_climate#eca}" != "$FORM_climate" -o \
       "${FORM_climate#beca}" != "$FORM_climate" ]; then
    NPERYEAR=366
  fi
  if [ "${FORM_climate#gdcn}" != "$FORM_climate" ]; then
    NPERYEAR=366
  fi
  if [ "${FORM_climate%daily}" != "$FORM_climate" ]; then
    NPERYEAR=366
  fi
fi
. ./nperyear2timescale.cgi
if [ -n "$FORM_name" ]; then
  FORM_name=`echo "$FORM_name" | tr ' ' '+'`
fi

if [ -z "$listname" ]; then
  # not sourced from another script that already set a lot of things
  if [ -n "$FORM_name" ]; then
    fortargs=`echo "$FORM_name" | tr '[:lower:]' '[:upper:]'`
    . ./myvinkhead.cgi "Found station data" "$timescale$FORM_climate station $fortargs"
  elif [ -z "$FORM_lon" -a -z "$FORM_lat" \
      -a -z "$FORM_lon1" -a -z "$FORM_lon2" \
      -a -z "$FORM_lat1" -a -z "$FORM_lat2" -a -n "$FORM_list" ]; then
    list=data/list$$.txt
    forbidden='!`;&|'
    cat << ditisheteinde | tr '\r' '\n' | tr $forbidden '?' > $list
$FORM_list
ditisheteinde
    fortargs="list $list"
    . ./myvinkhead.cgi "Uploaded time series" "$timescale$FORM_climate station list"
  else
    if [ -z "$FORM_lat" -o -z "$FORM_lon" ] ; then
      if [ -z "$FORM_lat1" -o -z "$FORM_lon1" -o \
           -z "$FORM_lat2" -o -z "$FORM_lon2" ]; then
        . ./myvinkhead.cgi "Search station data" ""
        echo '<div class="alineakop">Error</div>'
        echo 'Please specify both latitude and longitude'
        . ./myvinkfoot.cgi
        exit
      fi
      location="between ${FORM_lat1}N to ${FORM_lat2}N and ${FORM_lon1}E to ${FORM_lon2}E"
      . ./myvinkhead.cgi "Found station data" "$timescale$FORM_climate stations $location"
      fortargs="${FORM_lat1}:${FORM_lat2} ${FORM_lon1}:${FORM_lon2}"
    else
      location="near ${FORM_lat}N ${FORM_lon}E"
      . ./myvinkhead.cgi "Found station data" "$timescale$FORM_climate stations $location"
      fortargs="$FORM_lat $FORM_lon $FORM_num"
    fi
    if [ -n "$FORM_min" ] ; then
      fortargs="$fortargs min $FORM_min"
      if [ -n "$FORM_month" -a "$FORM_month" != "-1" ]; then
        fortargs="$fortargs mon $FORM_month sum $FORM_sum"
      fi
    fi
    if [ -n "$FORM_dist" ] ; then
      fortargs="$fortargs dist $FORM_dist"
    fi
    if [ -n "$FORM_elevmin" ] ; then
      fortargs="$fortargs elevmin $FORM_elevmin"
    fi
    if [ -n "$FORM_elevmax" ] ; then
      fortargs="$fortargs elevmax $FORM_elevmax"
    fi
    if [ -n "$FORM_yr1" ] ; then
      fortargs="$fortargs begin $FORM_yr1"
    fi
    if [ -n "$FORM_yr2" ] ; then
      fortargs="$fortargs end $FORM_yr2"
    fi
  fi
  format=new
  if [ "$FORM_climate" = "precipitation" ]; then
    prog=getprcp
  elif [ "$FORM_climate" = "precipitation_all" ]; then
    prog=getprcpall
  elif [ "$FORM_climate" = "temperature" ]; then
    prog=gettemp
  elif [ "$FORM_climate" = "min_temperature" ]; then
    prog=getmin
  elif [ "$FORM_climate" = "max_temperature" ]; then
    prog=getmax
  elif [ "$FORM_climate" = "temperature_all" ]; then
    prog=gettempall
  elif [ "$FORM_climate" = "min_temperature_all" ]; then
    prog=getminall
  elif [ "$FORM_climate" = "max_temperature_all" ]; then
    prog=getmaxall
  elif [ "$FORM_climate" = "sealevel_pressure" ]; then
    prog=getslp
  elif [ "$FORM_climate" = "sealevel" ]; then
    prog=getsealevel
  elif [ "$FORM_climate" = "sealev" ]; then
    prog=getsealev
  elif [ "$FORM_climate" = "runoff" ]; then
    prog=getrunoff
  elif [ "$FORM_climate" = "streamflow" ]; then
    prog=getusrunoff
  elif [ "$FORM_climate" = "streamflowdaily" ]; then
    prog=getdailyusrunoff
  elif [ "$FORM_climate" = "ecaprcp" ]; then
    prog=ecaprcp
  elif [ "$FORM_climate" = "ecatemp" ]; then
    prog=ecatemp
  elif [ "$FORM_climate" = "ecatmin" ]; then
    prog=ecatmin
  elif [ "$FORM_climate" = "ecatmax" ]; then
    prog=ecatmax
  elif [ "$FORM_climate" = "ecatave" ]; then
    prog=ecatave
  elif [ "$FORM_climate" = "ecatdif" ]; then
    prog=ecatdif
  elif [ "$FORM_climate" = "ecapres" ]; then
    prog=ecapres
  elif [ "$FORM_climate" = "ecasnow" ]; then
    prog=ecasnow
  elif [ "$FORM_climate" = "ecaclou" ]; then
    prog=ecaclou
  elif [ "$FORM_climate" = "becaprcp" ]; then
    prog=becaprcp
  elif [ "$FORM_climate" = "becatemp" ]; then
    prog=becatemp
  elif [ "$FORM_climate" = "becatmin" ]; then
    prog=becatmin
  elif [ "$FORM_climate" = "becatmax" ]; then
    prog=becatmax
  elif [ "$FORM_climate" = "becapres" ]; then
    prog=becapres
  elif [ "$FORM_climate" = "becasnow" ]; then
    prog=becasnow
  elif [ "$FORM_climate" = "becaclou" ]; then
    prog=becaclou
  elif [ "$FORM_climate" = "gdcnprcp" ]; then
    prog=gdcnprcp
  elif [ "$FORM_climate" = "gdcnprcpall" ]; then
    prog=gdcnprcpall
  elif [ "$FORM_climate" = "gdcnsnow" ]; then
    prog=gdcnsnow
  elif [ "$FORM_climate" = "gdcnsnwd" ]; then
    prog=gdcnsnwd
  elif [ "$FORM_climate" = "gdcntmin" ]; then
    prog=gdcntmin
  elif [ "$FORM_climate" = "gdcntmax" ]; then
    prog=gdcntmax
  elif [ "$FORM_climate" = "eu_sealevel_pressure" ]; then
    prog=geteuslp
  elif [ "$FORM_climate" = "snow" ]; then
    prog=getsnow
  else
    echo "<div class=\"alineakop\">Error</div>The database for $FORM_climate is not (yet?) available"
    . ./myvinkfoot.cgi
    exit
  fi

  listname=data/list_${FORM_climate}_${FORM_lon1:-$FORM_lon}:${FORM_lon2}_${FORM_lat1}:${FORM_lat2:-$FORM_lat}_${FORM_min}_${FORM_sum}_${FORM_month}_${FORM_elevmin}:${FORM_elevmax}_${FORM_dist}_${FORM_name}.txt
  if [ "$lwrite" = true ]; then
    echo "<pre>"
    echo ./bin/$prog $fortargs
    echo "</pre>"
  fi
  if [ -n "$FORM_yr1" -o -n "$FORM_yr2" ]; then
      echo "Selecting a period takes quite a bit longer.  Please be patient.<p>"
  fi
  if [ ! -z "$listname" ]; then
    ./bin/$prog $fortargs > "$listname"
  fi
elif [ ${listname#data} = $listname ]; then
# the list is not in the data directory, so it has been pre-made
# this is the case for the Indian and Dutch data (maybe more)
  . ./myvinkhead.cgi "Found station data" "$timescale$FORM_climate stations"
# there are too many scripts (i.e., at least one) that expect that the 
# list lives in data/
  cp $listname data/`basename $listname`
else
# called from daily2longerbox.cgi
  . ./myvinkhead.cgi "Derived time series" "$timescale$FORM_climate stations"
fi

if [ -z "$FORM_name" ]; then
  location=`echo $location|tr ' ' '_'`
###  echo "NPERYEAR = $NPERYEAR"
  if [ "$NPERYEAR" = 366 ]; then
    echo "<form action=\"daily2longerbox.cgi\" method=\"POST\">"
    EMAIL="$FORM_email"
    TYPE="$FORM_climate"
    WMO="$prog"
    NAME=`basename "$listname"`
    cat <<EOF
<div class="formheader"><a href="javascript:pop_page('help/lowerresolutionset.shtml',568,450)"><img src="images/info-i.gif" align="right"alt="help" border="0"></a>Create a new set of station data</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>
EOF
    . ./daily2longerform.cgi
cat <<EOF
<input type="submit" class="formbutton" value="make new set of time series">
</td></tr></table>
</div>
</form>
EOF
  fi
fi
if [ 1 = 0 ]; then
echo '<pre>'
cat $listname
echo '</pre>'
fi
if [ "$format" = new ]; then
    sed \
	-e 's/====*//' \
	-e 's/^# //' \
	-e 's/ *$//' \
	-e "s#\([-GHCNDECAWMONRCS Ss]*tation code: *\)\([0-9\.]*[0-9A-Z]*\) *\(.*\)\$#\1\2 (<a href=\"$prog.cgi\?id=$FORM_email\&WMO=\2\\&STATION=\3\&extraargs=$extraargs\">get data</a>)#" \
	-e "s#\(grid point: *\)\([0-9\._in-]*\) *\(.*\)\$#\1\2 (<a href=\"getindices.cgi\?WMO=data/grid${FORM_field}\2\&STATION=\3\&TYPE=i\&id=$FORM_email\&NPERYEAR=$NPERYEAR\">get data</a>)#" \
	-e 's/$/<br>/' "$listname"
else
    sed \
	-e 's/====*//' \
	-e 's/^# //' \
	-e 's/ *$//' \
	-e "s#\([-GHCNDECAWMONRCS Ss]*tation code: *\)\([0-9\.]*[0-9A-Z]*\) *\(.*\)\$#\1\2 (<a href=\"$prog.cgi\?$FORM_email+\2\+\3+$extraargs\">get data</a>)#" \
	-e "s#\(grid point: *\)\([0-9\._in-]*\) *\(.*\)\$#\1\2 (<a href=\"getindices.cgi\?WMO=data/grid${FORM_field}\2\&STATION=\3\&TYPE=i\&id=$FORM_email\&NPERYEAR=$NPERYEAR\">get data</a>)#" \
	-e 's/$/<br>/' "$listname"
fi

. ./myvinkfoot.cgi
