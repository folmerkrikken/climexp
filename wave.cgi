#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

# to find netpbm on MacOS X
export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
WMO=$FORM_WMO
TYPE=$FORM_TYPE
STATION=$FORM_STATION

# check email address
. ./checkemail.cgi

if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

if [ -n "$EMAIL" -a "$EMAIL" != "someone@somewhere" ]; then
  . ./save_commonoptions.cgi
  cat > ./prefs/$EMAIL.waveoptions.$FORM_NPERYEAR << EOF
FORM_number=$FORM_number;
FORM_type=$FORM_type;
FORM_var=$FORM_var;
FORM_maskout=$FORM_maskout;
FORM_pmin=$FORM_pmin;
FORM_logplot=$FORM_logplot;
FORM_period1=$FORM_period1;
FORM_period2=$FORM_period2;
FORM_cmin=$FORM_cmin;
FORM_cmax=$FORM_cmax;
FORM_shadingtype=$FORM_shadingtype;
FORM_nocbar=$FORM_nocbar;
EOF
fi

CLIM=`echo "$FORM_CLIMATE" | tr '[:upper:]' '[:lower:]'`
station=`echo $FORM_STATION | tr '_' ' '`
# common options
corrargs="$DIR/data/$TYPE$WMO.dat $FORM_type $FORM_param"
n=0
[ -n "$FORM_month" ] && corrargs="$corrargs month $FORM_month"
[ "$FORM_sum" = "1" ] && FORM_sum=""
[ -n "$FORM_sum" ] && corrargs="$corrargs sum $FORM_sum"
[ -n "$FORM_detrend" ] && corrargs="$corrargs detrend"
[ -n "$FORM_diff" ] && corrargs="$corrargs diff"
[ -n "$FORM_ndiff" ] && corrargs="$corrargs diff $FORM_ndiff"
[ -n "$FORM_anom" ] && corrargs="$corrargs anom"
[ -n "$FORM_begin" ] && corrargs="$corrargs begin $FORM_begin"
[ -n "$FORM_end" ] && corrargs="$corrargs end $FORM_end"
[ -n "$FORM_nens1" -o -n "$FORM_nens2" ] && corrargs="$corrargs ens ${FORM_nens1:-0} ${FORM_nens2:-99}"

. ./myvinkhead.cgi "$FORM_type $FORM_param wavelet transform" "$FORM_CLIM $station" "noindex,nofollow"

if [ $EMAIL != someone@somewhere ]; then
  explanation="(to read while waiting for the wavelets)"
  . ./headlines.cgi
fi

echo `date` "$FORM_EMAIL ($REMOTE_ADDR) wave $corrargs" >> log/log
id=$$
root=data/wave${TYPE}${WMO}$id

echo "Computing wavelet transform (using <a href=\"http://paos.colorado.edu/research/wavelets/\" target=\"_top\">wavelet software</a> by C. Torrence and G. Compo)<br>"
if [ -f $root.ctl ]; then
  rm $root.ctl
fi
###echo ./bin/wave $corrargs $root.ctl
(./bin/wave $corrargs $root.ctl > $root.log ) 2>&1

./bin/gnuplot <<EOF
$gnuplot_init
set term png $gnuplot_png_font_hires
set size 0.5,0.5
set out "${root}m.png"
set title "wavelet used"
plot "$root.log" using 1:2 title "real part" w l lt 1, "$root.log" using 1:3 title "imaginary part" w l lt 2
quit
EOF

pngfile=${root}m.png
getpngwidth
cat <<EOF
<div class="bijschrift">$FORM_type $FORM_param wavelet (<a href="$root.log">raw data</a>)</div>
<center><img src="${root}m.png" alt="wavelet" width="$halfwidth"></center>
EOF

if [ -n "$FORM_sum" ]; then
  eval `$DIR/bin/month2string "$FORM_month" "$FORM_sum" 0`
  seriesmonth="$seriesmonth "
fi
title="$FORM_var of $FORM_type $FORM_param wavelet transform\\$seriesmonth$CLIM $station ($WMO)"
if [ -n "$FORM_nens1" -o -n "$FORM_ens2" ]; then
  title="$title ${FORM_nens1}:${FORM_nens2}"
fi
if [ -n "$FORM_end" ]; then
  if [ -n "$FORM_begin" ]; then
    title="$title ${FORM_begin}-${FORM_end}"
  else
    title="$title ending $FORM_end"
  fi
elif [ -n "$FORM_begin" ]; then
  title="$title beginning $FORM_begin"
fi
if [ -n "$FORM_ndiff" ]; then
title="$title ($FORM_ndiff-yr running mean)"
else
if [ -n "$FORM_diff" ]; then
title="$title (diff)"
fi
fi
if [ -n "$FORM_detrend" ]; then
title="$title (detrend)"
fi
if [ -n "$FORM_colourscale" ]; then
  flipcolor=$FORM_colourscale
elif [ -n "$FORM_flipcolor" ]; then
  flipcolor=$FORM_flipcolor
else
  flipcolor=3
fi

# mathematically more correct
plotvar="$FORM_var"
if [ "$FORM_logplot" = "logarithmic" ]; then
  ctlfile=$root.ctl
  ylab="period [yr]"
elif [ "$FORM_logplot" = "linear" ]; then
  if [ $FORM_var = power ]; then
    plotvar="$FORM_var/lev"
  fi
  ctlfile=$root.ctl
  ylab="period [yr]"
else
  if [ $FORM_var = power ]; then
    plotvar="$FORM_var*lev"
  fi
  ctlfile=${root}f.ctl
  ylab="frequency [1/yr]"
  if [ -n "$FORM_period1" ]; then
    a1=$((1/$FORM_period1))
  fi
  if [ -n "$FORM_period2" ]; then
    a2=$((1/$FORM_period2))
  fi
  FORM_period1=$a2
  FORM_period2=$a1
fi
nt=`fgrep TDEF $root.ctl | sed -e 's/TDEF//' -e 's/LIN.*//' -e 's/^ *//'`
nz=`fgrep ZDEF $root.ctl | sed -e 's/ZDEF//' -e 's/LIN.*//' -e 's/^ *//'`
if [ -z "$FORM_nocbar" ]; then
    FORM_cbar=0
else
    FORM_cbar=1
fi
if [ -z "$FORM_maskout" -o "$FORM_maskout" = mask ]; then
    pminarg=${FORM_pmin:-100}
else
    pminarg=${FORM_pmin:-100}:$FORM_maskout
fi

if [ -z "$FORM_period1" ]; then
    if [ "$FORM_mon" = 0 ]; then
	period1=`echo "1/$NPERYEAR" | bc -l`
    else
	period1=1
    fi
else
    period1=$FORM_period1
fi
if [ -z "$FORM_period2" ]; then
    period2=`echo ${FORM_period1}*${nt}/2 | bc -l`
else
    period2=$FORM_period2
fi
if [ -n "$FORM_period1" -o -n "$FORM_period2" ]; then
    setperiods="set lev $period1 $period2"
fi
xylint=0
if [ "$FORM_logplot" = "logarithmic" ]; then
    xylint=log
fi

dano="$setperiods
run danoprob $plotvar 1:$nt $FORM_shadingtype $flipcolor $FORM_cbar $xylint $pminarg $FORM_cmin $FORM_cmax"
if [ "$FORM_logplot" = "logarithmic" ]; then
  dano="set zlog on
$setylevs
$dano"
fi
hiresmap=true
if [ "$hiresmap" = true ]; then
	doublesize="x1804 y1394"
else
	doublesize="x902 y697"
fi
grads=$DIR/bin/grads
config=`$grads -b -l -c quit| fgrep Config`
c=`echo $config | fgrep -c v2.0`
if [ $c -gt 0 ]; then
    grads20=true
    gradsver=2.0
    printeps="print $root.eps"
else
    gradsver=1.8
    printeps="enable print $root.gm
print
disable print"
fi

export GADDIR=$DIR/grads
export UDUNITS_PATH=$DIR/grads/udunits.dat
export HOME=/tmp
$grads -l -b << EOF > /tmp/grads$id.log
open $ctlfile
set xlopts 1 4 0.15
set ylopts 1 4 0.15
set t 1 $nt
set parea 1 10.8 1 7.8
$dano
set gxout contour
set ccolor 1
set cthick 6
set clab off
set clevs 0.5
d coi
draw title $title
draw ylab $ylab
printim $root.png white $doublesize
$printeps
EOF

if [ -z "$grads20" ]; then
    ./bin/gxeps -c -d -i $root.gm
    rm $root.gm
fi
size=`wc -c $root.eps | sed -e 's/data.*//'`
if [ "$size" -lt 5000 ];then
  echo "Something went wrong!"
  echo "<pre>"
  cat /tmp/grads$id.log
  echo "</pre>"
else
  if [ -f /tmp/grads$id.log ]; then
    if [ "$lwrite" = true ]; then
      echo '<pre>'
      cat /tmp/grads$id.log
      echo '</pre>'
    fi
    rm /tmp/grads$id.log
  fi
fi

gzip -f $root.eps &
(pngtopnm $root.png | pnmscale 0.5 | pnmcrop | pnmtopng > $root.new.png ) 2> /dev/null
mv $root.new.png $root.png

cat <<EOF
<div class="bijschrift">Wavelet transform.  
The black line indicates the cone of influence; points outside have been influenced by the boundaries of the time series
(EPS: <a href="$root.eps.gz">colour</a>, 
<a href="makebw.cgi?color=${flipcolor}&file=$root.eps.gz&format=eps">B/W</a>,
PDF: <a href="ps2pdf.cgi?file=$root.eps.gz">colour</a>,
<a href="makebw.cgi?color=${flipcolor}&file=$root.eps.gz&format=pdf">B/W</a>,
data: <a href="grads2nc.cgi?file=$root.ctl&id=$EMAIL">netcdf</a>)</div>
EOF
if [ "$hiresmap" = true ]; then
	pngfile=$root.png
	getpngwidth
	echo "<center><img src=\"$root.png\" alt=\"wavelet\" width=$halfwidth><br clear=all></center>"
else
	echo "<center><img src=\"$root.png\" alt=\"wavelet\"><br clear=all></center>"
fi

. ./myvinkfoot.cgi
