#!/bin/sh
# form with options for yearly2shorter.cgi

if [ "$TYPE" = "p" ]; then
  sel_sum="selected"
else
  sel_ave="selected"
fi
cat <<EOF
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="NPERNEW" value="12">
<tr><td>New time scale:</td><td><p><br>Monthly</td></tr><tr><td>
Operation:</td><td><p><br>
<select name="oper">
<option value="ave" $sel_ave>distribute
<option value="sum" $sel_sum>divide
</select>
the annual value into the 
<select name="sum">
<option>1
<option>2
<option>3
<option>4
<option>5
<option>6
<option>7
<option>8
<option>9
<option>10
<option>11
<option selected>12
</select>
months starting in 
<select name="mon">
<option value="1" selected>Jan
<option value="2">Feb
<option value="3">Mar
<option value="4">Apr
<option value="5">May
<option value="6">Jun
<option value="7">Jul
<option value="8">Aug
<option value="9">Sep
<option value="10">Oct
<option value="11">Nov
<option value="12">Dec
</select>
</td></tr>
EOF
