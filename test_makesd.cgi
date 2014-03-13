#!/bin/sh

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != 82.95.194.243 ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

cmd="./makesd.cgi 30 tas 0"
echo $cmd
$cmd
echo klaar
exit
