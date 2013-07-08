#!/bin/sh
echo 'Content-Type: text/plain'
echo
echo

ls -lt /tmp/*.log /tmp/*.ps /tmp/*.nc | fgrep nobody
rm /tmp/*.log  /tmp/*.ps /tmp/*.nc
