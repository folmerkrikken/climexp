#!/bin/sh
file="$1"
if [ -z "$file" ]; then
  echo "usage: $0 file"
  exit -1
fi
describefile=${0%.sh}
if [ ${file%.nc} = $file -a ${file%.cdf} = $file -o ${file#data} != $file ]; then
  ($describefile $file > /dev/null) 2>&1
  eval `./bin/getunits $file`
else
  c1=`echo $file | fgrep -c '%%'`
  c2=`echo $file | fgrep -c '++'`
  if [ $c1 -eq 0 -a $c2 -eq 0 ]
  then
    ensfile=$file
  else
  	c3=`echo $file | fgrep -c '%%%'`
  	i=0
  	if [ $c3 = 0 ]; then
    	ii=00
    	nmax=99
    else
    	ii=000
    	nmax=999
    fi
    newestfile=""
    while [ $i -le $nmax ]
    do
    	if [ $c3 = 0 ]; then
		    ensfile=`echo $file | sed -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
		else
		    ensfile=`echo $file | sed -e "s:\%\%\%:$ii:"`
		fi
	    if [ -s $ensfile -a \( -z "$newestfile" -o $ensfile -nt "$newestfile" \) ]; then
	    	newestfile=$ensfile
	    fi
	    if [ $i -lt 1 -o -s $ensfile ]; then
		    i=$((i+1))
		else
			i=$((1+nmax))
		fi
		if [ $c3 = 0 ]; then
		    if [ $i -lt 10 ]; then
		    	ii=0$i
  			else
  				ii=$i
  			fi
  		else
		    if [ $i -lt 10 ]; then
		    	ii=00$i
  			elif [ $i -lt 100 ]; then
  				ii=0$i
  			else
  				ii=$i
  			fi
  		fi
	done
	ensfile=$newestfile
  fi
  metadata=./metadata/`echo $file|tr '/' '.'`.txt
  if [ ! $metadata -ot $ensfile ]; then
#   quick from chache
    cat $metadata
    eval `cat $metadata.eval`
#   but make sure the field is read once to make it faster on the next page
    ( ./bin/getunits $file < /dev/null > /dev/null 2>&1 ) &
  else
    ($describefile $file > /dev/null ) 2>&1 | tee $metadata
    ./bin/getunits $file > $metadata.eval
    touch -r $file $metadata
    touch -r $file $metadata.eval
  fi
fi
