#!/bin/sh

. ./getargs.cgi
export DIR=`pwd`

NPERYEAR=$FORM_nperyearnew
FORM_climate="$FORM_TYPE"
FORM_email="$EMAIL" #...
FORM_EMAIL="$EMAIL" #...
prog="$FORM_WMO"
listname=data/`basename "$FORM_NAME"`
extraargs="${FORM_nperyearnew}_${FORM_oper}"
if [ "$FORM_lgt" = "lt" -o "$FORM_lgt" = "gt" ]; then
  extraargs="${extraargs}_${FORM_lgt}_${FORM_cut}${FORM_typecut}"
fi

. ./save_daily2longer.cgi
format=new
. ./getstations.cgi

