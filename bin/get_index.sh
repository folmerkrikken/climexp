#!/bin/sh
lwrite=false
if [ -n "$EMAIL " -a "$EMAIL" = oldenbor@knmi.nl ]; then
	lwrite=true # false
fi
if [ -z "$DIR" ]; then
	DIR=`pwd`
fi
PROG=`basename $0 .sh`
if [ -z "$file" ]; then
	echo "error: \$file is undefined!"
	exit -1
fi
if [ -z "$TYPE$WMO" ]; then
	echo "error: \$TYPE\$WMO is undefined!"
	exit -1
fi
c1=`echo $file | fgrep -c '%%'`
c2=`echo $file | fgrep -c '++'`
c3=`echo $file | egrep -c '%%%|\+\+\+'`
if [ $c1 -eq 0 -a $c2 -eq 0 ]
then
	outfile=data/$TYPE$WMO.dat
	if [ ! -s $outfile -o $outfile -ot $file ]; then
		[ $lwrite = true ] && echo "# $DIR/bin/$PROG $*"
		$DIR/bin/$PROG $*
	fi
else
	i=0
	if [ $c3 = 0 ]; then
		ii=00
		nmax=100
		format="%02i"
	else
		ii=000
		nmax=1000
		format="%03i"
	fi
	ensfile=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
	while [ $i -lt $nmax ]
	do
		[ "$lwrite" = true ] && echo "ensfile = $ensfile"
		if [ -s $ensfile -o -s data/$ensfile ]
		then
			ensargs=`echo $* | sed -e "s@$file@$ensfile@"`
			ensout=`echo data/$TYPE$WMO.dat | sed -e "s@\+\+\+@$ii@" -e "s@\%\%\%@$ii@" -e "s@\+\+@$ii@" -e "s@\%\%@$ii@"`
			[ $lwrite = true ] && echo "$DIR/bin/$PROG $ensargs > $ensout" 1>&2
			if [ ! -s $ensout ]; then
				$DIR/bin/$PROG $ensargs > $ensout
    			c=`fgrep -v '#' $ensout | wc -l`
				if [ $c = 0 ]; then
					echo "<br>Something went wrong in bin/$PROG $ensargs"
					echo "<br>Retrying...<br>" 1>&2
			        $DIR/bin/$PROG $ensargs > $ensout
				    c=`fgrep -v '#' $ensout | wc -l`
			        if [ $c = 0 ]; then
						echo "<br>Something again went wrong"
				    	echo "<br>Retrying...<br>"  1>&2
				        $DIR/bin/$PROG $ensargs > $ensout
					    c=`fgrep -v '#' $ensout | wc -l`
						if [ $c = 0 ]; then
							echo "<br>And again"
					    	echo "<br>Retrying for the last time...<br>"  1>&2
					        $DIR/bin/$PROG $ensargs > $ensout
						    c=`fgrep -v '#' $ensout | wc -l`
							if [ $c = 0 ]; then
					        	rm $ensout
								echo "<br>$0: error in bin/$PROG $ensargs > $ensout<br>" 1>&2
							fi
						fi
					fi
				fi
			fi
			echo "# $ensout"
		fi
		i=$(($i + 1))
		ii=`printf $format $i`
		ensfile=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
	done
fi
