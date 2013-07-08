#!/bin/sh
file=$1
metadata=metadata/`echo "$file" | tr '/' '.'`.txt.eval
if [ -s "$metadata" -a "$metadata" -nt "$file" ]; then
  echo used=cache
  cat "$metadata"
else
  echo used=prog
  ./bin/getunits $file
fi
