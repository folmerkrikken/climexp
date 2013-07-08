#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=s
NAME="eu sealevel pressure"
NPERYEAR=12
export DIR=`pwd`
PROG=geteuslp
FROM="from <a href="advice.cgi?id=$EMAIL" target="_new">ADVICE database</a>"

. $DIR/getdata.cgi
