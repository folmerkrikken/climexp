#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo

export DIR=`pwd`
. ./getargs.cgi

# cleaner
FORM_netcdf=true

NPERYEAR=$FORM_NPERYEAR
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.diffoptions.$NPERYEAR << EOF
FORM_var=$FORM_var;
FORM_month=$FORM_month;
FORM_sum=$FORM_sum;
FORM_begin=$FORM_begin;
FORM_end=$FORM_end;
FORM_begin2=$FORM_begin2;
FORM_end2=$FORM_end2;
EOF
fi

# what field is field2?
if [ -z "$FORM_field" ]; then
# assume I meant the same field
  FORM_field=$FORM_field1
fi
. ./queryfield.cgi
# and save
file2=$file
kindname2=$kindname
climfield2=$climfield
map2=$map
flipcolor2=$flipcolor
# what field is field1?
FORM_field=$FORM_field1
. ./queryfield.cgi
# and save
field1=$FORM_field
file1=$file
kindname1=$kindname
climfield1=$climfield
map1=$map
flipcolor1=$flipcolor

corrargs="$file1 $file2"
if [ -n "$LSMASK" -a -n "$FORM_masktype" -a "$FORM_masktype" != "all" ]; then
  corrargs="$corrargs lsmask $LSMASK $FORM_masktype"
fi
corrargs="$corrargs interp 1"
. ./getopts.cgi
. ./getfieldopts.cgi

corrargs="$corrargs standardunits"
if [ "$FORM_var" = reldiff ]; then
  corrargs="$corrargs normsd"
fi

# Writes to the log file what the user is doing
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) difffield $corrargs" | sed -e  "s:$DIR/::g" >> log/log

. ./myvinkhead.cgi "Plot difference of fields" "$kindname1 $climfield1 minus $kindname2 $climfield2"  ""

if [ 1 = 0 ]; then
  echo '<pre>'
  echo ./bin/getunits.sh $file1
  ./bin/getunits.sh $file1
  echo ./bin/getunits.sh $file2
  ./bin/getunits.sh $file2
  echo ./bin/month2string "$FORM_month" "$FORM_sum" ave
  ./bin/month2string "$FORM_month" "$FORM_sum" ave
  echo '</pre>'
fi
eval `./bin/getunits.sh $file1`
if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname1 $climfield1 from $UNITS to $NEWUNITS<br>"
fi
eval `./bin/getunits.sh $file2`
if [ "$NEWUNITS" != "$UNITS" ];then
  echo "Converting $kindname2 $climfield2 from $UNITS to $NEWUNITS<br>"
fi

id=`date "+%Y%m%d_%H%M"`_$$
if [ -z "$FORM_netcdf" ]; then
    file=data/d$id.ctl
else
    file=data/d$id.nc
fi
###echo bin/difffield $corrargs $file
echo bin/difffield $corrargs $file > /tmp/diffield$$.log
(bin/difffield $corrargs $file >> /tmp/diffield$$.log) 2>&1
if [ ! -s $file ]; then
  echo 'Something went wrong!'
  echo '<pre>'
  cat /tmp/diffield$$.log
  echo '</pre>'
  . ./myvinkfoot.cgi
  exit
fi
if [ 1 = 0 ]; then
  echo '<pre>'
  cat /tmp/diffield$$.log
  echo '</pre>'
else
  rm /tmp/diffield$$.log
fi

FORM_STATION="$kindname1"
CLIM="$climfield1"
station="$kindname1"
kindname="$kindname2"
climfield="$climfield2"
datafile="data/d$id"
. ./grads.cgi

. ./myvinkfoot.cgi
