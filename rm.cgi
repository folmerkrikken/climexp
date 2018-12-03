#!/bin/bash

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

[ -z "$QUERY_STRING" -o "$QUERY_STRING" = '*' ] && exit
ls -l data/$QUERY_STRING
rm data/$QUERY_STRING
ls -l data/$QUERY_STRING
exit
