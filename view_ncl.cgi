#!/bin/bash

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

ls -td /tmp/tmp* | head -5
dir=`ls -td /tmp/tmp* | head -2 | tail -1`
ls -l $dir
cp $dir/* /tmp/
cat $dir/*.ncl $dir/*.gnuplot
exit
