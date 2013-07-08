#!/bin/ksh

prog=`basename $1`
shift
wmo=`echo $* | cut -f $# -d ' '`

tmpfile=/tmp/pipe.$$
bin/$prog $wmo > $tmpfile
bin/daily2longer $tmpfile $*
rm $tmpfile
