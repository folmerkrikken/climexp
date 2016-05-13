#!/bin/sh
. ./init.cgi
. ./nosearchenginewithheader.cgi
echo "Content-type: text/html"
echo

. ./getargs.cgi
file="$FORM_file"
title="$FORM_title"

scriptname=`basename $0 .cgi`
filetype=`echo $scriptname | sed -e 's/^.*2//'`
. ./myvinkhead.cgi "Download $filetype file" "$title"

echo "Generating $filetype file.  Just a moment.<p>"
DIR=`pwd`
cd data/
tmpfile=`basename $file .ctl`
if [ ! -f $tmpfile.ctl ]; then
  ln -s $DIR/$file .
fi
datafile=$DIR/`dirname $file`/`head -1 $tmpfile.ctl | sed -e 's/[dD][sS][eE][tT] *\^*//'`
datfile=`basename $datafile`
if [ ! -f $datfile ]; then
  if [ ! -f $datafile ]; then
    gunzip -c $datafile.gz > $datfile
  elif [ ! -f $datfile ]; then
    ln -s $datafile .
  fi
fi

case $scriptname in
grads2nc)
  mime="x-netcdf"
  outfile=$DIR/data/$tmpfile.nc
  if [ -f $outfile -a $outfile -ot $DIR/$file ]; then
    rm $outfile
  fi
  if [ ! -f $outfile ]; then
    export UDUNITS_PATH=$DIR/etc/udunits.dat
    ###echo "<br>cd `pwd`;$DIR/bin/grads2nc $tmpfile.ctl $outfile<br>"
    $DIR/bin/grads2nc $tmpfile.ctl $outfile > /tmp/grads2nc$$.log 2>&1
  fi
  ;;
grads2hdf)
  mime="x-hdf"
  outfile=$DIR/data/$tmpfile.hdf
  if [ ! -f $outfile ]; then  
    export GADDIR=$DIR/grads
    export GASCRP=$GADDIR
    export UDUNITS_PATH=$GADDIR/udunits.dat
    export HOME=/tmp
    $DIR/bin/gradshdf -bl <<EOF >> /tmp/grads2nc$$.log 2>&1
run lats4d.gs -q -i $tmpfile -o $tmpfile
EOF
    mv $tmpfile.nc $outfile
    ###echo 'compressing <p>'
    ###gzip $outfile
  fi
  ;;
grads2hdf5)
  mime="x-hdf5"
  outfile=$DIR/data/$tmpfile.h5
  if [ ! -f $outfile ]; then
    export GADDIR=$DIR/grads
    export GASCRP=$GADDIR
    export HOME=/tmp
    $DIR/bin/gradshdf -bl <<EOF >> /tmp/grads2nc$$.log 2>&1
run lats4d.gs -q -i $tmpfile -o $tmpfile
EOF
    mv $tmpfile.nc $tmpfile.hdf
    $DIR/bin/h4toh5 $tmpfile.hdf
    rm $tmpfile.hdf
    mv $tmpfile.h5 $outfile
    ###echo 'compressing <p>'
    ###gzip $outfile
  fi
  ;;
esac

if [ ! -f $outfile ]; then
  echo 'Something went wrong in the netCDF/HDF/HDF5 generation routine.  Please send the following cryptic output to <a href="mailto:oldenborgh@knmi.nl">me</a> and I will try to fix it.<pre>'
  cat /tmp/grads2nc$$.log
  de $DIR
  . ./myvinkfoot.cgi
  exit
fi
rm -f /tmp/grads2nc$$.log
rm -f /tmp/$tmpfile.ctl
rm -f /tmp/$datfile

cat<<EOF
The requested file has been generated and is available <a href="data/`basename $outfile`">here</a>.

EOF
cd $DIR
. ./myvinkfoot.cgi
