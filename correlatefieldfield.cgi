#!/bin/sh
if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

flipcolor=0

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

if [ $field1 = $field2 ]; then
  . ./myvinkhead.cgi "Field lag correlations" "$kindname1 $climfield1 lag $FORM_lag" "noindex,nofollow"
else
  . ./myvinkhead.cgi "Field-field correlations" "$kindname1 $climfield1 with $kindname2 $climfield2" "noindex,nofollow"
fi

prog="$DIR/bin/correlatefieldfield $file1 $file2"
# TAO fields are very sparse
if [ "$kindname1" = "TAO" -o "$kindname2" = "TAO" ]; then
    if [ -z "$FORM_minfac" ]; then
	FORM_minfac=25
    fi
fi

# process options related to fields only
. $DIR/getfieldopts.cgi
id=`date "+%Y%m%d_%H%M"`_$$
startstop="/tmp/startstop$id.txt"
corrargs="$corrargs startstop $startstop"

pagetitle="Field-field correlations of $kindname1 $climfield1 with $kindname2 $climfield2"
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) correlatefieldfield $file1 $file2 $corrargs" | sed -e "s:$DIR/::g" >> log/log
echo "Computing correlations... (this may take a minute or so)<p>"
# generate GrADS data file
( (echo $prog $corrargs $DIR/data/g$id.ctl; $prog $corrargs $DIR/data/g$id.ctl) > /tmp/correlatefieldfield$id.log ) 2>&1
if [ ! -s $DIR/data/g$id.ctl ]; then
    cat $DIR/wrong.html
    echo "<pre>"
    cat /tmp/correlatefieldfield$id.log
    echo "</pre>"
    . ./myvinkfoot.cgi
    exit
else
    if [ "$lwrite" = true ]; then
	cat  /tmp/correlatefieldfield$id.log
    fi
    rm /tmp/correlatefieldfield$id.log
fi

# set some variables - this piece was written for station-field correlations
FORM_STATION="$kindname1"
CLIM="$climfield1"
station="$kindname1"
kindname="$kindname2"
climfield="$climfield2"
file=data/g$id.ctl
. ./grads.cgi

#
# let the user download the raw data
#
echo "<p>"
gzip data/g$id.grd
echo "Get the correlation map(s) as GrADS <a href=\"data/g$id.ctl\">ctl</a>"
echo "and (gzipped) <a href=\"data/g$id.grd.gz\">dat</a> files,"
echo "as a (gzipped) <a href=\"grads2nc.cgi?file=data/g$id.ctl&id=$EMAIL&title=correlation_map\">netCDF</a> file or"
echo "as (gzipped) <a href=\"grads2ascii.cgi?file=data/g$id.ctl\">ascii</a> (big)."

. ./myvinkfoot.cgi
