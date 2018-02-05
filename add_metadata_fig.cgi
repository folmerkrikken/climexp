#!/bin/sh

# adds the metadata from the netcdf or ascii file to the graphics file for complete traceability.
# accepts PNG, EPS and PDF planned
# expects datfile, pngfile set in calling routine

[ -z "$datfile" ] && echo "$0: error: datfile undefined<br>" && exit
[ -z "$pngfile" ] && echo "$0: error: pngfile undefined<br>" && exit
[ ! -s "$datfile" ] && echo "$0: error: cannot find $datfile<br>" && exit
[ ! -s "$pngfile" ] && echo "$0: error: cannot find $pngfile<br>" && exit

# standard metadata

if [ -z "$NX" ]; then
    eval `./bin/getunits $datfile`
fi
for key in author title creation_time copyright variable_name variable_long_name variale_standard_name variable_units
do
    value=""
    command="cat $pngfile.bak"
    case $key in
        author) value="$EMAIL";;
        title) value="$title"
        creation_time) value=`date`;;
        copyright) value="Figures from the KNMI Climate Explorer may be used freely as long as the source KNMI is acknowledged";;
        variable_name) value="$VAR";;
        variable_long_name) value="$LVAR";;
        variable_standard_name) value="$SVAR";;
        variable_units) value="$UNITS";;
    esac
    if [ -n "$value" ]; then
        command="$command | ./bin/png-text-append \"$key\" \"$value\""
    fi
    command="$command > $pngfile"
    mv $pngfile $pngfile.bak
    eval $command
done
if [ ${datfile%.txt} != $datfile -o ${datfile%.dat} != $datfile  -o ${datfile%.plt} != $datfile ]; then
    # ascii metadata
    key=startvalue
    head -n 200 $datfile | fgrep ' :: ' | sed -e 's/^# //' -e 's/ :://' \
        | ( IPS=':'; while [ -n "$key" ]; do
            read -r key value
            if [ -n "$key" ]; then
                mv $pngfile $pngfile.bak
                cat $pngfile.bak | ./bin/png-text-append "$key" "$value" > $pngfile
            fi
        done )
    rm $pngfile.bak
else
    # netcdf metadata
    echo "cannot handle netcdf yet"
fi