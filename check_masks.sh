#!/bin/bash
# echo "$0: searching for missing mask files from queryfield.cgi"
fgrep 'LSMASK=' queryfield.cgi | sed -e 's/^.*LSMASK=//' -e 's/;.*$//' | tr -d '"' | sort | uniq > /tmp/masks.txt
for file in `cat /tmp/masks.txt`
do
    if [ ! -s $file ]; then
        echo $file
    fi
done