#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Combining CRUTEM3 and HadSST2" ""

sed -e "s/FORM_EMAIL/$EMAIL/" crutem3_hadsst2.html

. ./myvinkfoot.cgi
