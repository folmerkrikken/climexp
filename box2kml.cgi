#!/bin/bash
. ./init.cgi
echo "Content-Type: text/html"
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"

if [ "$EMAIL" = oldenbor@knmi.nl ]; then
    lwrite = true
else
    lwrite=false
fi

. ./nosearchengine.cgi
climate=`echo "$FORM_climate" | tr ' ' '_'`
prog="$FORM_prog"
listname="$FORM_listname"
extraargs="$FORM_extraargs"

plotlist=data/plotlist$$.txt
kml=data/climexp$$.kml
[ $lwrite = true ] && echo "bin/stationlist $listname $plotlist $prog list"
bin/stationlist $listname $plotlist $prog list
if [ ! -s $plotlist ]; then
    . ./myvinkhead.cgi "Error" "No data were generated"
    echo "Sorry, something went wrong. Please contact <a href=\"mailto:oldenborgh@knmi.nl\">me</a> to solve this."
    . ./myvinkfoot.cgi
    exit
fi

echo `date`" $EMAIL ($REMOTE_ADDR) list2kml $plotlist $climate $EMAIL $prog $extraargs" >> log/log
./bin/list2kml $plotlist $climate $EMAIL $prog $extraargs > $kml

if [ ! -s $kml ]; then
    . ./myvinkhead.cgi "Error" "No KML was generated"
    echo "Sorry, something went wrong. Please contact <a href=\"mailto:oldenborgh@knmi.nl\">me</a> to solve this."
    . ./myvinkfoot.cgi
    exit
fi

rm $plotlist
cat <<EOF
<html>
<meta http-equiv="Refresh" content="0;url=$kml">
</html>
EOF
