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
[ -z "$EMAIL" ] && EMAIL=FORM_email

if [ "$EMAIL" = someone@somewhere -o -z "$FORM_username" ]; then
    . ./checkemail.cgi
else
    c1=`echo "$EMAIL" | fgrep -c @`
    c2=`echo "$EMAIL" | fgrep -c http`
    if [ $c1 != 1 -o $c2 != 0 ]; then
        . ./myvinkhead.cgi "Error" "Invalid email address"
        echo "Please give somthing resembling your real e-mail address."
        echo "This helps me to justify my time to the boss, and allows me to contact you in case I find bugs in routines you used."
        . ./myvinkfoot.cgi
        exit
    fi
    c=`echo "$FORM_username" "$FORM_institute" | fgrep -c http`
    if [ $c != 0 ]; then
        . ./myvinkhead.cgi "Error" "Invalid username or institute"
        echo "Please do not use web addresses in these fields"
        . ./myvinkfoot.cgi
        exit
    fi
    if [ -n "$FORM_username" ]; then
        username=`echo $FORM_username | tr ' ' '+'`
        [ -z "$FORM_institute" ] FORM_institute="nowhere"
        institute=`echo $FORM_institute | tr ' ' '+'`
        md5=`echo "$EMAIL" | md5sum | cut -f 1 -d ' '`
        echo "^$EMAIL $username $institute $md5 `date`" >> $DIR/log/newlist
    fi
fi
echo "<meta http-equiv=\"Refresh\" content=\"0;url=start.cgi?id=$md5\">"
