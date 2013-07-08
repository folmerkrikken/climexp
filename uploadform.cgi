#!/bin/sh
if [ -z "$myvinkhead" ]; then
  echo 'Content-Type: text/html'
  echo
  echo

  # check if a search engine, if so set user to anonymous
  . ./getargs.cgi
  . ./searchengine.cgi
  . ./myvinkhead.cgi "Select a monthly time series" "Upload a series"
fi

. ./read_getstations.cgi

if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "Anonymous users cannot use user-defined indices. Please <a href=\"registerform.cgi\">register or log in</a>"
  . ./myvinkfoot.cgi
  exit
fi
cat <<EOF
<a name='upload'></a>
<div class='formheader'>Upload text data</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<form action="upload.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<tr><td>
Name:
</td><td>
<input type="text" name="STATION" size=20>
</td></tr><tr><td>
Type:
</td><td>
<input type="radio" class="formradio" name="TYPE" value="p"> precipitation, 
<input type="radio" class="formradio" name="TYPE" value="t"> temperature, 
<input type="radio" class="formradio" name="TYPE" value="s"> pressure, <br>
<input type="radio" class="formradio" name="TYPE" value="l"> sealevel, 
<input type="radio" class="formradio" name="TYPE" value="r"> runoff, 
<input type="radio" class="formradio" name="TYPE" value="i" checked> something else.
</td></tr><tr><td colspan="2">
<textarea class="forminput" name="data" class="forminput" rows="6" cols="52">
# Overwrite this text by your data.  Lines starting
# with a hash are considered comments.  A line 
# variable [units] is interpreted for labelling.
# The data can be in many different formats, e.g.,
#   yyyy val_jan val_feb ... val_dec
#   yyyy mm [dd] val
# Undefined data should be represented by -999.9
</textarea>
</td></tr><tr><td colspan=2>
<input type="submit" class="formbutton" value="Upload">
<input type="reset" class="formbutton" value="Clear Form" align="right">
</td></tr>
</form>
</table>
</div>
<p>
<div class='formheader'>Upload a netCDF file</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<form action="uploadseries.cgi" method="POST"  enctype="multipart/form-data">
<input type="hidden" name="email" value="$EMAIL">
<tr><td>
Name:
</td><td>
<input type="text" name="station" size=20>
</td></tr><tr><td>
Type:
</td><td>
<input type="radio" class="formradio" name="type" value="p"> precipitation, 
<input type="radio" class="formradio" name="type" value="t"> temperature, 
<input type="radio" class="formradio" name="type" value="s"> pressure,<br>
<input type="radio" class="formradio" name="type" value="l"> sealevel, 
<input type="radio" class="formradio" name="TYPE" value="r"> runoff, 
<input type="radio" class="formradio" name="type" value="i" checked> something else.
</td></tr><tr><td>
File:
</td><td>
<input type="file" class="formbutton" name="myfield.nc" value="myfield.nc">
<a href="javascript:pop_page('help/netcdf.shtml',426,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a><br>
</td></tr><tr><td colspan=2>
<input type="submit" class="formbutton" value="Upload">
<input type="reset" class="formbutton" value="Clear Form" align="right">
</td></tr>
</form>
</table>
</div>
EOF

. ./myvinkfoot.cgi
