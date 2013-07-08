#!/bin/sh
. ./searchengine.cgi
if [ -n "$ROBOT" ]
then
  echo "No access for robots and other non-human life forms"
  echo "Please contact me (Geert Jan van Oldenborgh) if you are human"
  exit
fi

