#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi
WMO=ar1_$$
if [ "$FORM_a1" = "0.0" ]; then
  if [ "$FORM_a2" = "0.0" ]; then
    STATION="white noise"
  else
    STATION="yearly red noise $FORM_a2"
  fi
else
  if [ "$FORM_a2" = "0.0" ]; then
    STATION="monthly red noise $FORM_a1"
  else
    STATION="doubly red noise $FORM_a1 $FORM_a2"
  fi
fi
TYPE=i
NAME="Index"
PROG="ar1 12 $FORM_a1 $FORM_a2"

. $DIR/getdata.cgi
