#!/bin/sh
echo 'Content-Type: text/html'
echo

export DIR=`pwd`
. ./getargs.cgi
###echo '<pre>'
###set | fgrep FORM_
###echo '</pre>'
###exit
STATION=$FORM_STATION
WMO=$FORM_WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
FORM_num=$$

lwrite=false
[ "$EMAIL" = oldenbor@knmi.nl ] && lwrite=false

# check email address
. ./checkemail.cgi

# real work
. ./save_commonoptions.cgi
. ./save_variable.cgi

CLIM=`echo "$FORM_CLIMATE" | tr '[:upper:]' '[:lower:]'`
station=`echo $STATION | tr '_%' ' +'`
NAME=$FORM_NAME
# common options
sfile="$DIR/data/$TYPE$WMO.dat"
corrargs=$sfile
c1=`echo $WMO | fgrep -c "++"`
c2=`echo $WMO | fgrep -c "%%"`
[ $c1 != 0 -o $c2 != 0 ] && ENSEMBLE=true
. ./getopts.cgi
if [ 0 = 1 ]; then
    echo "WMO,c1,2 = $WMO,$c1,$c2<br>"
    echo "FORM_nens1,2 = $FORM_nens1,$FORM_nens2<br>"
    echo "corrargs = $corrargs<br>"
fi
# field?
if [ ${FORM_field:-none} != none ]; then
    . $DIR/correlatefield.cgi
  exit
fi
# no field...
. ./getuserindex.cgi
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs bootstrap startstop $startstop"

echo `date` "$EMAIL ($REMOTE_ADDR) correlate $corrargs" | sed -e  "s:$DIR/::g" >> log/log
corrargs="$corrargs plot $DIR/data/$TYPE$WMO${FORM_num}.cor dump $DIR/data/$TYPE$WMO${FORM_num}.dump"
. ./myvinkhead.cgi "Time series correlations" "$CLIM $station with $index" "noindex,nofollow"

if [ -n "$FORM_runcorr" -a -n "$FORM_runwindow" ]; then
	if [ -n "$FORM_minnum" -a "$FORM_minnum" -gt $FORM_runwindow ]; then
		echo "Warning: you requested a minimum number of points ($FORM_minnum) that is higher then the running correlation window length ($FORM_runwindow). Adjusted it to be the same.<p>"
		FORM_minnum=$FORM_runwindow
		corrargs="$corrargs minnum $FORM_minnum"
	fi
echo "Computing running $FORM_runvar and its significance with a Monte Carlo.  This may take a while<p>"
fi
corrroot=$DIR/data/$TYPE${WMO}corr${FORM_num}
[ "$lwrite" = true ] && echo "correlate $corrargs <p>"
./bin/correlate $corrargs
if [ -s "$startstop" ]; then
  yrstart=`head -1 $startstop`
  yrstop=`tail -1 $startstop`
  rm $startstop
fi

. $DIR/setyaxis.cgi

if [ -z "$FORM_conting" ]; then
  if [ -n "$FORM_dgt" ]; then
    if [ -n "$FORM_dlt" ]; then
      title="$station ($FORM_dgt < $CLIM < $FORM_dlt) vs $index"
    else
      title="$station ($FORM_dgt < $CLIM) vs $index"
    fi
  elif [ -n "$FORM_dlt" ]; then
    title="$station ($CLIM < $FORM_dlt) vs $index"
  else
    title="$station $CLIM vs $index"
  fi
  if [ -n "$FORM_gt" ]; then
    if [ -n "$FORM_lt" ]; then
      title="$title ($FORM_gt < $index < $FORM_lt)"
    else
      title="$title ($FORM_gt < $index)"
    fi
  elif [ -n "$FORM_lt" ]; then
    title="$title ($index < $FORM_lt)"
  fi
else
  title="$station $CLIM vs $index"
fi

if [ -n "$yrstart" ]; then
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

if [ -n "$ndiff" ]; then
  if [ -n "$ndiff2" ]; then
    title="$title ($ndiff2-yr, $ndiff-yr running means)"
  else
    title="$title ($ndiff-yr running mean)"
  fi
else
  if [ -n "$ndiff2" ]; then
    title="$title ($ndiff2-yr running mean)"
  fi
  if [ -n "$FORM_diff" ]; then
    title="$title (diff)"
  fi
fi
if [ -n "$FORM_detrend" ]; then
  title="$title (detrend)"
fi
if [ -n "$FORM_ensanom" ]; then
  title="$title (anomalies wrt ensemble mean)"
fi

correlation="correlation"
[ "$FORM_whichvar" = regr ] && correlation=regression
[ -n "$FORM_runcorr" -a -n "$FORM_runwindow" ] && correlation="$FORM_runvar"
[ -n "$FORM_rank" ] && correlation="rank $correlation"
corr=`echo $correlation | cut -b 1-4`

if [ -n "$FORM_xlo" -o -n "$FORM_xhi" ]; then
  xrange="set xrange [${FORM_xlo}:${FORM_xhi}]"
fi
if [ -n "$FORM_ylo" -o -n "$FORM_yhi" ]; then
  yrange="set yrange [${FORM_ylo}:${FORM_yhi}]"
fi

if [ -n "$FORM_runcorr" -a -n "$FORM_runwindow" ]; then
  if [ -n "$FORM_lag" -a "$FORM_lag" != 0 ]; then
    echo "</table>"
    ###echo "Error: cannot handle lagged running correlations/regressions yet"
    . ./myvinkfoot.cgi
    exit
  fi
  # plot the running correlations
  $DIR/bin/gnuplot <<EOF
set size 0.7,0.5
set zeroaxis
$xrange
$yrange
set term postscript epsf color solid
set output "${corrroot}_runcor.eps"
set title "$title"
set ylabel "$correlation"
plot "$DIR/data/$TYPE$WMO${FORM_num}.runcor" using 1:3 title "${FORM_runwindow}-yr $corr" with lines lt 1, \
     "$DIR/data/$TYPE$WMO${FORM_num}.runcor" using 1:5 title " 2.5%" with lines lt 2, \
     "$DIR/data/$TYPE$WMO${FORM_num}.runcor" using 1:9 title "97.5%" with lines lt 2
set term png $gnuplot_png_font_hires
set output "${corrroot}_runcor.png"
replot
EOF
  gzip ${corrroot}_runcor.eps &
  pngfile=data/$TYPE${WMO}corr${FORM_num}_runcor.png
  getpngwidth
  cat <<EOF
<p>The global significance of the minimum, maximum and difference
against a straight line plus white noise is given above.  The 95%
confidence interval in the plot below is local.
<div class="bijschrift">Running $FORM_runvar of $title (<a href="data/$TYPE${WMO}corr${FORM_num}_runcor.eps.gz">eps</a>, <a href="ps2pdf.cgi?file=data/$TYPE${WMO}corr${FORM_num}_runcor.eps.gz">pdf</a>,
<a href="data/$TYPE${WMO}${FORM_num}.runcor">raw data</a>)</div>
<center>
<img src="data/$TYPE${WMO}corr${FORM_num}_runcor.png" width="$halfwidth" alt="Running $FORM_runvar of $title">
<br clear=all>
</center>
EOF
fi

# is it a lag-correlation plot?
tmp=`echo $FORM_lag | fgrep ':'`
if [ -z "$tmp" ]; then
  [ "$lwrite" = true ] && echo "No range of lags"

  if [ ${FORM_lag:-0} -gt 0 ]; then
    title="$title lag $FORM_lag ($index leading)"
  elif [ ${FORM_lag:-0} -lt 0 ]; then
    title="$title lag $FORM_lag ($CLIM leading)"
  fi

# one month?
  tmp=`echo $FORM_month | fgrep ':'`
  if [ "$NPERYEAR" -gt 1 -a \( -z "$FORM_month" -o -n "$tmp" \) ]; then
# two or fewer indices?
    if [ $n -le 2 ]; then

      if [ "$FORM_fix" = "fix2" ]; then
        echo "<div class=\"alineakop\">Yearly cycle of $index correlated with $CLIM $station ($WMO)</div>"
      else
        echo "<div class=\"alineakop\">Yearly cycle of $CLIM $station ($WMO)</div>"
      fi
      echo "If present, the band around the correlations indicates the 95% confidence limits."
      $DIR/bin/extendyear < $DIR/data/$TYPE$WMO${FORM_num}.cor > $DIR/data/$TYPE$WMO${FORM_num}.corr
      for ext in eps png 
      do
        if [ $ext = eps ];then
          term="postscript epsf color solid"
        elif [ $ext = png ]; then
          term="png $gnuplot_png_font_hires"
        else
          term=weetikniet
        fi

        if [ -n "$FORM_sum" ];then
          xlabel="first month of ${FORM_sum}-month season"
        else
          xlabel="month"
        fi
	if [ "$FORM_fix" = "fix2" ]; then
	  xlabel="$xlabel $index"
	fi
	if [ -z "$FORM_conting" ]; then
	  prob1="index 0 using 1:4"
          if [ $n -eq 1 ]; then
            prob2="index 0 using 1:4"
          else
	    prob2="index 1 using 1:4"
          fi
	  if [ "$FORM_whichvar" = regr ]; then
	      corr1="using 1:15"
	      corr2="using 1:(\$15-2*\$16)"
	      corr3="using 1:(\$15+2*\$16)"
	  else
	      corr1="using 1:3"
	      corr2="using 1:10"
	      corr3="using 1:14"
	  fi
          yformat="%5.2f"
	  if [ -n "$FORM_rank" ]; then
	    mean="median"
	    sd="IQR"
	  else
	    mean="mean"
	    sd="s.d."
	  fi
	  if [ -n "$FORM_log" ]; then
	    if [ "$FORM_fix" = "fix2" ]; then
	      [ $ext = png ] && [ -z "FORM_rank" ] && echo "Note that the mean and s.d. have been recomputed from the mean and s.d. of the logarithms of $index"
	      clim1="using 1:(10**\$8) title \"$mean $index\""
	      clim2="using 1:(2.302585*10**\$8*\$9) title \"sd $index\""
	    else
	      [ $ext = png ] && [ -z "FORM_rank" ] && echo "Note that the mean and s.d. have been recomputed from the mean and s.d. of the logarithms of $CLIM"
              clim1="using 1:(10**\$6) title \"$mean $CLIM\""
	      clim2="using 1:(2.302585*10**\$6*\$7) title \"$sd $CLIM\""
	    fi
	  elif [ -n "$FORM_sqrt" ]; then
	    if [ "$FORM_fix" = "fix2" ]; then
	      [ $ext = png ] && [ -z "FORM_rank" ] && echo "Note that the mean and s.d. have been recomputed from the mean and s.d. of the sqrt of $index"
	      clim1="using 1:(\$8**2) title \"$mean $index\""
	      clim2="using 1:(2*\$8*\$9) title \"$sd $index\""
	    else
	      [ $ext = png ] && [ -z "FORM_rank" ] && echo "Note that the mean and s.d. have been recomputed from the mean and s.d. of the sqrt of $CLIM"
              clim1="using 1:(\$6**2) title \"$mean $CLIM\""
	      clim2="using 1:(2*\$6*\$7) title \"$sd $CLIM\""
	    fi
	  else
	    if [ "$FORM_fix" = "fix2" ]; then
	      clim1="using 1:8 title \"$mean $index\""
	      clim2="using 1:9 title \"$sd $index\""
	    else
              clim1="using 1:6 title \"$mean $CLIM\""
	      clim2="using 1:7 title \"$sd $CLIM\""
	    fi
	  fi
        else
	  prob1="using 1:3"
	  prob2="using 1:3"
	  corr1='using 1:($9+$19)'
	  corr2='using 1:($11+$17)'
	  corr3='index 0 using 1:($11+$17)'
          correlation="(<<)+(>>), (<>)+(><)"
          yformat="%5.0f"
	  if [ -n "$FORM_log" ]; then
	    if [ "$FORM_fix" = "fix2" ]; then
	      clim1="using 1:(10**\$22) title \"cut1 $index\""
	      clim2="using 1:(10**\$23) title \"cut2 $index\""
	    else
	      clim1="using 1:(10**\$20) title \"cut1 $index\""
	      clim2="using 1:(10**\$21) title \"cut2 $index\""
	    fi
	  elif [ -n "$FORM_sqrt" ]; then
	    if [ "$FORM_fix" = "fix2" ]; then
	      clim1="using 1:(\$22**2) title \"cut1 $index\""
	      clim2="using 1:(\$23**2) title \"cut2 $index\""
	    else
	      clim1="using 1:(\$20**2) title \"cut1 $index\""
	      clim2="using 1:(\$21**2) title \"cut2 $index\""
	    fi
	  else
            if [ "$FORM_fix" = "fix2" ]; then
              clim1="using 1:22 title \"cut1 $index\""
	      clim2="using 1:23 title \"cut2 $index\""
	    else
              clim1="using 1:20 title \"cut1 $CLIM\""
	      clim2="using 1:21 title \"cut2 $CLIM\""
	    fi
          fi
	fi

        $DIR/bin/gnuplot << EOF
set size 0.7,1
set zeroaxis
set xrange [1:24]
set xtics ("All year" -0.5, "J" 1, "F" 2, "M" 3, "A" 4, "M" 5, "J" 6, "J" 7, "A" 8, "S" 9, "O" 10, "N" 11, "D" 12, "J" 13, "F" 14, "M" 15, "A" 16, "M" 17, "J" 18, "J" 19, "A" 20, "S" 21, "O" 22, "N" 23, "D" 24)
set term $term
set output "$corrroot.$ext"
set multiplot
set size 0.7,0.30
set origin 0,0.70
set log y
set ylabel 'probability'
set zero 1e-40
set format y "%5.0e"
set title "$title"
plot "data/$TYPE$WMO${FORM_num}.corr" $prob1 notitle with lines,\
     "data/$TYPE$WMO${FORM_num}.corr" $prob2 notitle with lines
set nolog y
set origin 0,0.40
set title
set ylabel "$correlation"
$yrange
set format y "$yformat"
plot "data/$TYPE$WMO${FORM_num}.corr" $corr1 notitle with lines lt 1 lw 2,\
     "data/$TYPE$WMO${FORM_num}.corr" $corr2 notitle with lines lt 2,\
     "data/$TYPE$WMO${FORM_num}.corr" $corr3 notitle with lines lt 2
set size 0.7,.4
set origin 0,0.00
set xlabel "$xlabel"
$setyrange
$setformaty
set ylabel "$ylabel"
plot "data/$TYPE$WMO${FORM_num}.corr" $clim1 with lines,\
     "data/$TYPE$WMO${FORM_num}.corr" $clim2 with lines
set nomultiplot
EOF
      done
    fi
    [ "$lwrite" = true ] && echo "n = $n, FORM_sum = $FORM_sum, FORM_sum2 = $FORM_sum2"
    if [ $n -le 1 -a -z "$FORM_sum" -a -z "$FORM_sum2" ]; then
      a=`awk '{print -$15}' $DIR/data/$TYPE$WMO${FORM_num}.cor | tr '\n' ':'`
      if [ ! -s $DIR/data/dummy.$NPERYEAR.dat ]; then
	$DIR/bin/gen_time 1700 2200 $NPERYEAR > $DIR/data/dummy.$NPERYEAR.dat
      fi
      if [ -n "$FORM_soi" -o -n "$FORM_nao" -o -n "$FORM_nino12" -o -n "$FORM_nino3" -o -n "$FORM_nino4" -o -n "$FORM_nino34" -o -n "$FORM_time" ]; then
        a1=$a
        a2=1
      else
        a1=1
        a2=$a
      fi
      cat <<EOF
<form action="addseries.cgi" method="post">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="nperyear" value="$NPERYEAR">
<input type="hidden" name="corrargs" value="$DIR/data/dummy.$NPERYEAR.dat file $corrargs">
<input type="hidden" name="a1" value="$a1">
<input type="hidden" name="a2" value="$a2">
<input type="submit" class="formbutton" value="subtract seasonally varying influence">
</form>
EOF
    fi

  elif [ -z "$FORM_conting" ]; then
    . ./month2string.cgi
    echo "<div class=\"alineakop\">Fit of $seriesmonth $CLIM $station ($WMO) vs $indexmonth $index</div>"
    xlabel="$index"
    if [ -n "$ndiff" ]; then
      xlabel="$xlabel ($ndiff-yr running mean)"
    else
      [ -n "$FORM_diff" ] && xlabel="$xlabel (diff)"
    fi
    [ -n "$FORM_detrend" ] && xlabel="$xlabel (detrended)"
    if [ "$lwrite" = true ]; then
	echo "FORM_diff=$FORM_diff<br>"
	echo "ndiff=$ndiff<br>"
	echo "FORM_detrend=$FORM_detrend<br>"
	echo "FORM_anomal=$FORM_anomal<br>"
    fi
    [ -z "$FORM_diff" -a -z "$ndiff" -a -z "$FORM_detrend" -a -n "$FORM_anomal" ] && xlabel="$xlabel (anomalies)"
    corrval="r = "`cut -b 11-17 data/$TYPE$WMO${FORM_num}.cor`
    FIT_LOG=/tmp/FIT${FORM_num}.log
    export FIT_LOG
    if [ $n -gt 1 ]; then
      corrval=''
      ext1="1"
      echo "<pre>"
      ./bin/multifit "data/$TYPE$WMO${FORM_num}.dump" $index
      echo "</pre>"
      taillines=0
      added=" (added with fitted weights)"

      echo "(view the <a href=\"data/$TYPE$WMO${FORM_num}.dump\">raw data</a>)"
      echo "<form action=\"addseries.cgi\" method=\"POST\">"
      echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
      echo "<input type=\"hidden\" name=\"corrargs\" value=\"$corrargs\">"
      echo "<p>Add $index with the following weights: "
      i=0
      while [ $i -lt $n ]
      do
        i=$(($i+1))
        echo "<input type=\"number\" step=any name=\"a$i\" size=\"10\" style=\"width: 11em;\" value=\""`tail -$((n-i+1)) data/$TYPE$WMO${FORM_num}.dump$ext1 | head -1 | cut -b '7-' | tr ',' '.' | tr -d ' '`"\">"
      done
      echo "<input type=\"submit\" class=\"formbutton\" value=\"and create new timeseries\">"
      echo "</form>"
    else
      taillines=16
    fi
    if [ -n "$FORM_log" ]; then
	y='(10**$2)'
	axb='10**(a+b*x*(1+c*x))'
    elif [ -n "$FORM_sqrt" ]; then
	y='($2**2)'
	axb='(a+b*x*(1+c*x))**2'
    else
	y='($2)'
	axb="a+b*x*(1+c*x)"
    fi
    yy='2'
    if [ "$FORM_fitfunc" = "fittime" ]; then
	ylabel="$ylabel minus fitted tendency"
        fitfunc="a+b*x+c*y"
        fitpars="a,b,c"
        taillines=18
        yy="3:2:(1)"
        y="(\$2-c*\$3)"
	axb='a+b*x'
    elif [ "$FORM_fitfunc" = "quadratic" ]; then
        fitfunc="a+b*x*(1+c*x)"
        fitpars="a,b,c"
        taillines=18
    elif [ "$FORM_fitfunc" = "cubic" ]; then
        fitfunc="a+b*x*+c*x*x+d*x*x*x"
        fitpars="a,b,c,d"
        cixzero='c=0.001;d=0.001'
        taillines=20
    elif [ "$FORM_fitfunc" = "phase" ]; then
        fitfunc=""
        fitpars=""
        taillines=1
	withlines="with linespoints #"
    else
        fitfunc="a+b*x"
        fitpars="a,b"
        ciszero="c=0"
    fi
    if [ -n "$fitfunc" ]; then
      fitit="fit $fitfunc 'data/$TYPE$WMO${FORM_num}.dump$ext1' using 1:$yy via $fitpars"
      echo "<p>$fitit"
    fi
    echo "<pre>"
###    cat <<EOF
    $DIR/bin/gnuplot << EOF 2>&1 | sed -e '/^ *$/d' -e '/====/d' | tail -$taillines
set size 0.7,0.93
set size square
set datafile missing '-999.9000'
set zeroaxis
$ciszero
FIT_LIMIT=1e-8
$fitit
set term postscript epsf color solid
set output "$corrroot.eps"
set title "$title"
set xlabel "$indexmonth $xlabel$added"
set ylabel "$seriesmonth $CLIM $ylabel"
set key left samplen -1
$xrange
$yrange
plot "data/$TYPE$WMO${FORM_num}.dump$ext1" using 1:$y notitle $withlines, $axb title "$corrval" with lines lt 4
set term png $gnuplot_png_font_hires
set output "$corrroot.png"
replot
EOF
    ###echo $DIR/bin/diamond2year "$corrroot.eps" "data/$TYPE$WMO${FORM_num}.dump$ext1" ${FORM_xlo:--3e33} ${FORM_xhi:-3e33} ${FORM_ylo:--3e33} ${FORM_yhi:-3e33}
    $DIR/bin/diamond2year "$corrroot.eps" "data/$TYPE$WMO${FORM_num}.dump$ext1" ${FORM_xlo:--3e33} ${FORM_xhi:-3e33} ${FORM_ylo:--3e33} ${FORM_yhi:-3e33} > "${corrroot}_yr.eps"
    echo "</pre>"
    rm $FIT_LOG
    if [ -n "$fitfunc" ]; then
    echo "<div class=\"alineakop\">Tercile probabilities</div>"
    echo "These are the probabilities that you will get a value below normal (lowest 33%), normal or above normal (top 33%) of the distribution of $title, given a certain value of the index $index.  It makes the following three assumptions"
    echo "<ol><li>There is a significant correlation"
    echo "<li>The width and shape of the distribution around the best fit is independent of the index.  For a rainfall distribution this is often not true, try selecting a sqrt or logarithm on the previous page"
    echo "<li>The distribution did not change over time"
    echo "</ol><p>Therefore, use with care."
    echo "<pre>"
    $DIR/bin/getchance : 3 $DIR/data/$TYPE$WMO${FORM_num}.dump$ext1
    $DIR/bin/gnuplot << EOF
set size 0.7,0.5
$xrange
set yrange [0:100]
set title "$seriesmonth $title"
set xlabel "$indexmonth $xlabel$added"
set ylabel "probability [%]"
set term postscript epsf color solid
set output "$corrroot.trc.eps"
plot "data/$TYPE$WMO${FORM_num}.dump$ext1.trc" u 1:2 title 'below normal' with lines, "data/$TYPE$WMO${FORM_num}.dump$ext1.trc" u 1:3 title 'not above normal' with lines
set term png $gnuplot_png_font_hires
set output "$corrroot.trc.png"
replot
EOF
    echo "</pre>"
    cat <<EOF
<div class="formheader">Subtract influence of $index from $station $CLIM ($WMO)</div>
<div class="formbody">
<form action="addseries.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="corrargs" value="$DIR/data/dummy.$NPERYEAR.dat file ${corrargs%%startstop*}">
EOF
    if [ ! -s ./data/dummy.$NPERYEAR.dat ]; then
        ./bin/gen_time 1 2300 $NPERYEAR > ./data/dummy.$NPERYEAR.dat
    fi
    a=`awk '{print '-' $15}' $DIR/data/$TYPE$WMO${FORM_num}.cor`
    [ "$lwrite" = true ] && echo "n=$n<br>"
    if [ $n = 1 ]; then
        if [ -n "$FORM_soi" -o -n "$FORM_nao" -o -n "$FORM_nino12" -o -n "$FORM_nino3" -o -n "$FORM_nino4" -o -n "$FORM_nino34" -o -n "$FORM_time" ]; then
            a1=$a
            a2=1
        else
            a1=1
            a2=$a
        fi
        cat <<EOF
<input type="hidden" name="a1" value="$a1">
<input type="hidden" name="a2" value="$a2">
EOF
    else
        # the numbers for the predefined indices are ordered before the rest...
        i=0
        for index in "FORM_soi" "FORM_nao" "FORM_nino12" "FORM_nino3" "FORM_nino4" "FORM_nino34" "FORM_time"
        do
            if [ -n "${!index}" ]; then
                i=$((i+1))
                # not very elegant
                ai=`echo $a | tr ' ' '\n' | head -1`
                a=`echo $a | tr ' ' '\n' | tail -n +2`
                echo "<input type=\"hidden\" name=\"a$i\" value=\"$ai\">"
            fi
        done
        i=$((i+1))
        echo "<input type=\"hidden\" name=\"a$i\" value=\"1\">"
        while [ -n "$a" ]
        do
            i=$((i+1))
            # not very elegant
            ai=`echo $a | tr ' ' '\n' | head -1`
            a=`echo $a | tr ' ' '\n' | tail -n +2`
            echo "<input type=\"hidden\" name=\"a$i\" value=\"$ai\">"
        done
    fi
cat <<EOF
<input type="submit" class="formbutton" value="Make new series">
</form>
</div>
EOF
    fi
  fi

else
  [ "$lwrite" = true ] && ( echo "found range of lags, FORM_lag=$FORM_lag contains a :"; echo "Found $n indices" )

# one index?
  
  if [ $n -eq 1 ]; then
    eval `$DIR/bin/month2string "$FORM_month" "$sumstring" "" "$FORM_operation"`

# one month?
    tmp=`echo $FORM_month | fgrep ':'`
    [ "$lwrite" = true ] && echo "Range of months? NPERYEAR=$NPERYEAR, FORM_month=$FORM_month, tmp=$tmp"
    if [ "$NPERYEAR" -gt 1 -a \( -z "$FORM_month" -o -n "$tmp" \) ]; then
      [ "$lwrite" = true ] && echo "Yes, range of months"
      if [ -z "$FORM_conting" ]; then
	FORM_ver="60"
	FORM_hor="60"
	FORM_num=${FORM_num}
	. $DIR/plot3dcor.cgi
      fi
    else # more than one month?

      if [ "$FORM_fix" = "fix2" ]; then
        title="$title $indexmonth"
	echo "<div class=\"alineakop\">Lag correlations of $CLIM $station ($WMO) with $indexmonth $index</div>"
      else
        title="$seriesmonth $title"
        echo "<div class=\"alineakop\">Lag correlations of $seriesmonth $CLIM $station ($WMO) with $index</div>"
      fi
      case "$NPERYEAR" in
      1)  lagunit="years";;
      12) lagunit="months";;
      36) lagunit="decades";;
      73) lagunit="5-day periods";;
      360) lagunit="days";;
      365) lagunit="days";;
      366) lagunit="days";;
      *)  lagunit="periods";;
      esac
      if [ -z "$FORM_conting" ]; then
        echo "If present, the band around the ${correlation}s indicates the 95% confidence limits"
	if [ "$FORM_whichvar" = regr ]; then
	    echo "assuming normally distributed errors"
	    corr1='using 2:15'
	    corr2="using 2:(\$15-2*\$16)"
	    corr3="using 2:(\$15+2*\$16)"
	else
	    echo "computed with a non-parametric bootstrap"
	    corr1='using 2:3'
	    corr2='using 2:10'
	    corr3='using 2:14'
	fi
        $DIR/bin/gnuplot << EOF
set size 0.7,0.5
set zeroaxis
set title "$title"
set xlabel "lag [${lagunit}] (lag positive: $index leading $CLIM)"
set ylabel "$correlation"
set term postscript epsf color solid
$xrange
$yrange
set output "$corrroot.eps"
plot "data/$TYPE$WMO${FORM_num}.cor" $corr1 notitle with lines lt 1 lw 2,\
     "data/$TYPE$WMO${FORM_num}.cor" $corr2 notitle with lines lt 2,\
     "data/$TYPE$WMO${FORM_num}.cor" $corr3 notitle with lines lt 2,\
     0 notitle with lines 0
set term png $gnuplot_png_font_hires
set output "$corrroot.png"
replot
EOF
      else
        $DIR/bin/gnuplot << EOF
set size 0.7,0.5
$xrange
$yrange
set zeroaxis
set title "$seriesmonth $title"
set xlabel "lag [${lagunit}] (lag positive: $index leading $CLIM)"
set ylabel "(<<)+(>>), (<>)+(><)"
set term postscript epsf color solid
set output "$corrroot.eps"
plot "data/$TYPE$WMO${FORM_num}.cor" using 2:(\$9+\$19) notitle with lines, \
     "data/$TYPE$WMO${FORM_num}.cor" using 2:(\$11+\$17) notitle with lines
set term png $gnuplot_png_font_hires
set output "$corrroot.png"
replot
EOF
      fi
    fi
  fi 
fi
echo "<a name=\"plots\"></a>"
. ./showplots.cgi

. ./myvinkfoot.cgi
