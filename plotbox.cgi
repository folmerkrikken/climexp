#!/bin/sh

echo "Content-Type: text/html"
echo
echo

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

# check email address
. ./checkemail.cgi

. ./myvinkhead.cgi "Map of stations" "$FORM_climate" "noindex,nofollow"

plotlist=data/plotlist$$.txt
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
###echo ./bin/stationlist $FORM_listname $plotlist $FORM_prog plot
./bin/stationlist $FORM_listname $plotlist $FORM_prog plot

title="$FORM_climate stations"
oper=plot
. $DIR/plotparams.cgi
