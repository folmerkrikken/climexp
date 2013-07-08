#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi

. ./save_variable.cgi
# what field is field2?
. ./queryfield.cgi
# and save
field2=$FORM_field
file2=$file
kindname2=$kindname
climfield2=$climfield
map2=$map
flipcolor2=$flipcolor
# what field is field1?
FORM_field=$FORM_field1
. ./queryfield.cgi
# and save
field1=$FORM_field
file1=$file
kindname1=$kindname
climfield1=$climfield
map1=$map
flipcolor1=$flipcolor

. $DIR/getopts.cgi
[ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
[ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
[ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
[ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"
[ -n "$FORM_minfac" ] && corrargs="$corrargs minfac $FORM_minfac"

c1=`echo $file1 |  fgrep -c '%%'`
c2=`echo $file2 |  fgrep -c '%%'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  export WMO=${FORM_var}_++_$$
else
  export WMO=${FORM_var}_$$
fi
station="${kindname1}_${climfield1}_vs_${kindname2}_${climfield2}"
STATION=`echo $station | tr ' ' '_'`
export TYPE=c
NAME="correlation"
PROG="fieldcorrelate.sh $file1 $file2 $FORM_var $corrargs"

. $DIR/getdata.cgi
