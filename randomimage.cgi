#!/bin/sh
echo 'Content-Type: text/plain'
echo
echo

if [ `uname` = Darwin ]; then
  word=5
else
  word=5
fi
tmpfile=/tmp/start$$.txt
list=`ls -t data/ | fgrep .png | egrep '(^[ghR])|(.*corr.*)' | egrep -v 'kml|tmp' `
for file in $list
do
  if [ -s data/$file ]
  then
    file data/$file
    size=`file data/$file | cut -d ' ' -f $word`
    echo "size=$size"
    if [ $size -le 904 ]
    then
      cp data/$file data/randomimage.png
      exit 0
    fi
  fi
done
