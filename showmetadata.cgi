#!/bin/sh
# show some metadata about the file from the netcdf global attributes
echo "Content-Type: text/html"
echo

. ./init.cgi
. ./getargs.cgi

. ./queryfield.cgi

. ./myvinkhead.cgi "Metadata" "$kindname $climfield"

cat <<EOF
<table class="realtable" width="100%" cellspacing=0 cellpadding=0>
<tr><th colspan=2>Netcdf global metadata
EOF
file0=`echo "$file" | tr '%' '0'`
[ "$splitfield" = true ] && file0=`ls $file0|head -1`
if [ "$file0" != "$file" ]; then
    echo "of first ensemble member"
fi
if [ ! -s $file0 ]; then
    file0= `echo "$file | sed -e 's/%%%/001/' -e s/%%/01/'`
    if [ ! -s $file0 ]; then
        echo "Error: cannot find file $file"
        echo '</table>'
        . ./myvinkfoot.cgi
        exit
    fi
fi
echo "<tr><td>filename<td>$file0"
ncdump -h $file0 | sed \
-e '/{/,/global attributes/d' \
-e 's/^[ \t]*:/\<tr\>\<td\>/' \
-e 's/ = */\<td\>/' \
-e 's/ ;//' \
-e 's/"//g' \
-e 's/\\n,/\<br\>/g' \
-e 's/^}//'
echo "</table>"

. ./myvinkfoot.cgi
