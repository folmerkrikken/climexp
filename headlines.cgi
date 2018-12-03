#!/bin/bash
if [ ! -f ./prefs/$EMAIL.news -o ./prefs/$EMAIL.news -ot ./news.html ]; then
    touch ./prefs/$EMAIL.news
    echo '<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>'
    echo "<tr><th colspan=\"2\">News $explanation</th></tr>"
    head -3 news.html
    echo "<tr><td><a href=\"news.cgi?id=$EMAIL&all=all\">more...</a></td><td align=right></tr></table>"
fi
