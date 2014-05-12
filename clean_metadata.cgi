#!/bin/sh
cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

echo "Removing wrong metadata files"
for file in metadata/*.eval
do
    c=`fgrep -c error $file`
    if [ $c != 0 ]; then
        echo "rm $file"
        rm $file
        f=${file%.eval}
        [ -s $f ] && rm $f
    fi
done
echo "Done"