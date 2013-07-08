#!/bin/bash
if [ -z "$EOFID" ]
then
  echo '$0: cannot find EOFID'
  echo '$0: cannot find EOFID' 1>&2
  exit -1
fi
i=0
while [ `ps $EOFID | wc -l` -gt 1 ]
do
  i=$(($i+1))
  sleep 1
  echo "Still computing, $i/$1<p>"
done
