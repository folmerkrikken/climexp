#!/bin/sh
# maybe I should put this in the hooks, but for the time being explicit
if [ "${HOST#bvlclim}" = $HOST ]; then
    echo "$0: error: only run on bvlclim"
    exit -1
fi
cd $HOME
for dir in climexp.git Fortran.git update.git
do
    echo $dir
    ssh oldenbor@bvlclim "rsync -at --delete -r $dir bhlclim:climexp/; ssh bhlclim chmod -R u+w climexp/$dir"
    ssh oldenbor@bvlclim "rsync -at --delete -r $dir gjvo@shell.xs4all.nl:WWW/"
done
