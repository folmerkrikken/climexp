#!/bin/sh
file="$1"
if [ -z "$file" ]; then
    echo "usage: $0 logfile"
    exit -1
fi
hosts=`cat $file | awk '{print $8}' | tr -d '()'`
hosts=`echo $hosts | tr ' ' '\n' | sort | uniq`

for host in $hosts
do
    echo `host $host`
    fgrep $host $file
done
