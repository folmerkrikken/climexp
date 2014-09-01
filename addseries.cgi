#!/bin/sh
. ./init.cgi

export DIR=`pwd`
. ./getargs.cgi
NPERYEAR=$FORM_nperyear

j=0
while [[ $j -lt 20 ]]
do
    j=$(($j+1))
    export FORM_a$j
done
export EMAIL

echo bin/addseries $FORM_corrargs > /tmp/addseries$$.log
[ -n "$FORM_a1" ] && echo "FORM_a1 = $FORM_a1" >> /tmp/addseries$$.log
[ -n "$FORM_a2" ] && echo "FORM_a2 = $FORM_a2" >> /tmp/addseries$$.log
[ -n "$FORM_a3" ] && echo "FORM_a3 = $FORM_a3" >> /tmp/addseries$$.log
[ -n "$FORM_a4" ] && echo "FORM_a4 = $FORM_a4" >> /tmp/addseries$$.log
[ -n "$FORM_a5" ] && echo "FORM_a5 = $FORM_a5" >> /tmp/addseries$$.log
[ -n "$FORM_a6" ] && echo "FORM_a6 = $FORM_a6" >> /tmp/addseries$$.log
./bin/addseries $FORM_corrargs >> /tmp/addseries$$.log
file=`tail -1 /tmp/addseries$$.log`
file=./data/`basename $file`
WMO=`basename $file .dat | cut -b 2-`
STATION=`tail -2 /tmp/addseries$$.log | head -1`
###rm /tmp/addseries$$.log
TYPE=i
NAME="added series"

. ./getdata.cgi
