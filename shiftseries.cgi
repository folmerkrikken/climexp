#!/bin/bash
#
# Shift a time series in time
. ./init.cgi
export DIR=`pwd`
. ./getargs.cgi
NPERYEAR=$FORM_NPERYEAR
. ./nperyear2timescale.cgi
if [ -z "$FORM_shift" ]; then
    echo
    echo
    . ./myvinkhead.cgi "Time shifted series" "Error"
    echo "Please specify number of ${month}s to shift over."
    . ./myvinkfoot.cgi
    exit
fi
if [ $EMAIL != someone@somewhere ]; then
    cat > ./prefs/$EMAIL.shift <<EOF
FORM_shift=$FORM_shift;
EOF
fi

export WMO="${FORM_wmo}_shift$FORM_shift"
STATION="${FORM_station} shifted by $FORM_shift ${month}s"
export TYPE=$FORM_type
NAME="$FORM_NAME"
export file=data/$TYPE$FORM_wmo.dat
PROG="timeshift.sh ./data/$TYPE$FORM_wmo.dat $FORM_shift"

. ./getdata.cgi
