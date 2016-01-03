#!/bin/sh

. ./getargs.cgi

###echo "Content-Type: text/plain"; echo; set | fgrep FORM_ ; exit
WMO="$FORM_WMO"
STATION="$FORM_STATION"
extraargs=`echo "$FORM_extraargs" | tr '_;\`&|' ' ?'`
PROG=`basename $SCRIPT_FILENAME .cgi`

gts=""
case $PROG in
    gdcnprcp) NAME="precipitation";char=p;;
    gdcnprcpall) NAME="all_precipitation";char=p;gts=gts;;
    gdcnsnow) NAME="snow fall";char=f;;
    gdcnsnwd) NAME="snow depth";char=d;;
    gdcntmax) NAME="maximum temperature";char=x;;
    gdcntmin) NAME="minimum temperature";char=n;;
    gdcntave) NAME="average temperature";char=v;;
    *) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "Unknown GHCN-D data type" ""; . ./myvinkfoot.cgi; exit;;
esac
TYPE=${char}gdcn$gts

if [ -z "$extraargs" ]; then
  NPERYEAR=366
else
  NPERYEAR=`echo $extraargs | cut -f 1 -d ' '`
  NAME=`echo "$extraargs" | cut -f 2- -d ' '`" $NAME"
  PROG="pipe.sh $PROG $extraargs"
fi
export DIR=`pwd`
file=GDCNData/ghcnd/$WMO.dly.gz # to check whether the output is up-to-date
FROM="from <a href=\"ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/\" target=\"_new\">GHCN-D v2 database</a>"
makenetcdf=true

. ./getdata.cgi
