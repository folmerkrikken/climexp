#!/bin/bash
echo 'Content-Type: text/plain'
echo
echo

if [ `uname` = Darwin ]; then
  word=5
else
  word=5
fi
tmpfile=/tmp/start$$.txt
list=`ls -t data/ atlas/maps/*/rcp*/| fgrep .png | egrep '(^[dghrRw])|(.*corr.*)' | egrep -v 'kml|tmp' `
for file in $list
do
  if [ -s data/$file ]
  then
    file=data/$file
  else
    file=`find atlas/maps -name $file`
  fi
  if [ -s "$file"  -a "$file" != "data/randomimage.png" ]
  then
    file $file
    size=`file $file | cut -d ' ' -f $word`
    echo "size=$size"
    if [ $size -le 904 ]
    then
      cp $file data/randomimage.png
      exit 0
    fi
  fi
done
