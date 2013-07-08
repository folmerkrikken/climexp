#!/bin/sh
. ./init.cgi

tmpdir=/tmp
export PATH=/usr/local/free/installed/nco-3.9.1/bin:/usr/local/free/bin:/usr/local/bin:/opt/local/bin:$PATH

server=$HTTP_HOST:$SERVER_PORT
if [ "$HOST" = "bhw080" ]; then
  server="$server/~oldenbor/climexp"
fi

. ./getargs.cgi
CLASS=$FORM_CLASS
[ "$FORM_level" = choose ] && FORM_level=""
lwrite=$FORM_lwrite
if [ -n "$lwrite" ]; then
  echo 'Content-Type: text/plain'
else
  echo 'Content-Type: data/netcdf'
fi
echo

if [ "${REMOTE_ADDR#145.23}" = "$REMOTE_ADDR}" -a "$REMOTE_ADDR" != 127.0.0.1 ]
then
  echo "Access is only allowed from localhost and KNMI, not $REMOTE_ADDRESS"
  exit -1
fi

if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "<li>Anonymous users cannot retrieve non-local data</ul>"
  exit
fi

. ./selectdataset.cgi

# built the ncks statement to download to netcdf

# dataset and variable
ncks="ncks -p $path $file -v $FORM_var"
root="${FORM_var}_${CLASS}"
if [ -n "$FORM_id" ]; then
  root=${root}_`echo ${FORM_id}|tr '/' '_'`
fi

# time steps
if [ -n "$FORM_analysis" ]
then
  if [ 0 = 1 ]; then
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
  root="${root}_${FORM_analysis}"
fi

# level
if [ -n "$FORM_level" ]; then
  ncks="$ncks -d level,$FORM_level"
  root="${root}_${FORM_level%.00}"
fi

# coordinates
if [ "$FORM_lon1" != "$FORM_firstlon" -o \
     "$FORM_lon2" != "$FORM_lastlon" -o \
     "$FORM_lat1" != "$FORM_firstlat" -o \
     "$FORM_lat2" != "$FORM_lastlat" ]; then
  if [ "$FORM_lon1" != "$FORM_lon2" ]; then
    ncks="$ncks -d longitude,$FORM_lon1,$FORM_lon2"
    root="${root}_${FORM_lon1}-${FORM_lon2}E"
  else
    ncks="$ncks -d longitude,$FORM_lon1"
    root="${root}_${FORM_lon1}E"
  fi
  if [ "$FORM_lat1" != "$FORM_lat2" ]; then
    ncks="$ncks -d latitude,$FORM_lat1,$FORM_lat2"
    root="${root}_${FORM_lat1}-${FORM_lat2}E"
  else
    ncks="$ncks -d latitude,$FORM_lat1"
    root="${root}_${FORM_lat1}E"
  fi
fi

# longer time scales

wortel=`echo $root | tr ' ' '_'`
if [ ${FORM_nperyearnew:-366} -gt 73 ]; then
  echo "Can only produce pentad or longer timescales, not " $FORM_nperyearnew "values per year."
  exit -1
fi
corrargs="$FORM_nperyearnew $FORM_oper"
root="${root}_$FORM_oper$FORM_nperyearnew"
if [ "$FORM_lgt" = "lt" -o "$FORM_lgt" = "gt" ]; then
  if [ -z "$FORM_cut" -a "$FORM_typecut" != "n" ]; then
    FORM_cut=0
  fi
  corrargs="$corrargs $FORM_lgt $FORM_cut$FORM_typecut"
  root="${root}_$FORM_lgt$FORM_cut$FORM_typecut"
fi
root=`echo "$root" | tr ' ' '_'`

# ensemble members
if [ $CLASS = Demeter -o $CLASS = ENSEMBLES_stream_1_ocean ]; then
  id=experiment_id
else
  id=source
fi
if [ -n "$FORM_iens" ]; then
  ncks="$ncks -d ensemble,$FORM_iens"
  root="${root}_$FORM_iens"
fi

outfile="$tmpdir/${root}.nc"
uitfile="$tmpdir/${root}_temp.nc"
if [ ! -s $outfile ]; then
  if [ ! -s $uitfile ]; then
    [ -n "$lwrite" ] && echo $ncks $tmpdir/tmp$$.nc
    $ncks $tmpdir/tmp$$.nc
    [ -n "$lwrite" ] && echo bin/flattennc $tmpdir/tmp$$.nc $uitfile
    bin/flattennc $tmpdir/tmp$$.nc $uitfile
    rm $tmpdir/tmp$$.nc
  fi
  [ -n "$lwrite" ] && echo bin/daily2longerfield $uitfile $corrargs $outfile
  bin/daily2longerfield $uitfile $corrargs $outfile
  rm $uitfile
  [ -n "$lwrite" ] && echo ncatted -h -O -a Source,global,a,c,$path/$file $outfile
  ncatted -h -O -a Source,global,a,c,$path/$file $outfile
fi

if [ -n "$lwrite" ]; then
  ls -l $outfile
else
  cat $outfile
fi

exit
