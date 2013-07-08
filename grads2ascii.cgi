#!/bin/sh
. ./init.cgi
echo "Content-Type: text/plain"
echo

. ./getargs.cgi
ctlfile="$FORM_file"
if [ "${ctlfile%.ctl}" != "$ctlfile" ]; then
  filetype=grads
  ctldir=`dirname $ctlfile`
  datfile=`head -1 $ctlfile | sed -e 's/DSET //' -e 's/dset //' -e "s:\^:$ctldir/:" -e 's/ *$//'`
  if [ ! -s $datfile ]; then
      gunzip -c $datfile.gz > $datfile
  fi
  bin/grads2ascii $ctlfile $tmpfile
else # netcdf
  bin/grads2ascii $ctlfile $tmpfile
fi
