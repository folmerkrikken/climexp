#!/bin/sh
# to be source from correlatebox.cgi
###kop=`echo "${htmltitle}" | sed -e 's/\\.*$//'`
###subkop=`echo "${htmltitle}" | sed -e 's/^.*\\//'`
. ./myvinkhead.cgi "Map of stations" "$htmltitle" "noindex,nofollow"

cat <<EOF
When finished, the plot options will appear at <a href="#plotoptions">the end</a> of this page.  If your web browser gives up before the calculation is finished a complete copy of this page might be available <a href="$backupfile">here</a>.<p>
<small>If it takes too long you can abort the job <a href="killit.cgi?id=$FORM_email&pid=$$" target="_new">here</a> (using the [back] button of the browser does <it>not</it> kill the correlation job)</small><p>

EOF
cat | sed -e "s:$DIR::g" > pid/$$.$FORM_email <<EOF
$REMOTE_ADDR
correlatebox $corrargs
@
EOF
export SCRIPTPID=$$
export FORM_EMAIL=$EMAIL
if [ "$lwrite" = true ]; then
    echo "./bin/stationlist $corrargs<br>"
    [ -n "$attribute_args" ] && echo "attribute_args=$attribute_args<br>"
fi
(./bin/stationlist $corrargs) 2> /tmp/correlatebox_err_$$.log
rm pid/$$.$FORM_email

. ./plotparams.cgi

