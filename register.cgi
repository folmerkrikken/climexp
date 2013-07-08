#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi

if [ "$lwrite" = true ]; then
    echo "EMAlL = $EMAIL<br>"
    echo "FORM_email = $FORM_email<br>"
    echo "FORM_username = $FORM_username<br>"
    echo "FORM_institute = $FORM_institute<br>"
fi

. ./nosearchengine.cgi
c1=`echo "$EMAIL" | fgrep -c @`
c2=`echo "$EMAIL" | fgrep -c http:`
if [ $c1 != 1 -o $c2 != 0 ]; then
  . ./myvinkhead.cgi "Error" "Invalid email address"
  echo "Please give somthing resembling your real e-mail address."
  echo "This helps me to justify my time to the boss, and allows me to contact you in case I find bugs in routines you used."
  . ./myvinkfoot.cgi
  exit
fi
c=`echo "$FORM_username" "$FORM_institute" | fgrep -c http:`
if [ $c != 0 ]; then
    echo "Please do not use web addresses in these fields"
    exit
fi
if [ -n "$FORM_username" ]; then
#echo "New user $FORM_username"
    username=`echo $FORM_username | tr ' ' '+'`
    institute=`echo $FORM_institute | tr ' ' '+'`
    echo "^$EMAIL $username $institute" >> $DIR/log/list
#else
#echo "Old user $FORM_username"
fi
echo "<meta http-equiv=\"Refresh\" content=\"0;url=start.cgi?id=$EMAIL\">"
