#!/bin/sh
for file in *.cgi
do
    if [ -f $file -a ! -L $file ]; then
	c=`fgrep -c getargs.sh $file`
	if [ $c -gt 0 ]; then
	    mv $file $file.old
	    sed -e 's/getargs.sh/getargs.cgi/' $file.old > $file
	fi
    fi
done
