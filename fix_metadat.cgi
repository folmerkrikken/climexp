#!/bin/sh
echo "Content-Type: text/plain"
echo
echo

for file in metadata/*.txt
do
  c=`grep -c NX $file.eval`
  if [ $c = 0 ]; then
    echo $file has no NY
    rm $file $file.eval
  fi
done
