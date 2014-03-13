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
    getprcp) TYPE=p; NAME="GHCN v2 precipitation";;
    getprcpall) TYPE=pa; NAME="GHCN v2 precipitation (all)";;
    getslp) TYPE=s; NAME="GHCN v2 sealevel pressure";;
    gettemp) TYPE=t; NAME="GHCN v3 mean temperature";;
    gettempall) TYPE=ta; NAME="GHCN v3 mean temperature (all)";;
    getmin) TYPE=m; NAME="GHCN v3 minimum temperature";;
    getminall) TYPE=ma; NAME="GHCN v3 minimum temperature (all)";;
    getmax) TYPE=x; NAME="GHCN v3 maximum temperature";;
    getmaxall) TYPE=xa; NAME="GHCN v3 maximum temperature (all)";;
    *) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "Unknown GHCN data type" ""; . ./myvinkfoot.cgi; exit;;
esac

export DIR=`pwd`
FROM="from <a href="wipefeet.cgi?https://www.ncdc.noaa.gov/ghcnm/" target="_new">GHCN-M v2/v3 (adjusted) database</a>"

. $DIR/getdata.cgi
