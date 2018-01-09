#!/bin/sh
#
# select a period from a data file

export DIR=`pwd`
. ./getargs.cgi


WMO="${FORM_wmo}_F"
STATION="$FORM_station"
TYPE=$FORM_TYPE
NAME=$FORM_NAME
NPERYEAR=$FORM_NPERYEAR
eval `./bin/getunits $DIR/data/$TYPE$FORM_wmo.dat`
if [ "$NEWUNITS" = Celsius ]; then
    if [ "$FORM_anom" = true ]; then
        factor="1.8"
    else
        if [ "$UNITS" = "K" -o "$UNITS" = "Kelvin" ]; then
            factor="1.8:-459.67"
        else
            factor="1.8:32"
        fi
    fi
    NEWUNITS=Fahrenheit
else
    factor=1
    NEWUNITS=$UNITS
fi
PROG="scaleseries $factor $DIR/data/$TYPE$FORM_wmo.dat"
adjust_units_to_fahrenheit=true

. $DIR/getdata.cgi
