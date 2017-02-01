#!/bin/sh
###set -x
file="$1"
if [ -z "$file" ]; then
  echo "usage: $0 file"
  exit -1
fi
[ "$lwrite" = true ] && echo "file=$file<br>"
describefield=${0%.sh}
if [ ${file%.nc} = $file -a ${file%.cdf} = $file -o ${file#data} != $file ]; then
    [ "$lwrite" = true ] && echo "grads file $file<br>"
    ($describefield $file > /dev/null) 2>&1
    eval `./bin/getunits $file`
else
    [ "$lwrite" = true ] && echo "netcdf file $file"  
    c1=`echo $file | fgrep -c '%%'`
    c2=`echo $file | fgrep -c '++'`
    [ "$lwrite" = true ] && echo "ensemble? c1,c2 = $c1,$c2<br>"
    if [ $c1 -eq 0 -a $c2 -eq 0 ]; then
        if [ "$splitfield" = true ]; then
            ensfile=`ls -t $file 2>&1 | head -1`
            allfiles=`ls $file`
        else
            ensfile=$file
        fi
    else
        c3=`echo $file | fgrep -c '%%%'`
        i=0
        if [ $c3 = 0 ]; then
            ii=00
            nmax=99
            format="%02i"
            pattern='%%'
        else
            ii=000
            nmax=999
            format="%03i"
            pattern='%%%'
        fi
        newestfile=""
        while [ $i -le 1 ]; do
            if [ $c3 = 0 ]; then
                allfiles=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
            else
                allfiles=`echo $file | sed -e "s:\%\%\%:$ii:"`
            fi
            if [ "$splitfield" = true ]; then
                ensfile=`ls -t $allfiles 2>&1 | head -1`
            else
                ensfile=$allfiles
            fi
            if [ -s "$ensfile" -a \( -z "$newestfile" -o "$ensfile" -nt "$newestfile" \) ]; then
                [ "$lwrite" = true ] && echo "set newestfile to $ensfile"
                newestfile=$ensfile
                newestfiles=$allfiles
                newestii=$ii
            fi
            if [ $i -lt 1 -o -s "$ensfile" ]; then
                i=$((i+1))
            else
                i=$((1+nmax))
            fi
            ii=`printf $format $i`
        done
        ensfile=$newestfile
        allfiles=$newestfiles
    fi
    metadata=./metadata/$file.txt
    metadir=`dirname $metadata`
    [ ! -d $metadir ] && mkdir -p $metadir
    [ "$lwrite" = true ] && echo "echo ensfile=$ensfile<br>"
    if [ ! -s $ensfile ]; then
        echo "error: cannot locate $ensfile<br>"
        exit -1
    fi
    if [ "$splitfield" = true ]; then
        files=`echo $allfiles | sed -e "s/_$newestii/_$pattern/g"`
        [ "$lwrite" = true ] && echo "files=$files"
    else
        files=$file
    fi
    if [ -s $metadata -a ! $metadata -ot $ensfile ]; then
#       quick from cache
        cat $metadata
        if [ -s $metadata.eval ]; then
            eval `egrep '^[A-Z]*=[-"0-9a-zA-Z/*]*$' $metadata.eval`
        else
            ./bin/getunits $files | fgrep -v error > $metadata.eval        
            touch -r $ensfile $metadata.eval
            [ -s $metadata.eval ] && eval `egrep '^[A-Z]*=[-"0-9a-zA-Z/*]*$' $metadata.eval`
        fi
#       but make sure the field is read once to make it faster on the next page
        [ "$splitfield" != true ] && ( ./bin/getunits $files < /dev/null > /dev/null 2>&1 ) &
    else
        [ "$lwrite" = true ] && echo "executing $describefield $files"
        ($describefield $files > /dev/null ) 2>&1 | tee $metadata
        ###echo "./bin/getunits $file &gt; $metadata.eval<br>"
        ./bin/getunits $files | fgrep -v error > $metadata.eval
        touch -r $ensfile $metadata
        touch -r $ensfile $metadata.eval
    fi
fi
