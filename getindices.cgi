#!/bin/sh

export DIR=`pwd`

. ./init.cgi
. ./getargs.cgi

STATION="$FORM_STATION"
WMO="$FORM_WMO"
TYPE="$FORM_TYPE"
NPERYEAR="$FORM_NPERYEAR"
if [ -z "$WMO" -a -n "$QUERY_STRING" ]; then
    WMO=`echo "$QUERY_STRING" | sed -e 's/[^-a-zA-Z0-9_/.@]/_/g'`
    WMO=${WMO#/} # no absolute paths
    if [ `basename "$WMO"` = "$WMO" ]; then
        WMO=unknown/$WMO # only in subdirectories
    fi
fi
if [ -z "$TYPE" ]; then
    TYPE=i
fi
if [ -z "$STATION" ]; then
    file=$WMO.dat
    if [ -s $file ]; then
        eval `./bin/getunits $file`
        STATION=$VAR
    fi
fi
###echo "TYPE,WMO,STATION=$TYPE,$WMO,$STATION" >> log/log

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
c=`echo $file | egrep -c '\+\+|%%'`
if [ "$c" != 0 ]; then
  ens0=`echo $file | sed -e 's/+++/000/' -e 's/%%%/000/' -e 's/++/00/' -e 's/%%/00/'`
  ncens0=${ens0%.dat}.nc
  if [ -s "$ens0" ]; then
    i=0
    file=$ens0
    newfile=`echo $newfile | sed -e 's/+++/000/' -e 's/%%%/000/' -e 's/++/00/' -e 's/%%/00/'`
    ext=.dat
  elif [ -s "$ncens0" ]; then
    i=0
    file=$ncens0
    newfile=`echo $newfile | sed -e 's/+++/000/' -e 's/%%%/000/' -e 's/++/00/' -e 's/%%/00/'`
    ext=.nc
  else
    ens1=`echo $file | sed -e 's/+++/001/' -e 's/%%%/001/' -e 's/++/01/' -e 's/%%/01/'`
    ncens1=${ens1%.dat}.nc
    if [ -s "$ens1" ]; then
      i=1
      file=$ens1
      newfile=`echo $newfile | sed -e 's/+++/001/' -e 's/%%%/001/' -e 's/++/01/' -e 's/%%/01/'`
      ext=.dat
    elif [ -s "$ncens1" ]; then
      i=1
      file=$ncens1
      newfile=`echo $newfile | sed -e 's/+++/001/' -e 's/%%%/001/' -e 's/++/01/' -e 's/%%/01/'`
      ext=.nc
    fi
  fi
fi
if [ -s $file -a "$c" = 0 ]; then
  if [ `uname` = Linux ]; then
    LASTMODIFIED=`stat $file | fgrep Modify | cut -b 8-27`
    LASTMODIFIED=`date -R -d "$LASTMODIFIED"`    
  fi
fi
# make sure that the whole ensemble is in ./data, otherwise copy it again.
doit=false
if [ -n "$i" ]; then
    ensfile=$file
    while [ -s $ensfile ]; do
        i=$((i+1))
        ii=`printf %02i $i`
        iii=`printf %03i $i`
        ensfile=`echo $WMO$ext | sed -e "s/+++/$iii/" -e "s/%%%/$iii/" -e "s/++/$ii/" -e "s/%%/$ii/"`
        newensfile=`echo data/$TYPE$wmo$ext | sed -e "s/+++/$iii/" -e "s/%%%/$iii/" -e "s/++/$ii/" -e "s/%%/$ii/"`
        if [ ! -s $newensfile ]; then
            doit=true
        elif [ $newensfile -ot $ensfile ]; then
            doit=true
        fi
    done
fi
if [ $doit = true ]; then
  PROG=getindices
elif [ $newfile = $file -o $newfile -nt $file -a -s $newfile ]; then
  PROG=
else
  PROG=getindices
fi
###echo "newfile=$newfile" >> log/debug
###echo "PROG=$PROG" >> log/debug
export TYPE
. $DIR/getdata.cgi
