#!/bin/sh
#
# select a period from a data file

export DIR=`pwd`
. ./getargs.cgi

NPERYEAR=$FORM_nperyear
if [ $NPERYEAR = 12 ]; then
  month=month
elif [ $NPERYEAR = 360 -o $NPERYEAR = 365 -o $NPERYEAR = 366 ]; then
  month=day
else
  month=period
fi
. ./checkemail.cgi

if [ $EMAIL != someone@somewhere ]; then
    cat > ./prefs/$EMAIL.filtermonthoptions <<EOF
FORM_hilo=$FORM_hilo;
FORM_filtertype=$FORM_filtertype;
FORM_nfilter=$FORM_nfilter;
FORM_minfac=$FORM_minfac;
EOF
fi

case $NPERYEAR in
    4) yr=s;;
    12) yr=m;;
    36) yr=dec;;
    360|365|366) yr=d;;
    *) yr=;;
esac

corrargs="minfac ${FORM_minfac:-75}"

if [ -z "$FORM_field" ]; then
  export WMO="${FORM_wmo}_${FORM_nfilter}${month}_${FORM_hilo}_${FORM_filtertype}"
  [ ${FORM_minfac:-75} != 75 ] && WMO=${WMO}_${FORM_minfac}
  STATION="$FORM_station"
  export TYPE=$FORM_type
  NAME=$FORM_name
  export file=`basename $FORM_file`
  PROG="filtermonthseries.sh ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $DIR/data/$file $corrargs"
  . $DIR/getdata.cgi
else
  cat <<EOF
Content-type: text/html


EOF
  . ./queryfield.cgi
  . ./myvinkhead.cgi "Computing filtered field" "$kindname $climfield" "noindex,nofollow"
  outfile=`basename $file .ctl`
  outfile=`basename $outfile .nc`
  outfile=data/${outfile}_${FORM_nfilter}${yr}_${FORM_hilo}_${FORM_filtertype}
  [ -n "$FORM_minfac" -a "$FORM_minfac" != 75 ] && outfile=${outfile}_${FORM_minfac}
  if [ -z "$ENSEMBLE" ]; then
    if [ -f $outfile.ctl -a $outfile.ctl -nt $file ]; then
	  echo "Field already exists<br>"
    else
      [ -f $outfile.ctl ] && rm $outfile.???
      ###echo ./bin/filtermonthfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $file $corrargs $outfile.ctl
      ./bin/filtermonthfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $file $corrargs $outfile.ctl 2>& 1
    fi
  else
    i=0
    ii=00
    ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
    while [ $i -lt 100 ]
    do
      if [ -f $ensfile -o -f data/$ensfile ]
      then
        ensout=`echo $outfile | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
        if [ ! -s $ensout.ctl -o $ensout.ctl -ot $ensefile ]; then
          [ -f $ensout.ctl ] && rm $ensout.???
          ###echo ./bin/filtermonthfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $ensfile $corrargs $ensout.ctl
          ./bin/filtermonthfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $ensfile $corrargs $ensout.ctl 2>&1
        fi
      fi
      i=$(($i + 1))
      ii=`printf %02i $i`
      ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
    done    
  fi
  infofile=$outfile.$EMAIL.info
  cat > $infofile <<EOF
$outfile.ctl
NPERYEAR=$NPERYEAR
LSMASK=$LSMASK
${kindname} ${FORM_nfilter}${yr} ${FORM_hilo}
$climfield
EOF
  FORM_field="$infofile"
  . ./select.cgi
fi
