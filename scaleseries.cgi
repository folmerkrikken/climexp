#!/bin/sh
#
# select a period from a data file

export DIR=`pwd`
. ./getargs.cgi

WMO="${FORM_wmo}_${FORM_factor}"
STATION="$FORM_station"
TYPE=$FORM_type
NAME=$FORM_name
PROG="scaleseries ${FORM_factor} $DIR/data/$TYPE$FORM_wmo.dat"

. $DIR/getdata.cgi
