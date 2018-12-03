#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
forbidden='!`;/'
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
if [ ! -f $inffile ]; then
    . ./myvinkhead.cgi "Error"
    echo "Could not locate the index $FORM_STATION (" `basename $inffile .inf` ")."
    . ./myvinkfoot.cgi
else
    rm $inffile
    . ./myvinkhead.cgi "OK"
    echo "The index $FORM_STATION (" `basename $inffile .inf` ") has been removed from the list of user-defined indices. (Do not reload the previous page, that would add it back to the list.)"
    . ./myvinkfoot.cgi
fi
