#!/bin/sh

. ./getargs.cgi

lwrite=false
if [ "$lwrite" = true ]; then
    echo 'Content-Type: text/plain'
    echo
    printenv
    exit
fi

scale="$FORM_scale"
latlon="${FORM_latlon#\?}"
QUERY_STRING=$EMAIL
lon=`echo $latlon | cut -f 1 -d ','`
lat=`echo $latlon | cut -f 2 -d ','`
let lon=lon-200
let lon=lon*180
let lon=lon/200
let lat=100-lat
let lat=lat*90
let lat=lat/100

DIR=`pwd`
case $scale in
daily) prog=selectdailyseries.cgi;;
*)     prog=selectstation.cgi;;
esac
. ./$prog
