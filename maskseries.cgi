#!/bin/sh
#
# select part of a time series based on the values of another one

export DIR=`pwd`
. ./getargs.cgi

WMO="$FORM_WMO"
TYPE="$FORM_TYPE"
NAME="$FORM_CLIMATE"
NPERYEAR="$FORM_NPERYEAR"
data=data/$FORM_TYPE$WMO.dat

. ./getuserindex.cgi
. ./getopts.cgi

if [ -z "$FORM_lt" ]; then
  if [ -z "$FORM_gt" ]; then
    cat <<EOF
Content-type: text/html

<html><head><title>error</title></head><body bgcolor="#ffffff">Error: fill out least one boundary</body></html>
EOF
    exit
  else
    STATION="${FORM_STATION}/${index}_gt_${FORM_gt}"
    WMO="$FORM_WMO:`basename $datfile .dat|cut -b 2-`gt${FORM_gt}"
  fi
else
  if [ -z "$FORM_gt" ]; then
    STATION="${FORM_STATION}/${index}_lt_${FORM_lt}"
    WMO="$FORM_WMO:`basename $datfile .dat|cut -b 2-`lt${FORM_lt}"
  else
    STATION="${FORM_STATION}/${FORM_gt}_lt_${index}_lt_${FORM_lt}"
    WMO="$FORM_WMO:`basename $datfile .dat|cut -b 2-`${FORM_gt}lt${index}lt${FORM_lt}"    
  fi
fi
PROG="maskseries $data $datfile $corrargs "

. $DIR/getdata.cgi
