#!/bin/bash
. ./init.cgi

if [ -z "$FORM_period" ]; then
# stand-alone
echo 'Content-Type: text/html'
echo

export DIR=`pwd`
. ./getargs.cgi
# check email address
. ./checkemail.cgi
# off-limits for robots
. ./nosearchengine.cgi
# and save
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.field.$NPERYEAR <<EOF
FORM_field=$FORM_field;
EOF
  cat > ./prefs/$EMAIL.verification.$NPERYEAR <<EOF
FORM_verif=$FORM_verif;
EOF
fi

# what field is field2?
if [ "$FORM_field" = "perfectmodel" ]; then
  file="perfectmodel"
  climfield="perfect model"
  FORM_debias=""
else
  . ./queryfield.cgi
fi
field2=`basename $FORM_field .info`
file2=$file
kindname2=$kindname
climfield2=$climfield
map2=$map
flipcolor2=$flipcolor
# what field is field1?
FORM_field=$FORM_field1
. ./queryfield.cgi
# and save
field1=`basename $FORM_field .info`
file1=$file
kindname1=$kindname
climfield1=$climfield
map1=$map
flipcolor1=$flipcolor

else # called from forecast_verification.cgi
  if [ $FORM_period != custom ]; then
    FORM_begin=""
    FORM_end=""
  fi
fi # the rest is shared with forecast_verification.cgi

. ./getopts.cgi
. ./getfieldopts.cgi
commonargs=$corrargs
corrargs="$file1 $file2 $corrargs"
if [ ${FORM_verif%persist} != $FORM_verif -o ${FORM_verif%nino34} != $FORM_verif ]; then
  corrargs="$corrargs interp 2"
else
  corrargs="$corrargs interp 2" # for the time being
fi
l2=${FORM_lon2:-360}
l1=${FORM_lon1:-0}
# get rid of the part after the decimal point - bash cannot handle floating point numbers
dlon=$((${l2%%.*} - ${l1%%.*}))
if [ $dlon != 360 ]; then
  [ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
  [ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
fi
l2=${FORM_lat2:-90}
l1=${FORM_lat1:--90}
dlat=$((${l2%%.*} - ${l1%%.*}))
if [ $dlat != 180 ]; then
  [ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
  [ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"
fi
if [ "${FORM_verif#map}" != "$FORM_verif" ]; then
  makemap=map
fi


rootname=regionverification_${field1}_${field2}_${FORM_lon1}_${FORM_lon2}_${FORM_lat1}_${FORM_lat2}_${FORM_month}_${FORM_sum}_${FORM_begin}_${FORM_end}_${FORM_detrend}_${FORM_debias}_${FORM_nens1}_${FORM_nens2}_${FORM_makeensfull}_${FORM_diff}_${FORM_ndiff}_${FORM_log}_${FORM_sqrt}_${FORM_nooverlap}

# Writes to the log file what the user is doing
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) regionverification ${makemap:-table} $corrargs" | sed -e  "s:$DIR/::g" >> log/log
if [ -z "$makemap" ]; then
  table="data/$rootname.table"
  plotlist="data/$rootname.plotlist"
  # make sure to take anomalies so that the climatological gradients over the
  # area do not dominate the score
  corrargs="$corrargs dump $table plot $plotlist anomal"
  anomalies=", taking spatial anomalies"
  . ./myvinkhead.cgi "Verification of grid points" "$kindname1 $climfield1 against $kindname2 $climfield2"  ""
else
  table="data/$rootname.nc"
  corrargs="$corrargs plot $table"
  . ./myvinkhead.cgi "Verification map" "$kindname1 $climfield1 against $kindname2 $climfield2" ""
fi
startstop=data/$rootname.startstop
corrargs="$corrargs startstop $startstop"

if [ 0 = 1 ]; then
  echo '<pre>'
  echo ./bin/getunits.sh $file1
  ./bin/getunits.sh $file1
  echo ./bin/getunits.sh $file2
  ./bin/getunits.sh $file2
  echo ./bin/month2string "$FORM_month" "$FORM_sum" ave
  ./bin/month2string "$FORM_month" "$FORM_sum" ave
  echo '</pre>'
fi
eval `./bin/getunits.sh $file1`
[ "$UNITS" = Celsius ] && NEWUNITS="C"
[ "$NEWUNITS" = Celsius ] && NEWUNITS="C"
if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname1 $climfield1 from $UNITS to $NEWUNITS<br>"
fi
# Make sure reliability plots have no more bins than ensemble members...
if [ -n "$NENS" ]; then
  if [ -n "$FORM_nbins" ]; then
    if [ "$((NENS+1))" -lt "$FORM_nbins" ]; then
      echo "Adjusting number of bins down to number of ensemble members plus one<br>"
      FORM_nbins="$((NENS+1))"
    fi
  else
    echo "Setting number of bins equal to number of ensemble members plus one<br>"
    FORM_nbins="$((NENS+1))"
  fi
fi

eval `./bin/getunits.sh $file2`
[ "$UNITS" = Celsius ] && NEWUNITS="C"
[ "$NEWUNITS" = Celsius ] && NEWUNITS="C"
if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname2 $climfield2 from $UNITS to $NEWUNITS<br>"
fi

if [ -n "$FORM_lon1" ]; then
  if [ -n "$FORM_lon2" -a "$FORM_lon1" != "$FORM_lon2" ]; then
    cutting="cutting out ${FORM_lon1}:${FORM_lon2}&deg;E, "
  else
    cutting="cutting out ${FORM_lon1}&deg;E, "
  fi
fi
if [ -n "$FORM_lat1" ]; then
  if [ -n "$FORM_lat2" -a "$FORM_lat1" != "$FORM_lat2" ]; then
    cutting="$cutting ${FORM_lat1}:${FORM_lat2}&deg;N, "
  else
    cutting="$cutting ${FORM_lat1}&deg;N, "
  fi
fi
eval `./bin/month2string "$FORM_month" "$FORM_sum" ave`
if [ "$FORM_debias" = "mean" ]; then
  debias="correcting for bias in mean"
elif [ "$FORM_debias" = "var" ]; then
  debias="correcting for bias in mean and variance"
elif [ "$FORM_debias" = "all" ]; then
  debias="correcting for bias in whole PDF"
fi
cat <<EOF
<small>Verification is under active development and may still contain bugs.  Please report problems back to <a href="mailto:oldenborgh@knmi.nl">me</a>.</small><p>
EOF
if [ -s $table ]; then
  echo "Using cached data. "
else
  cat <<EOF
Retrieving data, $cutting $seriesmonth average, $debias $anomalies ...
<br><small>If it takes too long you can abort the job <a href="killit.cgi?id=$FORM_EMAIL&pid=$$" target="_new">here</a> (using the [back] button of the browser does <it>not</it> kill the extraction program)</small><p>
EOF

  cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
regionverification $corrargs
$$
EOF
  export SCRIPTPID=$$
  export FORM_EMAIL
###  echo regionverification $corrargs
# The FORTAN program by GJ called verification is run here to produce a
# nice table with columns year, month, obs, ens. member1, ens. member2 ...
# ensemble member n, or netcdf files of obs and forecasts
  ( (echo bin/regionverification $corrargs ; $DIR/bin/regionverification $corrargs) > /tmp/regionverification$$.log ) 2>&1
  rm pid/$$.$FORM_EMAIL
  if [ 0 = 1 ]; then
    echo '<pre>'
    cat /tmp/regionverification$$.log
    echo '</pre>'
  fi
  if [ ! -s $table ]; then
    echo 'Something went wrong!' 
    echo '<pre>'
    cat /tmp/regionverification$$.log
    echo '</pre>'
  fi
  rm /tmp/regionverification$$.log
fi # file cached
if [ ${table%.nc} = $table ]; then
  echo "<a href=$table>Download big table with intermediate results</a><p>"
else
  echo "Download big netcdf files with <a href=$table>intermediate model</a>, <a href=${table%.nc}_obs.nc>observational</a> results</a><p>"
fi
if [ ${FORM_verif%persist} != $FORM_verif -o ${FORM_verif%nino34} != $FORM_verif ]; then
  if [ -z "$FORM_analysis" ];then
    # deduce from field name...
    FORM_analysis=`echo $FORM_field1 | sed -e 's/^.*_//'`
  fi
  if [ ${FORM_verif%nino34} != $FORM_verif ]; then
    series="series NCDCData/ersst_nino3.4a.dat"
    seriesname="nino34"
  fi
  table2=data/statmodel_${field2}_${seriesname}_${FORM_analysis}_${FORM_lon1}_${FORM_lon2}_${FORM_lat1}_${FORM_lat2}_${FORM_month}_${FORM_sum}_${FORM_begin}_${FORM_end}_${FORM_detrend}_${FORM_nens2}.nc
  if [ ! -s $table2 ]; then
    . ./getfieldtype.cgi
    if [ $field_type = Temperature ]; then
      onc=10
      persistence=persistence
    else
      onc=0
      persistence=nopersistence
    fi
    echo "Constructing statistical model using "
    if [ $onc = 0 ]; then
      echo "climatology,"
    else
      echo "$onc-yr running mean climatology (ONC), "
    fi
    if [ $persistence = persistence ]; then
      echo "persistence,"
    fi
    if [ -n "$seriesname" ]; then
      echo "regression on $seriesname,"
    fi
    echo "analysis date 1 $FORM_analysis, summing both predeictor and predictand over $FORM_sum months" 
    echo ./bin/statmodel $file2 analysis $FORM_analysis $persistence onc $onc ensemble 40 $series $commonargs $table2
    ./bin/statmodel $file2 analysis $FORM_analysis $persistence onc $onc ensemble 40 $series $commonargs $table2
  fi
fi # end of statistical atmosphere model

. ./month2string.cgi
. $DIR/setyaxis.cgi
verifxlabel="$kindname2 $climfield2 [$NEWUNITS]"
verifylabel="$FORM_fcstname"
if [ -z "$makemap" ]; then
  ylabel="$ylabel in ${FORM_lat1}:${FORM_lat2}N, ${FORM_lon1}:${FORM_lon2}E"
fi

# the rest is common with verification
. ./verification1.cgi
