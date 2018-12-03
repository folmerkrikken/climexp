#!/bin/bash
# adds the metadata from the netcdf or ascii file to the graphics file for complete traceability.
# accepts PNG, EPS and PDF planned
# expects datfile, pngfile set in calling routine

# TODO: add variable name, long_name, standard_name.

[ -z "$datfile" ] && echo "$0: error: datfile undefined<br>" && exit
[ -z "$pngfile" ] && echo "$0: error: pngfile undefined<br>" && exit
[ ! -s "$datfile" ] && echo "$0: error: cannot find $datfile<br>" && exit
[ ! -s "$pngfile" ] && echo "$0: error: cannot find $pngfile<br>" && exit

# Adobe XMP / Dublin Core metadata

if [ -z "$NX" ]; then
    eval `./bin/getunits $datfile`
fi
cat > /tmp/exifargs$$.txt <<EOF
-Creator=KNMI Climate Explorer climexp.knmi.nl
-License=This figure may be used freely provided that the following source is acknowledged: KNMI Climate Explorer
-Rights=This figure may be used freely provided that the following source is acknowledged: KNMI Climate Explorer
-Date=`date`
EOF
# add date, edcationLevel, ...
references=""
sources=""
spatial="" # not yet used
temporal="" # not yet used
# ascii metadata
if [ ${datfile%.txt} != $datfile -o ${datfile%.dat} != $datfile  -o ${datfile%.plt} != $datfile ]; then
    # ascii metadata
    key=startvalue
    oldIPS=$IPS
    IPS=':'
    head -n 200 $datfile | fgrep ' :: ' | sed -e 's/^# //' -e 's/ :://' \
        | while [ -n "$key" ]; do
            read -r key value
            ###echo "$key" "$value"
            if [ -n "$key" ]; then
                case $key in
    description) key=Description ;;
    title) key=Title;;
    url|link|source_url) sources="$sources $value";key="";;
    reference*) references="$references $value";key="";;
                esac
            fi
            if [ -n "$key" ]; then
                cat >> /tmp/exifargs$$.txt <<EOF
-$key=$value
EOF
            fi
        done
    IPS=$oldIPS
    if [ -n "$references" ]; then
        echo "do something with references"
EOF
    fi
    if [ -n "$sources" ]; then
        echo "do something with sources"
    fi
else
    # netcdf metadata
    echo "cannot handle netcdf yet"
fi
###cat /tmp/exifargs$$.txt
exiftool -config exiftool/exiftool.config -@ /tmp/exifargs$$.txt $pngfile
rm /tmp/exifargs$$.txt
# pngfile
# pdffile
# epsfile