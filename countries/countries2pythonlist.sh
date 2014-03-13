#!/bin/sh
for file in *.txt
do
    f=${file%.txt}
    ff=`echo $f | tr '_' ' '`
    echo "               ['$f', '$ff'],"
done