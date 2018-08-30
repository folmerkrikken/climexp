#!/bin/sh

rm *.txt
dir=imd_met_subdivision_shp
abbrfile=$dir/abbr.txt
abbrs=`cat $abbrfile | cut -f 2 -d ' '`
for abbr in $abbrs; do
    name=`cat $abbrfile | fgrep " $abbr " | cut -f 3 -d ' '`
    echo $abbr $name
    ogr2ogr -f GML -t_srs "EPSG:4326" $abbr.gml $dir/$abbr/$abbr.shp
    if [ ! -f $abbr.gml ]; then
        echo "$0: something went wrong in ogr2ogr, $abbr.gml not generated"
        exit -1
    fi
    ./gml2txt.py $abbr.gml 0
    ./insert_breaks.py $abbr.txt
    mv ${abbr}_new.txt India_$name.txt
    cp India_$name.txt ../countries/
done

