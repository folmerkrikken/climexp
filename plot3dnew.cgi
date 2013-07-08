#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi

CLIM=$FORM_CLIM
WMO=$FORM_WMO
TYPE=$FORM_TYPE
index=$FORM_index
corrroot=$FORM_corrroot
title=$FORM_title
stack=$$

. ./myvinkhead.cgi "Time series correlations" "$CLIM $station with $index" "noindex,nofollow"
. ./plot3dcor.cgi
. ./showplots.cgi
. ./myvinkfoot.cgi
exit 
