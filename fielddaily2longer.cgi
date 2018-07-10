#!/bin/sh
cat <<EOF
Content-Type: text/html



EOF

. ./init.cgi
. ./getargs.cgi
# check email address
. ./checkemail.cgi
if [ "$EMAIL" = "someone@somewhere" ]; then
  . ./myvinkhead.cgi "Error" "noindex,nofollow"
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
if [ -n "$FORM_minfac" ]; then
    corrargs="$corrargs minfac $FORM_minfac"
    outfile=${outfile}_$FORM_minfac
fi
if [ -n "$FORM_sum" -a "$FORM_sum" != 0 -a "$FORM_sum" != 1 ]; then
    corrargs="$corrargs ave $FORM_sum"
    outfile=${outfile}_${FORM_sum}v
fi
if [ -n "$FORM_addoption" ]; then
    corrargs="$corrargs $FORM_addoption"
    if [ $FORM_addoption != add_anom ]; then
        outfile=${outfile}_${FORM_addoption#add_}
        NAME="$NAME ${FORM_addoption#add_}"
    fi
fi

if [ -n "$ENSEMBLE" ]; then
    c=`echo $file | fgrep -c '%%%'`
    if [ $c = 1 ]; then
        format='%03i'
        percent='%%%'
    else
        format='%02i'
        percent='%%'
    fi
    outfile=${outfile}_$percent
    doit=false
    iens=0
    ens=`print $format $iens`
    inensfile=`echo $file | sed -e "s/$percent/$ens/"`
    outensfile=`echo $outfile.nc | sed -e "s/$percent/$ens/"`
    while [ -s $inensfile -o $iens = 0 ]; do
        if [ ! -s $outensfile -o $outensfile -ot $inensfile ]; then
            doit=true
        fi
        [ -s $outensfile ] && testfile=$outensfile
        ((iens++))
        ens=`print $format $iens`
        inensfile=`echo $file | sed -e "s/$percent/$ens/"`
        outensfile=`echo $outfile | sed -e "s/$percent/$ens/"`
    done
else
    testfile=$outfile.nc
    if [ ! -s $outfile -o $outfile -ot $file ]; then
        doit=true
    else
        doit=false
    fi
fi

[ "$lwrite" = true ] && echo "c=$c<br>file=$file<br>testfile = $testfile<br>outfile=$outfile<br>"
if [ $doit = true ]; then
    [ "$lwrite" = true ] && echo "daily2longerfield.sh $corrargs $NOMISSING $outfile.nc"
    echo `date` "$EMAIL ($REMOTE_ADDR) daily2longerfield.sh $corrargs $NOMISSING $outfile.nc" >> log/log
    (./bin/daily2longerfield.sh $corrargs $NOMISSING $outfile.nc) 2>&1
fi
splitfield=false # we have concatenated the fields in daily2longerfield.sh

infofile=$outfile.$EMAIL.info
###echo "cat > $infofile <<EOF"
cat > $infofile <<EOF
$outfile.nc
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
