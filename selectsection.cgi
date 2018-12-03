#!/bin/bash
. ./init.cgi
export PATH=./bin:/usr/local/bin:/sw/bin:/usr/local/free/installed/nco-3.9.1/bin:/usr/local/free/bin:$PATH

###dailyserver=localhost/~oldenbor/climexp
dailyserver=climexp

if [ -z "$EMAIL" ]; then
  . ./getargs.cgi
  CLASS=$FORM_CLASS
  [ "$FORM_level" = choose -o "$FORM_level" = range ] && FORM_level=""
  echo 'Content-Type: text/html'
  echo
  echo
fi
if [ "$EMAIL" = oldenbor@knmi.nl ]; then
	lwrite=true
fi

. ./nosearchengine.cgi
. ./checkemail.cgi

. ./selectdataset.cgi

if [ ${CLASS:-choose} = choose ]
then
  . ./myvinkhead.cgi Error downloading
  echo "Unknown dataset: $CLASS"
  . ./myvinkfoot.cgi
  exit
fi
subtitle=`echo "$CLASS $FORM_expid $FORM_analysis $FORM_var" | tr '_/' '  '`
. ./myvinkhead.cgi "Downloading a $timescale 2D field" "$subtitle" "index,nofollow"

echo `date` "$EMAIL ($REMOTE_ADDR) selectsection $CLASS $FORM_expid $FORM_analysis $FORM_var z$FORM_level y$FORM_lat x$FORM_lon" >> log/log

if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "<li>Anonymous users cannot retrieve non-local data</ul>"
  . ./myvinkfoot.cgi
  exit
fi

[ -n "$FORM_oper" ] && . ./save_daily2longer.cgi

# built the ncks statement to download to netcdf
# ncks in case the file is downloaded directly (monthly data)
# args in case it is retrieved indirectly (daily data)
[ "$lwrite" = true ] && which ncks

if [ ${CLASS#ENSEMBLES_RT} != $CLASS -o $CLASS = ENSEMBLES_AMMA -o $CLASS = Prudence ]; then
  path=$path$file/$FORM_expid
  files=`echo "$FORM_varlist" | tr ' \r' '\n ' | egrep "_$FORM_var\.nc\.gz|^$FORM_var\."`
  file=`echo "$files" | tr ' \r' '\n ' | head -1`
  # strip trailing spaces
  files=${files% }
  file=${file% }
  [ "$lwrite" = true ] && echo "files=$files<br>"
else
  files=$file
fi
[ "$lwrite" = true ] && echo "path=$path<br>file=$file<br>"
# dataset and variable
ncks="ncks -p $path $file -v $FORM_var"
args=" -d EMAIL=$EMAIL -d CLASS=$CLASS -d id=$FORM_expid -d var=$FORM_var"
root="${FORM_var}_${CLASS}"
if [ -n "$FORM_expid" ]; then
  root=${root}_`echo ${FORM_expid}|tr '/' '_'`
fi

# time steps
if [ -n "$FORM_analysis" ]
then
  if [ "$lwrite" = true ]; then
    echo '<pre>'
    echo "bin/convertmetadata $path/$file convert reftime $FORM_analysis"
    bin/convertmetadata $path/$file convert reftime $FORM_analysis
    echo '</pre>'
  fi
  formatlist=`bin/convertmetadata $path/$file convert reftime $FORM_analysis`
  for format in $formatlist
  do
    ncks="$ncks -d time,$format"
  done
  args="$args -d analysis=$FORM_analysis"
  root="${root}_${FORM_analysis}"
fi

# level
if [ "${FORM_level:-range}" != range ]; then
  ncks="$ncks -d $level,$FORM_level"
  args="$args -d level=$FORM_level"
  root="${root}_${FORM_level%.00}"
fi

# latitude
if [ "${FORM_lat:-range}" != range ]; then
  ncks="$ncks -d $latitude,$FORM_lat"
  args="$args -d lon=$FORM_lat"
  root="${root}_${FORM_lat%.00}N"
fi

# longitude
if [ "${FORM_lon:-range}" != range ]; then
  ncks="$ncks -d $longitude,$FORM_lon"
  args="$args -d lon=$FORM_lon"
  root="${root}_${FORM_lon%.00}E"
fi

# coordinates
if [ "$FORM_lon1" != "$FORM_firstlon" -o \
     "$FORM_lon2" != "$FORM_lastlon" -o \
     "$FORM_lat1" != "$FORM_firstlat" -o \
     "$FORM_lat2" != "$FORM_lastlat" ]; then
  if [ "$FORM_lon1" != "$FORM_lon2" ]; then
    ncks="$ncks -d $longitude,$FORM_lon1,$FORM_lon2"
    root="${root}_${FORM_lon1}-${FORM_lon2}E"
  else
    ncks="$ncks -d $longitude,$FORM_lon1"
    root="${root}_${FORM_lon1}E"
  fi
  if [ "$FORM_lat1" != "$FORM_lat2" ]; then
    ncks="$ncks -d $latitude,$FORM_lat1,$FORM_lat2"
    root="${root}_${FORM_lat1}-${FORM_lat2}E"
  else
    ncks="$ncks -d $latitude,$FORM_lat1"
    root="${root}_${FORM_lat1}E"
  fi
  [ -n "$FORM_lon1" ] && args="$args -d lon1=$FORM_lon1"
  [ -n "$FORM_lon2" ] && args="$args -d lon2=$FORM_lon2"
  [ -n "$FORM_lat1" ] && args="$args -d lat1=$FORM_lat1"
  [ -n "$FORM_lat2" ] && args="$args -d lat2=$FORM_lat2"
fi

# data reducting parameters
if [ $timescale = daily ]; then
  [ -n "$FORM_nperyearnew" ] && args="$args -d nperyearnew=$FORM_nperyearnew"
  [ -n "$FORM_oper" ] && args="$args -d oper=$FORM_oper"
  [ -n "$FORM_lgt" ] && args="$args -d lgt=$FORM_lgt"
  [ -n "$FORM_cut" ] && args="$args -d cut=$FORM_cut"
  [ -n "$FORM_typecut" ] && args="$args -d typecut=$FORM_typecut"
fi

# ensemble members
if [ $CLASS = Demeter -o $CLASS = ENSEMBLES_stream_1_ocean ]; then
  expid=experiment_id
else
  expid=source
fi
site=${path##http://}
site=${site%%/*}
if [ -z "$FORM_enslist" ]; then
  FORM_enslist=`bin/convertmetadata $path/$file convert $expid $FORM_expid | tr '\n' ' '`
fi
if [ -n "$FORM_nens1" -a "$FORM_nens1" != "$FORM_nens2" ]
then
  offset=`echo $FORM_enslist | cut -f 1 -d ' '`
  if [ $FORM_nens1 != $offset ]; then
    echo "error: can only download multiple ensemble members starting from 0, but found first member $FORM_nens1 and offset $offset"
    . ./myvinkfoot.cgi
    exit
  fi
  iens=$FORM_nens1
  while [ $iens -le "$FORM_nens2" ]
  do
    ens="-d ensemble,$iens"
    aens="-d iens=$iens"
    i=$(($iens - $FORM_nens1))
    if [ $i -lt 10 ]; then
      outfile="data/${root}_0$i.nc"
    else
      outfile="data/${root}_$i.nc"
    fi
    if [ -s $outfile ]; then
      echo "Using cached ensemble member $i<br>"
    else
      echo "Retrieving $timescale ensemble member $i from $site."
      [ $iens = "$FORM_nens1" ] && echo "<br>This may take a while, please be patient. If the connection is dropped please reload this page.<p>"
      if [ $timescale = daily ]; then
        # daily data, indirectly
        flatten=mv
	[ "$lwrite" = true ] && echo "curl -s $args $aens http://$dailyserver/selectdailysection.cgi data/tmp$$.nc"
	(curl -s $args $aens http://$dailyserver/selectdailysection.cgi > data/tmp$$.nc 2>&1)&
      else
        # monthly data, directly from server
        [ "$lwrite" = true ] && echo "$ncks $ens data/tmp$$.nc"
        ($ncks $ens data/tmp$$.nc > /tmp/ncks$$.$iens.log 2>&1) &
        i=1
        c=1
        while [ $c -gt 0 ]; do
          sleep 5
          echo "$((i++)) "
          [ $((12*((i-1)/12))) = $((i-1)) ] && echo '<p>'
          [ "$lwrite" = true ] && (ps axuw | fgrep data/tmp$$$ext.nc | fgrep -v grep) && echo '<p>'
          c=`ps axuw | fgrep data/tmp$$$ext.nc | fgrep -v grep | wc -l`
        done
      fi
      ncdump -h data/tmp$$.nc > /dev/null 2>&1
      if [ $? != 0 ]; then
      	echo "Something went wrong downloading the data. Please try again."
        . ./myvinkfoot.cgi
        exit   	
      fi
      [ "$lwrite" = true ] && echo $flatten data/tmp$$.nc $outfile
      $flatten data/tmp$$.nc $outfile 2>&1
      if [ $? != 0 ]; then
        echo "Abort"
        . ./myvinkfoot.cgi
        exit
      fi
      rm /tmp/ncks$$.$iens.log data/tmp$$.nc
      if [ $CLASS = Demeter -o ${CLASS##ENSEMBLES} != $CLASS ]; then
        ncatted -h -O -a Source,global,a,c,$path/$file $outfile
      fi
    fi
    iens=$(($iens + 1))
  done
  outfile="data/${root}_%%.nc"
else
  if [ -n "$FORM_nens1" ]; then
    root="${root}_${FORM_nens1}"
    ncks="$ncks -d ensemble,$FORM_nens1"
    args="$args -d iens=$FORM_nens1"
  fi
  outfile="data/$root.nc"
  if [ -s $outfile ]; then
    echo "Using cached data<p>"
  else
    echo "Retrieving $timescale data from $site.  This may take a while, depending on file size and how busy the server is.  If the connection is dropped please check <a href=\"selectfield_use.cgi?id=$EMAIL\">here</a> to see if the field has been downloaded anyway.<p>"
    if [ $timescale = daily ]; then
      # daily data, indirectly
      flatten=mv
      [ "$lwrite" = true ] && echo "curl -s $args $aens http://$dailyserver/selectdailysection.cgi data/tmp$$.nc"
      (curl -s $args $aens http://$dailyserver/selectdailysection.cgi > data/tmp$$.nc 2>&1)&
    else
      # monthly data, directly from server
      # there are some multiple time slices in the ENSEMBLES RT2b data
      ifile=0
      touch /tmp/ncks$$.log
      for thisfile in $files
      do
        if [ "$file" = "$files" ]; then
          [ "$lwrite" = true ] && echo "$ncks data/tmp$$.nc"
          ($ncks data/tmp$$.nc >> /tmp/ncks$$.log 2>&1) &
	  ext=""
	else
	  ifile=$((ifile+1))
	  ext=.$ifile
	  # adjust statement
	  thisncks=`echo $ncks | sed -e "s/$file/$thisfile/"`
          [ "$lwrite" = true ] && echo "$thisncks data/tmp$$$ext.nc"
          ($thisncks data/tmp$$$ext.nc >> /tmp/ncks$$.log 2>&1) &	    
        fi
        i=1
        c=1
        while [ $c -gt 0 ]; do
          sleep 5
          echo "$((i++)) "
	  [ $((12*((i-1)/12))) = $((i-1)) ] && echo '<p>'
          c=`ps axuw | fgrep data/tmp$$$ext.nc | fgrep -v grep | wc -l`
        done
	[ -n "ext" ] && echo "<p>"
      done
      if [ -n "$ext" ]; then
        [ "$lwrite" = true ] && echo "cdo copy data/tmp$$.*.nc data/tmp/$$.nc"
        cdo copy data/tmp$$.*.nc data/tmp$$.nc
        rm data/tmp$$.*.nc
      fi
    fi
    echo "Converting data<p>"
    [ "$lwrite" = true ] && echo $flatten data/tmp$$.nc $outfile
    $flatten data/tmp$$.nc $outfile 2>&1
    if [ $? != 0 ]; then
      echo "Abort"
      . ./myvinkfoot.cgi
      exit
    fi
    rm data/tmp$$.nc
    if [ $CLASS = Demeter -o ${CLASS##ENSEMBLES} != $CLASS ]; then
      ncatted -h -O -a Source,global,a,c,$path/$file $outfile
    fi
  fi  
fi

# construct a user-defined field

eval `bin/getunits $outfile`
infofile=data/$root.$EMAIL.info
[ ${FORM_level:-range} != range ] && lev=${FORM_level%.00}
cat > $infofile <<EOF
$outfile
NPERYEAR=$NPERYEAR
UNITS=$UNITS
$classname $FORM_expid $FORM_analysis
$FORM_var$lev
EOF

# and continue

if [ -n "$FORM_lon1" -a "$FORM_lon1" = "$FORM_lon2" \
  -a -n "$FORM_lat1" -a "$FORM_lat1" = "$FORM_lat2" ]; then
# single point - convert to a time series
  STATION="$FORM_var $CLASS $FORM_expid $FORM_analysis"
  export WMO=`basename $outfile .nc | sed -e 's/%%/++/'`
  export TYPE=i
  export file=$outfile
  NAME=index
  DIR=`pwd`
  PROG="netcdf2dat.sh $outfile"
  . ./getdata.cgi
else
# whole field
  export EMAIL
  export FORM_field="$infofile"
  . ./select.cgi
fi
