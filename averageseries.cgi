#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
email="$EMAIL"
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
location="$FORM_location"

# check email address
EMAIL=$email
. ./checkemail.cgi

# real work
WMO="$location"
STATION="averaged stations"
EMAIL="$email"
NAME="$climate"
# common options
plotlist=$DIR/data/plotcorr$$.txt
corrargs="$FORM_listname $plotlist $prog average"
PROG="$DIR/bin/stationlist $corrargs"

. $DIR/getdata.cgi

