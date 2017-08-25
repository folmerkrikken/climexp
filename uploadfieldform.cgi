#!/bin/sh
if [ -z "$myvinkhead" ]; then
  echo 'Content-Type: text/html'
  echo
  echo

  # check if a search engine, if so set user to anonymous
  . ./getargs.cgi
  . ./searchengine.cgi
  . ./myvinkhead.cgi "Select a field" "Upload a field"
fi

. ./read_getstations.cgi

if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "Anonymous users cannot use user-defined field. Please <a href=\"registerform.cgi\">register or log in</a>"
  . ./myvinkfoot.cgi
  exit
fi

cat <<EOF
<div class="formheader">Upload your own field into the Climate Explorer</div>
<div class="formbody">
<form action="uploadfield.cgi" method="POST"  enctype="multipart/form-data">
<input type="hidden" name="email" value="$EMAIL">
<table border=0 cellpadding=0 cellspacing=0>
<tr>
<td>Type of field:
<td><input type="text" class="formtext" name="kindname" size="10"> (e.g., SLP, temp, precip, ...)
<tr>
<td>Name of field:
<td><input type="text" class="formtext" name="climfield" size="20"> (e.g., KNMI analysis)
<tr>
<td>NetCDF file:
<td><a href="javascript:pop_page('help/netcdf.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a><input type="file" class="formbutton" name="myfield.nc" value="myfield.nc">

<tr>
<td><input type="submit" class="formbutton" value="Upload">
<td>&nbsp;
</table>
</form>
</div>
The Climate Explorer only accepts fields as netcdf files with one 2D time-varying variable on a lat/lon, lev/lon or lev/lat grid. The netcdf should be reasonably <a href="http://cf-pcmdi.llnl.gov/" target=_new>CF</a>-compliant.

EOF

. ./myvinkfoot.cgi
