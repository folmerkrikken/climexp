#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select or upload a field" "User-defined field" "index,nofollow"

if [ "$EMAIL" != "someone@somewhere" ]; then
  cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<div class="formheader">
<input type="submit" class="formbutton" value="Select field"> Choose a field and press this button
</div>
<div class="formbody">
EOF
  . ./selectuserfield.cgi
  echo '</div></form>'
else
  echo "Anonymous users cannot use user-defined fields</ul>"
fi

. ./uploadfieldform.cgi

