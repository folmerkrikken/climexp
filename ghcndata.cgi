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

WMO="$FORM_WMO"
STATION="$FORM_STATION"
PROG=`basename $SCRIPT_FILENAME .cgi`
NPERYEAR=12

case $PROG in
    getprcp) TYPE=p; NAME="GHCN precipitation";;
    getprcpall) TYPE=pa; NAME="GHCN precipitation (all)";;
    getslp) TYPE=s; NAME="GHCN sealevel pressure";;
    gettemp) TYPE=t; NAME="GHCN mean temperature";;
    gettempall) TYPE=ta; NAME="GHCN mean temperature (all)";;
    getmin) TYPE=m; NAME="GHCN minimum temperature";;
    getminall) TYPE=ma; NAME="GHCN minimum temperature (all)";;
    getmax) TYPE=x; NAME="GHCN maximum temperature";;
    getmaxall) TYPE=xa; NAME="GHCN maximum temperature (all)";;
    *) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "Unknown GHCN data type" ""; . ./myvinkfoot.cgi; exit;;
esac

export DIR=`pwd`
FROM="from <a href="wipefeet.cgi?http://www.ncdc.noaa.gov/oa/climate/ghcn-monthly/" target="_new">GHCN v2 (adjusted) database</a>"

. $DIR/getdata.cgi
