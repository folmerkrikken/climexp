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
    echo "Something went wrong.  Please send the following line to <a href="http://www.knmi.nl/~oldenbor/">me</a> and I'll try to fix it."
    echo ./bin/geowind $file $gwest.ctl $gsouth.ctl $vort.ctl
    . ./myvinkfoot.cgi
    exit
  fi
else
  gwest=data/gwest_${FORM_field}_%%
  gsouth=data/gsouth_${FORM_field}_%%
  vort=data/vort_${FORM_field}_%%
  iens=0
  while [ $iens -lt 100 ]; do
    if [ $iens -lt 10 ]; then
      ens=0$iens
    else
      ens=$iens
    fi
    ensfile=`echo $file | sed -e "s/\%\%/$ens/" -e "s/\+\+/$ens/"`
    if [ -s $ensfile ]; then
      if [ -z "$computing" ]; then
        echo "Computing geostrophic winds...<p>"
        computing=done
      fi
      ensgwest=`echo $gwest | sed -e "s/\%\%/$ens/"`
      ensgsouth=`echo $gsouth | sed -e "s/\%\%/$ens/"`
      ensvort=`echo $vort | sed -e "s/\%\%/$ens/"`    
      if [ ! -s $ensvort.ctl ]; then
        echo "$iens"
        [ -f $ensvort.ctl ] && rm $ensvort.???
        [ -f $ensgsouth.ctl ] && rm $ensgsouth.???
        [ -f $ensgwest.ctl ] && rm $ensgwest.???
        ###echo ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl
        ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl > /dev/null
      fi
      if [ \( ! -s $ensgwest.ctl \) -o \( ! -s $ensgsouth.ctl \) -o \( ! -s $ensvort.ctl \) ]; then
        echo "Something went wrong.  Please send the following line to <a href="http://www.knmi.nl/~oldenbor/">me</a> and I'll try to fix it.<p>"
        echo ./bin/geowind $ensfile $ensgwest.ctl $ensgsouth.ctl $ensvort.ctl
        . ./myvinkfoot.cgi
        exit
      fi
    fi
    iens=$((iens + 1))
  done
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

