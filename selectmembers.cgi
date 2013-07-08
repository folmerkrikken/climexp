#!/bin/sh
#
# select an ensemble member from an ensemble of time series

export DIR=`pwd`
. ./getargs.cgi

if [ $FORM_nens1 -lt 10 ]; then
  WMO=`echo $FORM_wmo | sed -e "s/\+\+\+/00$FORM_nens1/" -e "s/\+\+/0$FORM_nens1/"`
elif [ $FORM_nens1 -lt 100 ]; then
  WMO=`echo $FORM_wmo | sed -e "s/\+\+\+/0$FORM_nens1/" -e "s/\+\+/$FORM_nens1/"`
else
  WMO=`echo $FORM_wmo | sed -e "s/\+\+\+/$FORM_nens1/"`
fi
STATION="$FORM_station member $FORM_nens1"
TYPE=$FORM_type
NAME=$FORM_name
if [ -z "$FORM_ensanom" ]; then
  PROG=""
else
  PROG="seriesensanomal $FORM_nens1 data/$TYPE$FORM_wmo.dat"
  STATION="$STATION ens anom"
  WMO=${WMO}_ensanom
fi

. $DIR/getdata.cgi
