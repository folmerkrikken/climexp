#!/bin/sh
c1=`echo "$1" | fgrep -c '%%'`
c2=`echo "$2" | fgrep -c '%%'`
if [ $c1 = 0 -a $c2 = 0 ]; then
  echo bin/fieldcorrelate $* /tmp/tmp$$.dat > /tmp/fieldcorr$$.log
  bin/fieldcorrelate $* /tmp/tmp$$.dat >> /tmp/fieldcorr$$.log
else
  iens=${FORM_nens1:-0}
  touch /tmp/tmp$$.dat
  while [ $iens -le ${FORM_nens2:-99} ]
  do
    if [ $iens -lt 10 ]; then
      args=`echo $* | sed -e "s/%%/0$iens/"`
      file1=`echo $1 | sed -e "s/%%/0$iens/"`
      file2=`echo $2 | sed -e "s/%%/0$iens/"`
      series=`echo data/$TYPE$WMO.dat | sed -e "s/\+\+/0$iens/"`
    else
      args=`echo $* | sed -e "s/%%/$iens/"`
      file1=`echo $1 | sed -e "s/%%/$iens/"`
      file2=`echo $1 | sed -e "s/%%/$iens/"`
      series=`echo data/$TYPE$WMO.dat | sed -e "s/\+\+/$iens/"`
    fi
    if [ -f $file1 -a -f $file2 ]; then
      echo bin/fieldcorrelate $args $series > /tmp/fieldcorr$$.log
      bin/fieldcorrelate $args $series >> /tmp/fieldcorr$$.log
      echo $series >> /tmp/tmp$$.dat
    fi
    iens=$(($iens + 1))
  done  
fi
cat /tmp/tmp$$.dat
rm /tmp/tmp$$.dat
