#!/bin/sh
. ./init.cgi
echo "Content-Type: text/plain"
echo

. ./getargs.cgi
infile="$FORM_file"
if [ "${infile%.ctl}" != "$infile" ]; then
  filetype=grads
  ctldir=`dirname $infile`
  datfile=`head -1 $infile | sed -e 's/DSET //' -e 's/dset //' -e "s:\^:$ctldir/:" -e 's/ *$//'`
  if [ ! -s $datfile ]; then
      gunzip -c $datfile.gz > $datfile
  fi
  bin/netcdf2ascii $infile
else # netcdf
  bin/netcdf2ascii $infile
fi
