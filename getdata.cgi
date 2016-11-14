#!/bin/sh
. ./init.cgi
# should be sourced from one of the get* scripts
lwrite=false
if [ "$EMAIL" = oldenborgh@knmi.nl -o $REMOTE_ADDR = 127.0.0.1 ]; then
    lwrite=false # true
fi
if [ -z "$myvinkhead" ]; then
  echo 'Content-Type: text/html'
  if [ -n "$LASTMODIFIED" ]; then
    echo "Last-Modified: $LASTMODIFIED"
  fi
  . ./expires.cgi
  echo
  echo
  # do not work too hard!  although I have not yet seen this in practice
  if [ "$REQUEST_METHOD" = "HEAD" ]
  then 
    exit
  fi
fi

# check if search engine
. ./searchengine.cgi

# check email address
. ./checkemail.cgi

if [ -z "$ROBOT" ]; then
echo `date` "$EMAIL ($REMOTE_ADDR) $NAME $STATION ($WMO)" >> log/log
###else
###echo `date` "$HTTP_USER_AGENT ($REMOTE_ADDR) $NAME $STATION ($WMO)" >> log/log
fi

# start real work
if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12
fi
. ./nperyear2timescale.cgi
station=`echo "$STATION" | tr '_' ' '`
. ./myvinkhead.cgi "Time series" "$timescale $station $NAME" "index,nofollow"

if [ -n "$warning" ]; then
    echo "$warning<p>"
fi

if [ "$lwrite" = true ]; then
    echo "WMO=$WMO<br>"
    echo "PROG=$PROG<br>"
    echo "extraargs=$extraargs<br>"
    echo "doit=$doit<br>"
fi

# if a mask has been used in the construction of the time series, plot it and enable its download
if [ -n "$masknetcdf" ]; then
    i=0
    c=1
    while [ ! -s "$masknetcdf" -a $c != 0 -a $i -lt 100 ]; do
        i=$((i+1))
        c=`ps axuw | fgrep polygon2mask | fgrep -v grep | wc -l`
        if [ "$lwrite" = true ]; then
            ps axuw | fgrep polygon2mask | fgrep -v grep
            echo "<br>i,c = '$i,$c<br>"
        fi
        if [ $c -gt 0 ]; then
            [ $((i%10)) = 1 ] && echo "Computing mask...<p>"
            sleep 3
        fi
    done
	if [ ! -s "$masknetcdf" ]; then
		echo "Something went wrong, cannot locate gridded mask file $masknetcdf<br>"
		echo "Please contact <a href=\"mailto:oldenborgh@knmi.nl\">me</a> about this. I need the following command:<br> $polycommand"
		if [ "$lwrite" = true ]; then
            echo "<br>"
            ls -l "$masknetcdf"
            echo "<br>i,c = $i,$c<br>"
            date
            echo "<br>"
            ps axuw | fgrep polygon2mask
            echo "<br>"
            ps axuw | fgrep polygon2mask | fgrep -v grep | wc -l
		fi
		. ./myvinkfoot.cgi
	fi

    cat <<EOF
Download <a href="$masknetcdf">mask file</a>
EOF
	FORM_var=mask
	oldfile=$file
	file=$masknetcdf
	oldnperyear=$NPERYEAR
	NPERYEAR=1
    FORM_year=0001 # grads puts netcdf files without date on 1:1:1:0
    m=jan
    oldstation=$station
    oldCLIM=$CLIM
	station=$kindname
	CLIM=$climfield
	. ./getfieldopts.cgi # set lat/lon etc
	. ./grads.cgi
	NPERYEAR=$oldnperyear
    station=$oldstation
    CLIM=$oldCLIM
    file=$oldfile
fi

wmo=$WMO
WMO=`basename "$WMO"`
if [ "${wmo#data}" != "$wmo" ]; then
  WMO=${WMO##i}
fi
TYPE=`basename "$TYPE"`
# if the output file exists and is newer than the input file skip this step
# doit is set to true by getindices if some ensemble members are missing, 
# this can happen in practice :-(
if [ -n "$file" -a -s "$file" -a -s ./data/$TYPE$WMO.dat -a ./data/$TYPE$WMO.dat -nt "$file" -a "$doit" != true ]; then
    [ "$lwrite" = true ] && echo "Skipping generating the data, already there"
    skipit=true
else
    skipit=false
fi
if [ $skipit = false -a -n "$PROG" -a \( -z "$ROBOT" -o "$PROG" = getindices \) ];then
  echo "Retrieving data $FROM ...<p>"
  if [ "$NPERYEAR" -ge 360 -o -n "$kill" ]; then
    echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the data extraction job)</small><p>"
    export FORM_EMAIL=$EMAIL
    export SCRIPTPID=$$
    cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
$PROG
@
EOF
  fi
  if [ "$lwrite" = true ]; then
    echo "./bin/$PROG $wmo<br>"
    echo "file = $file<br>"
    echo "TYPE = $TYPE<br>"
    echo "WMO = $WMO<br>"
    echo "PROG = $PROG<br>"
  fi
  if [ "$makenetcdf" = true ]; then
      (./bin/$PROG $wmo ./data/$TYPE$WMO.dat ) 2>&1
  else
      (./bin/$PROG $wmo > ./data/$TYPE$WMO.dat.$$ ) 2>&1
  fi
  return=$?
  return=0
  if [ "$return" != 0 ]; then
    echo "Something went wrong, return value $return"
    rm -f pid/$$.$EMAIL
    echo "<pre>"
    echo $DIR/bin/$PROG $wmo
    echo "</pre>"
    . ./myvinkfoot.cgi
    exit
  fi
  rm -f pid/$$.$EMAIL
  # in case two people retrieve the same data at the same time - make atomic
  [ -s $DIR/data/$TYPE$WMO.dat.$$ ] && mv $DIR/data/$TYPE$WMO.dat.$$ $DIR/data/$TYPE$WMO.dat
  fgrep 'annot locate' $DIR/data/$TYPE$WMO.dat
  if [ $? = 0 ]; then
	echo '<pre>'
	cat $DIR/data/$TYPE$WMO.dat
	echo "</pre>"
        . ./myvinkfoot.cgi
	exit
  fi
  [ "$lwrite" = true ] && echo "<p>extraargs=$extraargs<p>"
  if [ -n "$extraargs" ]; then
    infile=./data/$TYPE$WMO.dat
    WMO=$WMO`echo $extraargs | tr ' ' '_'`_$NPERYEAR
    outfile=./data/$TYPE$WMO.dat
    daily2longer $infile `echo $extraargs | tr '_' ' '` > $outfile
  fi
else
    if [ -z "$PROG" -o $skipit = true ]; then
        if [ 0 = 1 ]; then
            if [ -z "$PROG" ]; then
                echo "PROG unset, data should be there"
            else
                echo "skipit = true, data should be there"
            fi
            echo '<pre>'
            echo "TYPE=$TYPE"
            echo "WMO=$WMO"
            ls -l data/$TYPE$WMO.dat 2>&1
            echo '</pre>'
        fi
    fi
fi
c1=`echo $WMO | fgrep -c '++'`
c2=`echo $WMO | fgrep -c '%%'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
  firstfile=`echo ./data/$TYPE$WMO.dat | sed -e 's/%%%/000/' -e 's/+++/000/' -e 's/%%/00/' -e 's/++/00/'`
  if [ ! -s $firstfile ]; then
    firstfile=`echo ./data/$TYPE$WMO.dat | sed -e 's/%%%/001/' -e 's/+++/001/' -e 's/%%/01/' -e 's/++/01/'`
  fi
else
  firstfile=./data/$TYPE$WMO.dat
fi
if [ ! -s $firstfile ]; then
  if [ -n "$ROBOT" ]; then
    echo "For search engines this data is not retrieved."
  else
    # something went wrong
    echo `date`" $REMOTE_ADDR error: could not find ./data/$TYPE$WMO.dat" 1>&2
    echo "Something went wrong.  Please contact <a href=\"mailto:oldenborgh@knmi.nl\">me</a>"
  fi
  VAR="unknown"
  UNITS="unknown"
  NEWUNITS="unknown"
else
    # speed up subsequent operations
    ncfile=${firstfile%.dat}.nc
    if [ ! -s $ncfile -o $ncfile -ot $firstfile ]; then
        [ -f $ncfile ] && rm $ncfile
        [ "$lwrite" = true ] && echo "dat2nc $firstfile $TYPE "$STATION" $ncfile<br>"
        dat2nc $firstfile ${TYPE:-i} "$STATION" $ncfile
    fi
    eval `./bin/getunits $firstfile`
    if [ -z "$VAR" ]; then
    # something went wrong
        echo `date`" $REMOTE_ADDR error: getunits failed for ./data/$TYPE$WMO.dat" 1>&2
    fi
    if [ -n "$ENSEMBLE" ]; then
        # also generate netcdf files for the rest of the ensemble
        ensfile=$firstfile
        i=0
        while [ -s $ensfile ]; do
            ncfile=${ensfile%.dat}.nc
            if [ ! -s $ncfile -o $ncfile -ot $ensfile ]; then
                [ -f $ncfile ] && rm $ncfile
                [ "$NPERYEAR" -ge 360 ] && echo "Converting $i to netcdf<p>"
                [ "$lwrite" = true ] && echo "dat2nc $firstfile $TYPE "$STATION" $ncfile<br>"
                dat2nc $ensfile ${TYPE:-i} "$STATION" $ncfile
            fi
            i=$((i+1))
            ii=`printf %02i $i`
            iii=`printf %03i $i`
            ensfile=`echo ./data/$TYPE$WMO.dat | sed -e "s/%%%/$iii/" -e "s/+++/$iii/" -e "s/%%/$ii/" -e "s/++/$ii/"`
        done
    fi
fi

if [ "$TYPE" = "i" -a "$EMAIL" != "someone@somewhere" ]; then
  if [ ! -f ./data/$TYPE$WMO.$NPERYEAR.$EMAIL.inf ]; then
    inffile=./data/$TYPE$WMO.$NPERYEAR.$EMAIL.inf
    echo data/$TYPE$WMO.dat > $inffile
    echo "$STATION" | tr ' ' '_' >> $inffile
    echo "$WMO" >> $inffile
  fi
fi
###echo "<div class=\"alineakop\">Timeseries</div>"

###echo '<p>Converting data...'
###echo "$DIR/bin/plotdat $DIR/data/$TYPE$WMO.dat | fgrep -v 'disregarding' > $DIR/data/$TYPE$WMO.txt"
if [ -s $firstfile ]; then
  if [ \( ! -s ./data/$TYPE$WMO.txt \) -o ./data/$TYPE$WMO.dat -nt ./data/$TYPE$WMO.txt ]; then
    ( ./bin/plotdat $DIR/data/$TYPE$WMO.dat | fgrep -v 'disregarding' > ./data/$TYPE$WMO.txt ) 2>&1
    c=`cat $DIR/data/$TYPE$WMO.txt | fgrep -v '#' | wc -l`
    if [ $c -eq 0 ]; then
      mv data/$TYPE$WMO.dat data/$TYPE$WMO.dat.wrong
      [ -f data/$TYPE$WMO.nc ] && rm data/$TYPE$WMO.nc
      echo "No valid data were found.  Please check your choices on the previous page.<br>"
      echo "Having a look at the <a href=\"data/$TYPE$WMO.dat.wrong\">raw data</a> might help."
      if [ "${PROG#get_index}" != "$PROG" ]; then
      	echo "<p>Often, this is caused by selecting an area without data, for instance a sea area in a dataset with only land data or the other way around."
      	echo "You can make a map of the mean values in the region (<a href=\"/getmomentsfieldform.cgi?id=$EMAIL&field=$FORM_field\">Compute mean, s.d. or extremes</a>) to determine where the dataset has data."
      	echo "<font color=\"#FF2222\">An unfixed bug in the area averaging routine sometimes also gives this. Please retry one or two times...</font>"
      fi
      . ./myvinkfoot.cgi  
      exit
    fi
  fi
###  echo "Plotting data:"
  echo '<div class="bijschrift">'
  egrep '^#' data/$TYPE$WMO.dat | fgrep -v 'bin/' | egrep -v -i '(jan *feb)|(VRIJ WORDEN GEBRUIKT)|(CAN BE USED)|(ROYAL NETHERLANDS METEOROLOGICAL INSTITUTE)|(^# Searching )|(non-commercial )|(any commercial)|(intentionally)|(coauthors)|(1441-1453)' | grep -v '^ *$' | sed -e 's/^#//' -e 's/^.#//' -e 's/$/,/' -e 's/^ *, *//' | tr '_' ' ' | sed -e 's/antieke wrn/antieke_wrn/'
  [ -n "$UNITS" ] && plotunits="[$UNITS]"
  if [ \( ! -s $DIR/data/$TYPE$WMO.png \) -o \( ! -s $DIR/data/$TYPE$WMO.eps.gz \) -o $DIR/data/$TYPE$WMO.png -ot $DIR/data/$TYPE$WMO.dat ]; then
    wmo_=`echo $WMO | tr '_' ' '`
    var_=`echo $VAR | tr '_' ' '`
    name_=`echo $NAME | tr '_' ' '`
    station_=`echo $station | tr '_' ' '`
    ./bin/gnuplot << EOF
$gnuplot_init
set xzeroaxis
set size .7057,.4
set term postscript epsf color solid
set output "$DIR/data/$TYPE$WMO.eps"
set ylabel "$var_ $plotunits"
plot "$DIR/data/$TYPE$WMO.txt" title "$name_ $station_ ($wmo_)" with steps
set term png $gnuplot_png_font_hires
set out "$DIR/data/$TYPE$WMO.png"
replot
quit
EOF
    gzip -f $DIR/data/$TYPE$WMO.eps &
  fi
  if [ -n "$ENSEMBLE" ]; then
    mywmo=`echo $WMO | tr '+' '%'`
    mystation=`echo $STATION | tr ' +' '_%'`
    cat << EOF 
(<a href="data/$TYPE$WMO.eps.gz">eps</a>, <a href="ps2pdf.cgi?file=data/$TYPE$WMO.eps.gz">pdf</a>, <a href="rawdata.cgi?wmo=$mywmo&station=$mystation&type=$TYPE&id=$EMAIL&nperyear=$NPERYEAR">raw data</a>)
EOF
  else
    c=`echo "$HTTP_USER_AGENT" | fgrep -i -c 'MSIE'`
    if [ $c != 0 ]; then
      echo "(<a href=\"data/$TYPE$WMO.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=data/$TYPE$WMO.eps.gz\">pdf</a>, <a href=\"data/$TYPE$WMO.dat\">raw data</a>, <a href=\"dat2nc.cgi?datafile=data/$TYPE$WMO.dat&type=$TYPE&station=$STATION&id=$EMAIL\">netcdf</a>, <a href=\"dat2dos.cgi?file=data/$TYPE$WMO.dat\">DOS</a>)"
    else
      echo "(<a href=\"data/$TYPE$WMO.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=data/$TYPE$WMO.eps.gz\">pdf</a>, <a href=\"data/$TYPE$WMO.dat\">raw data</a>, <a href=\"dat2nc.cgi?datafile=data/$TYPE$WMO.dat&type=$TYPE&station=$STATION&id=$EMAIL\">netcdf</a>)"
    fi    
  fi
  pngfile=data/$TYPE$WMO.png
  getpngwidth
  cat <<EOF
</div>
<center>
<img src="data/$TYPE$WMO.png" alt="time series" width="$halfwidth" border=0 class="realimage" hspace=0 vspace=0>
<br>
</center>
EOF
  name=`echo $NAME | tr ' +' '_%'`
  wmo=`echo $WMO | tr '+' '%'`
  STATION=`echo $STATION | tr '+' '%'`
else
# robots, other errors.
  echo "<p>Cannot locate $TYPE$WMO.dat ($firstfile)"
###  echo "<p>Here a plot of the data would be shown"
fi

if [ -s ./data/$TYPE$WMO.dat -a "$WMO" != "time" ]; then
  . ./plot_anomalies.cgi
fi

if [ $NPERYEAR -gt 12 ]; then
    . ./count_missing.cgi
fi

if [ -n "$ROBOT" ]; then
  . ./myvinkfoot.cgi
  exit
fi  

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.selectyears
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-z]*[-+0-9.]*;$' $def`
  fi
fi
cat << EOF
<div class=formheader>Manipulate this time series</div>
<div class=formbody>
<table border=0 cellpadding=0 cellspacing=0 style="width:445px;">
<tr><td>Select years:</td><td><form action="selectyear.cgi" method="post">
<input type="hidden" name="wmo"     value="$WMO">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="email"   value="$EMAIL">
<input type="hidden" name="type"    value="$TYPE">
<input type="hidden" name="name"    value="$NAME">
<input type="hidden" name="file"    value="$TYPE$WMO.dat">
<input type="$number" class="forminput" name="yr1" min=1 max=2500 step=1 size="4" style="width: 5em;" value="$FORM_yr1">-<input type="$number" min=1 max=2500 step=1 class="forminput" name="yr2" size="4" style="width: 5em;" value="$FORM_yr2">
<input type="submit" class="formbutton" value="select">
</form></td>
<td><a href="javascript:pop_page('help/selectyears.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
EOF
inffile=data/$TYPE$WMO.$NPERYEAR.$EMAIL.inf
type=$TYPE
# sometimes things go wrong...
if [ ! -f $inffile -a -f data/$WMO.$NPERYEAR.$EMAIL.inf ]; then
    inffile=data/$WMO.$NPERYEAR.$EMAIL.inf
    type=""
fi
if [ "$lwrite" = true ]; then
    echo "inffile=$inffile<br>"
    ls -l $inffile 2>& 1
    echo "<br>"
fi
if [ ! -s $inffile ]; then
    cat <<EOF
</td></tr><tr><td>Make index:</td><td>
<form action="makeindex.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="type" value="$type">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="text" class="forminput" name="newname" size=15 value="${TYPE}_${STATION}">
<input type="submit" class="formbutton" value="Add to list">
</form></td>
<td><a href="javascript:pop_page('help/makeindex.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td></tr>
EOF
else
    cat <<EOF
</td></tr><tr><td>Remove index:</td><td>
<form action="rmindex.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="type" value="$type">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" class="forminput" name="STATION" value="$STATION">
<input type="submit" class="formbutton" value="Remove from list">
</form></td>
<td><a href="javascript:pop_page('help/makeindex.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td></tr>
EOF
fi
if [ $NPERYEAR -gt 1 ]; then
  (FORM_field="";. ./filtermonthform.cgi)
  echo '</td></tr>'
fi
echo '<tr valign="top"><td>Filter consecutive years:</td><td>'
(FORM_field="";. ./filteryearform.cgi)
cat << EOF
<td align="right"><a href="javascript:pop_page('help/daily2longer.shtml',568,450)"><img src="images/info-i.gif" align="right" alt="help" border="0"></a></td>
</td></tr><tr><td>Scale series:</td><td>
<form action="scaleseries.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="type" value="$TYPE">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
Scale factor: <input type="$number" step=any class="forminput" name="factor" $textsize10>
<input type="submit" class="formbutton" value="Scale">
</form>
</td><td><a href="javascript:pop_page('help/scaleseries.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td></tr>
EOF
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.diffdat
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-z]*[-+0-9.]*;$' $def`
  fi
  case "$FORM_ndiff" in
      2) n2=selected;;
      3) n3=selected;;
      5) n5=selected;;
      7) n7=selected;;
      9) n9=selected;;
      11) n11=selected;;
      13) n13=selected;;
      15) n15=selected;;
      31) n31=selected;;
      *) n3=selected;;
  esac
  def=./prefs/$EMAIL.shift
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-z]*[-+0-9.]*;$' $def`
  fi
fi
cat <<EOF
<tr><td>Time derivative:</td><td>
<form action="diffdat.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="type" value="$TYPE">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
using <select class="forminput" name="ndiff">
<option $n2>2
<option $n3>3
<option $n5>5
<option $n7>7
<option $n9>9
<option $n11>11
<option $n13>13
<option $n15>15
<option $n31>31
</select> ${month}s
<input type="submit" class="formbutton" value="Take time derivative">
</form>
</td><td><a href="javascript:pop_page('help/derivativeseries.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td><td>&nbsp</td></tr>
<tr><td>Shift:</td><td>
<form action="shiftseries.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="type" value="$TYPE">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
Shift data by 
<input type="$number" step=any class="forminput" name="shift" $textsize4 value="$FORM_shift"> ${month}s.
<input type="submit" class="formbutton" value="Shift">
</td></tr><tr><td>Normalise:</td><td>
<form action="normdiff.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$name">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="myindex0" value="nothing">
Take anomalies and set standard deviation to one
</td><td><a href="javascript:pop_page('help/derivativeseries.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>&nbsp;<td>
<input type="radio" class="formradio" name="my1" value="monthly">for each $month separately
<tr><td>&nbsp;<td>
<input type="radio" class="formradio" name="my1" value="yearly">for all ${month}s together
<tr><td>&nbsp;<td>
<input type="submit" class="formbutton" value="Normalise">
</form>
</td></tr><tr><td>Combine:</td><td>
<a href="normdiffform.cgi?id=$EMAIL&TYPE=$TYPE&WMO=$wmo&STATION=$STATION&NAME=$name&NPERYEAR=$NPERYEAR">Combine with another timeseries to form a normalized index</a>
</td><td><a href="javascript:pop_page('help/combineseries.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
<tr><td>Mask out:</td><td><a href="maskseriesform.cgi?id=$EMAIL&TYPE=$TYPE&WMO=$wmo&STATION=$STATION&NAME=$name&NPERYEAR=$NPERYEAR">Mask out based on another time series</a>
</td><td><a href="javascript:pop_page('help/maskseries.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
<tr><td>Noise:</td><td><a href="ar1.cgi?id=$EMAIL&TYPE=$TYPE&WMO=$wmo&STATION=$STATION&NAME=$name&NPERYEAR=$NPERYEAR&n=100">Make 100 random series with the same mean, variance and autocorrelation</a>
</td><td><a href="javascript:pop_page('help/ar1.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
</table>
</div>
EOF

if [ $NPERYEAR = 360 -o $NPERYEAR = 365 -o $NPERYEAR = 366 ]; then
	if [ "$NEWUNITS" = "Celsius" -o "$NEWUNITS" = "mm/day" ]; then
		cat <<EOF
<p><div class='formheader'><a href="javascript:pop_page('help/extremeindices.shtml',568,450)"><img src="images/info-i.gif" align="right"alt="help" border="0"></a>Compute extreme indices</div>
<div class='formbody'>
<form action="extremeseries.cgi" method="POST">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
EOF
	. ./extremeform.cgi
	cat << EOF
<tr><td colspan=2><input type="submit" class="formbutton" value="make new time series">
</td></tr>
</table>
</form>
</div>
EOF
	fi # supported variable: temperature or precipitation
fi # daily data

if [ $NPERYEAR -gt 1 ]; then
    cat <<EOF
<p><div class='formheader'><a href="javascript:pop_page('help/lowerresolutionseries.shtml',568,450)"><img src="images/info-i.gif" align="right"alt="help" border="0"></a>Create a lower resolution time series</div>
<div class='formbody'>
<form action="daily2longer.cgi" method="POST">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
EOF
    . ./daily2longerform.cgi
    cat << EOF
<tr><td colspan=2><input type="submit" class="formbutton" value="make new time series">
</td></tr>
</table>
</form>
</div>
EOF
fi # NPERYEAR > 1

if [ $NPERYEAR = 1 ]; then
cat <<EOF
<p><div class='formheader'>Create a monthly time series</div>
<div class='formbody'>
<form action="yearly2shorter.cgi" method="POST">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
EOF
. $DIR/yearly2shorterform.cgi
cat << EOF
<tr><td colspan=2><input type="submit" class="formbutton" value="make new time series"></td></tr>
</form>
</table>
</div>
EOF
fi

if [ -n "$ENSEMBLE" ]; then
	cat <<EOF
<p><div class="formheader">Select ensemble member</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>
<form action="selectmembers.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="type" value="$TYPE">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="checkbox" class="formcheck" name="ensanom">Take anomalies relative to the ensemble mean<br>
<select class="forminput" name="nens1">
EOF
	c3=`echo $WMO | egrep -c '%%%|\+\+\+'`
	if [ $c3 = 0 ]; then
		nmax=100
	else
		nmax=1000
	fi
	i=0
	exist=true
	while [ $i -lt $nmax -a $exist = true ]
	do
		if [ $c3 = 0 ]; then
	    	if [ $i -lt 10 ]; then
				member=`echo $WMO | sed -e "s/\+\+/0$i/"`
    		else
    			member=`echo $WMO | sed -e "s/\+\+/$i/"`
    		fi
		else
	    	if [ $i -lt 10 ]; then
				member=`echo $WMO | sed -e "s/\+\+\+/00$i/"`
	    	elif [ $i -lt 100 ]; then
				member=`echo $WMO | sed -e "s/\+\+\+/0$i/"`
    		else
    			member=`echo $WMO | sed -e "s/\+\+\+/$i/"`
    		fi
		fi
    	if [ -f data/$TYPE$member.dat ]; then
      		echo "<option>$i"
      	elif [ $i -gt 5 ]; then
      	    exist=false
    	fi
    	i=$(($i + 1))
	done
	cat <<EOF
</select>
<input type="submit" class="formbutton" value="Select">
</form>
</td></tr>
</table>
</div>

<p><div class="formheader">Compute ensemble statistic</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>
<form action="average_ensemble.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="type" value="$TYPE">
<input type="hidden" name="wmo" value="$WMO">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
Operation: 
<input type="radio" class="formradio" name="oper" value="mean" checked>mean, 
<input type="radio" class="formradio" name="oper" value="min">min, 
<input type="radio" class="formradio" name="oper" value="max">max
<br>
Ensemble members: <input type="$number" min=0 step=1 size="3" style="width: 4em;" name="nens1"> to <input type="$number" min=0 step=1 size="3" style="width: 4em;" name="nens2"><br>
<input type="submit" class="formbutton" value="Compute">
</form>
</td></tr>
</table>
</div>

EOF
fi

. ./myvinkfoot.cgi
