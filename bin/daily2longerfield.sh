#!/bin/bash
lwrite=false
declare -a ensargs
ensargs=("$@")
n=$(($# - 1))
if [ -z "$DIR" ]; then
  DIR=`pwd`
fi
PROG=`basename $0 .sh`
file=$1
c0=`echo $file | fgrep -c '%%%'`
c1=`echo $file | fgrep -c '%%'`
c2=`echo $file | fgrep -c '++'`
if [ $c1 -eq 0 -a $c2 -eq 0 ]
then
    ./bin/$PROG $*
else
    i=0
    if [ $c0 = 1 ]; then
        ii=000
        imax=1000
        format=%03i
    else
        ii=00
        imax=100
        format=%02i
    fi
	while [ $i -lt $imax ]
	do	    
        allfiles=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
        if [ "$splitfield" = true ]; then
            ensfile=`ls -t $allfiles 2>&1 | head -1`
        else
            ensfile=$allfiles
        fi
		[ $i -lt 10 -a "$lwrite" = true ] && echo "checking for ensfile = $ensfile<br>"
		if [ -s "$ensfile" -o -s "data/$ensfile" ]
		then

            if [ "$splitfield" = true ]; then
                iarg=1
                restargs=""
                while [ $iarg -lt $n ]; do
                    restargs="$restargs ${ensargs[$iarg]}"
                    ((iarg++))
                done
                ifile=0
                outfiles=""
                for ensfile in $allfiles; do
                    realoutfile=`echo ${ensargs[$n]} | sed -e "s:\+\+\+:$ii:g" -e "s:\+\+:$ii:g" -e "s:\%\%\%:$ii:g" -e "s:\%\%:$ii:g"`
                    outfile=${realoutfile%.ctl}
                    outfile=${realoutfile%.nc}
                    outfile=${realoutfile}_$ifile.nc
                    outfiles="$outfiles $outfile"
                    ((ifile++))
                    [ "$lwrite" = true ] && echo "$DIR/bin/$PROG $ensfile $restargs $outfile"
                    $DIR/bin/$PROG $ensfile $restargs $outfile
                done
                catnc $outfiles $realoutfile
                outfile=$realoutfile
            else
                ensargs=(`echo "$@" | sed -e "s:\+\+\+:$ii:g" -e "s:\+\+:$ii:g" -e "s:\%\%\%:$ii:g" -e "s:\%\%:$ii:g"`)
                outfile=${ensargs[$n]}
                [ "$lwrite" = true ] && echo "$DIR/bin/$PROG ${ensargs[*]}"
                $DIR/bin/$PROG ${ensargs[*]}
            fi
            echo "generated $outfile<p>"
        fi
        i=$(($i + 1))
        ii=`printf $format $i`
    done
fi
