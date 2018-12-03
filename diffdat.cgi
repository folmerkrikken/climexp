#!/bin/bash
#
# Take time derivative of a time series
. ./init.cgi
export DIR=`pwd`
. ./getargs.cgi
NPERYEAR=$FORM_NPERYEAR
if [ $EMAIL != someone@somewhere ]; then
    cat > ./prefs/$EMAIL.diffdat <<EOF
FORM_ndiff=$FORM_ndiff;
EOF
fi

export WMO="d${FORM_wmo}_dt_$FORM_ndiff"
STATION="trend $FORM_station"
EMAIL=$FORM_EMAIL
export TYPE=$FORM_type
NAME="$FORM_name"
export file=data/$TYPE$FORM_wmo.dat
PROG="diffdat.sh $DIR/data/$TYPE$FORM_wmo.dat ${FORM_ndiff:-2}"

. ./getdata.cgi
