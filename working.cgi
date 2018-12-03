#!/bin/bash
echo "Content-type: text/plain"
echo

c=`(ls /data/storage/climexp /data/storage/climexp/bin | wc -l) 2>&1`
if [ $c -gt 500 ]; then
  echo "OK"
else
  echo "something is wrong:
$c"
fi
