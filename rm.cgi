#!/bin/sh

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != 82.95.194.243 ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

ls -l data/$QUERY_STRING
rm data/$QUERY_STRING
ls -l data/$QUERY_STRING
exit
