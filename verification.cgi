#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo

export DIR=`pwd`
export PATH=/sw/bin:/usr/local/free/bin:/usr/local/bin:./bin:$PATH

. ./getargs.cgi
WMO=$FORM_WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
FORM_num=$$
c=`echo $WMO | egrep -c '\+\+|%'`
if [ $c -gt 0 ]; then
  ENSEMBLE=true
fi

# check email address
. ./checkemail.cgi

# real work
CLIM=`echo "$FORM_CLIMATE" | tr '[:upper:]' '[:lower:]'`
station=`echo $FORM_STATION | tr '_%' ' +'`

# common options
. $DIR/getopts.cgi
n=0
forbidden='!`;|&'
if [ "$FORM_timeseries" = "perfectmodel" ]; then
  obsfile="perfectmodel"
  index="perfect model"
  eval `bin/getunits $DIR/data/$TYPE$WMO.dat`
elif [ ! -s "$FORM_timeseries" ]; then
  . ./myvinkhead.cgi "Error"
  echo "Please select a timeseries"
  . ./myvinkfoot.cgi
else
  obsfile=$DIR/`head -1 $FORM_timeseries | tr $forbidden ' '`
  index=`head -2 $FORM_timeseries | tr $forbidden ' ' | tail -1`
  eval `bin/getunits $obsfile`
fi

# Writes to the log file what the user is doing
root=data/$TYPE$WMO${FORM_num}
table=$root.table
startstop=$root.startstop
corrargs="$corrargs file $obsfile dump $table startstop $startstop"
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) $FORM_verif $corrargs" | sed -e  "s:$DIR/::g" >> log/log

. ./myvinkhead.cgi "Time series $FORM_verif" "$station $VAR against $index" "noindex,nofollow"
cat <<EOF
Verification is under active development and may still contain bugs.  Please report problems back to <a href="mailto:oldenborgh@knmi.nl">me</a>.<p>
Extracting data...<p>
EOF
corrargs="$DIR/data/$TYPE$WMO.dat $corrargs"
if [ "$NEWUNITS" != "$UNITS" ]; then
  echo "Converting $VAR from $UNITS to $NEWUNITS"
fi
if [ "$FORM_debias" = "mean" ]; then
  debias="correcting for bias in mean"
elif [ "$FORM_debias" = "var" ]; then
  debias="correcting for bias in mean and variance"
elif [ "$FORM_debias" = "all" ]; then
  debias="correcting for bias in whole PDF"
fi
echo "$debias<br>"
# The FORTAN program by GJ called verification is run here to produce a
# nice table with columns year, month, obs, ens. member1, ens. member2 ...
# ensemble member n.
###echo '<pre>'
###echo ./bin/verification $corrargs
./bin/verification $corrargs > /tmp/verification$$.log
###echo '</pre>'
rm /tmp/verification$$.log
. ./month2string.cgi
. ./setyaxis.cgi
verifxlabel="$indexmonth $index $VAR [$NEWUNITS]"
verifylabel="$FORM_fcstname"

# the rest is common with regionverification
. ./verification1.cgi

