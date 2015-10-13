#!/bin/sh
# wrapper for getdata.cgi to analyse anomalies as a time series
export DIR=`pwd`

. ./init.cgi
. ./getargs.cgi
STATION="$FORM_STATION"
TYPE="$FORM_TYPE"
NPERYEAR="$FORM_NPERYEAR"
NAME="$FORM_NAME"

root=`basename $FORM_datafile .txt`
datafile=data/$root.txt
if [ ! -s $datafile ]; then
    echo 'Content-Type: text/html'
    echo
    . ./myvinkhead "Error" "analysing anomaly series"
    echo "Cannot find textfile $datafile"
    . ./myvinkfoot.cgi
    exit
fi

cp $datafile data/$root.dat
WMO=data/${root#$TYPE}
PROG=
. ./getdata.cgi
