#!/bin/bash
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
corrargs=$FORM_extend_method

if [ $EMAIL != someone@somewhere ]; then
    cat > prefs/$EMAIL.patchseries <<EOF
FORM_extend_method=$FORM_extend_method;
EOF
fi

STATION="${FORM_STATION}_with_${index}"
WMO=${FORM_WMO}_with_`basename ${index}`
PROG="patchseries $data $datfile $corrargs "

. ./getdata.cgi
