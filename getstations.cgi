#!/bin/sh
if [ -z "$myvinkhead" ]; then
    echo "Content-Type:text/html"
    . ./expires.cgi
    echo
    echo
fi

. ./searchengine.cgi

export DIR=`pwd`
# printenv
if [ -z "$EMAIL" ]; then
    . ./getargs.cgi
    save_preferences=true
else
    # do not save the preferences if not called directly
    save_preferences=false
fi
if [ -z "$EMAIL" ]; then
   echo "getstations: internal error: EMAIL undefined" 1>&2   
   EMAIL=someone@somewhere
fi
if [ $EMAIL = oldenborgh@knmi.nl ]; then
    lwrite=false
fi
if [ $save_preferences = true -a $EMAIL != someone@somewhere ]; then
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
  FORM_name=`echo "$FORM_name" | tr ' ' '_'`
fi

if [ -z "$listname" ]; then
  # not sourced from another script that already set a lot of things
  if [ -n "$FORM_name" ]; then
    fortargs=`echo "$FORM_name" | tr '[:lower:]' '[:upper:]'`
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
    . ./myvinkhead.cgi "Found station data" "$timescale$FORM_climate station $fortargs"
  elif [ -z "$FORM_lon" -a -z "$FORM_lat" \
      -a -z "$FORM_lon1" -a -z "$FORM_lon2" \
      -a -z "$FORM_lat1" -a -z "$FORM_lat2" -a -n "$FORM_list" ]; then
    list=data/list$$.txt
    forbidden='!`;&|#%\$'
    cat << EOF | tr '\r' '\n' | tr $forbidden '?' > $list
$FORM_list
EOF
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
    type=p
  elif [ "$FORM_climate" = "precipitation_all" ]; then
    prog=getprcpall
    type=p
  elif [ "$FORM_climate" = "temperature" ]; then
    prog=gettemp
    type=t
  elif [ "$FORM_climate" = "min_temperature" ]; then
    prog=getmin
    type=n
  elif [ "$FORM_climate" = "max_temperature" ]; then
    prog=getmax
  elif [ "$FORM_climate" = "temperature_all" ]; then
    prog=gettempall
    type=t
  elif [ "$FORM_climate" = "min_temperature_all" ]; then
    prog=getminall
    type=n
  elif [ "$FORM_climate" = "max_temperature_all" ]; then
    prog=getmaxall
    type=x
  elif [ "$FORM_climate" = "sealevel_pressure" ]; then
    prog=getslp
  elif [ "$FORM_climate" = "sealevel" ]; then
    prog=getsealevel
    type=l
  elif [ "$FORM_climate" = "sealev" ]; then
    prog=getsealev
    type=l
  elif [ "$FORM_climate" = "runoff" ]; then
    prog=getrunoff
    type=r
  elif [ "$FORM_climate" = "streamflow" ]; then
    prog=getusrunoff
    type=r
  elif [ "$FORM_climate" = "streamflowdaily" ]; then
    prog=getdailyusrunoff
    type=r
  elif [ "$FORM_climate" = "ecaprcp" ]; then
    prog=ecaprcp
    type=p
  elif [ "$FORM_climate" = "ecatemp" ]; then
    prog=ecatemp
    type=t
  elif [ "$FORM_climate" = "ecatmin" ]; then
    prog=ecatmin
    type=n
  elif [ "$FORM_climate" = "ecatmax" ]; then
    prog=ecatmax
    type=x
  elif [ "$FORM_climate" = "ecatave" ]; then
    prog=ecatave
    type=t
  elif [ "$FORM_climate" = "ecapres" ]; then
    prog=ecapres
    type=s
  elif [ "$FORM_climate" = "ecasnow" ]; then
    prog=ecasnow
    type=d
  elif [ "$FORM_climate" = "ecaclou" ]; then
    prog=ecaclou
    type=c
  elif [ "$FORM_climate" = "becaprcp" ]; then
    prog=becaprcp
    type=p
  elif [ "$FORM_climate" = "becatemp" ]; then
    prog=becatemp
    type=t
  elif [ "$FORM_climate" = "becatmin" ]; then
    prog=becatmin
    type=n
  elif [ "$FORM_climate" = "becatmax" ]; then
    prog=becatmax
    type=x
  elif [ "$FORM_climate" = "becapres" ]; then
    prog=becapres
    type=s
  elif [ "$FORM_climate" = "becasnow" ]; then
    prog=becasnow
    type=d
  elif [ "$FORM_climate" = "becaclou" ]; then
    prog=becaclou
    type=c
  elif [ "$FORM_climate" = "gdcnprcp" ]; then
    prog=gdcnprcp
    type=p
  elif [ "$FORM_climate" = "gdcnprcpall" ]; then
    prog=gdcnprcpall
    type=p
  elif [ "$FORM_climate" = "gdcnsnow" ]; then
    prog=gdcnsnow
    type=f
  elif [ "$FORM_climate" = "gdcnsnwd" ]; then
    prog=gdcnsnwd
    type=d
  elif [ "$FORM_climate" = "gdcntmin" ]; then
    prog=gdcntmin
    type=n
  elif [ "$FORM_climate" = "gdcntmax" ]; then
    prog=gdcntmax
    type=x
  elif [ "$FORM_climate" = "gdcntave" ]; then
    prog=gdcntave
    type=v
  elif [ "$FORM_climate" = "eu_sealevel_pressure" ]; then
    prog=geteuslp
    type=s
  elif [ "$FORM_climate" = "snow" ]; then
    prog=getsnow
    type=d
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
  if [ ! -s "$listname" ]; then
    . ./myvinkhead.cgi "Internal error"
    echo "Cannot find $listname"
    . ./myvinkfoot.cgi
    exit
  fi
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
else
    location=`echo "with string $FORM_name" | tr ' +' '__'`
fi
TYPE="$FORM_climate"
WMO="$prog"
NAME=`basename "$listname"`
if [ "$FORM_gridpoints" != true ]; then
    # when I have a set of grid ponts, the trick to append the options
    # separated by underscores does not work as the name already has 
    # underscores from FORM_field
    if [ "$NPERYEAR" = 366 ]; then
        echo "<form action=\"daily2longerbox.cgi\" method=\"POST\">"
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
if [ $EMAIL != someone@somewhere ]; then
    def=prefs/$EMAIL.setoper.$NPERYEAR
    if [ -s $def ]; then
        eval `egrep '^FORM_[A-Za-z0-9]*=[a-zA-Z_]*[-+0-9.]*;$' $def`
    fi  
fi

case ${FORM_setoper:-mean} in
    min) minselected=selected;;
    max) maxselected=selected;;
    num) numsleected=selected;;
    *) meanselected=selected;;
esac

cat <<EOF
<form action="average_set.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="type" value="$type">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="series $location">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="extraargs" value="$extraargs">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<div class="formheader"><a href="javascript:pop_page('help/averageseries.shtml',568,450)"><img src="images/info-i.gif" align="right"alt="help" border="0"></a>Aggregate this set of time series</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Type:
<td><select class="forminput" name="setoper">
<option value="mean" $meanselected>unweighted mean
<option value="min" $minselected>minimum
<option value="max" $maxselected>maximum
<option value="num" $numselected>number with data
</select>
<tr><td colspan=2><input type="submit" class="formbutton" value="make time series">
</td></tr></table>
</div>
</form>
EOF

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
	-e "s#\([-GHCNDECAWMONRCS Ss]*tation code: *\)\([0-9\.]*[-0-9A-Z]*\) *\(.*\)\$#\1\2 (<a href=\"$prog.cgi\?id=$FORM_email\&WMO=\2\\&STATION=\3\&extraargs=$extraargs\">get data</a>)#" \
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
