#!/bin/sh
# make a time series using the ETCCDI/ECA&D extreme indiex routines
# These may be subtly different from the ones I have in daily2longer.

export DIR=`pwd`
. ./getargs.cgi
STATION=$FORM_STATION
export WMO=$FORM_WMO
export TYPE=$FORM_TYPE
export file=data/$TYPE$WMO.dat
case "$FORM_climdex_type" in
	tx) climdex=$FORM_climdex_tx;;
	tn) climdex=$FORM_climdex_tn;;
	tg) climdex=$FORM_climdex_tg;;
	rr) climdex=$FORM_climdex_rr;;
esac

. ./save_extremeseries.cgi

if [ -z "$climdex" -o "$climdex" = none -o "$climdex" = other ]; then
	echo "Content-type: text/html"
	echo 
	. ./myvinkhead.cgi "Error" "Extreme index not defined"
	echo "Please select an extreme index from the list"
	. ./myvinkfoot.cgi
	exit
fi

corrargs="$DIR/data/$TYPE$WMO.dat $FORM_nperyearnew $climdex"
WMO=${WMO}_${climdex}_$FORM_nperyearnew
if [ $climdex = Rnnmm -o $climdex = SDIInn -o $climdex = RnnTOT ]; then
	if [ -z "$FORM_gt" ]; then
		echo "Content-type: text/html"
		echo
		. ./myvinkhead.cgi "Error" "no threshold"
		echo "For $climdex a threshold (in mm) is required."
		. ./myvinkhead.cgi
		exit
	fi
	WMO=${WMO}_${FORM_gt}
    corrargs="$corrargs gt $FORM_gt"
fi

PROG="extremeseries.sh $corrargs"

NPERYEAR=$FORM_nperyearnew
if [ $NPERYEAR = -1 ]; then
    NPERYEAR=1
fi

. $DIR/getdata.cgi

