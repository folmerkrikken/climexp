#!/bin/bash

outfile=`echo $corrroot.dat | sed -e 's/\+/X/g'`
if [ "$lwrite" = true ]; then
    echo "correlate $corrargs<p>"
    echo "outfile=$outfile<p>"
fi

n3=`echo $corrargs | egrep -c '\+\+\+|%%%'`
[ $n3 = 0 ] && n2=`echo $corrargs | egrep -c '\+\+|%%'`
if [ $n3 != 0 ]; then
    nmax=999
    pat='+++'
    format='%03i'
elif [ $n2 != 0 ]; then
    nmax=99
    pat='++'
    format='%02i'
else
    echo "$0: error: cannot find ++ or %% in $corrargs"
    . ./myvinkfoot.cgi
    exit -1
fi

# compute correlations and construct fake time series with correlations / regressions

if [ "$FORM_whichvar" = corr  ]; then
    with=with
    UNITS=1
else
    with=on
    i=0
    ii=`printf $format $i`
    indexfile=${corrargs#*file }
    indexfile=${indexfile%% *}
    eval `getunits $indexfile` # assume no ensemble for the time being
    indexunits=$UNITS
    firstfile=`echo $corrargs | cut -f 1  -d ' ' | sed -e "s/$pat/$ii/"`
    eval `getunits $firstfile`
    seriesunits=$UNITS
    if [ -z "$indexunits" -o "$indexunits" = "1" ]; then
        UNITS=$seriesunits
    else
        UNITS="$seriesunits/$indexunits"
    fi
fi
echo "# correlate $corrargs" > $outfile
echo "# $FORM_whichvar [$UNITS] $FORM_whichvar $STATION $with $index" >> $outfile
i=-1
nextfile=true
yrstart=
yrstop=
while [ $i -lt $nmax -a $nextfile = true ]; do
    ((i++))
    ii=`printf $format $i`
    enscorrargs=`echo $corrargs | sed -e "s/$pat/$ii/g"`
    infile=`echo $enscorrargs | cut -f 1  -d ' '`
    [ "$lwrite" = true ] && echo "infile=$infile<p>"
    startstop=/tmp/startstop$$_$i.txt
    if [ -s $infile ]; then
        if [ $i = 0 ]; then
            enscorrargs="$enscorrargs dump /tmp/dump$$.txt"
        fi
        correlate $enscorrargs startstop $startstop | sed -e "s/&nbsp;/$ii/"
        if [ $i = 0 ]; then
            fgrep ' :: ' /tmp/dump$$.txt >> $outfile
            rm /tmp/dump$$.txt
        fi
        # plotfile is set in correlate.cgi
        ensplotfile=`echo $plotfile | sed -e "s/$pat/$ii/g"`
        if [ ! -s $ensplotfile ]; then
            echo "$0: error: cannot find $ensplotfile"
            exit -1
        fi
        if [ "$FORM_whichvar" = corr  ]; then
            var=`cat $ensplotfile | awk '{print $3}'`
        else
            var=`cat $ensplotfile | awk '{print $10}'`
        fi
        if [ -s "$startstop" ]; then
	        yrstarti=`head -1 $startstop`
	        yrstopi=`tail -1 $startstop`
	        rm $startstop
            if [ -z "$yrstart" ]; then
                yrstart=$yrstarti
                yrstop=$yrstopi
            else
                [ $yrstarti -lt $yrstart ] && yrstart=$yrstarti
                [ $yrstopi -lt $yrstop ] && yrstop=$yrstopi
            fi
        fi
        yr=$((2000+i))
        echo "$yr $var" >> $outfile
        rm $ensplotfile
    else
        nextfile=false
    fi
done

cat <<EOF
Download the <a href="$outfile">results</a><p>
EOF

# call histogram routine

FORM_plot=hist
FORM_fit=gauss
FORM_nbin=20
FORM_TYPE=`basename $outfile | cut -b 1`
FORM_WMO=`basename $outfile .dat`
FORM_WMO=${FORM_WMO#$FORM_TYPE}
FORM_STATION="$FORM_whichvar $STATION $with $index"
FORM_yrbeg=""
FORM_yrend=""
nostartstop=true
notimescale=true
. ./histogram.cgi

exit