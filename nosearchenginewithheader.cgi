#!/bin/bash
. ./searchengine.cgi
if [ -n "$ROBOT" ]
then
  echo "Content-type: text/html"
  echo
  echo
  echo "<html><head><meta name=\"robots\" content=\"noindex\"></head><body>"
  echo "No access for robots and other non-human life forms"
  echo "Please contact me (Geert Jan van Oldenborgh) if you are human"
  echo "</body></html>"
  exit
fi

