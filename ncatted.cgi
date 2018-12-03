#!/bin/bash
export PATH=$PATH:/usr/local/free/bin/
cat << EOF
Content-Type: text/plain


EOF
if [ $REMIOTE_ADDR != ::1 -a $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != 82.95.194.243 ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

arg1=`echo "$QUERY_STRING" | cut -f 1 -d +`
arg2=`echo "$QUERY_STRING" | cut -f 2 -d +`
arg2=`basename $arg2`
ncdump -h data/$arg2
ncatted -a $arg1 data/$arg2
ncdump -h data/$arg2
exit
