#!/bin/sh
[ -z "$EOFID" ] && EOFID=$2
if [ -z "$EOFID" ]
then
  echo "$0: cannot find EOFID"
  echo "$0: cannot find EOFID" 1>&2
  exit -1
fi
i=0
j=0
###echo "This is stillcomputing.cgi with arg $1 and EOFID $EOFID" 1>&2
###ps $EOFID | wc -l 1>&2
while [ `ps $EOFID | wc -l` -gt 1 ]
do
  if [ $j -gt 30 ]; then
    echo "Still computing, $i/$1<p>" 1>&2
    i=$(($i+1))
    j=0
  fi
  sleep 1
  j=$(($j+1))
###  echo $i $j 1>&2
  if [ $i -gt 1200 ]
  then
    cat <<EOF 
More than 5 hours elapsed, killing the EOF job.
Please try again with fewer grid points (average 
over a few lon or lat grid points)"
EOF
    kill -9 $EOFID
    . ./myvinkfoot.cgi
    exit -1
  fi
done
