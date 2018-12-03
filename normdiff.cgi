#!/bin/bash
#
# subtract two (normalized) time series
#
export DIR=`pwd`
. ./getargs.cgi

WMO="$FORM_WMO"
export TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
NAME="Index"

if [ "$FORM_myindex0" = nothing ]; then
    datfile=nothing
    case "$FORM_my1" in
	monthly) WMO=${WMO}_mnorm;STATION="${FORM_STATION} (m.norm)";;
	yearly)  WMO=${WMO}_anorm;STATION="${FORM_STATION} (a.norm)";;
	*)  echo "Content-Type: text/html"
	    echo
	    . ./myvinkhead.cgi "Error" ""
	    echo "Unexpected input my1=$FORM_my1"
	    . ./myvinkfoot.cgi
	    exit;;
    esac
    FORM_my2=monthly # something, is not used
else
    . ./getuserindex.cgi
    if [ -z "$datfile" ]; then
	echo "Content-Type: text/html"
	echo
	. ./myvinkhead.cgi "Error" ""
	echo "Please select a time series on the previous page"
	. ./myvinkfoot.cgi
	exit
    fi
    STATION="${FORM_STATION}-$index"
    c1=`echo $FORM_WMO | egrep -c '%%|\+\+'`
    c2=`echo $datfile  | egrep -c '%%|\+\+'`
    if [ "$lwrite" = true ]; then
        echo "Content-Type: text/html"
        echo
        echo "FORM_WMO=$FORM_WMO<br>"
        echo "datfile =$datfile<br>"
    fi
    if [ $c1 = 1 -a $c2 = 1 ]; then
	    export WMO=`echo $FORM_WMO | sed -e 's:\+\+\+:___:' -e 's:\+\+:__:' -e 's:%%%:___:' -e 's:%%:__:'`-`basename $datfile .dat|cut -b 2-`
    else
	    export WMO=${FORM_WMO}-`basename $datfile .dat|cut -b 2-`
    fi
    [ "$lwrite" = true ] && echo "WMO(out)=$WMO<br>"
fi

PROG="normdiff.sh $DIR/data/$TYPE$FORM_WMO.dat $datfile $FORM_my1 $FORM_my2"

. ./getdata.cgi
