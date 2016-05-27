#!/bin/sh
if [ -z "$nmax" ]; then
    nmax=100
fi
i=0
iii=000
while [ $i -lt $nmax ]; do
    outfile=`echo data/$TYPE$WMO.dat | sed -e "s/%%%/$iii/" -e "s/\+\+\+/$iii/"`
    echo $iii > /dev/stderr
    echo "# $outfile"
    if [ ! -s $outfile ]; then
        ./bin/ar1 $file > $outfile.tmp$$
        mv $outfile.tmp$$ $outfile
    fi
    i=$((i+1))
    iii=`printf %03i $i`
done