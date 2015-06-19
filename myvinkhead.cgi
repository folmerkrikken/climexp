#!/bin/sh
# generates the vink headers with a user-defied title and subtitle
if [ -z "$myvinkhead" ]; then
myvinkhead="done"
if [ -n "$3" ]; then
  robot="<meta name=\"robots\" content=\""$3"\">"
fi
if [ -n "$absolute_paths" ]; then
    prefix="http://climexp.knmi.nl/"
else
    prefix=""  
fi
if [ -f images/logo_climexp.png ]; then
    cat <<EOF
<html>
<head>
<!-- beheerder: Geert Jan van Oldenborgh -->
<link rel="stylesheet" href="${prefix}styles/rccstyle.css" type="text/css">
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<script language="javascript" src="${prefix}library/javascript/hidden_info_switch.js"></script>
<script language="javascript" src="${prefix}library/javascript/pop_page.js"></script> 
$extrahead
$robot
<link rel="shortcut icon" href="/favicon.ico"> 
<title>Climate Explorer: $1</title>
<style type="text/css">
a { text-decoration: none }
</style>
</head>
<body>
EOF
    . ./searchengine.cgi
    sed -e "s/FORM_EMAIL/$EMAIL/" ./vinklude/rcc_pagehead.html 
cat <<EOF
<table border="0" width="762" cellspacing="0" cellpadding="0">
   <tr>
      <td width="80">&nbsp;</td>
      <td width="451" valign=top>
         <div id="printable" name="printable">
         <!-- div -->
<!-- Voeg hieronder de inhoud van de pagina in -->
<br>
         <div class="hoofdkop">$1</div>
         <div class="subkop">$2</div>
<div class="kalelink">
EOF

else # for linux the old lay-out

    cat <<EOF
<html>
<head>
<!-- beheerder: Geert Jan van Oldenborgh -->
<link rel="stylesheet" href="${prefix}styles/vinkstyle.css" type="text/css">
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
$extrahead
$robot
<link rel="shortcut icon" href="/favicon.ico"> 
<title>Climate Explorer: $1</title>
</head>
<body>
EOF
    sed -e "s/FORM_EMAIL/$EMAIL/g" ./vinklude/research_pagehead.html 

cat <<EOF
<table border="0" width="762" cellspacing="0" cellpadding="0">
   <tr>
      <td width="80">&nbsp;</td>
      <td width="451" valign=top>
         <div id="printable" name="printable">
         <!-- div -->
<!-- Voeg hieronder de inhoud van de pagina in -->
         <div class="rubriekkop">Climate Explorer</div>
         <div class="hoofdkop">$1</div>
         <div class="subkop">$2</div>
<div class="kalelink">
EOF
fi # old lay-out

# For safety only use type=number for Opera and mobile browsers
# In Safari this is buggy, and AFAIK not used in Firefox & Internet Explorer
c1=`echo "$HTTP_USER_AGENT" | egrep -i -c mobile`
c2=`echo "$HTTP_USER_AGENT" | egrep -i -c opera`
if [ $c1 = 1 -o $c2 = 1 ]; then
    number=number
    textsize2='style="width: 4em;"'
    textsize3='style="width: 5em;"'
    textsize4='style="width: 6em;"'
    textsize6='style="width: 7em;"'
    textsize10='style="width: 13em;"'
else
    number=text
    textsize2='size=2'
    textsize3='size=3'
    textsize4='size=4'
    textsize6='size=6'
    textsize10='size=10'
fi
###echo "HTTP_USER_AGENT = $HTTP_USER_AGENT<br>"
###echo "c1,c2,number=$c1,$c2,$number<br>"

fi
. ./init.cgi
