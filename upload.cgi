#!/bin/sh
. ./init.cgi
scriptname=`basename $0 .cgi`
if [ $scriptname = upload ]; then
    scriptname=uploaded
fi
. ./getargs.cgi
. ./checkemail.cgi

TYPE=`basename $FORM_TYPE`
STATION=`echo "$FORM_STATION" | tr ' <>&;%=' '_'`
[ -z "$STATION" ] && STATION=no_name
if [ "$TYPE" = "p" ]; then
NAME="Precipitation"
elif [ "$TYPE" = "t" ]; then
NAME="Temperature"
elif [ "$TYPE" = "s" ]; then
NAME="Pressure"
elif [ "$TYPE" = "l" ]; then
NAME="Sea level"
elif [ "$TYPE" = "r" ]; then
NAME="Runoff"
else
NAME=Index
TYPE="i"
fi
export DIR=`pwd`
PROG=""
i=-1
numberinuse=true
while [ $numberinuse = true ]
do
  i=$((i+1))
  WMO=$scriptname$i
  numberinuse=false
  if [ -f ./data/$TYPE$WMO.dat -o -f ./data/$TYPE$WMO.nc -o -f ./data/$TYPE${WMO}_00.dat -o -f ./data/$TYPE${WMO}_00.nc ]; then
    numberinuse=true
  else
    metadata=`echo ./data/$TYPE${WMO}.*.inf | tr " " "\n" |head -1`
    if [ -f $metadata ]; then
      numberinuse=true
    fi
  fi
done

if [ -n "$FORM_data" ]; then
  echo "$FORM_data" | tr '\r' '\n' > $DIR/data/$TYPE$WMO.dat
else
    echo "Content-Type: text/html"
    echo
    echo
    . ./myvinkhead.cgi "Retrieving series" "$STATION" "index,nofollow"
    . ./checkurl.cgi
    nens=`echo $FORM_url | wc -w`
    if [ $nens = 1 ]; then
        curl -s "$FORM_url" | tr '\r' '\n' > data/$TYPE$WMO.dat
    else
# ensemble
        iens=0
        for url in $FORM_url
        do
            if [ $iens -lt 10 ]; then
                ensfile=data/$TYPE${WMO}_0$iens.dat
            elif [ $iens -lt 100 ]; then
                ensfile=data/$TYPE${WMO}_$iens.dat
            else
                echo "Error: can only handle up to 100 ensemble members"
                . ./myvinkfoot.cgi
    	        exit
            fi
            echo "Retrieving $ensfile from $url<br>"
            curl -s "$url" > $ensfile
            iens=$(($iens + 1))
        done
        WMO=${WMO}_%%
    fi
fi

eval `./bin/getunits ./data/$TYPE$WMO.dat`
if [ -z "$NT" -o "$NT" = 0 ]; then
    rm ./data/$TYPE$WMO.dat
    echo "Content-Type: text/html"
    echo
    echo
    . ./myvinkhead.cgi "Error" "$station $NAME" "nofollow,index"
    echo "This does not appear to be a valid time series."
    . ./myvinkfoot.cgi
    exit -1
fi

. ./getdata.cgi
