#!/bin/sh
# maak oude plaatjes voor de on-line versie
climexp=http://climexp.knmi.nl

yrnow=`date +%Y`
yr=2001
while [ $yr -le $yrnow ]
do
	m=1
	while [ $m -le 20 ]
	do

		case $m in
			1) mon=jan;;
			2) mon=feb;;
			3) mon=mar;;
			4) mon=apr;;
			5) mon=may;;
			6) mon=jun;;
			7) mon=jul;;
			8) mon=aug;;
			9) mon=sep;;
			10) mon=oct;;
			11) mon=nov;;
			12) mon=dec;;
			13) mon=yr0;;
			14) mon=yr1;;
			15) mon=DJF;;
			16) mon=MAM;;
			17) mon=JJA;;
			18) mon=SON;;
			19) mon=summer;;
			20) mon=winter;;
		esac

		for var in rr rr_f # tlt # tg tg_f tn tn_f tx tx_f sst sst_f sst_w sst_w_f z500 z500_f z500sh z500sh_f slp slp_f ice ice_f ice_n ice_n_f ice_s t2m t2m_f t2mw t2mw_f tlt snow snow_f prcp prcp_frac pr pr_frac ice_s_f o3nh o3nh_f o3sh o3sh_f 
		do
			i=$mon
			. ./case.cgi

			file=$yr/${name}_$mon$yr.eps

			if [ ${var%%_frac} != $var ]
			then
				file=${file%.eps}_frac.eps
			fi
			echo "searching for $file"
			if [ \( ! -s $file \) -o ! -s ${file%.eps}.png ]
			then
				if [ $m -le 12 ]; then
					mm=$m
					yy=$yr
					sum=1
				elif [ $m = 13 ]; then
					mm=1
					yy=$yr
					sum=12
				elif [ $m = 14 ]; then
					mm=7
					yy=$((yr-1))
					sum=12
				elif [ $m = 15 ]; then
					mm=12
					yy=$((yr-1))
					sum=3
				elif [ $m = 16 ]; then
					mm=3
					yy=$yr
					sum=3
				elif [ $m = 17 ]; then
					mm=6
					yy=$yr
					sum=3
				elif [ $m = 18 ]; then
					mm=9
					yy=$yr
					sum=3
				elif [ $m = 19 ]; then
					mm=4
					yy=$yr
					sum=6
				elif [ $m = 20 ]; then
					mm=10
					yy=$((yr-1))
					sum=6
				else
					echo "error k,o0787b"; exit -1
				fi
				echo "calling climexp"
				command=$climexp/plotfield.cgi\?EMAIL=diagnose@knmi.nl\&climyear1=$climyear1\&climyear2=$climyear2\&cmax=${c2}\&cmin=${c1}\&colourscale=$colour\&field=${field}\&lat1=$lat1\&lat2=$lat2\&lon1=$lon1\&lon2=$lon2\&month=${mm}\&mproj=${mproj}\&plotanomaly=$plotanomaly\&plotanomalykind=$plotanomalykind\&plotsum=$sum\&plottype=lat-lon\&shadingtype=$gxout\&year=${yy}\&notitleonplot=on
				###echo "$command"
				url=`curl -s "$command" | fgrep ">eps<" | sed -e 's/.*href="//' -e 's/eps.gz.*/eps.gz/'`
				if [ -z "$url" ]; then
					echo "error computing $file"
					echo "$command"
					curl -s "$command" | sed -e '1,/Voeg hieronder de inhoud/d' -e '/Insert the body /,$d'
					exit
				fi
				if [ ! -s $file ]; then
					echo getting $climexp/$url
					curl -s $climexp/$url > $file.gz
					gunzip -f $file.gz
					size=`wc -c $file | awk '{print $1}'`
					if [ $size -gt 20000 ]; then
						if [ $var = sst -o $var = ice -o $var = prcp -o $var = prcp_frac ]; then
							mv $file $file.org
							sed -e 's/^c1 w5 c1/2000 0 translate c1 w5 c1/' $file.org > $file
						fi
						if [ $var = t2m -o $var = temp -o $var = snow -o $var = pr -o $var = pr_frac ]; then
							mv $file $file.org
							sed -e 's/^c1 w5 c1/-2000 0 translate c1 w5 c1/' $file.org > $file
						fi
					else
					    echo "Something went wrong, size=$size, deleting $file"
						rm $file
					fi
				fi
				if [ -s $file -a ! -s ${file%.eps}.png ]; then
					url=${url%.eps.gz}.png
					echo getting $climexp/$url
					curl -s $climexp/$url > ${file%.eps}.png
				fi
			fi
		done
		m=$((m+1))
	done
	yr=$((yr+1))
done
