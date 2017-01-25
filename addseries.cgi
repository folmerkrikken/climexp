#!/bin/sh
. ./init.cgi

export DIR=`pwd`
. ./getargs.cgi
NPERYEAR=$FORM_nperyear

j=0
while [[ $j -lt 20 ]]
do
    j=$((j+1))
    export FORM_a$j
done
export EMAIL
c=`echo $FORM_corrargs | fgrep -c '++'`
if [ $c = 0 ]; then
    # no ensemble, old code
    echo bin/addseries $FORM_corrargs > /tmp/addseries$$.log
    [ -n "$FORM_a1" ] && echo "FORM_a1 = $FORM_a1" >> /tmp/addseries$$.log
    [ -n "$FORM_a2" ] && echo "FORM_a2 = $FORM_a2" >> /tmp/addseries$$.log
    [ -n "$FORM_a3" ] && echo "FORM_a3 = $FORM_a3" >> /tmp/addseries$$.log
    [ -n "$FORM_a4" ] && echo "FORM_a4 = $FORM_a4" >> /tmp/addseries$$.log
    [ -n "$FORM_a5" ] && echo "FORM_a5 = $FORM_a5" >> /tmp/addseries$$.log
    [ -n "$FORM_a6" ] && echo "FORM_a6 = $FORM_a6" >> /tmp/addseries$$.log
    ./bin/addseries $FORM_corrargs >> /tmp/addseries$$.log 2>&1
    file=`tail -1 /tmp/addseries$$.log`
    file=./data/`basename $file`
    if [ -z "$file" -o ! -s "$file" ]; then
        echo "Content-type: text/html"
        echo
        echo
        . ./myvinkhead.cgi "Error subtracting series" ""
        echo "Something went wrong, maybe you can make sense of the error messages"
        echo '<pre>'
        cat /tmp/addseries$$.log
        echo '</pre>'
        . ./myvinkfoot.cgi
        exit
    fi
    WMO=`basename $file .dat | cut -b 2-`
    STATION=`tail -2 /tmp/addseries$$.log | head -1`
    ###rm /tmp/addseries$$.log
    TYPE=i
    NAME="added series"
else
    # ensemble, not yet robust enough to merge with old code
    infile=`echo $FORM_corrargs | tr ' ' '\n' | egrep '\.dat|\.nc' | fgrep '++' | head -1`
    i=0
    ensfile=`echo $infile | sed -e 's/+++/000/' -e 's/++/00/'`
    if [ ! -s $ensfile ]; then
        i=1
        ensfile=`echo $infile | sed -e 's/+++/001/' -e 's/++/01/'`
        if [ ! -s $ensfile ]; then
            echo "Content-type: text/html"
            echo
            echo
            . ./myvinkhead.cgi "Error subtracting ensembles" ""
            echo "Cannot find file $ensfile"
            . ./myvinkfoot.cgi
            exit
        fi
    fi
    while [ -s $ensfile ]; do
        ii=`printf %02i $i`
        iii=`printf %03i $i`
        enscorrargs=`echo "$FORM_corrargs" | sed -e "s/+++/$iii/g" -e "s/++/$ii/g"`
        if [ "$FORM_corrargs" = "$enscorrargs" ]; then
            echo "Content-type: text/html"
            echo
            echo
            . ./myvinkhead.cgi "Internal error subtracting series" ""
            echo "Something went wrong, maybe you can make sense of the error messages"
            echo "$FORM_corrargs"
            . ./myvinkfoot.cgi
            exit
        fi
        echo bin/addseries $enscorrargs > /tmp/addseries$$.log
        ./bin/addseries $enscorrargs >> /tmp/addseries$$.log
        file=`tail -1 /tmp/addseries$$.log`
        file=./data/`basename $file`
        if [ -z "$file" -o ! -s "$file" ]; then
            echo "Content-type: text/html"
            echo
            echo
            . ./myvinkhead.cgi "Error subtracting series" ""
            echo "Something went wrong, maybe you can make sense of the error messages"
            echo '<pre>'
            cat /tmp/addseries$$.log
            echo '</pre>'
            . ./myvinkfoot.cgi
            exit
        fi
        if [ -z "$WMO" ]; then
            WMO=`basename $file .dat | cut -b 2-`_+++
            touch data/i$WMO.dat
            STATION=`tail -2 /tmp/addseries$$.log | head -1`
            TYPE=i
            NAME="added series"
        fi
        mv $file ${file%.dat}_$iii.dat
        echo "# ${file%.dat}_$iii" >> data/i$WMO.dat
        i=$((i+1))
        ii=`printf %02i $i`
        iii=`printf %03i $i`
        ensfile=`echo $infile | sed -e "s/+++/$iii/" -e "s/++/$ii/"`
    done
fi
. ./getdata.cgi
