#!/bin/bash
# to be called from other scripts
# we can finally figure out where the data is ...
case ${FORM_var:-choose} in
temp) file=thetao;;
salt) file=so;;
u)    file=uo;;
v)    file=vo;;
w)    file=wo;;
ssh)  file=zoh;;
mld)  file=zmlo;;
d20)  file=t20d;;
t300) file=thetaot;;
*) echo "Unknown variable $FORM_var in ECMWF S3"
   echo '</table>'
   . ./myvinkfoot.cgi
   exit -1
esac
