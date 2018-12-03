#!/bin/bash
echo "Content-Type: text/html"
echo
echo
. ./init.cgi
. ./getargs.cgi
./myvinkhead.cgi "$FORM_set regions" ""
if [ -z "$FORM_set" -o ! -d "$FORM_set" ]; then
	echo "Set of masks $FORM_set unknown"
else
	echo '<ul>'
	for file in $FORM_set/*.txt
	do
		if [ ${file%kaal.txt} = $file -a ${file%nan.txt} = $file ]; then
			echo "<li><a href=$file>"`head -1 "$file" | tr -d '?' | sed -e 's/^# *//'`'</a>'
		fi
	done
	echo '</ul>'
fi
. ./myvinkfoot.cgi