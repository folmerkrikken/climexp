#!/bin/sh
. ./init.cgi
echo "Content-Type: text/plain"
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"

plotlist=data/plotlist$$.txt
./bin/stationlist $listname $plotlist $prog list

cat $plotlist
rm $plotlist
