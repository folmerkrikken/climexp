#!/bin/bash
c=`echo "$HTTP_USER_AGENT" | egrep -i -c 'MSIE 4|MSIE 5|MSIE 6'`
if [ $c != 0 ]; then
  echo "<font color=\"#FF0000\">The Climate Explorer works best in a standards-compliant browser.  I recommend that you upgrade to a free modern browser, such as <a href=\"www.mozilla.com\">Firefox</a> or <a href=\"http://www.google.com/chrome\">Chrome</a>, or upgrade to <a href=\"http://www.apple.com/safari\">Safari</a> or <a href=\"http://www.microsoft.com/ie7\">Internet Explorer 7</a>.</font>"
fi
