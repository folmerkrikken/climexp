#!/bin/sh

export DIR=`pwd`

. ./getargs.cgi

lwrite=false
if [ "$EMAIL" = oldenbor@knmi.nl ]; then
    lwrite=true # true
fi

. ./queryfield.cgi
FIELDNPERYEAR="$NPERYEAR"

export WMO
export file
export TYPE

WMO=`basename ${FORM_field} ".$EMAIL.info"`
WMO=`basename $WMO .ctl`
WMO=`basename $WMO .nc |tr '%' '_'`
WMO=${WMO}_hurr
station="${kindname} hurricanes"
if [ -n "$ENSEMBLE" ]; then
  WMO=${WMO}_++
  station="$station ensemble"
fi
STATION=`echo $station | tr ' ' '_'`
TYPE=i
NAME="Index"
NPERYEAR=1

if [ -n "$LSMASK" ]; then
    PROG="hurricane_vecchi.sh $file lsmask $LSMASK sea"
else
    PROG="hurricane_vecchi.sh $file"
fi

. $DIR/getdata.cgi
