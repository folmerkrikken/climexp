#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi

if [ -z "FORM_pagetitle" ]; then
  . ./myvinkhead.cgi "Replot" "$FORM_title" "noindex.nofollow"
else
  . ./myvinkhead.cgi "Replot" "$FORM_pagetitle" "noindex.nofollow"
fi

file="$FORM_file"
ctldir=`dirname $file`
datfile=`head -1 $file | sed -e 's/DSET //' -e 's/dset //' -e "s:\^:$ctldir/:" -e 's/ *$//'`
if [ ! -f "$datfile" ]; then
  if [ -f "$datfile.gz" ]; then
    gzip -c -d $datfile.gz > $datfile
  fi
fi

NPERYEAR=$FORM_NPERYEAR
sumstring="$FORM_sumstring"
title="$FORM_title"
pagetitle="$FORM_pagetitle"
map="$FORM_map"
kindname="$FORM_kindname"
climfield="$FORM_climfield"
field1=$FORM_field1
kindname1=$FORM_kindname1
climfield1=$FORM_climfield1
field2=$FORM_field2
kindname2=$FORM_kindname2
climfield2=$FORM_climfield2
RANK="$FORM_RANK"
CLIM="$FORM_CLIM"
station="$FORM_station"
yrstart="$FORM_yrstart"
yrstop="$FORM_yrstop"
ENSEMBLE="$FORM_ENSEMBLE"

. ./getopts.cgi
. ./getfieldopts.cgi

called_from_replot=true
. ./grads.cgi

. ./myvinkfoot.cgi
