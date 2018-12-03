#!/bin/bash
#
# average an ensemble of time series

export DIR=`pwd`
. ./getargs.cgi

[ -z "$FORM_oper" ] && FORM_oper=mean
if [ -z "$FORM_nens1" -a -z "$FORM_nens2" ]; then
    WMO=`echo "$FORM_wmo" | sed -e "s/\+\+\+/$FORM_oper/" -e "s/\+\+/$FORM_oper/"`
    STATION="$FORM_station $FORM_oper"
else
    WMO=`echo "$FORM_wmo" | sed -e "s/\+\+\+/${FORM_oper}_${FORM_nens1}_${FORM_nens2}/" -e "s/\+\+/${FORM_oper}_${FORM_nens1}_${FORM_nens2}/"`
    STATION="$FORM_station $FORM_oper ${FORM_nens1}:${FORM_nens2}"
fi
TYPE="$FORM_type"
NAME="$FORM_name"
PROG="average_ensemble data/$TYPE$FORM_wmo.dat ens ${FORM_nens1:-0} ${FORM_nens2:-999} $FORM_oper"

. ./getdata.cgi
