#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Some examples" ""

sed -e "s/FORM_EMAIL/$EMAIL/" examp.html

. ./myvinkfoot.cgi
