#!/bin/sh

export DIR=`pwd`

. ./getargs.cgi
STATION="$FORM_STATION"
WMO="$FORM_WMO"
TYPE="$FORM_TYPE"
NPERYEAR="$FORM_NPERYEAR"

case $TYPE in
t) NAME="temperature";;
x) NAME="maximum temperature";;
n) NAME="minimum temperature";;
p) NAME="precipitation";;
s) NAME="pressure";;
l) NAME="sealevel";;
r) NAME="runoff";;
c) NAME="correlation";;
*) NAME="";;
esac
wmo=`basename $WMO`
###echo "Content-Type: text/html"
###echo
###echo "WMO=$WMO<br>"
if [ "${wmo#data}" != "$wmo}" ]; then
  wmo="${wmo##i}"
fi
###echo "wmo=$wmo<br>"
file=$WMO.dat
newfile=data/$TYPE$wmo.dat
if [ ! -s "$file" ]; then
  ens0=`echo $file | sed -e 's/+++/000/' -e 's/%%%/000/' -e 's/++/00/' -e 's/%%/00/'`
  if [ -s "$ens0" ]; then
    file=$ens0
    newfile=`echo $newfile | sed -e 's/+++/000/' -e 's/%%%/000/' -e 's/++/00/' -e 's/%%/00/'`
  else
    ens1=`echo $file | sed -e 's/+++/001/' -e 's/%%%/001/' -e 's/++/01/' -e 's/%%/01/'`
    if [ -s "$ens1" ]; then
      file=$ens1
      newfile=`echo $newfile | sed -e 's/+++/001/' -e 's/%%%/001/' -e 's/++/01/' -e 's/%%/01/'`
    fi
  fi
fi
if [ -s $file ]; then
  if [ `uname` = Linux ]; then
    LASTMODIFIED=`stat $file | fgrep Modify | cut -b 8-27`
    LASTMODIFIED=`date -R -d "$LASTMODIFIED"`    
  fi
fi
if [ $newfile = $file -o $newfile -nt $file -a -s $newfile ]; then
  PROG=
else
  PROG=getindices
fi
###echo "PROG=$PROG<br>"
. $DIR/getdata.cgi
