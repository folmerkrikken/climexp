#!/bin/sh
cat selectfield_rea1.html | tr ',' '\n' | sed -e 's/^.*value=\"//' -e 's/\".*$//' > /tmp/aap
for name in `cat /tmp/aap`
do
  c=`egrep -c "^$name\)" queryfield.cgi`
  ###echo $c
  if [ $c = 0 -o $c -gt 1 ]; then
    echo "error: $name occurs $c times in queryfield.cgi"
  fi
done
