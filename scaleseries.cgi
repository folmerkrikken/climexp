#!/bin/bash
#
# select a period from a data file

export DIR=`pwd`
. ./getargs.cgi

WMO="${FORM_wmo}_${FORM_factor}"
STATION="$FORM_station"
TYPE=$FORM_type
NAME=$FORM_name
file=./data/$TYPE$FORM_wmo.dat
export WMO
export file
export TYPE
PROG="scaleseries.sh ${FORM_factor} $file"

. $DIR/getdata.cgi
