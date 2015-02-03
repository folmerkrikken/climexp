#!/bin/sh
n=0
[ -n "$FORM_soi" ] && corrargs="$corrargs soi"        && let n=n+1 && index="$index SOI"
[ -n "$FORM_nino12" ] && corrargs="$corrargs nino12"  && let n=n+1 && index="$index NINO12"
[ -n "$FORM_nino3" ] && corrargs="$corrargs nino3"    && let n=n+1 && index="$index NINO3"
[ -n "$FORM_nino34" ] && corrargs="$corrargs nino3.4" && let n=n+1 && index="$index NINO3.4"
[ -n "$FORM_nino4" ] && corrargs="$corrargs nino4"    && let n=n+1 && index="$index NINO4"
[ -n "$FORM_nao" ] && corrargs="$corrargs nao"        && let n=n+1 && index="$index NAO"
if [ ${NPERYEAR:-12} = 12 ]; then
[ -n "$FORM_co2" ] && corrargs="$corrargs file CDIACData/co2_monthly.dat" \
                                                      && let n=n+1 && index="$index CO2"
[ -n "$FORM_gmst" ] && corrargs="$corrargs file NASAData/giss_al_gl_m.dat" \
                                                      && let n=n+1 && index="$index GMST"
elif [ $NPERYEAR = 1 -o $NPERYEAR = -1 ]; then
[ -n "$FORM_co2" ] && corrargs="$corrargs file CDIACData/co2_annual.dat" \
                                                      && let n=n+1 && index="$index CO2"
[ -n "$FORM_gmst" ] && corrargs="$corrargs file NASAData/giss_al_gl_a_4yrlo.dat" \
                                                      && let n=n+1 && index="$index smoothed_GMST"
fi
[ -n "$FORM_time" ] && corrargs="$corrargs time"      && let n=n+1 && index="$index time"

if [ -n "$EMAIL" -a $EMAIL != someone@somewhere ]; then
  prefs=./prefs/$EMAIL.series.$NPERYEAR
  [ -f $prefs ] && rm $prefs
  touch $prefs
  [ -n "$FORM_soi" ] &&    echo soi    >> $prefs
  [ -n "$FORM_nino12" ] && echo nino12 >> $prefs
  [ -n "$FORM_nino3" ] &&  echo nino3  >> $prefs
  [ -n "$FORM_nino34" ] && echo nino34 >> $prefs
  [ -n "$FORM_nino4" ] &&  echo nino4  >> $prefs
  [ -n "$FORM_nao" ] &&    echo nao    >> $prefs
  [ -n "$FORM_co2" ] &&    echo co2    >> $prefs
  [ -n "$FORM_gmst" ] &&   echo gmst   >> $prefs
  [ -n "$FORM_time" ] &&   echo time   >> $prefs
fi

forbidden='!`;&|'
i=1
varname=FORM_myindex$i
###echo "varname=$varname, var=${!varname} <br>"
while [ $i -lt 500 ]
do
    if [ -n "${!varname}" ]; then
	file=${!varname}
	if [ -n "$EMAIL" -a $EMAIL != someone@somewhere ]; then
	    echo $file >> $prefs
	fi
	datfile=`head -1 $file | tr $forbidden '?'`
###itype=`basename $datfile | cut -b 1`
###case $itype in
###t) iname="temperature";;
###p) iname="precipitation";;
###s) iname="pressure";;
###l) iname="sealevel";;
###r) iname="runoff";;
###c) iname="correlation";;
###*) iname="";;
###esac
	corrargs="$corrargs file $datfile"
	let n=n+1
###index="$index `head -2 $file | tail -1`_$iname"
	index="$index `head -2 $file | tail -1`"
    fi
    i=$(($i+1))
    varname=FORM_myindex$i
    ###echo "varname=$varname, var=${!varname} <br>"
done

if [ $n = 0 ]; then
  n=3
  index="SOI NINO3 NAO"
fi
index=`echo $index`
