#!/bin/sh

. ./getargs.cgi
kindname=$FORM_kindname
climfield=$FORM_climfield

i=0
file=data/uploaded$i
while [ -f $file.nc -o -f ${file}_00.nc -o -f ${file}_01.nc ]
do
  i=$(($i + 1))
  file=data/uploaded$i
done
FORM_field=$file.$EMAIL.info

echo "Content-Type: text/html"
echo
echo
. ./myvinkhead.cgi "Retrieving field" "$kindname $climfield" "index,nofollow"

. ./checkurl.cgi
nens=`echo $FORM_url | wc -w`
if [ $nens = 1 ]; then
  curl -s "$FORM_url" > $file.nc
else
# ensemble
  iens=0
  for url in $FORM_url
  do
    if [ $iens -lt 10 ]; then
      ensfile=${file}_0$iens.nc
    elif [ $iens -lt 100 ]; then
      ensfile=${file}_$iens.nc
    else
      echo "Error: can only handle at most 100 ensemble members"
      . ./myvinkfoot.cgi
      exit
    fi
    echo "Retrieving $ensfile from $url<br>"
    curl -s "$url" > $ensfile
    iens=$(($iens + 1))
  done
  file=${file}_%%
fi

cat > $FORM_field <<EOF
$file.nc
$kindname
$climfield
EOF

. ./select.cgi
