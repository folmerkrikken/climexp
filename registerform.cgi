#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
if [ -z "$EMAIL" ]; then
  EMAIL=someone@somewhere
fi
. ./myvinkhead.cgi "Register or log in" ""

cat <<EOF
Please register as a user so that I can trace usage of the system,
and mail you if I find bugs.  If you have already registered just give
your e-mail address to log in.  The service is also available <a
href="start.cgi?id=someone@somewhere">anonymously</a>, but some
features (notably the ability to define your own indices, to upload 
your own data and to use large datasets) are then disabled.  As a registered user many forms remember their settings for a few days.

<p>
<table border=0 cellpadding=0 cellspacing=0><tr><td>
<form action="register.cgi" method="POST">
<div class="formheader">
Register / Log in
</div>
<div class="formbody">
<table border=0 cellpadding=0 cellspacing=0 style="width:100%;">
<tr>
<td><span style="float:left">E-mail address</span></td>
<td><span style="float:right;"><input type="email" name="email" class="forminput" style="width:250px;" placeholder="your e-mail address"></span></td>
</tr><tr>
<td><span style="float:left">Name</span></td>
<td><span style="float:right;"><input type="text" name="username" class="forminput" style="width:250px;" placeholder="your real name (only first time)"></span></td>
</tr><tr>
<td><span style="float:left">Institute</span></td>
<td><span style="float:right;"><input type="text" name="institute" class="forminput" style="width:250px;" placeholder="your institution (only first time)"></span></td>
</tr><tr>
<td colspan="2" align=right><input type="submit" value="register/log in" class="formbutton"></td></tr>
</table>
</div>
</form>
</td></tr></table>
EOF

. ./myvinkfoot.cgi


