#!/bin/bash
#
# select a period from a data file

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

WMO="${FORM_wmo}_${FORM_yr1}:${FORM_yr2}"
STATION="$FORM_station"
TYPE=$FORM_type
NAME=$FORM_name
file=`basename $FORM_file`
PROG="selectyear.sh ${FORM_yr1} ${FORM_yr2} $DIR/data/$file"
export WMO
export file
export TYPE

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.selectyears
  cat > $def << EOF
FORM_yr1=$FORM_yr1;
FORM_yr2=$FORM_yr2;
EOF
fi

. ./getdata.cgi
