#!/bin/sh
echo "Content-Type: text/plain"
echo
echo "Sleep 3 times 58 seconds"
i=0
while [ $i -lt 3 ]
do
  i=$(($i + 1))
  echo "$i: " `date`
  sleep 58
done
echo "Sleep 3 times 62 seconds"
i=0
while [ $i -lt 3 ]
do
  i=$(($i + 1))
  echo "$i: " `date`
  sleep 62
done
