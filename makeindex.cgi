#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
TYPE="$FORM_type"
WMO="$FORM_wmo"
NPERYEAR="$FORM_NPERYEAR"

if [ $EMAIL = "someone@somewhere" ]; then
  . ./myvinkhead.cgi "Error"
  echo "Anonymous users cannot use user-defined series, please register first \
    <a href=\"/\">here</a>."
  . ./myvinkfoot.cgi
  exit
fi

inffile=$DIR/data/$TYPE$WMO.$NPERYEAR.$EMAIL.inf
echo data/$TYPE$WMO.dat > $inffile
echo "$FORM_newname" | tr ' ' '_' >> $inffile
echo "$WMO" >> $inffile

. ./myvinkhead.cgi "OK"
echo "The index ${FORM_newname} should show up under your user-defined indices for the next 3 days."
. ./myvinkfoot.cgi
