#!/bin/sh

. ./getargs.cgi
# redirect old URL for search engines
if [ -z "$EMAIL" -a -n "$QUERY_STRING" ]; then
	email=`echo "$QUERY_STRING" | tr -d '<>&$;' | cut -f 1 -d '+'`
	[ -z "$email" ] && email=someone@somewhere
	wmo=`echo "$QUERY_STRING" | tr -d '<>&$;' | cut -f 2 -d '+'`
	station=`echo "$QUERY_STRING" | tr -d '<>&$;' | cut -f 3 -d '+'`
	cat <<EOF
Status: 301 Moved Permanently
Location: http://climexp.knmi.nl/${SCRIPT_NAME}?id=${email}&WMO=${wmo}&STATION=${station}
Content-Type: text/html

<html><head>
</head><body>
This page has moved to <a href="${SCRIPT_NAME}?id=${email}&WMO=${wmo}&STATION=${station}">a new URL</a>
</body></html>
EOF
	exit
fi

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
