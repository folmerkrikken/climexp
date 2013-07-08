#!/bin/sh
echo "Content-type: text/plain"
echo

c=`(ls /data/climexp/climexp /data/climexp/climexp/bin | wc -l) 2>&1`
if [ $c -gt 500 ]; then
  echo "OK"
else
  echo "something is wrong:
$c"
fi
