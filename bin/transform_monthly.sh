#!/bin/sh
#
export LD_LIBRARY_PATH=/usr/local/pgi/linux86/10.5/lib/
station=$1
scen=$2
year=$3

if [ -z "$year" ]; then
  echo "usage: $0 station scenario year"
  exit -1
fi
case $mytype in
S) var="prcp [mm/day]";transform=rr-trans;;
T) var="Tg [C]";transform=tm-trans-month;;
*) echo "internal error: mytype should be S or T but not $mytype" 1>&2 ;exit -1;;
esac

if [ $year = 1990 ]
then
  echo "# $var at station $STATION ($station) around year $year"
else
  echo "# $var at station $STATION ($station) under scenario $scen around year $year"
fi
cat << EOF
# a complete description can be found at the KNMI <a href="http://climexp.knmi.nl/Scenarios_monthly/">transformation</a> and <a href="http://www.knmi.nl/climatescenarios/">climate scenarios</a> pages
EOF
if [ $station != 999 ]; then
  echo "# (c) KNMI.  This data can be distributed freely as long as this header is kept intact."
fi

export DIR=`pwd`
cd Scenarios_monthly
cat $file | $DIR/bin/$transform $scen $year 2> /tmp/transform$$.log | tail -n +2
rm /tmp/transform$$.log
