#!/bin/sh
echo 'Content-Type: text/html'
. ./expires.cgi
echo
echo

export DIR=`pwd`
. ./getargs.cgi
[ "$EMAIL" = oldenbor@knmi.nl ] && lwrite=false # true

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

if [ $EMAIL != someone@somewhere ]; then
  . ./save_commonoptions.cgi
  cat > ./prefs/$EMAIL.svds <<EOF
FORM_nsvd=$FORM_nsvd;
FORM_normsd=$FORM_normsd;
FORM_avex=$FORM_avex;
FORM_avey=$FORM_avey;
FORM_minfac=$FORM_minfac;
FORM_normalization=$FORM_normalization;
EOF
fi

. ./myvinkhead.cgi "Compute $FORM_nsvd SVDs" "$kindname1 $climfield1 with $kindname2 $climfield2" "noindex,nofollow"

corrargs="$FORM_nsvd"
. $DIR/getopts.cgi
# lat[12], lon[12] are also job args here
[ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
[ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
[ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
[ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"
[ -n "$FORM_altlon1" ] && corrargs="$corrargs altlon1 $FORM_altlon1"
[ -n "$FORM_altlon2" ] && corrargs="$corrargs altlon2 $FORM_altlon2"
[ -n "$FORM_altlat1" ] && corrargs="$corrargs altlat1 $FORM_altlat1"
[ -n "$FORM_altlat2" ] && corrargs="$corrargs altlat2 $FORM_altlat2"
[ -n "$FORM_avex" ] && corrargs="$corrargs xave $FORM_avex"
[ -n "$FORM_avey" ] && corrargs="$corrargs yave $FORM_avey"
# adapt name if normalized to sd
[ -n "$FORM_normsd" ] && climfield="$climfield / s.d."
. $DIR/getfieldopts.cgi

if [ $EMAIL != someone@somewhere ]; then
  explanation="(to read while waiting for the SVDs)"
  . ./headlines.cgi
fi

echo `date` "$EMAIL ($REMOTE_ADDR) svd $field1 $field2 $corrargs" | sed -e "s:$DIR/::g"  >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"

echo "Computing SVDs.  This will take (quite) a while...<br>"
echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the SVD job)</small><p>"
# generate GrADS data file
cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
svd $FORM_field $corrargs
@
EOF
export SCRIPTPID=$$
export FORM_EMAIL=$EMAIL
( (echo bin/svd $file1 $file2 $corrargs data/svd1_$$.ctl data/svd2_$$.ctl; $DIR/bin/svd $file1 $file2 $corrargs data/svd1_$$.ctl  data/svd2_$$.ctl) > /tmp/svd$$.log ) 2>&1
rm pid/$$.$EMAIL
if [ ! \( -s data/svd1_$$.grd -a -s  data/svd2_$$.grd \) ]; then
  cat $DIR/wrong.html
  echo "<pre>"
  cat /tmp/svd$$.log
  rm /tmp/svd$$.log
  echo "</pre>"
  echo "</body></html>"
  exit
else
  rm /tmp/svd$$.log
fi

# plot data

  # left eigenvector
isvd=0
while [ $isvd -lt ${FORM_nsvd:-4} ]
do
  isvd=$(($isvd+1))
  id=${$}_${isvd}_l
  if [ $isvd -lt ${FORM_nsvd:-4} ]; then
    insideloop=true
  else
    insideloop=""
  fi
  if [ $isvd -lt 10 ]; then
    iisvd=0$isvd
  else
    iisvd=$isvd
  fi
  FORM_var=svd$iisvd
  if [ -s data/svd1_${$}_$iisvd.dat ]; then
    ext=$iisvd
  elif [ -n "$ENSEMBLE" ]; then
    ext="${iisvd}_%%"
  else
    echo "Something went wrong, cannot find data/svd1_${$}_$iisvd*<br>"
    ext=$iisvd    
  fi
  file=data/svd1_$$.ctl
  station=$kindname1
  CLIM=$climfield1
  pcname=`echo "PC$isvd of $kindname1 $climfield1" | tr " " "_"`
  [ "$lwrite" = true ] && echo "pcname=$pcname<br>"
  extra1="<br><a href=\"getindices.cgi?WMO=data/svd1_${$}_${ext}&STATION=$pcname&TYPE=i&id=$EMAIL\">Principal component PC$isvd</a><br><a href=\"patternfield.cgi?id=$EMAIL&patfile=svd1_$$.ctl&variable=svd$iisvd&month="
  # here the month will be added be grads.cgi
  extra2="&field=$field1\">project svd1_$isvd on the same field</a>, "
  extra3="<a href=\"patternfieldform.cgi?id=$EMAIL&patfile=svd1_$$.ctl&variable=svd$iisvd&month="
  # here the month will be added by grads.cgi
  extra4="&field=$field1\">project svd1_$isvd on another field</a><br>"
  if [ "$lwrite" = true ]; then
  	echo "<pre>"
  	echo "extra1=$extra1"
  	echo "extra2=$extra2"
  	echo "extra3=$extra3"
  	echo "extra4=$extra4"
  	echo "</pre>"
  fi
  . ./grads.cgi
  dano=''
done

# right eigenvector
if [ $FORM_month != "1:12" -a $FORM_month != 0 ]; then
    firstmonth=`echo ${FORM_month:-1:12} | sed -e 's/\:.*//'`
    lastmonth=`echo ${FORM_month:-1:12} | sed -e 's/.*\://'`
    firstmonth=$((firstmonth - (FORM_lag)))
    lastmonth=$((lastmonth - (FORM_lag)))
    while [ $firstmonth -gt $NPERYEAR ]; do
		firstmonth=$((firstmonth - NPERYEAR))
		lastmonth=$((lastmonth - NPERYEAR))
    done
    FORM_month=${firstmonth}:${lastmonth}
fi
if [ -n "$FORM_sum2" -a "$FORM_sum2" != "$FORM_sum" ]; then
    sumstring=${FORM_sum2}:${FORM_sum:-1}
fi
save_lon1=$FORM_lon1
save_lon2=$FORM_lon2
save_lat1=$FORM_lat1
save_lat2=$FORM_lat2
FORM_lon1=$FORM_altlon1
FORM_lon2=$FORM_altlon2
FORM_lat1=$FORM_altlat1
FORM_lat2=$FORM_altlat2
. ./getfieldopts.cgi
FORM_lon1=$save_lon1
FORM_lon2=$save_lon2
FORM_lat1=$save_lat1
FORM_lat2=$save_lat2
isvd=0
while [ $isvd -lt ${FORM_nsvd:-4} ]
do
  isvd=$(($isvd+1))
  id=${$}_${isvd}_r
  if [ $isvd -lt ${FORM_nsvd:-4} ]; then
    insideloop=true
  else
    insideloop=""
  fi
  if [ $isvd -lt 10 ]; then
    iisvd=0$isvd
  else
    iisvd=$isvd
  fi
  FORM_var=svd$iisvd
  if [ -s data/svd2_${$}_$iisvd.dat ]; then
    ext=$iisvd
  elif [ -n "$ENSEMBLE" ]; then
    ext="${iisvd}_%%"
  else
    echo "Something went wrong, cannot find data/svd2_${$}_$iisvd*<br>"
    ext=$iisvd
  fi
  file=data/svd2_$$.ctl
  station=$kindname2
  CLIM=$climfield2
  pcname=`echo "PC$isvd of $kindname2 $climfield2" | tr " " "_"`
  [ "$lwrite" = true ] && echo "pcname=$pcname<br>"
  extra1="<br><a href=\"getindices.cgi?WMO=data/svd2_${$}_${ext}&STATION=$pcname&TYPE=i&id=$EMAIL\">Principal component PC$isvd</a><br><a href=\"patternfield.cgi?id=$EMAIL&patfile=svd2_$$.ctl&variable=svd$iisvd&month="
  # here the month will be added be grads.cgi
  extra2="&field=$field2\">project svd2_$isvd on the same field</a>, "
  extra3="<a href=\"patternfieldform.cgi?id=$EMAIL&patfile=svd2_$$.ctl&variable=svd$iisvd&month="
  # here the month will be added be grads.cgi
  extra4="&field=$field2\">project svd2_$isvd on another field</a><br>"
  if [ "$lwrite" = true ]; then
  	echo "<pre>"
  	echo "extra1=$extra1"
  	echo "extra2=$extra2"
  	echo "extra3=$extra3"
  	echo "extra4=$extra4"
  	echo "</pre>"
  fi
  . ./grads.cgi
  dano=''
done
#
# let the user download the raw data
#
echo "<p>"
gzip -c data/svd1_$$.grd > data/svd1_$$.grd.gz &
gzip -c data/svd2_$$.grd > data/svd2_$$.grd.gz &
echo "Get the SVD map(s) of $kiname1 $climfield1 as GrADS <a href=\"data/svd1_$$.ctl\">ctl</a>"
echo "and (gzipped) <a href=\"data/svd1_$$.grd.gz\">dat</a> files,"
echo "as a (gzipped) <a href=\"grads2nc.cgi?file=data/svd1_$$.ctl&id=$EMAIL&title=SVDs of ${kindname1} ${climfield1} with ${kindname2} ${climfield2}\">netCDF</a> file,"
echo "as (gzipped) <a href=\"grads2ascii.cgi?file=data/svd1_$$.ctl&id=$EMAIL&title=SVDs of ${kindname1} ${climfield1} with ${kindname2} ${climfield2}\">ascii</a> (big)."
echo "Get the SVD map(s) of $kiname2 $climfield2 as GrADS <a href=\"data/svd2_$$.ctl\">ctl</a>"
echo "and (gzipped) <a href=\"data/svd2_$$.grd.gz\">dat</a> files,"
echo "as a (gzipped) <a href=\"grads2nc.cgi?file=data/svd2_$$.ctl&id=$EMAIL&title=SVDs of ${kindname1} ${climfield1} with ${kindname2} ${climfield2}\">netCDF</a> file,"
echo "as (gzipped) <a href=\"grads2ascii.cgi?file=data/svd2_$$.ctl&id=$EMAIL&title=SVDs of ${kindname1} ${climfield1} with ${kindname2} ${climfield2}\">ascii</a> (big)."

. ./myvinkfoot.cgi
