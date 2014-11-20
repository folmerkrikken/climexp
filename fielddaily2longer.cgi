#!/bin/sh
cat <<EOF
Content-Type: text/html



EOF

. ./getargs.cgi
# check email address
. ./checkemail.cgi
if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "Anonymous users cannot use this function as it stores new data on the server. Please <a href=\"registerform.cgi\">register or log in</a>"
  . ./myvinkfoot.cgi
  exit
fi
if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

. ./queryfield.cgi

. ./myvinkhead.cgi "Computing derived field" "$kindname $climfield" "noindex,nofollow"

# prevent abuse...
if [ "$NPERYEAR" = "$FORM_nperyearnew" -a "$FORM_oper" != "number" ]; then
   echo "The data is already at this time resolution.  Nothing to do, nothing done."
   . ./myvinkfoot.cgi
   exit
fi

if [ -z "$FORM_oper" ]; then
  FORM_oper="mean"
fi
. ./save_daily2longer.cgi

NAME="$climfield"
[ "$lwrite" = true ] && echo "NPERYEAR = $NPERYEAR<br>"
if [ "$NPERYEAR" = 366 -o "$NPERYEAR" = 365 -o "$NPERYEAR" = 360 ]; then
  NAME="daily $NAME"
elif [ "$NPERYEAR" = 73 ]; then
  NAME="pentad $NAME"
elif [ "$NPERYEAR" = 36 ]; then
  NAME="decadal $NAME"
elif [ "$NPERYEAR" = 12 ]; then
  NAME="monthly $NAME"
elif [ "$NPERYEAR" = 4 ]; then
  NAME="seasonal $NAME"
elif [ "$NPERYEAR" = 1 ]; then
  NAME="annual $NAME"
else
  NAME="$NAME"
fi
NAME="$FORM_oper of $NAME"
[ "$lwrite" = true ] && echo "FORM_nperyearnew = $FORM_nperyearnew<br>"
if [ "$FORM_nperyearnew" = 366 -o "$FORM_nperyearnew" = 365 -o "$FORM_nperyearnew" = 360 ]; then
  NAME="daily $NAME"
elif [ "$FORM_nperyearnew" = 73 ]; then
  NAME="pentad $NAME"
elif [ "$FORM_nperyearnew" = 36 ]; then
  NAME="decadal $NAME"
elif [ "$FORM_nperyearnew" = 12 ]; then
  NAME="monthly $NAME"
elif [ "$FORM_nperyearnew" = 4 ]; then
  NAME="seasonal $NAME"
elif [ "$FORM_nperyearnew" = 1 ]; then
  NAME="annual $NAME"
else
  NAME="$FORM_oper $NAME"
fi
corrargs="$file $FORM_nperyearnew $FORM_oper"
outfile=data/`basename ${FORM_field}_${FORM_nperyearnew}_${FORM_oper}`
if [ -n "$FORM_minfac" ]; then
    corrargs="$corrargs minfac $FORM_minfac"
    outfile=${outfile}_$FORM_minfac
fi
if [ "$FORM_lgt" = "lt" -o "$FORM_lgt" = "gt" ]; then
  if [ -z "$FORM_cut" -a "$FORM_typecut" != "n" ]; then
    FORM_cut=0
  fi
  corrargs="$corrargs $FORM_lgt $FORM_cut$FORM_typecut"
  NAME="$NAME $FORM_lgt$FORM_cut$FORM_typecut"
  if [ "$FORM_typecut" !+ " " ]; then
      outfile=${outfile}_$FORM_lgt$FORM_cut$FORM_typecut
  else
      outfile=${outfile}_$FORM_lgt$FORM_cut
  fi    
fi
if [ -n "$FORM_sum" -a "$FORM_sum" != 0 -a "$FORM_sum" != 1 ]; then
    corrargs="$corrargs ave $FORM_sum"
    outfile=${outfile}_${FORM_sum}v
fi

if [ -n "$ENSEMBLE" ]; then
    c=`echo $file | fgrep -c '%%%'`
    if [ $c = 1 ]; then
        testfile=${outfile}_000
        outfile=${outfile}_%%%
    else
        testfile=${outfile}_00
        outfile=${outfile}_%%
    fi
else
    testfile=$outfile
fi

if [ "$FORM_addoption" = add_trend -o "$FORM_addoption" = add_clim ]; then
    echo "Due to a problem with a software license (don''t ask) the option $FORM_addoption cannot be computed today"
    . ./myvinkfoot.cgi
    exit
fi

[ "$lwrite" = true ] && echo "c=$c<br>file=$file<br>testfile = $testfile<br>outfile=$outfile<br>"
if [ ! -s $testfile.ctl -o $testfile.ctl -ot $file ]; then
    if [ -s $testfile.ctl ]; then
       rm `echo $outfile.ctl | sed -e 's/%%%/???/' -e 's/%%/??/'`
       rm `echo $outfile.dat | sed -e 's/%%%/???/' -e 's/%%/??/'`
    fi
    [ "$lwrite" = true ] && echo "daily2longerfield.sh $corrargs $NOMISSING $outfile.ctl"
    echo "daily2longerfield.sh $corrargs $NOMISSING $outfile.ctl" >> log/log
    (./bin/daily2longerfield.sh $corrargs $NOMISSING $outfile.ctl) 2>&1
fi

infofile=$outfile.$EMAIL.info
###echo "cat > $infofile <<EOF"
cat > $infofile <<EOF
$outfile.ctl
NPERYEAR=$FORM_nperyearnew
LSMASK=$LSMASK
$kindname
$NAME
EOF

FORM_field=$infofile
. ./select.cgi
#cat <<EOF
#The field has been generated.  Use the links in the menu on the right to proceed.
#EOF
#FORM_field="$infofile"
#
#. ./myvinkfoot.cgi
