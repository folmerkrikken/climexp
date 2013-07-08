#!/bin/sh

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != 145.23.6.80 ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

ps axuw | fgrep $QUERY_STRING
killall $QUERY_STRING
sleep 1
ps axuw | fgrep $QUERY_STRING
exit

