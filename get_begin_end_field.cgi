#!/bin/sh
if [ -n "$describefield" ]; then
# the quotes are essential to keep lines apart
  line=`echo "$describefield"  | fgrep -i available`
else
  line=`./bin/describefield.sh $file | fgrep -i available`
fi
yrbeg=`echo $line | awk '{print substr($5,4)}'`
yrend=`echo $line | awk '{print substr($7,4)}'`
month=`echo $line | awk '{print substr($5,1,3)}'`
case $month in
JAN|Jan|jan) mobeg=1;;
FEB|Feb|feb) mobeg=2;;
MAR|Mar|mar) mobeg=3;;
APR|Apr|apr) mobeg=4;;
MAY|May|may) mobeg=5;;
JUN|Jun|jun) mobeg=6;;
JUL|Jul|jul) mobeg=7;;
AUG|Aug|aug) mobeg=8;;
SEP|Sep|sep) mobeg=9;;
OCT|Oct|oct) mobeg=10;;
NOV|Nov|nov) mobeg=11;;
DEC|Dec|dec) mobeg=12;;
*) echo "get_beg_end_field: cannot recognize month in \"$month\""
mobeg=0;;
esac
month=`echo $line | awk '{print substr($7,1,3)}'`
case $month in
JAN|Jan|jan) moend=1;;
FEB|Feb|feb) moend=2;;
MAR|Mar|mar) moend=3;;
APR|Apr|apr) moend=4;;
MAY|May|may) moend=5;;
JUN|Jun|jun) moend=6;;
JUL|Jul|jul) moend=7;;
AUG|Aug|aug) moend=8;;
SEP|Sep|sep) moend=9;;
OCT|Oct|oct) moend=10;;
NOV|Nov|nov) moend=11;;
DEC|Dec|dec) moend=12;;
*) echo "get_end_end_field: cannot recognize month in \"$month\""
moend=0;;
esac
