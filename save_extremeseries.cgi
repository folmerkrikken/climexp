#!/bin/sh
if [ -z "$NPERYEAR" ]; then
    NPERYEAR=$FORM_NPERYEAR
fi
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.extremeoptions.$NPERYEAR <<EOF
FORM_nperyearnew=$FORM_nperyearnew;
FORM_climdex_tn=$FORM_climdex_tn;
FORM_climdex_tx=$FORM_climdex_tx;
FORM_climdex_tg=$FORM_climdex_tg;
FORM_climdex_rr=$FORM_climdex_rr;
FORM_threshold=$FORM_threshold;
EOF
fi
