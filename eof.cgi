#!/bin/sh
echo 'Content-Type: text/html'
. ./expires.cgi
echo
echo

export DIR=`pwd`
. ./getargs.cgi

lwrite=false
if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

. $DIR/queryfield.cgi
# this sets NPERYEAR...

if [ $EMAIL != someone@somewhere ]; then
  . ./save_commonoptions.cgi
  cat > ./prefs/$EMAIL.eofs <<EOF
FORM_neof=$FORM_neof;
FORM_normsd=$FORM_normsd;
FORM_avex=$FORM_avex;
FORM_avey=$FORM_avey;
FORM_minfac=$FORM_minfac;
FORM_normalization=$FORM_normalization;
EOF
fi

. ./myvinkhead.cgi "Compute $FORM_neof EOFs" "$kindname $climfield" "noindex,nofollow"

corrargs="$FORM_neof"
. $DIR/getopts.cgi
# lat[12], lon[12] are also job args here
[ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
[ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
[ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
[ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"
[ -n "$FORM_avex" ] && corrargs="$corrargs xave $FORM_avex"
[ -n "$FORM_avey" ] && corrargs="$corrargs yave $FORM_avey"
# adapt name if normalized to sd
[ -n "$FORM_normsd" ] && climfield="$climfield / s.d."
. $DIR/getfieldopts.cgi

if [ $EMAIL != someone@somewhere ]; then
  explanation="(to read while waiting for the EOFs)"
  . ./headlines.cgi
fi

echo `date` "$EMAIL ($REMOTE_ADDR) eof $FORM_field $corrargs" | sed -e "s:$DIR/::g"  >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"

echo "Computing EOFs.  This will take (quite) a while...<br>"
echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the EOF job)</small><p>"
# generate GrADS data file
cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
eof $FORM_field $corrargs
@
EOF
export SCRIPTPID=$$
export FORM_EMAIL=$EMAIL
root=eof`date "+%Y%m%d_%H%M"`_${$}
( (echo bin/eof $file $corrargs $DIR/data/$root.ctl; $DIR/bin/eof $file $corrargs $DIR/data/$root.ctl) > /tmp/$root.log ) 2>&1
rm pid/$$.$EMAIL
if [ ! -s $DIR/data/$root.grd ]; then
  cat $DIR/wrong.html
  echo "<pre>"
  cat /tmp/$root.log
  rm /tmp/$root.log
  echo "</pre>"
  echo "</body></html>"
  exit
else
  if [ "$lwrite" = true ]; then
      cat /tmp/$root.log
  fi
  rm /tmp/$root.log
fi

# plot data

file=data/$root.ctl
station=$kindname
CLIM=$climfield
ieof=0
while [ $ieof -lt ${FORM_neof:-4} ]
do
  ieof=$(($ieof+1))
  FORM_var=eof$ieof
  uniq=${root}_$ieof
  if [ $ieof -lt ${FORM_neof:-4} ]; then
    insideloop=true
  else
    insideloop=""
  fi
  if [ $ieof -lt 10 ]; then
    iieof=0$ieof
  else
    iieof=$ieof
  fi
  if [ -n "$ENSEMBLE" ]; then
    ext="${iieof}_%%"
  else
    ext=$iieof
  fi
  pcname=`echo "PC$ieof of $kindname $climfield" | tr " " "_"`
  extra1="<br><a href=\"getindices.cgi?WMO=data/${root}_${ext}&STATION=$pcname&TYPE=i&id=$EMAIL\">Principal component PC$ieof</a><br><a href=\"patternfield.cgi?id=$EMAIL&patfile=$root.ctl&variable=eof$ieof&month="
  # here the month will be added be grads.cgi
  extra2="&field=$FORM_field\">project eof$ieof on the same field</a>, "
  extra3="<a href=\"patternfieldform.cgi?id=$EMAIL&patfile=$root.ctl&variable=eof$ieof&month="
  # here the month will be added be grads.cgi
  extra4="&field=$FORM_field\">project eof$ieof on another field</a><br>"
  . ./grads.cgi
  dano=''
done
#
# let the user download the raw data
#
echo "<p>"
gzip -c data/$root.grd > data/$root.grd.gz
echo "Get the EOF map(s) as GrADS <a href=\"data/$root.ctl\">ctl</a>"
echo "and (gzipped) <a href=\"data/$root.grd.gz\">dat</a> files,"
echo "as a (gzipped) <a href=\"grads2nc.cgi?file=data/$root.ctl&id=$EMAIL\">netCDF</a> file,"
echo "as (gzipped) <a href=\"grads2ascii.cgi?file=data/$root.ctl\">ascii</a> (big)."

. ./myvinkfoot.cgi
