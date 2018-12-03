#!/bin/bash
. ./nosearchenginewithheader.cgi

PATH=$PATH:/usr/local/free/bin

. ./getargs.cgi
FORM_file=`echo $FORM_file | sed -e 's/_W _/_W+_/' -e 's/_G _/_G+_/'`
file=data/`basename $FORM_file .dat`.dat
echo "Content-disposition: attachment; filename="`basename $file .dat`.txt
echo "Content-type: text/plain"
echo
cat $file | unix2dos
