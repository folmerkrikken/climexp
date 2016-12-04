#!/bin/sh
echo `date`" cleanup: starting with "`ls ./data|wc -l`" files" >> log/log
rm /tmp/readdatfile*
find ./data/ -size 0c -exec rm -f {} \;
find ./metadata/ -size 0c -exec rm -f {} \;
find ./data/ -atime +4 -exec rm -f {} \;
find ./data/ -ctime +30 -exec rm -f {} \;
find ./data/ -name 'g[0-9]*.dat.gz' -atime +1 -exec rm -f {} \;
find ./data/ -name 'regionverification*.nc' -atime +1 -exec rm -f {} \;
find ./data/ -name '*.inf' -ctime +10 -exec rm -f {} \;
find ./data/ -name '*.info' -ctime +10 -exec rm -f {} \;
echo '<html><body>No access</body></html>' > data/index.html
for file in ./data/*.inf ./data/*.info
do
    datfile=`head -1 $file | sed -e 's/%%%/000/' -e 's/%%/01/'`
    if [ -n "$datfile" ]
    then
        dir=`dirname $datfile`
        if [ $dir = data -a ! -f "$datfile" ]
        then
	        rm -f "$file"
        fi
    fi
done
find ./atlas/maps/ -atime +30 -exec rm -f {} \;
find ./atlas/series/ -atime +90 -exec rm -f {} \;
find ./atlas/regr/ -atime +90 -exec rm -f {} \;
find ./atlas/diff/ -atime +90 -exec rm -f {} \;
find ./atlas -type d -empty -exec rmdir {} \;
find ./pid/ -atime +1 -exec rm -f {} \;
find ./prefs/ -ctime +7 -exec rm -f {} \;
find ./metadata/ -name 'cache*' -ctime +7 -exec rm -f {} \;
fgrep -l "cannot" ./metadata/*.txt | xargs -n 20 rm -f
fgrep -l "cannot" ./metadata/*.txt.eval | xargs -n 20 rm -f
fgrep -l "does not exist" ./metadata/*.txt | xargs rm -f
fgrep -l "does not exist" ./metadata/*.txt.eval | xargs rm -f
find /tmp -group apache -atime +1 -exec rm -f {} \;
find /var/tmp -group apache -atime +1 -exec rm -f {} \;
find /tmp -group www -exec rm -f {} \;
find /var/tmp -group www -atime +1 -exec rm -f {} \;
echo `date`" cleanup: finished with "`ls ./data|wc -l`" files" >> log/log
