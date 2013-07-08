#!/bin/sh
# show some metadata about the file from the netcdf global attributes
echo "Content-Type: text/html"
echo

. ./getargs.cgi

. ./queryfield.cgi

. ./myvinkhead.cgi "Metadata" "$kindname $climfield"

cat <<EOF
<table class="realtable" width=451 cellspacing=0 cellpadding=0>
<tr><th colspan=2>Netcdf global metadata of first ensemble member
EOF
file0=`echo "$file" | tr '%' '0'`
bin/ncdump -h $file0 | sed \
-e '/{/,/global attributes/d' \
-e 's/^[ \t]*:/\<tr\>\<td\>/' \
-e 's/ = */\<td\>/' \
-e 's/ ;//' \
-e 's/"//g' \
-e 's/\\n,/\<br\>/g' \
-e 's/^}//'
echo "</table>"

. ./myvinkfoot.cgi
