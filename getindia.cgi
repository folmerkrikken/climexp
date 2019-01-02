#!/bin/bash
. ./init.cgi
. ./getargs.cgi
WHERE="$FORM_where"
TYPE="$FORM_type"

# set up the information that getstations.cgi expects

FORM_EMAIL=$EMAIL
FORM_email=$EMAIL
if [ "$TYPE" = 'p' ]; then
  FORM_climate="Indian_Precip"
  prog=getindiaprcp
elif [ "$TYPE" = 'x' ]; then
  FORM_climate="Indian_Tmax"
  prog=getindiatmax
elif [ "$TYPE" = 'n' ]; then
  FORM_climate="Indian_Tmin"
  prog=getindiatmin
else
  echo
  echo "UNKNOWN TYPE"
  exit
fi
listname=IITMData/${TYPE}${WHERE}.txt
format=new

. ./getstations.cgi
