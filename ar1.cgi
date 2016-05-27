#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi

NPERYEAR=${FORM_NPERYEAR:-12}
WMO=$FORM_WMO
if [ -z "$WMO" ]; then
    WMO=ar1_$$
    if [ "$FORM_a1" = "0.0" ]; then
      if [ "$FORM_a2" = "0.0" ]; then
        STATION="white noise"
      else
        STATION="yearly red noise $FORM_a2"
      fi
    else
      if [ "$FORM_a2" = "0.0" ]; then
        STATION="red noise $FORM_a1"
      else
        STATION="doubly red noise $FORM_a1 $FORM_a2"
      fi
    fi
    TYPE=i
    NAME="Index"
    PROG="ar1 $NPERYEAR $FORM_a1 $FORM_a2"
else
    export TYPE=$FORM_TYPE
    STATION="noise based on $FORM_STATION"
    NAME=$FORM_NAME
    export file=data/$TYPE$WMO.dat
    export WMO=${WMO}_noise_+++
    export nmax=$FORM_n
    PROG="ar1.sh $file"
fi

. ./getdata.cgi
