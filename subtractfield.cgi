#!/bin/sh
# subtract the influence of an index on a field, returning the new field
# Geert Jan van Oldenborgh, KNMI, 29-dec-2004
lwrite=false

echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
###echo '<pre>'
###set | fgrep FORM_
###echo '</pre>'
###exit
. ./queryfield.cgi

. ./myvinkhead.cgi "Generate field" "$kindname $climfield minus the influence of $FORM_station" ""

echo "One moment...<p>"
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) subtractfield $file $corrargs" | sed -e "s:$DIR/::g" >> log/log

c1=`echo $file | fgrep -c '%%'`
c2=`echo $file | fgrep -c '++'`
c3=`echo $file | egrep -c '%%%|\+\+\+'`
if [ $c1 -eq 0 -a $c2 -eq 0 ]
then
	outfile=data/s$$.ctl
	echo ./bin/correlatefield $file $FORM_corrargs subtract $outfile > /tmp/s$$.log
	(./bin/correlatefield $file $FORM_corrargs subtract $outfile >> /tmp/s$$.log) 2>&1
	if [ ! -s $outfile ]; then
		echo "Something went wrong...<pre>"
		echo $DIR/bin/correlatefield $file $FORM_corrargs subtract $outfile
		cat /tmp/s$$.log
		echo '</pre>'
		. ./myvinkfoot.cgi
		exit
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
	outfile=data/s$$_%%%.ctl
	touch /tmp/s$$.log
	ensfile=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
	while [ $i -lt $nmax ]
	do
		[ $lwrite = true ] && echo "ensfile = $ensfile"
		if [ -s $ensfile -o -s data/$ensfile ]
		then
			ensargs=`echo $FORM_corrargs | sed -e "s@\+\+\+@$ii@" -e "s@\%\%\%@$ii@" -e "s@\+\+@$ii@" -e "s@\%\%@$ii@"`
			ensout=`echo $outfile | sed -e "s@\%\%\%@$ii@"`
			echo ./bin/correlatefield $ensfile $ensargs subtract $ensout >> /tmp/s$$.log
			(./bin/correlatefield $ensfile $ensargs subtract $ensout >> /tmp/s$$.log) 2>&1
			if [ ! -s $ensout ]; then
				echo "Something went wrong...<pre>"
				echo ./bin/correlatefield $ensfile $ensargs subtract $ensout
				cat /tmp/s$$.log
				echo '</pre>'
				. ./myvinkfoot.cgi
				exit
			fi
			echo "# $ensout"
		fi
		i=$(($i + 1))
		ii=`printf $format $i`
		ensfile=`echo $file | sed -e "s:\+\+\+:$ii:" -e "s:\%\%\%:$ii:" -e "s:\+\+:$ii:" -e "s:\%\%:$ii:"`
	done	
fi
if [ "$lwrite" = true ]; then
	cat /tmp/s$$.log | sed -e 's/$/<br>/'
fi
rm /tmp/s$$.log

infofile=data/s$$.$EMAIL.info
cat > $infofile << EOF
$outfile
NPERYEAR=$NPERYEAR
LSMASK=$LSMASK
$kindname
$climfield - $FORM_station
EOF
cat << EOF
Field generated succesfully
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$FORM_EMAIL">
<input type="hidden" name="field" value="$infofile">
<input type="submit" class=formbutton value="Continue">
</form>
EOF
. ./myvinkfoot.cgi
