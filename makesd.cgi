#!/bin/sh
export PATH=$PATH:/sw/bin # for nco, ncdump/ncgen on Mac
# script to compute estimates of the sd of N-yr means based on Jan's Atlas script in NCL
length_of_period="$1"
orgvar="$2"
rel="$3"
if [ -z "$length_of_period" -o -z "$orgvar" -o -z "$rel" ]; then
   echo "usage: $0 length_of_period orgvar 0|1"
   exit -1
fi

n=`ps axuw | fgrep -v curl | fgrep -v grep | fgrep -c makesd.cgi`
if [ ${n:-0} -gt 3 ]; then # two processes
    echo "Somebody else is already generating natural variability files (n=$n)."
    echo "Try again later, the calculations should be ready in about half an hour.<br>"
    ###ps axuw | fgrep -v curl | fgrep -v fgrep | fgrep makesd.cgi
    exit -1
fi

if [ $rel = 0 ]; then
  relative=""
  ext=""
elif [ $rel = 1 ]; then
  relative=relative
  ext="_relative"
else
  echo "$0: error: expecting 0 or 1 for relative, not $rel"
  exit -1
fi
[ ! -d natvar ] && mkdir natvar

# first generate files from Jan's script in dir natvar

natvarfile=natvar/${orgvar}$ext.$length_of_period.nc
if [ ! -s $natvarfile ]; then
    echo "computing $natvarfile ...<p>"
    nclfile=/tmp/get_natvar_$$.ncl
    sed -e "s/LENGTH_OF_PERIOD/$length_of_period/" -e "s/VAR_NAME/$orgvar/" -e "s/RELATIVE/$rel/" get_natvar.ncl > $nclfile
    export NCARG_ROOT=./ncl
    klaarfile=/tmp/klaar$$.txt
    ( ./ncl/bin/ncl -Q < $nclfile > $nclfile.log; echo klaar > $klaarfile) &
    i=0
    while [ ! -s $klaarfile ]; do
        sleep 30
        echo "Still computing $((i++)) ... "
        ls -t natvar/ | head -1 | fgrep natvar
        echo "<p>"
    done
    rm $klaarfile
    if [ ! -s $natvarfile ]; then
        echo "$0: error: something went wrong in generating the standard deviation file $natvarfile"
        cat $nclfile.log
        exit -1
    fi
    ###rm $nclfile $nclfile.log
fi

# and then fill in the rest based on these files that Jan sent me.
ext=""
var=$orgvar
if [ $rel = 1 ]; then
    ext=_relative
    var=${var}rel
fi

dir=atlas/diff/CMIP5/sd_${length_of_period}
length=0
while [ $length -lt 12 ]
do
    s=0
    while [ $s -lt 12 ]
    do
        file=$dir/sd_${var}_${length_of_period}_mon$((s+1))_ave$((length+1)).nc
        if [ ! -s $file -o $file -ot $natvarfile ]; then
            ncks -O -d clusters,$length -d period,$s -v var_std $natvarfile $file
            ncdump $file > /tmp/aap$$.cdl
            sed -e 's/clusters, *period, *//' -e 's/var_std/sd/' /tmp/aap$$.cdl > /tmp/noot$$.cdl
            ncgen -o $file /tmp/noot$$.cdl
            rm /tmp/aap$$.cdl /tmp/noot$$.cdl
            if [ $var = pr -o $var = evspsbl -o $var = pme ]; then
                # convert from kg/m2/s to mm/dy
                cdo mulc,86400 $file $file.new
                mv $file.new $file
            fi
            if [ $var = psl ]; then
                # convert from Pa to hPa
                cdo mulc,0.01 $file $file.new
                mv $file.new $file
            fi
        fi
        s=$((s+1))
    done
    length=$((length+1))
done

