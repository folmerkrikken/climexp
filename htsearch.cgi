#!/bin/bash
# according to the manual, setting the environment variable should work
# but it does not for me.  The third method in the FAQ does work
. ./getargs.cgi
export CONFIG_DIR=/data/storage/climexp/htdig/
unset REQUEST_METHOD
###debug=true
if [ -n "$debug" ]; then
  echo "ContentType: text/plain"
  echo
  echo FORM_words=$FORM_words
  echo EMAIL=$EMAIL
  exit
fi
[ -z "$EMAIL" ] && EMAIL=someone@somewhere
# for some reason putting the words on the command line does not give any results!
/usr/bin/htsearch -c $CONFIG_DIR/htdig.conf <<EOF | sed -e "s/FORM_EMAIL/$EMAIL/g" -e "s/%40/@/g" -e "s/bhlclimtmp/climexp/g" -e "s/bhlclim/climexp/g"
$FORM_words

EOF
