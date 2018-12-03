#!/bin/bash
# wrapper for getdata.cgi to analyse anomalies as a time series
export DIR=`pwd`

. ./init.cgi
. ./getargs.cgi
STATION="$FORM_STATION"
export TYPE="$FORM_TYPE"
NPERYEAR="$FORM_NPERYEAR"
NAME="$FORM_NAME"

root=`basename $FORM_datafile .txt | tr '%' '+'`
datafile=data/$root.txt
ensemblefile=`echo "$datafile" | tr '%' '+'`
if [ $datafile != $ensemblefile ]; then
    ENSEMBLE=true
fi
if [ ! -s $ensemblefile ]; then
    echo 'Content-Type: text/html'
    echo
    . ./myvinkhead.cgi "Error" "Analysing anomaly series"
    echo "Cannot find file $ensemblefile<br>"
    . ./myvinkfoot.cgi
    exit
fi

if [ -z "$ENSEMBLE" ]; then
    cp $datafile data/$root.dat
else
    bin/txt2dat $ensemblefile > data/$root.dat
fi

PROG=
WMO=data/${root#$TYPE}
. ./getdata.cgi
