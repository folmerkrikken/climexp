#!/bin/sh
. ./init.cgi

export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_station

if [ "$FORM_var" = "p" ]; then
  case "$WMO" in
  496) STATION="West Terschelling";;
  497) STATION="De Kooy &amp; Den Helder";;
  499) STATION="Groningen";;
  500) STATION="Ter Apel";;
  501) STATION="Hoorn";;
  502) STATION="Heerde";;
  503) STATION="Hoofddorp";;
  504) STATION="De Bilt";;
  505) STATION="Winterswijk";;
  506) STATION="Kerwerve";;
  507) STATION="Westdorpe &amp; Axel";;
  509) STATION="Oudenbosch";;
  510) STATION="Roermond";;
  *)   echo 'Content-Type: text/html'
       echo
       echo
       . ./myvinkhead.cgi "Error" "Select a station" ""
       echo "Please select a valid station on the previous page, not $WMO"
       . ./myvinkfoot.cgi
       exit;;
  esac
  PROG="transform.sh $FORM_station"
  mytype=S
elif [ "$FORM_var" = "t" ]; then
  case "$WMO" in
  235) STATION="De Kooy &amp; Den Helder";;
  260) STATION="De Bilt";;
  280) STATION="Eelde";;
  380) STATION="Maastricht";;
  *)   echo 'Content-Type: text/html'
       echo
       echo
       . ./myvinkhead.cgi "Error" "Select a station" ""
       echo "Please select a valid station on the previous page, not $WMO"
       . ./myvinkfoot.cgi
       exit;;
  esac
  PROG="ttransform.sh $FORM_station"
  mytype=T
else
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myvinkhead.cgi "Error" "Select a variable" ""
  echo "Please select a valid variable on the previous page, not $FORM_var"
  . ./myvinkfoot.cgi
  exit
fi

TYPE=$FORM_var
NPERYEAR=366

case "$FORM_season" in
MAM) PROG="$PROG MAM";;
JJA) PROG="$PROG JJA";;
SON) PROG="$PROG SON";;
DJF) PROG="$PROG DJF";;
*)   echo 'Content-Type: text/html'
     echo
     echo
     . ./myvinkhead.cgi "Error" "Select a season" ""
     echo "Please select a valid season on the previous page, not $FORM_season"
     . ./myvinkfoot.cgi
     exit;;
esac

case "$FORM_scenario" in
0)  PROG="$PROG 0";;
G)  PROG="$PROG G";;
G+) PROG="$PROG G+";;
W)  PROG="$PROG W";;
W+) PROG="$PROG W+";;
GG)  PROG="$PROG GG";;
GG+) PROG="$PROG GG+";;
WW)  PROG="$PROG WW";;
WW+) PROG="$PROG WW+";;
*)   echo 'Content-Type: text/html'
     echo
     echo
     . ./myvinkhead.cgi "Error" "Select a scenario" ""
     echo "Please select a valid scenario on the previous page, not $FORM_scenario"
     . ./myvinkfoot.cgi
     exit;;
esac

WMO=${mytype}${WMO}_${FORM_season}_${FORM_scenario}
FROM='of the <a href="http://www.knmi.nl/scenarios/">KNMI 2006 scenarios</a>'
LASTMODIFIED=""

. $DIR/getdata.cgi
