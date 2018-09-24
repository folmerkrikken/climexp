#!/bin/sh
. ./init.cgi
. ./getargs.cgi
. ./checkemail.cgi
if [ "$EMAIL" = "someone@somewhere" ]; then
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myvinkhead.cgi "Error" "" "noindex,nofollow"
  echo "Anonymous users cannot upload a mask, please <a href=\"/registerform.cgi\">register or log in</a>."
  . ./myvinkfoot.cgi
fi

if [ "$FORM_set" = SREX -o "$FORM_set" = IPBES -o "$FORM_set" = eu_rivers_big -o "$FORM_set" = eu_rivers -o "$FORM_set" = ar5_atlas -o "$FORM_set" = countries ]; then
	for file in $FORM_set/*.txt
	do
		if [ -s $file -a ${file%kaal.txt} = $file -a ${file%nan.txt} = $file ]; then
			cp $file data/
			f=`basename $file .txt`
			maskfile=data/$f.txt
			maskmetadata=data/mask$f.$EMAIL.poly
			case $f in
				Antarctica) sp=on;;
				*) sp=off;;
			esac
			cat <<EOF > $maskmetadata
$maskfile
$f
$sp
EOF
		fi
	done
	maskfile="" # the last one should not be selected by default
elif [ -n "$FORM_set" ]; then
	echo 'Content-Type: text/html'
	echo
	echo
	. ./myvinkhead.cgi "Error" "Unknown set of predefined masks" "noindex,nofollow"
	echo " "
	. ./myvinkfoot.cgi	
else
	# user-defined mask
	i=0
	maskfile=./data/mask$i.txt
	while [ -f $maskfile ]
	do
		i=$((i+1))
		maskfile=./data/mask$i.txt
	done

	echo "$FORM_data" | tr '\r' '\n' > $maskfile
	maskmetadata=data/mask$i.$EMAIL.poly
	[ -z "$FORM_maskname" ] && FORM_maskname=`basename $maskfile`
	cat <<EOF > $maskmetadata
$maskfile
$FORM_maskname
${FORM_sp:-off}
EOF
fi

if [ "$FORM_field" = dailystation ]; then
    . ./selectdailyseries.cgi
else
    . ./select.cgi
fi
