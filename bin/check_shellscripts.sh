#!/bin/sh
for file in *
do
    c=`file $file | fgrep -c shell`
    if [ $c = 1 -a ! -L $file ]; then
	cc=`fgrep -c '++' $file`
	if [ $cc -gt 0 ]; then
	    echo $file
	    fgrep '++' $file
	fi
    fi
done
