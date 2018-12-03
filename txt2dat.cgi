#!/bin/bash

. ./init.cgi
. ./getargs.cgi
###echo "Content-Type: text/plain"; echo; set; exit
WMO="$FORM_WMO"
STATION="$FORM_STATION"
export TYPE=i
NAME=""
NPERYEAR=1
export DIR=`pwd`
PROG="txt2dat"

. $DIR/getdata.cgi
