#!/bin/sh
# make a time series with a longer time scale than the original

export DIR=`pwd`
. ./getargs.cgi
STATION=$FORM_STATION
export WMO=$FORM_WMO
export TYPE=$FORM_TYPE
export file=data/$TYPE$WMO.dat
if [ -z "$FORM_oper" ]; then
  FORM_oper="mean"
fi
[ -z "$NPERYEAR" ] && NPERYEAR=$FORM_NPERYEAR
. ./nperyear2timescale.cgi
. ./save_daily2longer.cgi

if [ "$FORM_oper" = sd ]; then
	if [ -z "$FORM_nperyearnew" -o "${FORM_nperyearnew#-}" -ge "${FORM_NPERYEAR#-}" ]; then
		echo "Content-type: text/html"
		echo 
		. ./myvinkhead.cgi "Error" "Operation not defined"
		echo "The standard deviation can only be determined for a lower-frequency time series than the original one."
		echo "Now you are requesting $FORM_nperyearnew steps per year but the original one has $NPERYEAR."
		. ./myvinkfoot.cgi
		exit
	fi
fi
if [ "$FORM_NPERYEAR" = 366 -o "$FORM_NPERYEAR" = 365 -o "$FORM_NPERYEAR" = 360 ]; then
  NAME="$FORM_oper daily $FORM_NAME"
elif [ "$FORM_NPERYEAR" = 12 ]; then
  NAME="$FORM_oper monthly $FORM_NAME"
else
  NAME="$FORM_oper $FORM_NAME"
fi
NPERYEAR="$FORM_nperyearnew"

corrargs="$DIR/data/$TYPE$WMO.dat $NPERYEAR $FORM_oper"
WMO=${WMO}_$FORM_oper$NPERYEAR
if [ "$FORM_lgt" = "lt" -o "$FORM_lgt" = "gt" ]; then
  if [ -z "$FORM_cut" -a "$FORM_typecut" != "n" ]; then
    FORM_cut=0
  fi
  corrargs="$corrargs $FORM_lgt $FORM_cut$FORM_typecut"
  WMO=${WMO}$FORM_lgt$FORM_cut$FORM_typecut
  NAME="$NAME $FORM_lgt$FORM_cut$FORM_typecut"
fi
if [ -n "$FORM_minfac" ]; then
    corrargs="$corrargs minfac $FORM_minfac"
fi
if [ -n "FORM_sum" -a "$FORM_sum" != 0 -a "$FORM_sum" != 1 ]; then
    corrargs="$corrargs ave $FORM_sum"
    WMO=${WMO}_${FORM_sum}v
    NAME="${FORM_sum}-$month mean"
fi

PROG="daily2longer.sh $corrargs"

if [ $NPERYEAR = -1 ]; then
    NPERYEAR=1
fi

. $DIR/getdata.cgi

