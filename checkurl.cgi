#!/bin/bash
# check and santize the variable FORM_url

if [ ${FORM_url#http://} = ${FORM_url} ]; then
  echo "Only http URLs are supported at this time"
  . ./myvinkfoot.cgi
  exit
fi

FORM_url=`echo $FORM_url | sed -e 's/[^-a-zA-Z.:/?+]//'`
