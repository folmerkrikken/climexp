#!/bin/ksh

prog=`basename $1`
shift
n=$#
wmo=`echo $* | cut -f $n -d ' '`
extraargs=`echo $* | cut -f 1-$(($n-1)) -d ' '`

tmpfile=/tmp/pipe.$$
###echo "pipe:sh: bin/$prog $wmo > $tmpfile" >> log/log
bin/$prog $wmo > $tmpfile
###echo "pipe:sh: bin/daily2longer $tmpfile $extraargs" >> log/log
bin/daily2longer $tmpfile $extraargs
rm $tmpfile
