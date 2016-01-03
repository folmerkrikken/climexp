#!/bin/sh

. ./getargs.cgi

WMO="$FORM_WMO"
STATION="$FORM_STATION"
extraargs="$FORM_extraargs"
PROG=`basename $SCRIPT_FILENAME .cgi`
if [ "${PROG#b}" != "$PROG" ]; then
    blend=b
else
    blend=""
fi

case $PROG in
    becaclou|ecaclou) NAME="cloud cover";char=c;;
    becaprcp|ecaprcp) NAME="precipitation";char=p;;
    becapres|ecapres) NAME="pressure";char=s;;
    becasnow|ecasnow) NAME="snow depth";char=d;;
    becatemp|ecatemp) NAME="mean temperature";char=t;;
    becatmax|ecatmax) NAME="maximum temperature";char=x;;
    becatmin|ecatmin) NAME="minimum temperature";char=n;;
    *) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "Unknown ECA data type" ""; . ./myvinkfoot.cgi; exit;;
esac
TYPE=${blend}${char}eca

if [ -z "$extraargs" ]; then
  NPERYEAR=366
else
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d ' '`
  NAME="`echo "$extraargs" | cut -f 2- -d ' '` $NAME"
  PROG="pipe.sh $PROG \"$extraargs\""
fi
export DIR=`pwd`
FROM="from <a href="http://www.ecad.eu/" target="_new">ECA&amp;D v1.1 database</a>"
makenetcdf=true

. $DIR/getdata.cgi
