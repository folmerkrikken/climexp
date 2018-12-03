#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo

export DIR=`pwd`
. ./getargs.cgi

. ./queryfield.cgi
# and save
field2=$FORM_field
file2=$file
kindname2=$kindname
climfield2=$climfield
map2=$map
flipcolor2=$flipcolor
# what field is field1?
FORM_field=$FORM_field1
. ./queryfield.cgi
# and save
field1=$FORM_field
file1=$file
kindname1=$kindname
climfield1=$climfield
map1=$map
flipcolor1=$flipcolor

. $DIR/getopts.cgi
case $FORM_analysis in
jan) analysis=1;;
feb) analysis=2;;
mar) analysis=3;;
apr) analysis=4;;
may) analysis=5;;
jun) analysis=6;;
jul) analysis=7;;
aug) analysis=8;;
sep) analysis=9;;
oct) analysis=10;;
nov) analysis=11;;
dec) analysis=12;;
*)   echo "error: expecting jan|...|dec, not $FORM_analysis"
     . ./myvinkfoot.cgi;;
esac
if [ -n "$FORM_persistence" ]; then
  persistence=persistence
  persistencename="persistence,"
else
  persistence=nopersistence
fi
[ -z "$FORM_sum2" ] && FORM_sum2=${FORM_sum:-1}
case "$FORM_timeseries" in
    nino34) series="series NCDCData/ersst_nino3.4a.dat $FORM_sum2";seriesname="Nino3.4,";;
    co2)    series="series CDIACData/maunaloa.dat $FORM_sum2";seriesname="CO2,";;
    *)      series="";seriesname="";;
esac
if [ $FORM_onc = 0 ]; then
  oncname="climatology,"
else
  oncname="${FORM_onc}-yr running mean climatology (ONC),"
fi
corrargs="$file analysis $analysis $persistence onc ${FORM_onc:-0} ensemble ${FORM_nfcstens:-15} $series begin2 1 end2 4000 $corrargs"

if [ $((${FORM_lon2:-360} - ${FORM_lon1:-0})) != 360 ]; then
  [ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
  [ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
fi
if [ $((${FORM_lat2:-90} - ${FORM_lat1:--90})) != 180 ]; then
  [ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
  [ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"
fi
if [ "${FORM_verif#map}" != "$FORM_verif" ]; then
  makemap=map
fi


rootname=statmodel_${field2}_${seriesname}_${FORM_analysis}_${FORM_lon1}_${FORM_lon2}_${FORM_lat1}_${FORM_lat2}_${FORM_month}_${FORM_sum}_${FORM_begin}_${FORM_end}_${FORM_detrend}_${FORM_nens2}

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
  . ./myvinkhead.cgi "Verification map" "Statistical model based on $kindname1 $climfield1 against $kindname2 $climfield2" ""
fi
startstop=data/$rootname.startstop
corrargs="$corrargs startstop $startstop"

if [ 1 = 0 ]; then
  echo '<pre>'
  echo ./bin/getunits.sh $file
  ./bin/getunits.sh $file
  echo ./bin/month2string "$FORM_month" "$FORM_sum" ave
  ./bin/month2string "$FORM_month" "$FORM_sum" ave
  echo '</pre>'
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

cat <<EOF
<small>Verification is under active development and may still contain bugs.  Please report problems back to <a href="imailto:oldenborgh@knmi.nl">me</a>.</small><p>
EOF
if [ -s $table ]; then
  echo "Using cached data<br>"
else
  cat <<EOF
Constructing statistical model, analysis date 1 $FORM_analysis, averaging predictors over ${FORM_sum2:-$FORM_sum} months, including $persistencename $seriesname $oncname $cutting $seriesmonth average ...
<br><small>If it takes too long you can abort the job <a href="killit.cgi?id=$FORM_EMAIL&pid=$$" target="_new">here</a> (using the [back] button of the browser does <it>not</it> kill the extraction program)</small><p>
EOF

  cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
statmodel $corrargs
$$
EOF
  export SCRIPTPID=$$
  export FORM_EMAIL
  ###echo regionverification $corrargs
# The FORTRAN program by GJ called verification is run here to produce a
# nice table with columns year, month, obs, ens. member1, ens. member2 ...
# ensemble member n, or netcdf files of obs and forecasts
  ( (echo bin/statmodel $corrargs ; $DIR/bin/statmodel $corrargs) > /tmp/statmodel$$.log ) 2>&1
  rm pid/$$.$FORM_EMAIL
  if [ 0 = 1 ]; then
    echo '<pre>'
    cat /tmp/statmodel$$.log
    echo '</pre>'
  fi
  if [ ! -s $table ]; then
    echo 'Something went wrong!' 
    echo '<pre>'
    cat /tmp/statmodel$$.log
    echo '</pre>'
  fi
  rm /tmp/statmodel$$.log
fi # file cached

. ./month2string.cgi
. $DIR/setyaxis.cgi
verifxlabel="$kindname2 $climfield2 [$NEWUNITS]"
verifylabel="$FORM_fcstname"
if [ -z "$makemap" ]; then
  ylabel="$ylabel in ${FORM_lat1}:${FORM_lat2}N, ${FORM_lon1}:${FORM_lon2}E"
fi

# the rest is common with verification
. ./verification1.cgi
