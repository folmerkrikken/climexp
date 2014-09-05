#!/bin/sh
# save all the commonn options in a preferences file

if [ -n "$EMAIL" -a "$EMAIL" != "someone@somewhere" ]; then
  cat > ./prefs/$EMAIL.plotfieldoptions.$FORM_NPERYEAR << EOF
FORM_var=$FORM_var;
FORM_year=$FORM_year;
FORM_month=$FORM_month;
FORM_day=$FORM_day;
FORM_sum=$FORM_sum;
EOF
fi
