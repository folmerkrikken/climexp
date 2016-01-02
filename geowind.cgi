#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
# check email address
. ./checkemail.cgi
# off-limits for robots
. ./nosearchengine.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) geowind $FORM_field" >> log/log

# start real work
. ./queryfield.cgi

. ./myvinkhead.cgi "Geostrophic wind" "$kindname $climfield" ""

eval `bin/getunits.sh $file`

if [ -z "$ENSEMBLE" ]; then
  gwest=data/gwest_`basename ${FORM_field}`
  gsouth=data/gsouth_`basename ${FORM_field}`
  vort=data/vort_`basename ${FORM_field}`
  if [ ! \( -s $vort.ctl -a -s $gwest.ctl -a -s $gsouth.ctl \) ]; then
    echo "Computing geostrophic winds...<p>"
    [ -f $vort.ctl ] && rm $vort.???
    [ -f $gsouth.ctl ] && rm $gsouth.???
    [ -f $gwest.ctl ] && rm $gwest.???
    ###echo ./bin/geowind $file $gwest.ctl $gsouth.ctl $vort.ctl
    ./bin/geowind $file $gwest.ctl $gsouth.ctl $vort.ctl
  fi
  if [ \( ! -s $gwest.ctl \) -o \( ! -s $gsouth.ctl \) -o \( ! -s $vort.ctl \) ]; then
    echo "Something went wrong.  Please send the following line to <a href="mailto:oldenborgh@knmi.nl">me</a> and I'll try to fix it."
    echo ./bin/geowind $file $gwest.ctl $gsouth.ctl $vort.ctl
    . ./myvinkfoot.cgi
    exit
  fi
else
  c=`echo $file | fgrep -c '%%%'`
  if [ $c = 1 ]; then
    ss='%%%'
    ensmax=1000
    n=3
  else
    ss='%%'
    ensmax=100
    n=2
  fi
  gwest=data/gwest_${FORM_field}_$ss
  gsouth=data/gsouth_${FORM_field}_$ss
  vort=data/vort_${FORM_field}_$ss
  iens=0
  first=true
  while [ $iens -lt $ensmax ]; do
    ens=`printf %0${n}i $iens`
    ensfile=`echo $file | sed -e "s/\%\%\%/$ens/" -e "s/\+\+\+/$ens/" -e "s/\%\%/$ens/" -e "s/\+\+/$ens/"`
    if [ -s $ensfile ]; then
      if [ -z "$computing" ]; then
        echo "Computing geostrophic winds...<p>"
        computing=done
      fi
      ensgwest=`echo $gwest | sed -e "s/\%\%\%/$ens/" -e "s/\%\%/$ens/"`
      ensgsouth=`echo $gsouth | sed -e "s/\%\%\%/$ens/" -e "s/\%\%/$ens/"`
      ensvort=`echo $vort | sed -e "s/\%\%\%/$ens/" -e "s/\%\%/$ens/"`    
      if [ ! -s $ensvort.ctl ]; then
        [ -f $ensvort.ctl ] && rm $ensvort.???
        [ -f $ensgsouth.ctl ] && rm $ensgsouth.???
        [ -f $ensgwest.ctl ] && rm $ensgwest.???
        ###echo ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl
        ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl > /dev/null
      fi
      if [ \( ! -s $ensgwest.ctl \) -o \( ! -s $ensgsouth.ctl \) -o \( ! -s $ensvort.ctl \) ]; then
        echo "Something went wrong.  Please send the following line to <a href="mailto:oldenborgh@knmi.nl">me</a> and I'll try to fix it.<p>"
        echo ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl
        . ./myvinkfoot.cgi
        exit
      fi
      first=false
    fi
    iens=$((iens + 1))
  done
  if [ $first = true ]; then
    echo "Could not find file $file ($ensfile)"
  fi
fi
cat > $gwest.$EMAIL.info <<EOF
$gwest.ctl
NPERYEAR=$NPERYEAR
$kindname geostrophic wind
Gwest
EOF
echo "<p>Continue with the<ul><li><a href=\"select.cgi?id=$EMAIL&field=$gwest.$EMAIL.info\">zonal component</a>,"

cat > $gsouth.$EMAIL.info <<EOF
$gsouth.ctl
NPERYEAR=$NPERYEAR
$kindname geostrophic wind
Gsouth
EOF
echo "<li><a href=\"select.cgi?id=$EMAIL&field=$gsouth.$EMAIL.info\">meridional component</a>,"

cat > $vort.$EMAIL.info <<EOF
$vort.ctl
NPERYEAR=$NPERYEAR
$kindname geostrophic wind
Vorticity
EOF
echo "<li><a href=\"select.cgi?id=$EMAIL&field=$vort.$EMAIL.info\">vorticity</a>."

echo "</ul><p>The geostrophic wind is defined over 20&deg; longitude &times; 10&deg; latitude rectangles around the grid points."

FORM_field=""

. ./myvinkfoot.cgi

