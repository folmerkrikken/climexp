#!/bin/sh
# common typo?
[ "$EMAIL" = someone@somehere ] && EMAIL=someone@somewhere
# new system
c=`fgrep -c " $EMAIL " log/newlist`
if [ $c != 0 ]; then
    realemail=`fgrep " $EMAIL " log/newlist | tail -1 | cut -f 1 -d ' ' | cut -b 2-`
    md5=`echo "$realemail" | md5sum | cut -f 1 -d ' '`
    if [ "$md5" != "$EMAIL" ]; then
        . ./myvinkhead.cgi "Error" "Id \"$EMAIL\" does not correspond to email address $realemail" "noindex,nofollow"
        EMAIL="someone@somewhere"
        id=someone@somewhere
        FORM_id=someone@somewhere
        . ./myvinkfoot.cgi
        exit
    fi
fi

# convert from old system
if [ $c = 0 ]; then
    c=`fgrep -c "^$EMAIL " ./log/newlist`
    if [ $c != 0 ]; then
        md5=`fgrep "^$EMAIL " ./log/newlist | cut -f 4 -d ' ' | tail -1`
        EMAIL=$md5
        id=$md5
    else
        c=`fgrep -c "^$EMAIL " ./log/list`
        if [ $c = 0 ]; then
            string=$EMAIL
            if [ ${string#p.della} != $string ]; then
                string=spam
            fi
            EMAIL=someone@somewhere
            id=someone@somewhere
            FORM_id=someone@somewhere
            . ./myvinkhead.cgi "User $string unknown" "" "noindex,follow"
            echo "Please <a href=\"registerform.cgi\">register or log in</a> or use the Climate Explorer <a href=\"/start.cgi?id=someone@somewhere\">anonymously</a> (with restrictions)"
            . ./myvinkfoot.cgi
        fi
        if [ $EMAIL != someone@somewhere ]; then
            . ./email2md5.cgi
        fi
    fi
fi    
