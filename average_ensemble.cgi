#!/bin/sh
#
# average an ensemble of time series

export DIR=`pwd`
. ./getargs.cgi

# no ensemble memebr selection yet

if [ -z "$FORM_nens1" -a -z "$FORM_nens2" ]; then
    WMO=`echo "$FORM_wmo" | sed -e "s/\+\+\+/mean/" -e "s/\+\+/mean/"`
    STATION="$FORM_station mean"
else
    WMO=`echo "$FORM_wmo" | sed -e "s/\+\+\+/mean_${FORM_nens1}_${FORM_nens2}/" -e "s/\+\+/mean_${FORM_nens1}_${FORM_nens2}/"`
    STATION="$FORM_station mean ${FORM_nens1}:${FORM_nens2}"
fi
TYPE="$FORM_type"
NAME="$FORM_name"
PROG="average_ensemble data/$TYPE$FORM_wmo.dat ens ${FORM_nens1:-0} ${FORM_nens2:-999}"

. $DIR/getdata.cgi
