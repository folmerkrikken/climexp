#!/bin/sh
# form with options for averagefieldspace.cgi

if [ "$EMAIL" != someone@somewhere ]; then
  if [ -n "$DIR" ]; then
    def=$DIR/prefs/$EMAIL.averagefieldspace.$NPERYEAR
  else
    def=prefs/$EMAIL.averagefieldspace.$NPERYEAR
  fi
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-a-zA-Z_]*[-+_0-9.]*;$' $def`
  fi
fi


cat <<EOF
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="field" value="$FORM_field">
Average over blocks of 
<input type="$number" type="$number" min=1 step=1 class="forminput" name="avex" $textsize3 value="$FORM_avex">
longitude and 
<input type="$number" type="$number" min=1 step=1 class="forminput" name="avey" $textsize3 value="$FORM_avey">
latitude grid cells
EOF
