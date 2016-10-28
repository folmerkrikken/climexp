#!/bin/sh
# make a list of unique IP addresses and IDs from a log file
logfile="$1"
if [ -z "$logfile" ]; then
    logfile=log/log
fi
egrep '[(][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*[)]' $logfile \
    | sed -e 's/^[^(]*(//' -e 's/).*$//' \
    | cut -b 1-15 | tr -d ') ' \
    | sort | uniq > ips.txt
egrep '@' $logfile \
    | awk '{print $7}' \
    | sort | uniq > ids.txt
