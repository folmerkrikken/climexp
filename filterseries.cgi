#!/bin/sh
#
# select a period from a data file

export DIR=`pwd`
. ./getargs.cgi

WMO="${FORM_wmo}_${FORM_month}${FORM_hilo}-pass"
STATION="$FORM_station"
TYPE=$FORM_type
NAME=$FORM_name
file=`basename $FORM_file`
PROG="filtermonthseries ${FORM_hilo} ${FORM_filtertype} ${FORM_month} $DIR/data/$file"

. $DIR/getdata.cgi
