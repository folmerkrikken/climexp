#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
###echo '<pre>'
###set | fgrep FORM_
###echo '</pre>'
###exit

# check email address
. ./checkemail.cgi

# real work
. ./save_commonoptions.cgi
. ./save_variable.cgi

# another field?
if [ ${FORM_field:-none} != none ]; then
# common options
  . $DIR/getopts.cgi
# and go
  . $DIR/correlatefieldfield.cgi
  exit
fi
# the sign of the lags is opposite to what correlatefield.cgi expects.
if [ -n "$FORM_lag" ]; then
  firstlag=`echo ${FORM_lag:-0} | sed -e 's/\:.*//'`
  lastlag=`echo ${FORM_lag:-0} | sed -e 's/.*\://'`
  if [ $firstlag = $lastlag ]; then
     FORM_lag=$((-1*($firstlag)))
  else
     FORM_lag=$((-1*($lastlag))):$((-1*($firstlag)))
  fi
fi
# the meaning of fix1, fix2 is reversed
if [ "$FORM_fix" = "fix1" ]; then
  FORM_fix="fix2"
else
  FORM_fix="fix1"
fi
# the meaning of index/data is reversed
aap="$FORM_lt"
FORM_lt="$FORM_dlt"
FORM_dlt="$aap"
aap="$FORM_gt"
FORM_gt="$FORM_dgt"
FORM_dgt="$aap"
# only one field...
FORM_field=$FORM_field1
. $DIR/queryfield.cgi
# common options
. $DIR/getopts.cgi

if [ -z "$FORM_timeseries" ]; then
  . ./myvinkhead.cgi "Error" "" "noindex,nofollow"
  echo "Please select a timeseries or field to correlate with."
  . ./myvinkfoot.cgi
  exit
fi
###echo "NPERYEAR=$NPERYEAR<br>"
CLIM=index
forbidden='!`;&|'
case $FORM_timeseries in
  nino12)    station="NINO12";sfile="$DIR/NCDCData/ersst_nino12a.dat";;
  nino3)     station="NINO3";sfile="$DIR/NCDCData/ersst_nino3a.dat";;
  nino34)    station="NINO3.4";sfile="$DIR/NCDCData/ersst_nino3.4a.dat";;
  nino4)     station="NINO4";sfile="$DIR/NCDCData/ersst_nino4a.dat";;
  soi)       station="SOI";sfile="$DIR/CRUData/soi.dat";;
  nao)       station="NAO-Gibraltar";sfile="$DIR/CRUData/nao.dat";;
  sunspots)  station="sunspots";sfile="$DIR/SIDCData/sunspots.dat";;
  co2)       station="CO2"
             if [ ${NPERYEAR:-12} = 12 ]; then
                sfile="$DIR/CDIACData/co2_monthly.dat"
             elif [ $NPERYEAR = 1 -o $NOERYEAR = -1 ]; then
                sfile="$DIR/CDIACData/co2_annual.dat"
             fi;;
  gmst)      station="GMST"
             if [ ${NPERYEAR:-12} = 12 ]; then
                sfile="$DIR/NASAData/giss_al_gl_m.dat"
             elif [ $NPERYEAR = 1 -o $NPERYEAR = -1 ]; then
                sfile="$DIR/NASAData/giss_al_gl_a_4yrlo.dat"
             fi;;
  time)      station="time";sfile="$DIR/KNMIData/time$NPERYEAR.dat";;
  *)         station=`head -2 $FORM_timeseries | tail -1 | tr '_' ' '`
             sfile=$DIR/`head -1 $FORM_timeseries | tr $forbidden '?'`
	   TYPE=`basename $sfile | cut -b 1`
	   case $TYPE in
	   t) CLIM="temperature";;
	   p) CLIM="precipitation";;
	   s) CLIM="pressure";;
	   l) CLIM="sealevel";;
	   r) CLIM="runoff";;
	   c) CLIM="correlation";;
           *) CLIM="index";;
           esac
           ;;
esac
WMO=`basename $sfile .dat`
# to signal to grads.cgi that we are doing a correlation (dirty)
FORM_STATION="$station" 
corrargs="$sfile $corrargs"

. $DIR/correlatefield.cgi
exit
