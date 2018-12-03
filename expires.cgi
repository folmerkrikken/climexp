#!/bin/bash
# add a max-age HTTP/1.1 header for easier control, also works on 
# machine where convdate is absent
###echo "Cache-Control: max-age=86400"
if [ -x bin/convdate ]; then
# make an Expires header for better performance
# (really, really should switch to perl or python!  another 3 processes!)
today=`date +%s`
# one day later, so that if the series is in active use it gets read again
# before the three days are over.
later=$(($today + 86400))
later=`bin/convdate -d -c $later | sed -e 's/+0000 (UTC)/GMT/'`
echo "Expires: $later"
fi
