#!/bin/bash
# select a member of an ensemble
# Geert Jan van Oldenborgh, KNMI, 13-jan-2005

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
FORM_email="$EMAIL"
i="$FORM_i"

. ./queryfield.cgi

field=`basename $FORM_field .info`
field=`basename $field .$EMAIL`
infofile=data/$field.$i.$EMAIL.info
c=`echo $file | fgrep -c '%%%'`
member="$FORM_member"
if [ -z "$member" ]; then
    c3=`echo "$file" | fgrep -c '%%%'`
    c2=`echo "$file" | fgrep -c '%%'`
    if [ $c3 = 1 ]; then
        ens=`printf %03i $i`
        pat="%%%"
    elif [ $c2 = 1 ]; then
        ens=`printf %02i $i`
        pat="%%"
    fi
    member=`echo $file | sed -e "s/$pat/$ens/"`
fi
echo "$member"           > $infofile
if [ -n "$LSMASK" ]; then
  echo "LSMASK=$LSMASK" >> $infofile
fi
if [ -n "$NPERYEAR" ]; then
  echo "NPERYEAR=$NPERYEAR" >> $infofile
fi
echo $kindname ens$i    >> $infofile
echo $climfield         >> $infofile

FORM_field=$infofile
ENSEMBLE=""
splitfield=""
. ./select.cgi
