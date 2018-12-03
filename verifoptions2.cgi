#!/bin/bash
# for pretty colours in emacs...

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12 # I hope
fi

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.verifoptions.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' ./prefs/$EMAIL.verifoptions.$NPERYEAR`
  fi
fi

case $FORM_debias in
    none) debias_none=checked;;
    var)  debias_var=checked;;
    all)  debias_all=checked;;
    *)    debias_mean=checked;;
esac

cat <<EOF
<tr><td>Remove bias:<td>
<input type="radio" class="formradio" name="debias" value="none" $debias_none>nothing,
<input type="radio" class="formradio" name="debias" value="mean" $debias_mean>mean,
<input type="radio" class="formradio" name="debias" value="var" $debias_var>mean and variance,
<input type="radio" class="formradio" name="debias" value="all" $debias_all>whole PDF.
<tr><td>Name on plots:<td>
<input type="text" size="40" name="fcstname" value="$CLIM$kindname $station$climfield">
<input type="hidden" name="fcstnameorg" value="$CLIM$kindname $station$climfield">
<tr><td colspan=3><input type="submit" class="formbutton" value="Verify">
EOF
