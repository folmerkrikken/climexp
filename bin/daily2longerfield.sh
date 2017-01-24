#!/bin/bash
declare -a ensargs
ensargs=("$@")
n=$(($# - 1))
if [ -z "$DIR" ]; then
  DIR=`pwd`
fi
PROG=`basename $0 .sh`
file=$1
c0=`echo $file | fgrep -c '%%%'`
c1=`echo $file | fgrep -c '%%'`
c2=`echo $file | fgrep -c '++'`
if [ $c1 -eq 0 -a $c2 -eq 0 ]
then
  $DIR/bin/$PROG $*
else
  i=0
  if [ $c0 = 1 ]; then
    ii=000
    imax=1000
    format=%03i
  else
    ii=00
    imax=100
    format=%02i
  fi
  while [ $i -lt $imax ]
  do
    ensfile=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\%\%:$ii:"`
    if [ -s $ensfile -o -s data/$ensfile ]
    then
      ensargs=(`echo $* | sed -e "s:\+\+\+:$ii:g" -e "s:\+\+:$ii:g" -e "s:\%\%\%:$ii:g" -e "s:\%\%:$ii:g"`)
      ###echo "$DIR/bin/$PROG ${ensargs[*]}"
      $DIR/bin/$PROG ${ensargs[*]}
      echo "generated ${ensargs[$n]}<p>"
    fi
    i=$(($i + 1))
    ii=`printf $format $i`
  done
fi
