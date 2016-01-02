#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Decadal hindcasts" "index,nofollow"
cat <<EOF
<div class="inhoudsopgave">
<div class="inhoudlink"><a href="#cmip5all">CMIP5 multi-model</a></div>
<div class="inhoudlink"><a href="#cmip5ens">CMIP5 full ensembles</a></div>
<div class="inhoudlink"><a href="#cmip5ave">CMIP5 ensemble means</a></div>
<div class="inhoudlink"><a href="#ensemblesens">ENSEMBLES full ensembles</a></div>
<div class="inhoudlink"><a href="#ensemblesave">ENSEMBLES ensemble means</a></div>
</div>

<div class="kalelink">
EOF
cat CMIP5_disclaimer.html
cat <<EOF
</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realTable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

years="1 2-5 6-9"
# CMIP5
vars="tas tasmin tasmax pr psl rsds tos"
for ensave in all ens ave
do
    case $ensave in
	all) echo '<tr><th colspan=13><a name="cmip5all"></a>CMIP5 MULTI-MODEL</th>';;
	ens) echo '<tr><th colspan=13><a name="cmip5ens"></a>CMIP5 FULL ENSEMBLES</th>';;
	ave) echo '<tr><th colspan=13><a name="cmip5ave"></a>CMIP5 MODEL MEANS</th>';;
    esac
    if [ $ensave = all ]; then
	models="modmean mod ens"
    else
	models="CanCM4 CNRM-CM5 HadCM3 MIROC4h MIROC5 MRI-CGCM3"
    fi
    for model in $models
    do
        echo "<tr><th>model<th>nr<th>year"
        for var in $vars
        do
    	    case $var in
	        tasmin)  varname="tas<br>min";;
	        tasmax)  varname="tas<br>max";;
	        evspsbl) varname="evsp<br>sbl";;
	        *)       varname=$var;;
	    esac
	    echo "<th>$varname"
        done
	case $model in
	    CanCM4) imin=1;imax=2;;
	    HadCM3) imin=2;imax=2;;
	    *)      imin=1;imax=1;;
	esac
	case $model in
	    modmean) nr="";;
	    mod) nr=7;;
	    ens) nr=57;;
	    CanCM4) nr=10;;
	    CNRM-CM5) nr=10;;
	    HadCM3) nr=10;;
            MIROC4h) nr=3;;
            MIROC5) nr=6;;
	    MRI-CGCM3) nr=9;;
	    *) nr=10;;
	esac
	ii=$((imin-1))
	while [ $ii -le $imax ]; do
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
                    MIROC5) nr=1;;
		    MRI-CGCM3) nr=3;;
		esac
	    fi
	    for ext in $years
	    do
		echo "<tr><td $align>$m<td>$nr<td>$ext"
		m=""
		for var in $vars
		do
		    case $var in
			tos|zos*) type=Omon;;
			mr*) type=Lmon;;
			*) type=Amon;;
		    esac
		    if [ $i = 0 -a $model = CanCM4 -a $var != tas -a $var != pr -a $var != psl ]; then
			echo "<td>&nbsp;"
		    elif [ $i = 0 -a $model = CNRM-CM5 -a $var = tos ]; then
			echo "<td>&nbsp;"
		    else
			echo "<td><input type=radio class=formradio name=field value=cmip5_${var}_${type}_${model}_decadal_${ext}_i${i}p1_${ensave}>"
		    fi
		done
	    done
	done
    done
done

# ENSEMBLES
models="ensembles multimodel ifs33r1 hadgem2 arpege46 echam5 depresys"
vars="tas tasmin tasmax pr psl ssr ts"
for ensave in ens ave
do
    case $ensave in
	ens) echo '<tr><th colspan=13><a name="ensemblesens"></a>ENSEMBLES FULL ENSEMBLES</th>';;
	ave) echo '<tr><th colspan=13><a name="ensemblesave">ENSEMBLES ENSEMBLE MEANS</th>';;
    esac
    echo "<tr><th>model<th>nr<th>year"
    for var in $vars
    do
	case $var in
	    tasmin)  varname="tas<br>min";;
	    tasmax)  varname="tas<br>max";;
	    evspsbl) varname="evsp<br>sbl";;
	    *)       varname=$var;;
	esac
	echo "<th>$varname"
    done
    for model in $models
    do
	m=$model
	case $model in
	    ensembles) nr=21;;
	    multimodel) nr=12;;
	    depresys)  nr=9;;
	    *)         nr=3;;
	esac
	for ext in $years
	do
	    echo "<tr><td>$m<td>$nr<td>$ext"
	    m=""
	    for var in $vars
	    do
		if [ $var = tasmin -o $var = tasmax -o $var = zos ]; then
		    echo "<td>&nbsp;"
		else
		    echo "<td><input type=radio class=formradio name=field value=\"${var}_${model}_${ensave}dec_$ext\">"
		fi
	    done
	done
    done
done
echo '</table>'

. ./myvinkfoot.cgi
