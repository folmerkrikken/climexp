#!/bin/sh
# make a time series with a shorter time scale than the original

export DIR=`pwd`
. ./getargs.cgi
STATION=$FORM_STATION
WMO=$FORM_WMO
TYPE=$FORM_TYPE
NAME=$FORM_NAME
NPERYEAR="$FORM_NPERNEW"

corrargs="$DIR/data/$TYPE$WMO.dat $NPERYEAR mon $FORM_mon $FORM_oper $FORM_sum"
WMO=${WMO}_$FORM_oper$NPERYEAR

PROG="yearly2shorter $corrargs"

. $DIR/getdata.cgi

