#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "EC-Earth scenario runs" "index,nofollow"

cat <<EOF
<div class="kalelink">
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr valign="baseline"><th colspan="14"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
<tr><th>EC-Earth 2.3<br>RCP8.5
<th>tas
<th>tas<br>min
<th>tas<br>max
<th>pr
<th>evsp<br>sbl
<th>pme
<th>ssr
<th>u10
<th>v10
<th>psl
<tr><td>KNMI'14 (16)
<td><input type=radio class=formradio name=field value=knmi14_2t_Amon_ECEARTH23_rcp85>
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=knmi14_tp_Amon_ECEARTH23_rcp85>
<td>&nbsp;
<td>&nbsp;
<td><input type=radio class=formradio name=field value=knmi14_ssr_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_10u_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_10v_Amon_ECEARTH23_rcp85>
<td><input type=radio class=formradio name=field value=knmi14_msl_Amon_ECEARTH23_rcp85>

</table>
</form>
EOF

. ./myvinkfoot.cgi
