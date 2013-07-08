#!/bin/sh
sleep 30 &
c=1
while [ $c -gt 0 ]
do
  sleep 5
  c=`ps axuw | fgrep "sleep 30" | fgrep -v grep | wc -l`
  echo "c=$c"
done
