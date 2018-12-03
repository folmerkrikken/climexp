#!/bin/bash
echo 'Content-Type: text/html'
if [ 0 = 1 ]; then # maybe do browser detection later, it is only a problem in Safari
echo 'Cache-Control: no-store, must-revalidate'
echo 'Expires: 0'
fi
echo
echo
