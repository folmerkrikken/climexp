#!/bin/sh
#
# pushes git changes to bvlclim & copy to bhlclim to publish them there.
# assumes I am logged in to the KNMI network using the SSH-only klludge, ie, that
# I can ssh to oldenbor@bvlclim

# climexp web interface
echo climexp
cd $HOME/climexp
git push bvlclim master
# Fortran & C programs
echo Fortran
cd $HOME/NINO/Fortran
git push bvlclim master
# update scripts & programs
echo update
cd $HOME/NINO
git push bvlclim master

# maybe I should put this in the hooks, but for the time being explicit
for dir in climexp.git Fortran.git update.git
do
    echo $dir
    ssh oldenbor@bvlclim "rsync -at --delete -r $dir bhlclim:climexp/; ssh bhlclim chmod -R u+w climexp/$dir"
    ssh oldenbor@bvlclim "rsync -at --delete -r $dir gjvo@shell.xs4all.nl:WWW/"
done
