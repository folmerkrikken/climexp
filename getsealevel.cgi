#!/bin/sh

 . ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=l
NAME="Sealevel"
NPERYEAR=12
export DIR=`pwd`
PROG=getsealevel
FROM="from <a href="wipefoot.cgi?http://ilikai.soest.hawaii.edu/UHSLC/jasl.html" target="_new">JASL database</a>"

. $DIR/getdata.cgi
