#!/bin/sh
file="$1"
metadata=metadata/$file.txt.eval
metadir=`dirname $metadata`
[ ! -d $metadir ] && mkdir -p $metadir
if [ -s "$metadata" -a "$metadata" -nt "$file" ]; then
  echo used=cache
  egrep '^[A-Z]*=[- "0-9a-zA-Z/*]*$' "$metadata"
else
  echo used=prog
  ./bin/getunits $file |fgrep -v error |tee $metadata
fi
