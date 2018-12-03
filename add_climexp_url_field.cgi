#!/bin/bash
[ -z "$file" ] && echo "$0: error: set variable file" && exit -1
[ ! -s "$file" ] && echo "$0: error: cannot find file $file" && exit -1
. $HOME/climexp/add_geospatial_time.sh
queryfield=$HOME/climexp/queryfield.cgi
if [ -s $queryfield ]; then
    field=`egrep "[=/]$file" $queryfield | tail -n 1 | sed -e 's/^ *//' -e 's/[|)].*$//'`
    ### echo "$0: field=$field"
    ###echo "$0: file=$file"
    if [ -n "$field" ]; then
        climexp_url="https://climexp.knmi.nl/select.cgi?$field"
        ###echo "ncatted -h -a climexp_url,global,a,c,$climexp_url $file"
        ncatted -h -a climexp_url,global,c,c,$climexp_url $file
        ncatted -h -a climexp_url,global,o,c,$climexp_url $file
    else
        echo "$0: error: cannot find $file in $queryfield"
    fi
fi
