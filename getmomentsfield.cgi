#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# check email address
. ./checkemail.cgi
# off-limits for robots
. ./nosearchengine.cgi
if [ "$EMAIL" = oldenborgh@knmi.nl ]; then
   lwrite=false # true
fi

. $DIR/queryfield.cgi
eval `./bin/getunits.sh $file`

if [ -z "$FORM_var" ]; then
  . ./myvinkhead.cgi "Error" "" "noindex,nofollow"
  echo "Please select property"
  . ./myvinkfoot.cgi
  exit
fi
FORM_year=""
if [ "$FORM_var" = "norm_rt" -o "$FORM_var" = "norm_z" ]; then
  FORM_year=$FORM_normyear
elif [ "$FORM_var" = "pot_rt" ]; then
  FORM_year=$FORM_potyear
elif [ "$FORM_var" = "gev_rt" ]; then
  FORM_year=$FORM_gevyear
elif [ "$FORM_var" = "rank" ]; then
  FORM_year=$FORM_rankyear
fi
if [ "$FORM_changesign" = "both" -a -z "FORM_year" ]; then
  . ./myvinkhead.cgi "Error" "" "noindex,nofollow"
  echo "Plotting both tails can only be done when computing a return time or z-value."
  . ./myvinkfoot.cgi
  exit
fi
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.momentsfield.$NPERYEAR << EOF
FORM_var=$FORM_var;
FORM_perc=$FORM_perc;
FORM_threshold=$FORM_threshold;
FORM_changesign=$FORM_changesign;
FORM_pot_return=$FORM_pot_return;
FORM_gev_return=$FORM_gev_return;
FORM_year=$FORM_year;
FORM_restrain=$FORM_restrain;
FORM_pot_tv=$FORM_pot_tv;
FORM_minfac=$FORM_minfac;
EOF
  . ./save_commonoptions.cgi
fi

###if [ ${FORM_var#pot} != $FORM_var ]; then
###  . ./getpotfield.cgi
###  exit
###fi

case $FORM_var in
mean) var="mean";;
sd)   var="standard deviation";;
sdm)  var="s.d./mean";;
skew) var="skewness";;
kurt) var="kurtosis";;
perc) var="${FORM_perc}% percentile";;
max)  var="maximum";;
min)  var="minimum";;
norm_rt)    var="Gauss return time of $FORM_year";;
norm_z)     var="z-value of $FORM_year";;
pot_scale)  var="scale parameter of GPD";;
pot_shape)  var="shape parameter of GPD";;
pot_return) var="$FORM_pot_return yr return value";;
pot_rt)     var="GPD return time of $FORM_year";;
gev_pos)    var="position parameter of GEV";;
gev_scale)  var="scale parameter of GEV";;
gev_shape)  var="shape parameter of GEV";;
gev_return) var="$FORM_gev_return yr return value";;
gev_rt)     var="GEV return time of $FORM_year";;
rank)       var="Rank of $FORM_year";;
timex)      var="Year of extreme";;
*)    var="UNKNOWN";;
esac

corrargs="$FORM_var"
if [ "$FORM_var" = "perc" ]; then
  corrargs="$corrargs $FORM_perc"
elif [  "$FORM_var" = "pot_rt" -o "$FORM_var" = "gev_rt" -o "$FORM_var" = "norm_rt" -o "$FORM_var" = "norm_z" -o "$FORM_var" = "rank" ]; then
  corrargs="$corrargs $FORM_year"
fi
if [ "${FORM_var#pot}" != "$FORM_var" ]; then
  if [ -z "$FORM_threshold" ]; then
    echo"<p>Error: threshold not given"
    . ./myvinkfoot.cgi
  fi
  corrargs="$corrargs dgt ${FORM_threshold}%"
fi
. ./getopts.cgi
. ./getfieldopts.cgi

. ./myvinkhead.cgi "Compute $var" "$kindname $climfield" "noindex,nofollow"

echo `date` "$EMAIL ($REMOTE_ADDR) getfieldmoments $corrargs" | sed -e "s:$DIR/::g" >> log/log

c=`echo $FORM_field | fgrep -c "mean_"`
if [ $c != 0 -a \( $FORM_var = perc -o $FORM_var = sd \) ]; then
    echo "Warning: percentiles and s.d. of a multi-model mean field do not have a physical meaning. Proceed at your own risk."
fi

startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
echo "Computing $var...<p>"
# generate GrADS data file
[ \( "${FORM_var%_rt}" != "$FORM_var" -o "${FORM_var}" = "rank" \) -a "$FORM_changesign" = "both" ] && echo "High extremes...<br>"
( (echo ./bin/getmomentsfield $file $corrargs ./data/m$$.nc;./bin/getmomentsfield $file $corrargs ./data/m$$.nc) > /tmp/getmomentsfield$$.log ) 2>& 1
if [ "${FORM_var%_rt}" != "$FORM_var" -a "$FORM_changesign" = "both" ]; then
    mv ./data/m$$.nc ./data/m$$p.nc
    echo "<p>Low extremes...<br>"
    ( (echo ./bin/getmomentsfield $file $corrargs changesign ./data/m$$m.nc;./bin/getmomentsfield $file $corrargs changesign ./data/m$$m.nc) >> /tmp/getmomentsfield$$.log ) 2>& 1
    echo "<p>Merging results...<p>"
    ( (./bin/merge_pm.py $FORM_var $FORM_year ./data/m$$p.nc ./data/m$$m.nc  ./data/m$$.nc) >> /tmp/getmomentsfield$$.log 2>&1) 
    FORM_var=bo_$FORM_var
    rm data/m$$p.nc data/m$$m.nc data/m$$*.nc.tmp data/m$$*.nc.m.tmp
fi
if [ ! -s ./data/m$$.nc -a ! -s ./data/m$$.dat -a ! -s ./data/m$$.grd ]; then
  cat ./wrong.html
  echo "<pre>"
  cat /tmp/getmomentsfield$$.log
  echo "</pre>"
  . ./myvinkfoot.cgi
  exit
else
  if [ "$lwrite" = true ]; then
    echo '<pre>'
    cat /tmp/getmomentsfield$$.log
    echo '</pre>'
  fi
  rm /tmp/getmomentsfield$$.log
fi

# plot data

# the right place to put
if [ "$FORM_var" = "perc" ]; then
  RANK="${FORM_perc}%"
fi
file=data/m$$.nc
station=$kindname
CLIM=$climfield
if [ ${FORM_var%%_rt} != $FORM_var ]; then
  CLIM="$CLIM [yr]"
elif [ $FORM_var = skew -a $FORM_var = kurt -a $FORM_var = sdm -o $FORM_var = pot_shape -o $FORM_var = norm_z ]; then
  CLIM="$CLIM"
elif [ "$FORM_standardunits" = standardunits ]; then
  CLIM="$CLIM [${NEWUNITS}]"
else
  CLIM="$CLIM [${UNITS}]"
fi
if [ ${FORM_var%%pot} != $FORM_var -o  ${FORM_var%%gev} != $FORM_var ]; then
  if [ "$FORM_changesign" = "both" ]; then
    CLIM="$CLIM\\both extremes"
  elif [ -n "$FORM_changesign" ]; then
    CLIM="$CLIM\\low extremes"
  else
    CLIM="$CLIM\\high extremes"
  fi
fi
if [ ${FORM_var%%pot} != $FORM_var ]; then
  CLIM="$CLIM threshold ${FORM_threshold}%"
fi
if [ $FORM_var = pot_return ]; then
  FORM_var="t$FORM_pot_return"
elif [ $FORM_var = gev_return ]; then
  FORM_var="t$FORM_gev_return"
elif [ ${FORM_var%%_rt} != $FORM_var ]; then
  FORM_var=${FORM_var}_${FORM_year}
elif [ ${FORM_var} = norm_z ]; then
  FORM_var=z_${FORM_year}
fi
datafile="data/m$$"
. ./grads.cgi
. ./myvinkfoot.cgi
