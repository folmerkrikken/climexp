#!/bin/sh

. ./getargs.cgi
export DIR=`pwd`

FORM_climate="$FORM_TYPE"
FORM_email="$EMAIL" #...
FORM_EMAIL="$EMAIL" #...
prog="$FORM_WMO"
listname=data/`basename "$FORM_NAME"`
listname=`echo "$listname" | tr -d '\\'` # I get spurious backslashes...
extraargs="${FORM_nperyearnew}_${FORM_oper}"
if [ "$FORM_lgt" = "lt" -o "$FORM_lgt" = "gt" ]; then
    extraargs="${extraargs}_${FORM_lgt}_${FORM_cut}${FORM_typecut}"
fi
if [ -n "$FORM_sum" -a "$FORM_sum" != 0 -a "$FORM_sum" != 1 ]; then
    extraargs="${extraargs}_ave_${FORM_sum}"
fi
if [ -n "$FORM_minfac" ]; then
    extraargs="${extraargs}_minfac_${FORM_minfac}"
fi
if [ -n "$FORM_addoption" -a "$FORM_addoption" != add_anom ]; then
    extraargs="${extraargs}_${FORM_addoption}"
fi

NPERYEAR=$FORM_NPERYEAR
. ./save_daily2longer.cgi
NPERYEAR=$FORM_nperyearnew
format=new
. ./getstations.cgi

