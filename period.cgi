#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_WMO
TYPE=$FORM_TYPE
STATION=$FORM_STATION
NPERYEAR=${FORM_NPERYEAR:-12}

# check email address
. ./checkemail.cgi

CLIM=`echo "$FORM_CLIMATE" | tr '[:upper:]' '[:lower:]'`
station=`echo $FORM_STATION | tr '_' ' '`
c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

# common options
if [ $EMAIL != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.period << EOF
FORM_which=$FORM_which;
FORM_ave=$FORM_ave;
FORM_normplot=$FORM_normplot;
EOF
fi
. ./save_commonoptions.cgi
corrargs="$DIR/data/$TYPE$WMO.dat"
. ./getopts.cgi
[ -n "$FORM_ave" ] && corrargs="$corrargs xave $FORM_ave"
n=0

if [ $FORM_which = 'period' ]; then
  if [ -z "$FORM_ave" -o "$FORM_ave" = 1 ]; then
    . ./myvinkhead.cgi "Periodogram" "$FORM_CLIM $station" "noindex,nofollow"
  else
    . ./myvinkhead.cgi "Spectrum" "$FORM_CLIM $station" "noindex,nofollow"
  fi
else
    . ./myvinkhead.cgi "Autocorrelation function" "$FORM_CLIM $station" "noindex,nofollow"
fi

echo `date` "$FORM_EMAIL ($REMOTE_ADDR) $FORM_which $corrargs" >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
if [ $FORM_which != period ]; then
    a=""
elif [ "$FORM_normplot" = area ]; then
    arg2="(\$1*\$2)"
    arg3="(\$1*\$3)"
    a=a
else
    arg2="2"
    arg3="3"
    a=h
fi
root=data/${FORM_which}${TYPE}${WMO}m${FORM_month}s${FORM_sum}d${FORM_detrend}f${FORM_diff}${FORM_ndiff}a${FORM_anomal}e${FORM_ensanom}$FORM_begin-$FORM_end$FORM_ave

if [ $FORM_which = period ]; then
  echo '<font color=\"#ff2222\">The spectrum routine often produces nonsense results. Please handle with caution...</font><p>'
  if [ ! -s $root.txt ]; then
    echo "Computing spectrum and significances. This may take a while...<p>"
    ###echo "bin/spectrum $corrargs <p>"
    (./bin/spectrum $corrargs > $root.txt) 2>&1 |tee $root.out
    if [ ! -s $root.txt ]; then
      echo "<p>Something went wrong.  Please send the following line to <a href="mailto:oldenborgh@knmi.nl">me</a> and I'll try to fix it."
      echo '<pre>'
      echo spectrum $corrargs
      echo '</pre>'
      . ./myvinkfoot.cgi
      exit
    fi
  else
    cat $root.out
  fi
  if [ ! -s $root$a.png ]; then
    if [ -n "$FORM_sum$FORM_sel" ]; then
      sumstring=$FORM_sel
      . ./month2string.cgi
      seriesmonth="$seriesmonth "
    fi
    if [ -n "$ENSEMBLE" -o -n "$FORM_ave" -a "$FORM_ave" != "1" ]; then
      title="Spectrum of $seriesmonth$CLIM $station ($WMO)"
    else
      title="Periodogram of $seriesmonth$CLIM $station ($WMO)"
    fi
    if [ -n "$ndiff" ]; then
      title="$title ($ndiff-yr running mean)"
    elif [ -n "$FORM_diff" ]; then
      title="$title (diff)"
    fi
    if [ -n "$FORM_detrend" ]; then
      title="$title (detrend)"
    fi
    if [ -s "$startstop" ]; then
      yrstart=`head -1 $startstop`
      yrstop=`tail -1 $startstop`
      rm $startstop
      title="$title ${yrstart}:${yrstop}"
    fi
    timeunits=`fgrep 'frequency in [' $root.txt | sed -e 's/^.*\[//' -e 's/\^..\].*//'`
    xlabel="period [$timeunits]"
    ./bin/gnuplot << EOF
$gnuplot_init
set size 0.7,0.4
set logscale x
set term png $gnuplot_png_font_hires
set output "$root$a.png"
set title "$title"
set xlabel "$xlabel"
set ylabel "power"
plot "$root.txt" u (1/\$1):$arg2 notitle with lines lw 3, "$root.txt" u (1/\$1):$arg3 notitle with lines lw 3 lt 3
set term postscript eps color solid
set output "$root$a.eps"
replot
quit
EOF
  fi
else
  # autocorrelation function requested
  echo "#$DIR/bin/autocor $corrargs" > $root.txt
  (./bin/autocor $corrargs >> $root.txt )2>&1
  echo "The horizontal lines give the 95% significance for a single point in the case of white noise, assuming all measurements are independent."
  if [ -n "$FORM_sum$FORM_month" ]; then
    sumstring=$FORM_sel
    . ./month2string.cgi
    seriesmonth="$seriesmonth "
  fi
  title="Autocorrelation of $seriesmonth$CLIM $station ($WMO)"
  if [ -s "$startstop" ]; then
    yrstart=`head -1 $startstop`
    yrstop=`tail -1 $startstop`
    rm $startstop
    title="$title ${yrstart}:${yrstop}"
  elif [ -n "$FORM_end" ]; then
    if [ -n "$FORM_begin" ]; then
      title="$title ${FORM_begin}-${FORM_end}"
    else
      title="$title ending $FORM_end"
    fi
  elif [ -n "$FORM_begin" ]; then
    title="$title beginning $FORM_begin"
  fi
  if [ -n "$FORM_detrend" ]; then
      title="$title (detrend)"
  fi
  title=`echo $title | tr '_' ' '`
  units=`fgrep '# lag in' $root.txt | cut -b 10-11`
  xlabel="lag [${units}]"
  ./bin/gnuplot << EOF
$gnuplot_init
set size 0.7,0.4
set zeroaxis
set logscale x
set term png $gnuplot_png_font_hires
set output "$root.png"
set title "$title"
set xlabel "$xlabel"
set ylabel "autocorrelation"
plot "$root.txt" notitle with lines lt 1 lw 3, "$root.txt" u 1:4 notitle with lines lt 3, "$root.txt" u 1:(-\$4) notitle with lines lt 3
set term postscript eps color solid
set output "$root.eps"
replot
quit
EOF
fi

gzip -f $root$a.eps
pngfile=$root$a.png
getpngwidth
echo "<div class="bijschrift">$title (<a href=\"$root$a.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=$root$a.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
echo "<center><img src=\"$root$a.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
