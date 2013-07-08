#!/bin/sh
. ./init.cgi

. ./getargs.cgi
WHERE="$FORM_WHERE"
STATION="$FORM_STATION"
WMO="$FORM_WMO"

# set up the information that getstations.cgi expects

if [ -z "$STATION" ]; then
    FORM_EMAIL=$EMAIL
    FORM_email=$EMAIL
    FORM_climate="sea-level"
    prog=getsealevelave
    listname=CUData/${WHERE}.txt
    format=new
    . ./getstations.cgi
else
    TYPE=l
    NAME="Sealevel"
    NPERYEAR=12
    export DIR=`pwd`
    FROM="from <a href=\"http://sealevel.colorado.edu/results.php\" target="_new">University of Colorado at Boulder</a>"
    LASTMODIFIED=`stat CUData/sl_global.dat | fgrep Modify | cut -b 8-27`
    LASTMODIFIED=`date -R -d "$LASTMODIFIED"`
    PROG=getsealevelave
    export STATION
    export WMO
    . ./getdata.cgi
fi
