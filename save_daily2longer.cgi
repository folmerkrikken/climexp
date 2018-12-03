#!/bin/bash
if [ -z "$NPERYEAR" ]; then
    NPERYEAR=$FORM_NPERYEAR
fi
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.daily2longeroptions.$NPERYEAR <<EOF
FORM_nperyearnew=$FORM_nperyearnew;
FORM_oper=$FORM_oper;
FORM_lgt=$FORM_lgt;
FORM_cut=$FORM_cut;
FORM_typecut=$FORM_typecut;
FORM_minfac=$FORM_minfac;
FORM_sum=$FORM_sum;
FORM_addoption=$FORM_addoption;
EOF
fi
