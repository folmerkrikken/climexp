#!/bin/sh
logfile=/var/log/apache2/access_log
tmpfile=/tmp/browsers.tmp
cp $logfile $tmpfile

for browser in IE6 IE5 Firefox Mozilla Safari Konqueror Opera Google Yahoo MSN Surfnet Jeeves curl wget cfetch
do

case $browser in
IE5) id='MSIE 5';;
IE6) id='MSIE 6';;
Mozilla) id="Gecko/200";;
Firefox) id="Firefox";;
Safari) id="Safari";;
Konqueror) id="Konqueror";;
Opera) id="Opera";;
Google) id="Googlebot";;
Yahoo) id="Slurp";;
MSN) id="msnbot";;
Surfnet) id="Enterprise Crawler";;
Jeeves) id="Jeeves";;
curl) id="curl/";;
wget) id="wget";;
cfetch) id="cfetch";;
esac

echo $browser `fgrep -c "$id" $tmpfile`
fgrep -v "$id" $tmpfile > /tmp/aap
mv /tmp/aap $tmpfile

done
echo Unidentified `wc -l $tmpfile`
echo '----------------------------'
head $tmpfile
