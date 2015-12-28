#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=l
NAME="Sealevel"
NPERYEAR=12
export DIR=`pwd`
PROG=getsealev
FROM="from <a href="wipefoot.cgi?http://www.pol.ac.uk/psmsl/datainfo/" target="_new">PSMSL database</a>"

. $DIR/getdata.cgi
