#!/bin/sh
. ./nosearchenginewithheader.cgi
echo "Content-Type: data"
echo "Content-Encoding: x-gzip"
echo

. ./getargs.cgi
ctldir=`dirname $FORM_file`
datafile=`head -1 $FORM_file | sed -e 's/DSET //' -e 's/dset //' -e "s:\^:$ctldir/:" -e 's/ *$//'`
if [ -f $datafile.gz ]; then
  cat $datafile.gz
else
  gzip -c $datafile
fi
