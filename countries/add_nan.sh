#!/bin/sh
if [ -z "$1" ]; then
    files="*.txt"
else
    files="$@"
fi
for file in $files
do
    if [ $file != "Readme.txt" -a ${file%_nan.txt} = $file ]; then
        newfile=${file%.txt}_nan.txt
        sed -e 's/^ *$/NaN  NaN/' $file | fgrep -v '#' > $newfile
        [ $? != 0 ] && echo "problems in $file"
    fi
done
