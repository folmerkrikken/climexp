#!/bin/bash

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

ps -p $QUERY_STRING
kill $QUERY_STRING
sleep 1
ps -p $QUERY_STRING
exit

