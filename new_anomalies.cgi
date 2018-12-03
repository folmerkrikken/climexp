#!/bin/bash
#
# select a period over which to compute the climatology
DIR=`pwd`
. ./getargs.cgi

WMO=${FORM_wmo}
STATION=$FORM_station
station=`echo "$STATION" | tr '_' ' '`
TYPE=$FORM_type
NAME=$FORM_name
NPERYEAR=$FORM_NPERYEAR

if [ "$EMAIL" != someone@somewhere ]; then
# remember options for next plot
cat > ./prefs/$EMAIL.plot_anomalies <<EOF
FORM_climyear1=$FORM_climyear1;
FORM_climyear2=$FORM_climyear2;
EOF
fi

echo 'Content-Type: text/html'
echo
. ./myvinkhead.cgi "Yearly cycle and anomalies over ${FORM_climyear1}:${FORM_climyear2}" "$station $NAME" "index,nofollow"

. $DIR/plot_anomalies.cgi

. ./myvinkfoot.cgi
