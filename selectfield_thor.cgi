#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "THOR decadal hindcasts" "index,nofollow"

if [ ${REMOTE_ADDR#145.23} = $REMOTE_ADDR \
  -a $REMOTE_ADDR != 82.95.194.243 \
  -a $REMOTE_ADDR != 193.61.196.141 \
  -a $REMOTE_ADDR != 193.61.196.142 \
  -a $REMOTE_ADDR != 127.0.0.1 \
  ]; then
    echo "$EMAIL ($REMOTE_ADDR) Select THOR hindcast" >> log/log
    echo "Access denied. Please contact <a href=\"mailto:oldenborgh@knmi.nl\">me</a> if you think you should have access to these data"
    . ./myvinkfoot.cgi
    exit
fi
touch /tmp/missing$$.txt

cat <<EOF
<div class="inhoudsopgave">
<div class="inhoudlink"><a href="#THOR_all">THOR multi-model</a></div>
<div class="inhoudlink"><a href="#THOR_ens">THOR full ensembles</a></div>
<div class="inhoudlink"><a href="#THOR_ave">THOR ensemble means</a></div>
</div>

<div class="kalelink">
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realTable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

years="1 2-5 6-9"
# THOR
for ensave in all ens ave
do
    case $ensave in
		all) echo '<tr><th colspan=13><a name="THOR_all"></a>THOR MULTI-MODEL</th>';;
		ens) echo '<tr><th colspan=13><a name="THOR_ens"></a>THOR FULL ENSEMBLES</th>';;
		ave) echo '<tr><th colspan=13><a name="THOR_ave"></a>THOR MODEL MEANS</th>';;
    esac
    if [ $ensave = all ]; then
		models="modmean mod ens"
    else
		models="ECMWF-S4 EC-EARTH23 HadCM3 ECHAM5"
    fi
	    
    for model in $models
    do

	    for ivars in 1 2 3
    	do
			case $ivars in
	    		1) vars="tas pr psl sic tos sos zos mlotst msftbarot"
					echo "<tr><th>model<th>nr<th>year";;
	    		2) vars="amoc ohc400 ohc700 ohc1000 ohc2000 osc400 osc700 osc1000 osc2000"
					echo "<tr><th>&nbsp<th>nr<th>year";;
				3) vars="Tglobal amo amoc26 amoc40"
					echo "<tr><th>&nbsp<th>nr<th>year";;					
	    		*) echo "$0: error: unknown value for $ivars"; exit -1;;
			esac
        	for var in $vars
        	do
    	    	case $var in
			        tasmin)  varname="tas<br>min";;
	    		    tasmax)  varname="tas<br>max";;
			        evspsbl) varname="evsp<br>sbl";;
	    		    mlotst)  varname="mlo<br>tst";;
			        msftbarot) varname="msft<br>barot";;
					ohc*)    varname="ohc<br>${var#ohc}";;
					osc*)    varname="osc<br>${var#osc}";;
					amoc)    varname=$var;;
					amoc*)   varname="amoc<br>${var#amoc}";;
					Tglobal) varname="tas<br>global";;
	        		*)       varname=$var;;
		    	esac
		    	echo "<th>$varname"
        	done
			case $model in
	    		*)      imin=1;imax=1;;
			esac
			case $model in
	    		modmean) nr="1";;
			    mod) nr=4;;
	    		ens) nr=30;;
			    HadCM3) nr=10;;
	    		EC-EARTH23) nr=5;;
			    ECMWF-S4) nr=5;;
	    		ECHAM5) nr=10;;
			    *) nr=-1;;
			esac
			ii=$((imin-1))
			while [ $ii -le $((imax-1)) ]; do  # was -le $imax to include NoAssim
	    		ii=$((ii+1))
			    if [ $ii -le $imax ]; then
					i=$ii
					align=""
					case $model in
					    modmean) m="multi-model mean";;
		    			mod) m="all models";;
					    ens) m="all members";;
		    			*) m="$model i$i";;
					esac
			    else
					i=0
					align="align=right"
					m="no-assim"
					# only the ones that differ from above
					case $model in
		    			*) nr=1;;
					esac
			    fi
	    		for ext in $years
			    do
					echo "<tr><td $align>$m<td>$nr<td>$ext"
					m=""
					for var in $vars
					do
		    			case $var in
							tos|sos|zos*|ohc*|osc*|msft*|mlo*|amoc) type=Omon;;
							sic) type=OImon;;
							mr*) type=Lmon;;
							amoc*)   firstpart=amoc_Omon;ave=max${var#amoc};;
							Tglobal) firstpart=tas_Amon;ave=global;;
							amo)     firstpart=tos_Omon;ave=amo;;
							*) type=Amon;;
					    esac
					    if [ "${model#mod}" = $model -a "${model#ens}" = $model ]; then
					    	ippart=_i${i}p1
					    else
					    	ippart=""
					    fi
					    if [ $ensave = ave ]; then
					    	seriesensave="ave"
					    else
					    	seriesensave="%%"
					    fi
		    			if [ $model = ECMWF-S4 -a $i = 0 ]; then
							echo "<td>&nbsp;"
		    			elif [ $model = ECMWF-S4 -a \( $var = msftbarot \) ]; then
							echo "<td>&nbsp;"
		    			elif [ $model = EC-EARTH23 -a $i = 0 ]; then
							echo "<td>&nbsp;"
		    			elif [ $model = ECHAM5 -a \( $var = sos -o $var = pr -o $var  = tas -o $var = Tglobal \) ]; then
							echo "<td>&nbsp;"
		    			elif [ $model = ECMWF-S4 -a $i = 0 ]; then
							echo "<td>&nbsp;"
		    			elif [ $model = HadCM3 -a $var = msftbarot ]; then
							echo "<td>&nbsp;"
		    			elif [ $ivars -le 2 ]; then
							echo "<td><input type=radio class=formradio name=field value=thor_${var}_${type}_${model}_decadal_${ext}_i${i}p1_${ensave}>"
		    			else
		    				series=THOR/${firstpart}_${model}_yr${ext}${ippart}_${seriesensave}_${ave}
		    				file=`echo "$series" | sed -e 's/%%/00/'`
		    				if [ ! -f $file.dat -a ! -f $file.nc ]; then
		    					echo "$file" >> /tmp/missing$$.txt
		    					echo "<td>E"
		    				else
								echo "<td><a href=\"getindices.cgi?WMO=${series}\&STATION=THOR_${model}_${var}\&TYPE=i\&id=$EMAIL\">X</a>"
							fi
		    			fi
					done
			    done
			done
	    done
	done
done

echo '</table>'

if [ -s /tmp/missing$$.txt ]; then
	echo "<pre>Could not locate files:"
	cat /tmp/missing$$.txt
	echo '</pre>'
fi
rm -f /tmp/missing$$.txt

. ./myvinkfoot.cgi
