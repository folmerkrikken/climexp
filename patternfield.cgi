#!/bin/sh

. ./getargs.cgi
export DIR=`pwd`
FORM_minfac=0.5
if [ -z "$FORM_field2" ]; then
  FORM_field1=$FORM_field
  FORM_field2=$FORM_field
else
  FORM_field1=$FORM_field
  FORM_field=$FORM_field2
fi

. ./queryfield.cgi

WMO=${FORM_field}_${FORM_variable}_$$
STATION=`echo "${FORM_variable} of ${kindname} ${climfield}" | tr ' ' '_'`
if [ "$FORM_field1" != "$FORM_field2" ]; then
  FORM_field=$FORM_field1
  # it is irrelevant whether the pattern came from an ensemble
  ENSEMBLE=""
  . ./queryfield.cgi
  WMO=$FORM_field_$WMO
  STATION=`echo "${STATION} projected on $kindname $climfield" | tr ' ' '_'`
fi
if [ -n "$ENSEMBLE" ]; then
  WMO=${WMO}_++
  station="$station ensemble"
fi
TYPE=i
NAME="Index"
PROG="patternfield.sh $file data/$FORM_patfile $FORM_variable $FORM_month minfac $FORM_minfac"
kill=true

export file
export WMO
export TYPE
. $DIR/getdata.cgi
