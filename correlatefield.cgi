#!/bin/sh

lwrite=false
if [ $EMAIL = oldenborgh@knmi.nl ]; then
    lwrite=false # true
fi

if [ $FORM_var = chi -o $FORM_var = chibar ]; then
  . ./getpotfield.cgi
  exit
fi

. ./queryfield.cgi

. ./myvinkhead.cgi "Field correlations" "$station $NAME with $kindname $climfield" "noindex,nofollow"
prog="./bin/correlatefield $file"

###echo "FORM_nens1,2 = $FORM_nens1,$FORM_nens2<br>"
###echo "corrargs = $corrargs<br>"

if [ $FORM_maskout != mask -a $FORM_colourscale -gt 9 ]; then
    echo "Drawing non-significant areas $FORM_maskout is not possible with the new colour scales, masking them out instead.<br>"
    FORM_maskout=mask
fi

# process options related to fields only
. ./getfieldopts.cgi
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"

pagetitle="Field correlations of $station $CLIM ($WMO) with $kindname $climfield"

if [ $EMAIL != someone@somewhere ]; then
  explanation="(to read while waiting for the correlation)"
  . ./headlines.cgi
fi
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) correlatefield $file $corrargs" | sed -e "s:$DIR/::g" >> log/log
if [ -n "$FORM_runcorr" -a -n "$FORM_runwindow" ]; then
  echo "Computing running $FORM_runvar and their significance with a Monte Carlo.  This will take quite a while<p>"
else
  echo "Computing correlations... (this may take a minute or so)<p>"
fi
# license to kill
echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$FORM_EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the correlation job)</small><p>"
cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
$prog $corrargs
@
EOF
export SCRIPTPID=$$
export FORM_EMAIL
# generate GrADS data file
id=`date "+%Y%m%d_%H%M"`_$$
[ "$lwrite" = true ] && echo $prog $corrargs $DIR/data/g$id.nc
( (echo $prog $corrargs $DIR/data/g$id.nc; $prog $corrargs $DIR/data/g$id.nc) > /tmp/correlatefield$id.log ) 2>&1
if [ ! -s $DIR/data/g$id.nc ]; then
  cat ./wrong.html
  cat /tmp/correlatefield$id.log | sed -e 's/$/<br>/'
  rm /tmp/correlatefield$id.log
  echo "</body></html>"
  exit
else
  if [ "$lwrite" = true ]; then
    cat /tmp/correlatefield$id.log | sed -e 's/$/<br>/'
  fi
  rm /tmp/correlatefield$id.log
fi

file=data/g$id.nc
datafile=data/g$id
if [ ${FORM_var:-corr} != composite -a ${FORM_var:-corr} != comperr ]; then
  subtractform="yes"
fi
. ./grads.cgi

. ./myvinkfoot.cgi
