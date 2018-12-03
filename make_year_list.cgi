#!/bin/bash
# make a list of years in a select statement
# expects variable $yrbeg and $yrend to be set
[ -z "$yrbeg" ] && yrbeg=1958
[ -z "$yrend" ] && yrend=`date +"%Y"`
yr=$yrbeg
while [ $yr -le $yrend ]; do
  echo "<option ${yr_selected[$yr]}>$yr</option>"
  yr=$(($yr + 1))
done
