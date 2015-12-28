#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=w
NAME="snow water eq"
NPERYEAR=12
export DIR=`pwd`
PROG=getsnow
FROM="from <a href="wipefoot.cgi?http://www.wcc.nrcs.usda.gov/snowcourse/" target="_new">NRCS database</a>"

. $DIR/getdata.cgi
