#!/bin/sh
if [ -z "$alreadycalledgetargs" ]; then
    export alreadycalledgetargs=true
    eval `./bin/proccgi "$@"`

    EMAIL="$FORM_id"
    [ -z "$EMAIL" ] && EMAIL="$FORM_EMAIL"
    [ -z "$EMAIL" ] && EMAIL="$FORM_email"
    if [ -z "$EMAIL" ]; then
        # maybe someone used the old links
        c1=`echo "$QUERY_STRING" | fgrep -c '@'`
        c2=`echo "$QUERY_STRING" | fgrep -c '+'`
        if [ $c1 = 1 -a $c2 = 0 ]; then
            EMAIL="$QUERY_STRING"
        fi
    fi
    EMAIL=`echo "$EMAIL" | fgrep -v '/' `
    EMAIL=`echo "$EMAIL" | tr -cd '[:alnum:]@.-_' | fgrep -v "/" | egrep -v '(@|\.|-)sexy(@|\.|-)|(@|\.|-)sex(@|\.|-)|(@|\.|-)porn(@|\.|-)|(@|\.|-)porno(@|\.|-)|youtube.com|fynalcut.com|shop.*ru$|della-marta'`
    EMAIL=${EMAIL#id=}
    [ "$EMAIL" = FORM_EMAIL ] && EMAIL=""
    id=$EMAIL
    ###echo "EMAIL=$EMAIL<br>"
    [ -n "FORM_WMO" ] && FORM_WMO=`echo "$FORM_WMO" | sed -e 's/%%%/+++/' -e 's/%%/++/'`
    [ -n "FORM_wmo" ] && FORM_wmo=`echo "$FORM_wmo" | sed -e 's/%%%/+++/' -e 's/%%/++/'`
fi # alreadycalledgetargs