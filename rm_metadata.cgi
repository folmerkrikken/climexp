#!/bin/sh

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

ls -l metadata/$QUERY_STRING
rm metadata/$QUERY_STRING
ls -l metadata/$QUERY_STRING
exit
