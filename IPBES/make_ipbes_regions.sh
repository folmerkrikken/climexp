#!/bin/sh
# usage: make_ipbes_regions.sh < IPBES\ regions\ for\ KNMI\ website.csv
# I assume the .csv file has udnerscores instead of spaces.
IFS=";"
lastregion="none"
lastsubregion="none"
# header line
read
status=$?
while [ $status = 0 ]; do
    read region subregion ipbes_name climexp_name
    status=$?
    if [ $status = 0 -a -n "$climexp_name" ]; then
        [ -z "$region" ] && region=$lastregion
        [ -z "$subregion" ] && subregion=$lastsubregion
        ###echo $region,$subregion,$climexp_name
        if [ $region != $lastregion ]; then
            [ -f IPBES_$region.txt ] && rm IPBES_$region.txt
            echo "# IPBES $region" > IPBES_$region.txt
            [ -f IPBES_${region}_nan.txt ] && rm IPBES_${region}_nan.txt
            touch IPBES_${region}_nan.txt
        fi
        if [ $subregion != $lastsubregion ]; then
            [ -f IPBES_$subregion.txt ] && rm IPBES_$subregion.txt
            echo "# IPBES $subregion" > IPBES_$subregion.txt
            [ -f IPBES_${subregion}_nan.txt ] && rm IPBES_${subregion}_nan.txt
            touch IPBES_${subregion}_nan.txt
        fi
        file=../countries/$climexp_name.txt
        if [ ! -s $file ]; then
            echo "$0: error: cannot find $file, please repair CSV input"
            ls -l `echo $file | cut -b 1-15`*
            exit
        fi
        for myregion in IPBES_$region IPBES_$subregion
        do
            cat $file >> $myregion.txt
            echo >> $myregion.txt
            cat ${file%.txt}_nan.txt >> ${myregion}_nan.txt
            echo "NaN  NaN" >> ${myregion}_nan.txt
        done
        lastregion=$region
        lastsubregion=$subregion
    fi
done