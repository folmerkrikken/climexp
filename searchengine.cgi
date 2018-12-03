#!/bin/bash
[ "$EMAIL" = someone@somehere ] && EMAIL=someone@somewhere
# to be sourced from other scripts
# checks whether the UA is a search engine, if so set to anonymous

# this catches a lot
c=`echo "$HTTP_USER_AGENT" | egrep -i -c 'htdig|bot|crawl|slurp|/search|jeeves|spider|archive|pompos|heritrix|litefinder|scout|yandex|ltx71|qwant'`
cc=`echo "$EMAIL" | fgrep -c "http:"`
###echo "searchengine: $HTTP_USER_AGENT"
###echo "searchengine: $c"
if [ -n "$HTTP_X_FORWARDED_FOR" ]; then
    REMOTE_ADDR=$HTTP_X_FORWARDED_FOR
fi
# change to blacklisted address if needed
if [ $c -gt 0 -o $cc -gt 0 -o "$REMOTE_ADDR" = 163.172.71.23 -o -z "$HTTP_USER_AGENT" ]
then
  ROBOT=true
  if [ -z "$EMAIL" ]; then
    EMAIL=someone@somewhere
  fi
  if [ "$EMAIL" != "someone@somewhere" ]; then
          echo
          echo
	  echo "robots and crawlers should use someone@somewhere"
	  echo "contact me (Geert Jan van Oldenborgh) if you are not a robot"
	  exit
  fi
fi

