#!/bin/sh
#
# get rid of referrer-tag when following external links
# this may contain the e-mail address of the user.
# necessary to be in compliance with EU privacy regulations...
#
# more strict checking than proccgi:
QUERY_STRING=`echo $QUERY_STRING | tr -cd '[:alnum:]?:/._=#~-'`
[ -z "$SERVER_NAME" ] && echo "QUERY_STRING=$QUERY_STRING"
c=`echo $QUERY_STRING | egrep -c 'games|sex|gossip|fake|[^a-z]sms|\.net|\.com|\.se'`
[ -z "$SERVER_NAME" ] && echo "c=$c"
if [ \( $c = 0 \
    -o "$QUERY_STRING" = "http://www.ssmi.com/sst/microwave_oi_sst_data_description.html" \
    -o  "$QUERY_STRING" = "http://www.remss.com/msu/msu_data_description.html" \
    \) -a "${HTTP_REFERER#http://$SERVER_NAME}" != "${HTTP_REFERER}" \
       -a "${HTTP_REFERER#http://$SERVER_NAME/wipefeet}" = "${HTTP_REFERER}" ]; then
    echo "wipefeet to $QUERY_STRING" >> log/log
    cat << EOF
Content-Type: text/html

<html>
<head>
<title>Leaving the Climate Exlorer</title>
<meta http-equiv="Refresh" content="0;url=$QUERY_STRING">
</head>
<BODY BGCOLOR="#FFFFFF">
You are leaving the Climate Explorer. You are being forwarded to <a
href="$QUERY_STRING">$QUERY_STRING</a>. If this link no longer works, please notify <a href="http://www.knmi.nl/~oldenbor/">the Climate Explorer maintainer</a>.

<p>Have a nice day.

</body>
</html>
EOF
else
    echo "Content-Type: text/plain"
    echo
    echo "This redirection is not allowed."
fi
