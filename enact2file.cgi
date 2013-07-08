#!/bin/sh
# to be called from other scripts
# we can finally figure out where the data is ...
if [ "$FORM_id" != cerfacs-fd1 ]; then
  ext1="oia-or"
else
  ext1="3dv-or" # ...
fi
case ${FORM_var:-choose} in
sea_water_potential_temperature)
  ext2=129;;
sea_water_salinity)
  ext2=130;;
sea_water_x_velocity)
  ext2=131;;
sea_water_y_velocity)
  ext2=132;;
sea_water_y_velocity)
  ext2=132;;
upward_sea_water_velocity)
  ext2=133;;
sea_surface_height)
  ext2=145;;
*) echo "Unknown variable $FORM_var in ENACT"
   echo '</table>'
   . ./myvinkfoot.cgi
   exit -1
esac
file=enact-${FORM_id}-${ext1}-${ext2}
