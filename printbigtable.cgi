#!/bin/sh
#
# print an ensemble of time series
. ./init.cgi
. ./getargs.cgi

# no ensemble member selection yet

echo "Content-type: text/plain"
echo
if [ -z "$FORM_listname" ]; then
    ./bin/printbigtable data/$FORM_TYPE$FORM_wmo.dat
else
    prog=$FORM_prog
    if [ -n "$FORM_extraargs" ]; then
        prog=${prog}_$FORM_extraargs
    fi
    ./bin/printbigtable file $FORM_listname $prog
fi
