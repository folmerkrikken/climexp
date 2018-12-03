#!/bin/bash
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  cat > ./prefs/$EMAIL.averagefieldspace <<EOF
FORM_avex=$FORM_avex;
FORM_avey=$FORM_avey;
EOF
fi
