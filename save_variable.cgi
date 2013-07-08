#!/bin/sh
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.choosevariable
  cat > $def << EOF
FORM_var=$FORM_var;
FORM_threshold=$FORM_threshold;
FORM_minfac=$FORM_minfac;
EOF
fi
