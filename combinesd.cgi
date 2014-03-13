#!/bin/sh
export PATH=$PATH:/sw/bin # for nco, ncdump/ncgen on Mac
# script to combine estimates of the sd of N-yr means to get the estimate for unequal intervals
sd1file="$1"
sd2file="$2"
sdfile="$3"

if [ -z "$sdfile" ]; then
    echo "usage: $0 sd1file sd2file sdfile"
    exit -1
fi

# make a tmp file with the variable from sd1file and sd2file
tmp1file=/tmp/combinefile1_$$.nc
tmp2file=/tmp/combinefile2_$$.nc
cp $sd1file $tmp1file
ncrename -v sd,sd1 $tmp1file
cdo merge $tmp1file $sd2file $tmp2file
ncrename -v sd,sd2 $tmp2file
echo "cdo expr,'sd=sqrt(sd1^2+sd2^2)' $tmp2file $sdfile"
cdo expr,'sd=sqrt(sd1^2+sd2^2)' $tmp2file $sdfile

if [ ! -s $sdfile ]; then
    echo "$0: error: something went wrong"
    exit -1
fi

rm $tmp1file $tmp2file
