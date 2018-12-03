#!/bin/bash
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.statistical.$NPERYEAR
  cat > $def << EOF
FORM_var=$FORM_var;
FORM_year=$FORM_year;
FORM_changesign=$FORM_changesign;
FORM_dgt=$FORM_dgt;
FORM_restrain=$FORM_restrain;
FORM_minnum=$FORM_minnum;
EOF
fi
