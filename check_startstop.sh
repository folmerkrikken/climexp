#!/bin/sh
for file in data/regionver*.startstop
do
  yr1=`head -1 $file`
  yr2=`tail -1 $file`
  if [ $yr1 -gt $yr2 ]
  then
    echo "error in $file"
    cat $file
  fi
done
