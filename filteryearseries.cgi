#!/bin/bash
#
# select a period from a data file

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
# check email address
. ./checkemail.cgi

if [ $EMAIL != someone@somewhere ]; then
    cat > ./prefs/$EMAIL.filteryearoptions <<EOF
FORM_hilo=$FORM_hilo;
FORM_filtertype=$FORM_filtertype;
FORM_nfilter=$FORM_nfilter;
FORM_minfac=$FORM_minfac;
EOF
fi

corrargs="minfac ${FORM_minfac:-75} minfacsum ${FORM_minfac:-75}"

if [ -z "$FORM_field" ]; then
  export WMO="${FORM_wmo}_${FORM_nfilter}yr_${FORM_hilo}_${FORM_filtertype}"
  [ ${FORM_minfac:-75} != 75 ] && WMO=${WMO}_${FORM_minfac}
  STATION="$FORM_station"
  export TYPE=$FORM_type
  NAME=$FORM_name
  export file=`basename $FORM_file`
  PROG="filteryearseries.sh ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $DIR/data/$file $corrargs"
  . $DIR/getdata.cgi
else
  cat <<EOF
Content-type: text/html


EOF
  . ./queryfield.cgi
  . ./myvinkhead.cgi "Computing filtered field" "$kindname $climfield" "noindex,nofollow"
  outfile=`basename $file .ctl`
  outfile=`basename $outfile .nc`
  outfile=data/${outfile}_${FORM_nfilter}yr_${FORM_hilo}_${FORM_filtertype}
  [ -n "$FORM_minfac" -a "$FORM_minfac" != 75 ] outfile=${outfile}_${FORM_minfac}
  if [ -z "$ENSEMBLE" ]; then
    if [ -f $outfile.nc ]; then
	  echo "Field already exists<br>"
    else
      ###echo ./bin/filteryearfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $file $corrargs $outfile.nc
      # note that my routine does not yet produce compressed netcdf4
      tmpfile=data/aap$$.nc
      ./bin/filteryearfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $file $corrargs $tmpfile 2>&1
      cdo -r -f nc4 -z zip copy $tmpfile $outfile.nc
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
        ###echo ./bin/filteryearfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $ensfile $corrargs $ensout.nc
        ./bin/filteryearfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $ensfile $corrargs 
        # note that my routine does not yet produce compressed netcdf4
        tmpfile=data/aap$$.nc
        ./bin/filteryearfield ${FORM_hilo} ${FORM_filtertype} ${FORM_nfilter} $ensfile $corrargs $tmpfile 2>&1
        cdo -r -f nc4 -z zip copy $tmpfile $ensout.nc
      fi
      i=$(($i + 1))
      ii=`printf %02i $i`
      ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
    done    
  fi
  infofile=$outfile.$EMAIL.info
  cat > $infofile <<EOF
$outfile.nc
NPERYEAR=$NPERYEAR
LSMASK=$LSMASK
${kindname} ${FORM_nfilter}yr ${FORM_hilo}
$climfield
EOF
  FORM_field="$infofile"
  . ./select.cgi
fi
