#!/bin/sh
for file in $HOME/climexp_numerical/$PVM_ARCH/*
do
    if [ -x $file ]; then
        ln -s $file
    fi
done