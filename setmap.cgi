#!/bin/sh
# sets correct map for GrADS, called from grads.cgi and plotstations.cgi
#
if [ -n "$FORM_lat1" -a -n "$FORM_lat2" ]; then
# round to integer boundaries...
    dlat=$((${FORM_lat2%.*} - ${FORM_lat1%.*}))
else
    dlat=180
fi
if [ -n "$FORM_lon1" -a -n "$FORM_lon2" ]; then	
    mlon=$(((${FORM_lon2%.*} + ${FORM_lon1%.*})/2))
else
    mlon=5
fi
[ $dlat -lt 0 ] && dlat=$((0 - $dlat))
[ "$lwrite" = true ] && echo "dlat,mlon = $dlat,$mlon<br>"
if [ $dlat -lt 39 ]; then
    if [ $mlon -lt 0 -o \( $mlon -gt 180 -a $mlon -lt 360 \) ]; then
        [ "$lwrite" = true ] && echo "dlat -lt 39, WH, hence hires map<br>"
        map="$map
set mpdset hires"
    else
        if [ -n "$FORM_nopoli" ]; then
            [ "$lwrite" = true ] && echo "dlat -lt 39, EH, nopoli hence hires map<br>"
            map="$map
set mpdset hires"
        else
            [ "$lwrite" = true ] && echo "dlat -lt 39, EH, hence newmap map<br>"
            map="$map
set mpdset newmap"
        fi
    fi
else
    [ "$lwrite" = true ] && echo "dlat -ge 39 hence lowres map<br>"
    map="$map
set mpdset lowres"
    FORM_nopoli="" # otherwise the coastlines disappear as well...
fi
