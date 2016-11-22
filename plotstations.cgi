#!/bin/sh
. ./init.cgi
. ./getargs.cgi
# check email address
. ./checkemail.cgi
export DIR=`pwd`

if [ "$EMAIL" = oldenborgh@knmi.nl ]; then
    lwrite=false # true
fi

hiresmap=true
if [ "$hiresmap" = true ]; then
	doublesize="x1804 y1394"
else
	doublesize="x902 y697"
fi
grads=./bin/grads
config=`$grads -b -l -c quit| fgrep Config`
c=`echo $config | fgrep -c v2.0`
if [ $c -gt 0 ]; then
    grads20=true
    gradsver=2.0
else
    gradsver=1.8
	if [ "$FORM_mapformat" = geotiff ]; then
		echo "geotiff export is not supported by GrADS 1.8"
		exit
	fi
fi

if [ -z "$plotlist" ]; then
  echo 'Content-Type: text/html'
  echo
  echo

  # to find netpbm on MacOS X
  # fix title...
  FORM_title=`echo "$FORM_title" | sed -e 's/with /\\\\with /'`
  title=`echo "$FORM_title" | sed -e 's/\\\\/ /'`
  . ./myvinkhead.cgi "Map of stations" "$title" "noindex,nofollow"


  # copy (possibly edited) plotdata into file, filter out metachars
  forbidden='!`;&|'
  plotlist=data/plotlist$$.txt
  cat << ditisheteinde | tr '\r' '\n' | tr $forbidden '?' > $plotlist
$FORM_list
ditisheteinde

  if [ `wc -l $plotlist | awk '{print $1}'` -le 2 ]
  then
    # stupid MacOS X...
    ###echo '<p>Circumventing bug in Mac OS X...'
    sed -e 's/\([A-Z][^ ]*\) \([1-9][0-9]\)/\1\@\2/g' $plotlist | tr '@' '\n' | sed -e 's/\(^# [-.0-9]*  *[-.0-9]*  *[-.0-9]*  *[-.0-9]*\) /\1@/' | tr '@' '\n' > /tmp/plhack$$
    mv /tmp/plhack$$ $plotlist
  fi
fi
####listname=$plotlist

# sort the list so that the brightest colours come out on top

if [ "$FORM_col" = precipitation ]; then
    sortsig="-r"
    sortval=""
elif [ "$FORM_col" = newcolour -o "$FORM_col" = newflipcolour -o \
     "$FORM_col" = colour -o "$FORM_col" = flipcolour -o \
     "$FORM_col" = color -o "$FORM_col" = flipcolor ]; then
    sortsig="-r"
    sortval=""
else
    sortsig=""
    sortval="-r"
fi
if [ "$FORM_var" = sign ]; then
    # sort with the smallest values at the end so that they come out on top
    head -1 $plotlist > /tmp/plotstat$$
    tail -n +2 $plotlist | sort -g -k 5 $sortsig >> /tmp/plotstat$$
    mv /tmp/plotstat$$ $plotlist
else
    # sort with the largest absolute values at the end
    head -1 $plotlist > /tmp/plotstat$$
    tail -n +2 $plotlist \
    | sed -e 's/^ *\([^ ][^ ]*\)  *\([^ ][^ ]*\)  *\([^ ][^ ]*\)  *-\(.*\)/@\1 \2 \3 \4/' \
    | sort -g -k 4 $sortval \
    | sed -e 's/^@\([^ ][^ ]*\)  *\([^ ][^ ]*\)  *\([^ ][^ ]*\)  *\(.*\)/\1 \2 \3 -\4/' \
    >> /tmp/plotstat$$
    mv /tmp/plotstat$$ $plotlist
fi

if [ -z "$FORM_notitleonplot" ]; then
  drawtitle="draw title $FORM_title"
else
  drawtitle=""
fi
if [ -n "$FORM_nogrid" ]; then
  grid="set grid off"
else
  grid="set grid on"
fi
line=`head -1 $plotlist`
FORM_lon1=`echo $line | awk '{print $2}'`
FORM_lon2=`echo $line | awk '{print $3}'`
FORM_lat1=`echo $line | awk '{print $4}'`
FORM_lat2=`echo $line | awk '{print $5}'`
. ./setmap.cgi
if [ -n "$FORM_nopoli" ]; then
    grid="$grid
set poli off"
fi

forbidden='!`;&|'
scale=`echo $FORM_scale | tr $forbidden '?'`
cmax=`echo $FORM_cmax   | tr $forbidden '?'`
mproj=`echo $FORM_mproj | tr $forbidden '?'`
xlint=`echo $FORM_xlint | tr $forbidden '?'`
ylint=`echo $FORM_ylint | tr $forbidden '?'`
if [ -n "$xlint" ]; then
  setxlint="set xlint $xlint"
else
  setxlint=""
fi
if [ -n "$ylint" ]; then
  setylint="set ylint $ylint"
else
  setylint=""
fi

if [ $EMAIL != someone@somewhere ]; then
# save values for next plot
  cat > prefs/$FORM_EMAIL.plotstations <<EOF
FORM_scale=$scale;
FORM_var=$FORM_var;
FORM_value=$FORM_value;
FORM_code=$FORM_code;
FORM_name=$FORM_name;
FORM_col=$FORM_col;
FORM_cmax=$cmax;
FORM_greycut=$FORM_greycut;
FORM_mproj=$mproj;
FORM_nogrid=$FORM_nogrid;
FORM_nopoli=$FORM_nopoli;
FORM_nocbar=$FORM_nocbar;
FORM_notitleonplot=$FORM_notitleonplot;
FORM_xlint=$FORM_xlint;
FORM_ylint=$FORM_ylint;
EOF
fi

if [ -n "$FORM_value" ]; then
  label="value"
fi
if [ -n "$FORM_code" ]; then
  label="${label}code"
fi
if [ -n "$FORM_name" ]; then
  label="${label}name"
fi

echo "Plotting with <a href=\"http://grads.iges.org/grads/\" target=_top>GrADS</a> $gradsver...<p>"

. $DIR/getfieldopts.cgi

export GADDIR=$DIR/grads
f=data/g$$
id=$$
if [ -z "$FORM_col" ]; then
  FORM_col = bw
fi
size8=`echo "${scale}*0.8/2" | bc -l -q`
size5=`echo "${scale}*0.5/2" | bc -l -q`
size2=`echo "${scale}*0.2/2" | bc -l -q`
y8=`echo "0.18+$size8/2" | bc -l -q`
y5=`echo "0.18+$size5/2" | bc -l -q`
y2=`echo "0.18+$size2/2" | bc -l -q`
y0=0.15
if [ -z "$cmax" -o "$cmax" = "0.6" ]; then
  c=0.5
  o=0.1
else
  c=$cmax
  o=0
fi
if [ "$FORM_col" = precipitation ]; then
val10=`echo "1.0*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val9=`echo "0.9*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val8=`echo "0.8*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val7=`echo "0.7*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val6=`echo "0.6*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val5=`echo "0.5*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val4=`echo "0.4*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val3=`echo "0.3*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val2=`echo "0.2*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val1=`echo "0.1*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
elif [ 0 = 1 ]; then
val6=`echo "1.0*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val5=`echo "0.8*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val4=`echo "0.6*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val3=`echo "0.4*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
val2=`echo "0.2*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^\./0./'`
else
val6=`echo "1.0*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^0\././'`
val5=`echo "0.8*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^0\././'`
val4=`echo "0.6*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^0\././'`
val3=`echo "0.4*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^0\././'`
val2=`echo "0.2*$c + $o" | bc -l -q | sed -e 's/0*$//' -e 's/^0\././'`
fi
if [ -n "$FORM_nocbar" ]; then
  if [ "$lwrite" = true ]; then
    echo "no legend requested"
  fi
else
if [ "$lwrite" = true ]; then
  echo "cmax=$cmax x=$c o=$o <br>"
  echo "scale=$scale<br>"
  echo "size2=$size2 size5=$size5 size8=$size8<br>"
  echo "val2=$val2 val3=$val3 val4=$val4 val5=$val5 val6=$val6<br>"
  echo "y2=$y2 y5=$y5 y8=$y8<br>"
  echo "FORM_col  = $FORM_col<br>"
  echo "FORM_oper = $FORM_oper<br>"
  echo "Computing legend<br>"
fi
if [ "$FORM_oper" = "hivr" -o "$FORM_oper" = "hivR" -o "$FORM_oper" = "higr" -o "$FORM_oper" = "higR" -o "$FORM_oper" = "hipr" -o "$FORM_oper" = "hipR" -o "$FORM_oper" = "atr1" -o "$FORM_oper" = "atr2" ]; then
  if [ $FORM_col = 'colour' -o "$FORM_col" = "flipcolour" -o $FORM_col = 'color' -o "$FORM_col" = "flipcolor" ]; then
    FORM_cmax=return
# coordinate with plotbox.gs ...
    legenda="\
set string 1 tc
set line 50
draw mark 3 3 $y8 $size8
set line 1
draw mark 2 3 $y8 $size8
draw string 3.25 $y0 10
set line 15
draw mark 3 3.5 $y8 $size8
set line 1
draw mark 2 3.5 $y8 $size8
draw string 3.75 $y0 20
set line 11
draw mark 3 4 $y8 $size8
set line 1
draw mark 2 4 $y8 $size8
draw string 4.25 $y0 50
set line 3
draw mark 3 4.5 $y8 $size8
set line 1
draw mark 2 4.5 $y8 $size8
draw string 4.75 $y0 100
set line 10
draw mark 3 5 $y8 $size8
set line 1
draw mark 2 5 $y8 $size8
draw string 5.25 $y0 200
set line 7
draw mark 3 5.5 $y8 $size8
set line 1
draw mark 2 5.5 $y8 $size8
draw string 5.75 $y0 500
set line 12
draw mark 3 6 $y8 $size8
set line 1
draw mark 2 6 $y8 $size8
draw string 6.25 $y0 1000
set line 8
draw mark 3 6.5 $y8 $size8
set line 1
draw mark 2 6.5 $y8 $size8
draw string 6.75 $y0 2000
set line 2
draw mark 3 7 $y8 $size8
set line 1
draw mark 2 7 $y8 $size8
draw string 7.25 $y0 5000
set line 6
draw mark 3 7.5 $y8 $size8
set line 1
draw mark 2 7.5 $y8 $size8
draw string 7.75 $y0 10000
set line 14
draw mark 3 8 $y8 $size8
set line 1
draw mark 2 8 $y8 $size8
"
  else
    echo "legend with return times and this colour scale not yet ready"
  fi  
elif [ "$FORM_var" = "sign" ]; then
  if [ $FORM_col = 'colour' -o "$FORM_col" = "flipcolour" ]; then
# coordinate with plotbox.gs ...
    legenda="\
set string 1 tc
set line 50
draw mark 3 4.25 $y8 $size8
set line 1
draw mark 2 4.25 $y8 $size8
draw string 4.5 $y0 10%
set line 15
draw mark 3 4.75 $y8 $size8
set line 1
draw mark 2 4.75 $y8 $size8
draw string 5 $y0 5%
set line 7
draw mark 3 5.25 $y8 $size8
set line 1
draw mark 2 5.25 $y8 $size8
draw string 5.5 $y0 1%
set line 12
draw mark 3 5.75 $y8 $size8
set line 1
draw mark 2 5.75 $y8 $size8
draw string 6 $y0 0.5%
set line 2
draw mark 3 6.25 $y8 $size8
set line 1
draw mark 2 6.25 $y8 $size8
draw string 6.5 $y0 0.1%
set line 6
draw mark 3 6.75 $y8 $size8
set line 1
draw mark 2 6.75 $y8 $size8
"
  else
    echo "legend with significance and this colour scale not yet ready"
  fi  
elif [ "$FORM_oper" = 'corr' ]; then
  if [ $FORM_col = 'bw' ]; then
    legenda="\
set string 1 tc
draw mark 2 3 $y8 $size8
draw string 3 $y0 r=-0.8
draw mark 2 4 $y5 $size5
draw string 4 $y0 r=-0.5
draw mark 2 5 $y2 $size2
draw string 5 $y0 r=-0.2
draw mark 3 6 $y2 $size2
set line 0
draw mark 2 6 $y2 $size2
set line 1
draw string 6 $y0 r=+0.2
draw mark 3 7 $y5 $size5
set line 0
draw mark 2 7 $y5 $size5
set line 1
draw string 7 $y0 r=+0.5
draw mark 3 8 $y8 $size8
set line 0
draw mark 2 8 $y8 $size8
set line 1
draw string 8 $y0 r=+0.8
"
  elif [ $FORM_col = 'flipbw' ]; then
    legenda="\
set string 1 tc
draw mark 3 3 $y8 $size8
set line 0
draw mark 2 3 $y8 $size8
set line 1
draw string 3 $y0 r=-0.8
draw mark 3 4 $y5 $size5
set line 0
draw mark 2 4 $y5 $size5
set line 1
draw string 4 $y0 r=-0.5
draw mark 3 5 $y2 $size2
set line 0
draw mark 2 5 $y2 $size2
set line 1
draw string 5 $y0 r=-0.2
draw mark 2 6 $y2 $size2
draw string 6 $y0 r=+0.2
draw mark 2 7 $y5 $size5
draw string 7 $y0 r=+0.5
draw mark 2 8 $y8 $size8
draw string 8 $y0 r=+0.8
"
  elif [ $FORM_col = 'rb' ]; then
    legenda="\
set string 1 tc
set line 4
draw mark 3 3 $y8 $size8
set line 1
draw mark 2 3 $y8 $size8
draw string 3 $y0 r=-0.8
set line 4
draw mark 3 4 $y5 $size5
set line 1
draw mark 2 4 $y5 $size5
draw string 4 $y0 r=-0.5
set line 4
draw mark 3 5 $y2 $size2
set line 1
draw mark 2 5 $y2 $size2
draw string 5 $y0 r=-0.2
set line 2
draw mark 3 6 $y2 $size2
set line 1
draw mark 2 6 $y2 $size2
draw string 6 $y0 r=+0.2
set line 2
draw mark 3 7 $y5 $size5
set line 1
draw mark 2 7 $y5 $size5
draw string 7 $y0 r=+0.5
set line 2
draw mark 3 8 $y8 $size8
set line 1
draw mark 2 8 $y8 $size8
draw string 8 $y0 r=+0.8
set line 1
"
  elif [ $FORM_col = 'br' ]; then
    legenda="\
set string 1 tc
set line 2
draw mark 3 3 $y8 $size8
set line 1
draw mark 2 3 $y8 $size8
draw string 3 $y0 r=-0.8
set line 2
draw mark 3 4 $y5 $size5
set line 1
draw mark 2 4 $y5 $size5
draw string 4 $y0 r=-0.5
set line 2
draw mark 3 5 $y2 $size2
set line 1
draw mark 2 5 $y2 $size2
draw string 5 $y0 r=-0.2
set line 4
draw mark 3 6 $y2 $size2
set line 1
draw mark 2 6 $y2 $size2
draw string 6 $y0 r=+0.2
set line 4
draw mark 3 7 $y5 $size5
set line 1
draw mark 2 7 $y5 $size5
draw string 7 $y0 r=+0.5
set line 4
draw mark 3 8 $y8 $size8
set line 1
draw mark 2 8 $y8 $size8
draw string 8 $y0 r=+0.8
"
  elif [ $FORM_col = 'colour' -o $FORM_col = 'color' ]; then
# coordinate with plotbox.gs ...
    legenda="\
set string 1 tc
set line 14
draw mark 3 3 $y8 $size8
set line 1
draw mark 2 3 $y8 $size8
draw string 3.25 $y0 -$val6
set line 4
draw mark 3 3.5 $y8 $size8
set line 1
draw mark 2 3.5 $y8 $size8
draw string 3.75 $y0 -$val5
set line 11
draw mark 3 4 $y8 $size8
set line 1
draw mark 2 4 $y8 $size8
draw string 4.25 $y0 -$val4
set line 3
draw mark 3 4.5 $y8 $size8
set line 1
draw mark 2 4.5 $y8 $size8
draw string 4.75 $y0 -$val3
set line 10
draw mark 3 5 $y8 $size8
set line 1
draw mark 2 5 $y8 $size8
draw string 5.25 $y0 -$val2
set line 15
draw mark 3 5.5 $y8 $size8
set line 1
draw mark 2 5.5 $y8 $size8
draw string 5.75 $y0 +$val2
set line 7
draw mark 3 6 $y8 $size8
set line 1
draw mark 2 6 $y8 $size8
draw string 6.25 $y0 +$val3
set line 12
draw mark 3 6.5 $y8 $size8
set line 1
draw mark 2 6.5 $y8 $size8
draw string 6.75 $y0 +$val4
set line 8
draw mark 3 7 $y8 $size8
set line 1
draw mark 2 7 $y8 $size8
draw string 7.25 $y0 +$val5
set line 2
draw mark 3 7.5 $y8 $size8
set line 1
draw mark 2 7.5 $y8 $size8
draw string 7.75 $y0 +$val6
set line 6
draw mark 3 8 $y8 $size8
set line 1
draw mark 2 8 $y8 $size8

set line 50
draw mark 3 9 $y8 $size8
set line 15
draw mark 2 9 $y8 $size8
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  elif [ $FORM_col = 'flipcolour' -o $FORM_col = 'flipcolor' ]; then
# coordinate with plotbox.gs ...
    legenda="\
set string 1 tc
set line 6
draw mark 3 3 $y8 $size8
set line 1
draw mark 2 3 $y8 $size8
draw string 3.25 $y0 -$val6
set line 2
draw mark 3 3.5 $y8 $size8
set line 1
draw mark 2 3.5 $y8 $size8
draw string 3.75 $y0 -$val5
set line 8
draw mark 3 4 $y8 $size8
set line 1
draw mark 2 4 $y8 $size8
draw string 4.25 $y0 -$val4
set line 12
draw mark 3 4.5 $y8 $size8
set line 1
draw mark 2 4.5 $y8 $size8
draw string 4.75 $y0 -$val3
set line 7
draw mark 3 5 $y8 $size8
set line 1
draw mark 2 5 $y8 $size8
draw string 5.25 $y0 -$val2
set line 15
draw mark 3 5.5 $y8 $size8
set line 1
draw mark 2 5.5 $y8 $size8
draw string 5.75 $y0 +$val2
set line 10
draw mark 3 6 $y8 $size8
set line 1
draw mark 2 6 $y8 $size8
draw string 6.25 $y0 +$val3
set line 3
draw mark 3 6.5 $y8 $size8
set line 1
draw mark 2 6.5 $y8 $size8
draw string 6.75 $y0 +$val4
set line 11
draw mark 3 7 $y8 $size8
set line 1
draw mark 2 7 $y8 $size8
draw string 7.25 $y0 +$val5
set line 4
draw mark 3 7.5 $y8 $size8
set line 1
draw mark 2 7.5 $y8 $size8
draw string 7.75 $y0 +$val6
set line 14
draw mark 3 8 $y8 $size8
set line 1
draw mark 2 8 $y8 $size8

set line 50
draw mark 3 9 $y8 $size8
set line 15
draw mark 2 9 $y8 $size8
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  fi
elif [ "$FORM_oper" != "grid" ]; then
# not a correlation.  We would still like a legend, though...
  invscale=`echo "100000/$scale"|bc -l -q`
  invscale=${invscale%%\.*}
  if [ "$lwrite" = true ]; then
    echo "Not a correlation, compute legend<br>"
    echo "invscale=$invscale<br>"
  fi
  if [ $invscale -lt 1 ]; then
    legend1=0.000002
    legend2=0.000005
  elif [ $invscale -lt 2 ]; then
    legend1=0.000005
    legend2=0.00001
  elif [ $invscale -lt 5 ]; then
    legend1=0.00001
    legend2=0.00002
  elif [ $invscale -lt 10 ]; then
    legend1=0.00002
    legend2=0.00005
  elif [ $invscale -lt 20 ]; then
    legend1=0.00005
    legend2=0.0001
  elif [ $invscale -lt 50 ]; then
    legend1=0.0001
    legend2=0.0002
  elif [ $invscale -lt 100 ]; then
    legend1=0.0002
    legend2=0.0005
  elif [ $invscale -lt 200 ]; then
    legend1=0.0005
    legend2=0.001
  elif [ $invscale -lt 500 ]; then
    legend1=0.001
    legend2=0.002
  elif [ $invscale -lt 1000 ]; then
    legend1=0.002
    legend2=0.005
  elif [ $invscale -lt 2000 ]; then
    legend1=0.005
    legend2=0.01
  elif [ $invscale -lt 5000 ]; then
    legend1=0.01
    legend2=0.02
  elif [ $invscale -lt 10000 ]; then
    legend1=0.02
    legend2=0.05
  elif [ $invscale -lt 20000 ]; then
    legend1=0.05
    legend2=0.1
  elif [ $invscale -lt 50000 ]; then
    legend1=0.1
    legend2=0.2
  elif [ $invscale -lt 100000 ]; then
    legend1=0.2
    legend2=0.5
  elif [ $invscale -lt 200000 ]; then
    legend1=0.5
    legend2=1
  elif [ $invscale -lt 500000 ]; then
    legend1=1
    legend2=2
  elif [ $invscale -lt 1000000 ]; then
    legend1=2
    legend2=5
  elif [ $invscale -lt 2000000 ]; then
    legend1=5
    legend2=10
  elif [ $invscale -lt 5000000 ]; then
    legend1=10
    legend2=20
  elif [ $invscale -lt 10000000 ]; then
    legend1=20
    legend2=50
  elif [ $invscale -lt 20000000 ]; then
    legend1=50
    legend2=100
  elif [ $invscale -lt 50000000 ]; then
    legend1=100
    legend2=200
  elif [ $invscale -lt 100000000 ]; then
    legend1=20
    legend2=500
  elif [ $invscale -lt 200000000 ]; then
    legend1=500
    legend2=1000
  elif [ $invscale -lt 500000000 ]; then
    legend1=1000
    legend2=2000
  elif [ $invscale -lt 1000000000 ]; then
    legend1=2000
    legend2=5000
  elif [ $invscale -lt 2000000000 ]; then
    legend1=5000
    legend2=10000
  elif [ $invscale -lt 5000000000 ]; then
    legend1=10000
    legend2=20000
  elif [ $invscale -lt 10000000000 ]; then
    legend1=20000
    legend2=50000
  else
    legend1=50000
    legend2=100000
  fi
  if [ "$lwrite" = true ]; then
    echo "legend1 = $legend1"
    echo "legend2 = $legend2"
  fi
  size1=`echo "${scale}*${legend1}/2" | bc -l -q`
  size2=`echo "${scale}*${legend2}/2" | bc -l -q`
  y1=`echo "0.15+$size1/2" | bc -l -q`
  y2=`echo "0.15+$size2/2" | bc -l -q`
  y0=0.12
  if [ $FORM_col = 'bw' ]; then
    legenda="\
set string 1 tc
draw mark 2 4 $y2 $size2
draw string 4 $y0 -$legend2
draw mark 2 5 $y1 $size1
draw string 5 $y0 -$legend1
draw mark 3 6 $y1 $size1
set line 0
draw mark 2 6 $y1 $size1
set line 1
draw string 6 $y0 +$legend1
draw mark 3 7 $y2 $size2
set line 0
draw mark 2 7 $y2 $size2
set line 1
draw string 7 $y0 +$legend2
"
  elif [ $FORM_col = 'flipbw' ]; then
    legenda="\
set string 1 tc
draw mark 3 4 $y2 $size2
set line 0
draw mark 2 4 $y2 $size2
set line 1
draw string 4 $y0 -$legend2
draw mark 3 5 $y1 $size1
set line 0
draw mark 2 5 $y1 $size1
set line 1
draw string 5 $y0 -$legend1
draw mark 2 6 $y1 $size1
draw string 6 $y0 +$legend1
draw mark 2 7 $y2 $size2
draw string 7 $y0 +$legend2
"
  elif [ $FORM_col = 'rb' ]; then
    legenda="\
set string 1 tc
set line 4
draw mark 3 4 $y2 $size2
set line 1
draw mark 2 4 $y2 $size2
draw string 4 $y0 -$legend2
set line 4
draw mark 3 5 $y1 $size1
set line 1
draw mark 2 5 $y1 $size1
draw string 5 $y0 -$legend1
set line 2
draw mark 3 6 $y1 $size1
set line 1
draw mark 2 6 $y1 $size1
draw string 6 $y0 +$legend1
set line 2
draw mark 3 7 $y2 $size2
set line 1
draw mark 2 7 $y2 $size2
draw string 7 $y0 +$legend2
set line 1
"
  elif [ $FORM_col = 'br' ]; then
    legenda="\
set string 1 tc
set line 2
draw mark 3 4 $y2 $size2
set line 1
draw mark 2 4 $y2 $size2
draw string 4 $y0 -$legend2
set line 2
draw mark 3 5 $y1 $size1
set line 1
draw mark 2 5 $y1 $size1
draw string 5 $y0 -$legend1
set line 4
draw mark 3 6 $y1 $size1
set line 1
draw mark 2 6 $y1 $size1
draw string 6 $y0 +$legend1
set line 4
draw mark 3 7 $y2 $size2
set line 1
draw mark 2 7 $y2 $size2
draw string 7 $y0 +$legend2
"
  elif [ $FORM_col = 'newcolour' ]; then
# coordinate with plotbox.gs ...
    y0=0.15
    legenda="\
set string 1 tc
set line 34
draw mark 3 3 $y8 $size5
set line 1
draw mark 2 3 $y8 $size5
draw string 3.25 $y0 -$val6
set line 24
draw mark 3 3.5 $y8 $size5
set line 1
draw mark 2 3.5 $y8 $size5
draw string 3.75 $y0 -$val5
set line 31
draw mark 3 4 $y8 $size5
set line 1
draw mark 2 4 $y8 $size5
draw string 4.25 $y0 -$val4
set line 23
draw mark 3 4.5 $y8 $size5
set line 1
draw mark 2 4.5 $y8 $size5
draw string 4.75 $y0 -$val3
set line 30
draw mark 3 5 $y8 $size5
set line 1
draw mark 2 5 $y8 $size5
draw string 5.25 $y0 -$val2
set line 50
draw mark 3 5.5 $y8 $size5
set line 1
draw mark 2 5.5 $y8 $size5
draw string 5.75 $y0 +$val2
set line 27
draw mark 3 6 $y8 $size5
set line 1
draw mark 2 6 $y8 $size5
draw string 6.25 $y0 +$val3
set line 32
draw mark 3 6.5 $y8 $size5
set line 1
draw mark 2 6.5 $y8 $size5
draw string 6.75 $y0 +$val4
set line 28
draw mark 3 7 $y8 $size5
set line 1
draw mark 2 7 $y8 $size5
draw string 7.25 $y0 +$val5
set line 22
draw mark 3 7.5 $y8 $size5
set line 1
draw mark 2 7.5 $y8 $size5
draw string 7.75 $y0 +$val6
set line 26
draw mark 3 8 $y8 $size5
set line 1
draw mark 2 8 $y8 $size5

set line 50
draw mark 3 9 $y8 $size5
set line 15
draw mark 2 9 $y8 $size5
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  elif [ $FORM_col = 'newflipcolour' ]; then
# coordinate with plotbox.gs ...
    y0=0.15
    legenda="\
set string 1 tc
set line 26
draw mark 3 3 $y8 $size5
set line 1
draw mark 2 3 $y8 $size5
draw string 3.25 $y0 -$val6
set line 22
draw mark 3 3.5 $y8 $size5
set line 1
draw mark 2 3.5 $y8 $size5
draw string 3.75 $y0 -$val5
set line 28
draw mark 3 4 $y8 $size5
set line 1
draw mark 2 4 $y8 $size5
draw string 4.25 $y0 -$val4
set line 32
draw mark 3 4.5 $y8 $size5
set line 1
draw mark 2 4.5 $y8 $size5
draw string 4.75 $y0 -$val3
set line 27
draw mark 3 5 $y8 $size5
set line 1
draw mark 2 5 $y8 $size5
draw string 5.25 $y0 -$val2
set line 15
draw mark 3 5.5 $y8 $size5
set line 1
draw mark 2 5.5 $y8 $size5
draw string 5.75 $y0 +$val2
set line 30
draw mark 3 6 $y8 $size5
set line 1
draw mark 2 6 $y8 $size5
draw string 6.25 $y0 +$val3
set line 23
draw mark 3 6.5 $y8 $size5
set line 1
draw mark 2 6.5 $y8 $size5
draw string 6.75 $y0 +$val4
set line 31
draw mark 3 7 $y8 $size5
set line 1
draw mark 2 7 $y8 $size5
draw string 7.25 $y0 +$val5
set line 24
draw mark 3 7.5 $y8 $size5
set line 1
draw mark 2 7.5 $y8 $size5
draw string 7.75 $y0 +$val6
set line 34
draw mark 3 8 $y8 $size5
set line 1
draw mark 2 8 $y8 $size5

set line 50
draw mark 3 9 $y8 $size5
set line 15
draw mark 2 9 $y8 $size5
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  elif [ $FORM_col = 'colour' -o $FORM_col = color ]; then
# coordinate with plotbox.gs ...
    y0=0.15
    legenda="\
set string 1 tc
set line 14
draw mark 3 3 $y8 $size5
set line 1
draw mark 2 3 $y8 $size5
draw string 3.25 $y0 -$val6
set line 4
draw mark 3 3.5 $y8 $size5
set line 1
draw mark 2 3.5 $y8 $size5
draw string 3.75 $y0 -$val5
set line 11
draw mark 3 4 $y8 $size5
set line 1
draw mark 2 4 $y8 $size5
draw string 4.25 $y0 -$val4
set line 3
draw mark 3 4.5 $y8 $size5
set line 1
draw mark 2 4.5 $y8 $size5
draw string 4.75 $y0 -$val3
set line 10
draw mark 3 5 $y8 $size5
set line 1
draw mark 2 5 $y8 $size5
draw string 5.25 $y0 -$val2
set line 15
draw mark 3 5.5 $y8 $size5
set line 1
draw mark 2 5.5 $y8 $size5
draw string 5.75 $y0 +$val2
set line 7
draw mark 3 6 $y8 $size5
set line 1
draw mark 2 6 $y8 $size5
draw string 6.25 $y0 +$val3
set line 12
draw mark 3 6.5 $y8 $size5
set line 1
draw mark 2 6.5 $y8 $size5
draw string 6.75 $y0 +$val4
set line 8
draw mark 3 7 $y8 $size5
set line 1
draw mark 2 7 $y8 $size5
draw string 7.25 $y0 +$val5
set line 2
draw mark 3 7.5 $y8 $size5
set line 1
draw mark 2 7.5 $y8 $size5
draw string 7.75 $y0 +$val6
set line 6
draw mark 3 8 $y8 $size5
set line 1
draw mark 2 8 $y8 $size5

set line 50
draw mark 3 9 $y8 $size5
set line 15
draw mark 2 9 $y8 $size5
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  elif [ $FORM_col = 'flipcolour' -o $FORM_col = flipcolor ]; then
# coordinate with plotbox.gs ...
    y0=0.15
    legenda="\
set string 1 tc
set line 6
draw mark 3 3 $y8 $size5
set line 1
draw mark 2 3 $y8 $size5
draw string 3.25 $y0 -$val6
set line 2
draw mark 3 3.5 $y8 $size5
set line 1
draw mark 2 3.5 $y8 $size5
draw string 3.75 $y0 -$val5
set line 8
draw mark 3 4 $y8 $size5
set line 1
draw mark 2 4 $y8 $size5
draw string 4.25 $y0 -$val4
set line 12
draw mark 3 4.5 $y8 $size5
set line 1
draw mark 2 4.5 $y8 $size5
draw string 4.75 $y0 -$val3
set line 7
draw mark 3 5 $y8 $size5
set line 1
draw mark 2 5 $y8 $size5
draw string 5.25 $y0 -$val2
set line 15
draw mark 3 5.5 $y8 $size5
set line 1
draw mark 2 5.5 $y8 $size5
draw string 5.75 $y0 +$val2
set line 10
draw mark 3 6 $y8 $size5
set line 1
draw mark 2 6 $y8 $size5
draw string 6.25 $y0 +$val3
set line 3
draw mark 3 6.5 $y8 $size5
set line 1
draw mark 2 6.5 $y8 $size5
draw string 6.75 $y0 +$val4
set line 11
draw mark 3 7 $y8 $size5
set line 1
draw mark 2 7 $y8 $size5
draw string 7.25 $y0 +$val5
set line 4
draw mark 3 7.5 $y8 $size5
set line 1
draw mark 2 7.5 $y8 $size5
draw string 7.75 $y0 +$val6
set line 14
draw mark 3 8 $y8 $size5
set line 1
draw mark 2 8 $y8 $size5

set line 50
draw mark 3 9 $y8 $size5
set line 15
draw mark 2 9 $y8 $size5
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  elif [ $FORM_col = 'precipitation' ]; then
# coordinate with plotbox.gs ...
    y0=0.15
    legenda="\
set string 1 tc
set line 1
draw mark 2 2.5 $y8 $size5
draw string 2.75 $y0 0
set line 21
draw mark 3 3 $y8 $size5
set line 1
draw mark 2 3 $y8 $size5
draw string 3.25 $y0 $val1
set line 22
draw mark 3 3.5 $y8 $size5
set line 1
draw mark 2 3.5 $y8 $size5
draw string 3.75 $y0 $val2
set line 23
draw mark 3 4 $y8 $size5
set line 1
draw mark 2 4 $y8 $size5
draw string 4.25 $y0 $val3
set line 24
draw mark 3 4.5 $y8 $size5
set line 1
draw mark 2 4.5 $y8 $size5
draw string 4.75 $y0 $val4
set line 25
draw mark 3 5 $y8 $size5
set line 1
draw mark 2 5 $y8 $size5
draw string 5.25 $y0 $val5
set line 26
draw mark 3 5.5 $y8 $size5
set line 1
draw mark 2 5.5 $y8 $size5
draw string 5.75 $y0 $val6
set line 27
draw mark 3 6 $y8 $size5
set line 1
draw mark 2 6 $y8 $size5
draw string 6.25 $y0 $val7
set line 28
draw mark 3 6.5 $y8 $size5
set line 1
draw mark 2 6.5 $y8 $size5
draw string 6.75 $y0 $val8
set line 29
draw mark 3 7 $y8 $size5
set line 1
draw mark 2 7 $y8 $size5
draw string 7.25 $y0 $val9
set line 30
draw mark 3 7.5 $y8 $size5
set line 1
draw mark 2 7.5 $y8 $size5
draw string 7.75 $y0 $val10
set line 31
draw mark 3 8 $y8 $size5
set line 1
draw mark 2 8 $y8 $size5

set line 50
draw mark 3 9 $y8 $size5
set line 15
draw mark 2 9 $y8 $size5
set line 1
draw string 9.25 $y0 P>${FORM_greycut}%
"
  fi
fi
fi # nocbar

if [ -z "$grads20" ]; then
    printeps="enable print $f.gm
print
disable print"
else
    printeps="print $f.eps"
fi

export HOME=/tmp
if [ ${FORM_mapformat:-png} = geotiff ]; then
	$DIR/bin/grads -l -b -c 'run grads/startup.gs' << EOF > /tmp/grads$id.log
$map
set xlab off
set ylab off
set grid off
set gxout geotiff
set geotiff $f.tif
run plotbox $plotlist $scale ${FORM_col:-bw} $FORM_greycut 1$label $FORM_var $FORM_cmax
quit
EOF
	
	size=`wc -c $f.tif | sed -e 's/data.*//'`
	if [ "$size" -lt 50 ];then
		echo "Something went wrong!"
		echo "<pre>"
		cat /tmp/grads$id.log
		rm /tmp/grads$id.log
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
	echo "<p>"
	echo "<a href=\"$f.tif\">GeoTIFF</a> of"

else # normal PNG figure
	$DIR/bin/grads -l -b -c 'run grads/startup.gs' << EOF > /tmp/grads$id.log
$map
$setxlint
$setylint
$grid
set gxout contour
run plotbox $plotlist $scale ${FORM_col:-bw} $FORM_greycut 1$label $FORM_var $FORM_cmax
$legenda
$drawtitle
printim $f.png white $doublesize
$printeps
quit
EOF
	
	if [ -s $f.png ];then
	  if [ "$lwrite" = true ]; then
		echo '<pre>'
		cat /tmp/grads$id.log
		echo '</pre>'
	  fi
	  [ -f /tmp/grads$id.log ] && rm /tmp/grads$id.log  
	else
	  echo "Something went wrong!"
	  echo "<pre>"
	  cat /tmp/grads$id.log
	  echo "</pre>"
	  . ./myvinkfoot.cgi
	  exit
	fi
	
	# scale PNG 
	(pngtopnm $f.png | pnmscale 0.5 | pnmcrop | pnmtopng > $f.new.png) 2> /dev/null
	mv $f.new.png $f.png
	
	if [ -z "$grads20" ]; then
		# convert to EPS
		echo "<p>Converting to postscript with <a href=\"http://www.bol.ucla.edu/~munnich/grads/gxeps.html\" target=_top>gxeps</a>...<p>"
		
		$DIR/bin/gxeps -c -d -i $f.gm
		rm $f.gm
	fi
	gzip $f.eps &
	echo "<div class=\"bijschrift\">$title (<a href=\"$f.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=$f.eps.gz\">pdf</a>)"
	if [ "$hiresmap" = true ]; then
		pngfile=$f.png
		getpngwidth
		echo "<center><img src=\"$f.png\" alt=\"$title\" width=$halfwidth><br clear=all></center>"
	else
		echo "<center><img src=\"$f.png\" alt=\"$title\"></center>"
	fi
fi # mapformat

. ./myvinkfoot.cgi
