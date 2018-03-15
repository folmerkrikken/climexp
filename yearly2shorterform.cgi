#!/bin/sh
# form with options for yearly2shorter.cgi

if [ "$TYPE" = "p" ]; then
  sel_sum="selected"
else
  sel_ave="selected"
fi
cat <<EOF
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
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
EOF
if [ $NPERYEAR = 1 -o $NPERYEAR = -1 ]; then
    case $NPERYEAR in
        1) selected1=selected;;
        -1) selected7-selected;;
    esac
    cat <<EOF
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
<option value="1" $selected1>Jan
<option value="2">Feb
<option value="3">Mar
<option value="4">Apr
<option value="5">May
<option value="6">Jun
<option value="7" $selected7>Jul
<option value="8">Aug
<option value="9">Sep
<option value="10">Oct
<option value="11">Nov
<option value="12">Dec
EOF
elif [ $NPERYEAR = 2 ]; then
    cat <<EOF
the biannual values into the 
<select name="sum">
<option>1
<option>2
<option>3
<option>4
<option>5
<option selected>6
</select>
months starting in 
<select name="mon">
<option value="1">Jan/Jul
<option value="2">Feb/Aug
<option value="3">Mar/Sep
<option value="4" selected>Apr/Oct
<option value="5">May/Nov
<option value="6">Jun/Dec
EOF
elif [ $NPERYEAR = 4 ]; then
    cat <<EOF
the seasonal values into the 
<select name="sum">
<option>1
<option>2
<option selected>3
</select>
months starting in 
<select name="mon">
<option value="1">Jan-Apr-Jul-Oct
<option value="2">Feb-May-Aug-Nov
<option value="3" selected>Dec-Mar-Jun-Sep
EOF
fi
cat <<EOF
</select>
</td></tr>
EOF
