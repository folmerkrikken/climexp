#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR

if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false
fi

# check email address
. ./checkemail.cgi

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  . ./save_commonoptions.cgi
  cat > ./prefs/$EMAIL.runningmoments.$NPERYEAR <<EOF
FORM_moment=$FORM_moment;
FORM_runwindow=$FORM_runwindow;
FORM_minnum=$FORM_minnum;
EOF
fi

CLIM=$FORM_CLIMATE
STATION="$FORM_STATION"
station=`echo $FORM_STATION | tr '_' ' '`
if [ "$FORM_moment" = "all" ]
then
   moments="mean sd skew curtosis"
else
   moments="$FORM_moment"
fi
n=0
FORM_num=$$

. ./myvinkhead.cgi "Running $moments" "$station $NAME" "noindex,nofollow"

for FORM_moment in $moments
do

corrargs="$DIR/data/$TYPE$WMO.dat $FORM_moment"
. ./getopts.cgi
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) runningmoments $corrargs" | sed -e "s@$DIR/@@g" >> log/log
if [ -z "$FORM_separate" ]; then
  root=`echo data/running${FORM_moment}_$TYPE${WMO}_$$ | sed -e 's/++/__/'`
  if [ "$lwrite" = true ]; then
      echo ./bin/runningmoments $corrargs
      corrargs="$corrargs debug"
      echo '<pre>'
      ( ./bin/runningmoments $corrargs > /tmp/runningmoments$$.lo1 ) 2>&1 && true
      cat /tmp/runningmoments$$.lo1
      sed -e 's/# *//' /tmp/runningmoments$$.lo1 > /tmp/runningmoments$$.log
      rm /tmp/runningmoments$$.lo1
      echo '</pre>'
  else
      ( ./bin/runningmoments $corrargs | sed -e 's/# *//' > /tmp/runningmoments$$.log ) 2>&1 && true
      tail -n +2 /tmp/runningmoments$$.log
  fi
  rm /tmp/runningmoments$$.log
  mv data/$TYPE$WMO${FORM_num}.runcor $root.txt
  egrep '^#' $root.txt | sed -e 's/# *//'
  mean=`egrep '^#' $root.txt | fgrep '<td>' |  cut -b 24-43`
  ###echo "mean = $mean"
  lowerr=`egrep '^#' $root.txt | fgrep '<td>' |  cut -b 53-72`
  ###echo "lowerr = $lowerr"
  higherr=`egrep '^#' $root.txt | fgrep '<td>' |  cut -b 76-95`
  ###echo "higherr = $higherr"
else # treat all ensemble members separately
  root=data/running${FORM_moment}_$TYPE${WMO}_$$
  touch $root.txt
  iens=0
  touch /tmp/runningmoments$$.log
  while [ $iens -lt 100 ]
  do
    if [ $iens -lt 10 ]; then
      ens=0$iens
    else
      ens=$iens
    fi
    iens=$((iens + 1))
    list=( $corrargs )
    file=${list[0]}
    ensfile=`echo $file | sed -e "s/++/$ens/"`
    enscorrargs=`echo $corrargs | sed -e "s/++/$ens/"`
    if [ -f $ensfile ]; then
      echo "# ensemble member $ens" >> $root.txt
      [ "$lwrite" = true ] && echo bin/runningmoments $enscorrargs
      ($DIR/bin/runningmoments $enscorrargs | sed -e 's/# *//' >> /tmp/runningmoments$$.log) 2>&1 && true
      cat data/$TYPE$WMO${FORM_num}.runcor >> $root.txt
      rm data/$TYPE$WMO${FORM_num}.runcor
      echo >> $root.txt
      echo '<p>'
    fi
  done
  tail -n +2 /tmp/runningmoments$$.log
  rm /tmp/runningmoments$$.log
fi

. $DIR/setyaxis.cgi
[ -n "$FORM_log" ] && ylabel="log $ylabel"
[ -n "$FORM_sqrt" ] && ylabel="sqrt $ylabel"
[ -n "$FORM_square" ] && ylabel="${ylabel}^2"
ylabel="$FORM_moment $ylabel"

if [ -n "$FORM_sum" ]; then
  eval `$DIR/bin/month2string "$FORM_month" "$FORM_sum" 0`
  seriesmonth="$seriesmonth "
  ylabel="$seriesmonth $ylabel"
fi

title="Running $FORM_moment of $seriesmonth$CLIM $station ($WMO)"
if [ -n "$ndiff" ]; then
  title="$title ($ndiff-yr running mean)"
else
  if [ -n "$FORM_diff" ]; then
    title="$title (diff)"
  fi
fi
if [ -n "$FORM_detrend" ]; then
  title="$title (detrend)"
fi

$DIR/bin/gnuplot << EOF
set size 0.7,.4
set term png $gnuplot_png_font_hires
set output "$root.png"
set title "$title"
set xzeroaxis
set ylabel "$ylabel"
plot "$root.txt" u 1:2 notitle with lines lw 4, "$root.txt" u 1:3 title "2.5%" with lines lt 2 lw 1, "$root.txt" u 1:7 title "97.5%" with lines lt 2 lw 1
#, $mean notitle w l lt 3 lw 4, $lowerr notitle w l lt 2 lw 1, $higherr notitle lt 2 lw 1
set term postscript epsf color solid
set output "$root.eps"
replot
quit
EOF
gzip -f $root.eps
pngfile=$root.png
getpngwidth
echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>, "
echo "<a href=\"txt2dat.cgi?id=$EMAIL&WMO="`echo $root.txt | sed -e 's/++/@@/'`"&STATION=running_${FORM_moment}_of_$FORM_STATION\">analyze as time series</a>)</div>"
echo "<center><img src=\"${root}.png\" alt=\"$FORM_moment\" width=\"$halfwidth\"></center>"

done
. ./myvinkfoot.cgi
