#!/bin/bash
# check whether $file really is a netcdf file

. ./init.cgi

EMAIL=$FORM_email
ncdump -h "$file" > /dev/null 2>&1
if [ $? != 0 ]; then
    rm $file
    [ -n "$FORM_field" -a -f "$FORM_field" ] && rm $FORM_field
    echo 'Content-Type: text/html'
    echo
    echo
    . ./myvinkhead.cgi "Error" "" "nofollow,index"
    echo "This does not appear to be a valid netcdf file."
    if [ $EMAIL = oldenbor@knmi.nl ]; then
	    echo "<pre>"
	    ncdump -h $file
	echo "</pre>"
    fi
    STATION=""
    . ./myvinkfoot.cgi

    exit -1
fi
#if [ -n "$STATION" ]; then
#    . ./getdata.cgi
#else
#    . ./select.cgi
#fi
