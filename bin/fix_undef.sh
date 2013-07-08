#!/bin/sh
# pass notorious files to the Fortran program fix_undef, mv the rest
infile=$1
outfile=$2
c1=`echo $outfile | egrep -c 'HadRM|_HC_'`
c2=`echo $outfile | fgrep -c SMHI`
if [ $c1 = 0 -a $c2 = 0 ]; then
  mv $infile $outfile
else
  bin/fix_undef $infile $outfile
  rm $infile
fi
