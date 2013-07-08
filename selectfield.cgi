#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

base_url=`dirname $SCRIPT_NAME`
. $DIR/selectuserfield.cgi > data/userfields.html
sed -e "s/EMAIL/$EMAIL/g" \
    -e "/include_select_obs_field_here/r selectfield_obs.html" \
    -e "/include_select_rea_field_here/r selectfield_rea.html" \
    -e "/include_select_co2_field_here/r selectfield_co2.html" \
    -e "/include_select_sea_field_here/r selectfield_sea.html" \
    -e "/include_select_sea_field_here/r selectfield_seaens.html" \
    -e "/include_selectfield_here/r selectfield.html" \
    -e "/include_userfields_here/r data/userfields.html" \
    $DIR/getfirstfield.html
