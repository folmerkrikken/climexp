#!/bin/sh
. ./init.cgi
# average an ensemble of fields
echo "Content-type: text/html"
echo

export DIR=`pwd`
. ./getargs.cgi

# no ensemble member selection yet

. ./queryfield.cgi
. ./myvinkhead.cgi "Ensemble mean" "$kindname $climfield" "nofollow,index"

ensfile=$file
file=`echo $file | sed -e 's/%%/ave/' -e 's/\+\+/ave/' -e s/\.nc$/.ctl/`
file=data/`basename $file`

if [ -s $file ]; then
  echo "Using cached data<p>"
else
  echo "Computing ensemble mean ...<p>"
  echo "bin/averagefield_ensemble $ensfile mean $file" >> log/log
###  echo bin/averagefield_ensemble $ensfile mean $file
  bin/averagefield_ensemble $ensfile mean $file
  if [ ! -s $file ]; then
    echo "Something went wrong in the averaging routine."
    echo "Most likely, the fields are too large. Please first select the region you are interested in and then average."
    . ./myvinkfoot.cgi
    exit
  fi
fi

eval `bin/getunits.sh $file`
ENSEMBLE=""
kindname="mean $kindname"
FORM_field=data/mean_`basename $FORM_field .info`.info
cat > $FORM_field <<EOF
$file
NPERYEAR=$NPERYEAR
UNITS=$UNITS
$kindname
$climfield
EOF

. ./select.cgi
