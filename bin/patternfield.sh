#!/bin/sh
if [ -z "$DIR" ]; then
  DIR=`pwd`
fi
c1=`echo $file | fgrep -c '%%'`
c2=`echo $file | fgrep -c '++'`
if [ $c1 -eq 0 -a $c2 -eq 0 ]
then
  $DIR/bin/patternfield $*
else
  i=0
  ii=00
  iii=000
  ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%\%:$iii:" -e "s:\%\%:$ii:"`
  echo "ensemble member " 1>&2
  while [ -f $ensfile -o $i = 0 ]
  do
  	###echo "searching for $ensfile<br>" 1>&2
    if [ -f $ensfile ]
    then
      ensargs=`echo $* | sed -e "s:$file:$ensfile:"`
      ensout=`echo data/$TYPE$WMO.dat | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
      ###echo "./bin/patternfield $ensargs &gt; $ensout<br>" 1>&2
      ./bin/patternfield $ensargs > $ensout
      echo "# $ensout"
    fi
    i=$(($i + 1))
    ii=`printf %02i $i`
    iii=`printf %03i $i`
    ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%\%:$iii:" -e "s:\%\%:$ii:"`
    echo "$i" 1>&2
  done
fi
