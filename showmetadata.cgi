#!/bin/sh
# show some metadata about the file from the netcdf global attributes
echo "Content-Type: text/html"
echo

. ./init.cgi
. ./getargs.cgi

. ./queryfield.cgi
. ./get_url.cgi

. ./myvinkhead.cgi "Metadata" "$kindname $climfield"

cat <<EOF
<table class="realtable" width="100%" cellspacing=0 cellpadding=0>
<tr><th colspan=2>References
EOF
file0=`echo "$file" | tr '%' '0'`
[ "$splitfield" = true ] && file0=`ls $file0|head -1`
if [ ! -s $file0 ]; then
    file0= `echo "$file | sed -e 's/%%%/001/' -e s/%%/01/'`
    if [ ! -s $file0 ]; then
        echo "Error: cannot find file $file"
        echo '</table>'
        . ./myvinkfoot.cgi
        exit
    fi
fi
if [ -n "$url" ]; then
    echo "<tr><td>official web page<td><a href=$url>$url</a>"
fi
echo "<tr><td>Climate Explorer URL<td><a href=>climexp.knmi.nl/select.cgi?field=$FORM_field<a/>"
if [ "$file0" = "$file" ]; then
    echo "<tr><td>filename<td>$file0"
else
    echo "<tr><td>filename<td>$file"
    echo "<tr><td>first ensemble member<td>$file0"
fi
echo "<tr><th colspan=2>Netcdf global metadata"
if [ "$file0" != "$file" ]; then
    echo "of first ensemble member"
fi
ncdump -h $file0 | sed \
-e '/{/,/global attributes/d' \
-e 's/^[ \t]*:/\<tr\>\<td\>/' \
-e 's/ = */\<td\>/' \
-e 's/ ;//' \
-e 's/"//g' \
-e 's/\n,/\<br\>/g' \
-e 's/\\n,/\<br\>/g' \
-e 's/^}//' \
-e 's@doi:\([^ ]*\)@<a href=https://doi.org/\1>doi:\1</a>@' \
-e 's@https://\([^ ]*\)@<a href=https:\1>\1</a>@'
echo "</table>"

. ./myvinkfoot.cgi
