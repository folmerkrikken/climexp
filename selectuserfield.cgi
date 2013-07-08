#!/bin/sh

echo '<p><b><a name="field_user">user-defined</a>: </b><br>'

for userfile in data/*.$EMAIL.info
do
  if [ -f $userfile ]; then
    echo "<input type=\"radio\" class=\"formradio\" name=\"field\" value=\"$userfile\">"
    tail -1 $userfile
    tail -2 $userfile | head -1
    echo "("`basename $userfile .$EMAIL.info`")<br>"
  fi
done
