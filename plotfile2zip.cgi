#!/bin/bash
# extract the raw data used in a gnuplot plotfile and zips it
. ./getargs.cgi

echo "Content-Type: text/html"
echo

if [ -z "$FORM_plotfile" -o ! -f "$FORM_plotfile" -o "${FORM_plotfile%.gnuplot}" "$FORM_plotfile" ]; then
    . ./myvinkhead.cgi "Error" ""
    echo "Cannot locate plotfile $FORM_plotfile"
    exit -1
fi

. ./myvinkhead.cgi "KNMI Atlas" "raw data"

echo "Generating zip-file with raw data...<p>"
dumpfilelist=`cat $FORM_plotfile | fgrep dump | sed -e 's/^"//' -e 's/".*$//'`
quantfilelist=`cat $FORM_plotfile | fgrep quant | sed -e 's/^"//' -e 's/".*$//'`
zip data/rawdata_$$.zip $dumpfilelist $quantfilelist > /dev/null 2>&1

echo "The raw data is available in <a href=\"data/rawdata_$$.zip\">this zip-file</a>."

. ./climexp_footer.cgi