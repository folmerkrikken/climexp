#!/bin/sh
echo 'Content-Type: text/plain'
echo
echo

. ./getargs.cgi

###printenv
###exit
echo yr1 = $FORM_yr1
echo yr2 = $FORM_yr2
exit
