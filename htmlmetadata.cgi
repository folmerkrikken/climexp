#!/bin/bash
# get metadata from HTML view of opendap server
# in particluar from the DMI ENSEMBLES RCM archive
# may not waork for other archives...
level=$2
if [ -z "$level" ]
then
  echo "usage: $0 path level [dir]"
  exit -1
fi
debug=false
dir=$3
# the DMI dods server cannot handle double slashes
path=`echo $1 | sed -e 's@//@/@g' -e 's@/$@@' -e s@:/@://@`
if [ ${path#http://ensemblesrt3.dmi.dk/} = $path ]
then
  echo "$0: only works for DMI at the moment"
  exit -1
fi
urllist="$path"/
while [ $level -gt 0 ]
do
  level=$((level-1))
  newlist=""
  for url in $urllist
  do
    list=`wget -q -O - $url | egrep 'folder.gif|compressed.gif' | sed -e 's/^.*HREF="//' -e 's/".*$//'`
    if [ "$debug" = true ]; then
      echo "wget -q -O - $url | egrep 'folder.gif|compressed.gif' | sed -e 's/^.*HREF=\"//' -e 's/\".*$//'"
      echo "$level $url =>"
      echo "$list"
    fi
    newlist="$newlist $list"
  done
  urllist=$newlist
done
if [ -n "$dir" ]
then
  echo $newlist | tr ' ' '\n' | sed -e "s@$path@@" -e "s@^/@@g" -e "s@\$@$dir/@" -e "s@/*\$@/@"
else
  echo $newlist | tr ' ' '\n' | sed -e "s@$path@@" -e "s@^/@@g" -e "s/.html\$//"
fi
