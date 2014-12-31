#!/bin/sh
for file in *.txt
do
    if [ $file != "Readme.txt" -a ${file%_nan.txt} = $file ]; then
        f=${file%.txt}
        ff=`echo $f | tr '_' ' '`
        echo "               ['$f', '$ff'],"
    fi
done