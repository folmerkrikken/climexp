#!/bin/sh
echo "Content-Type: text/html"
echo
echo

(cd ..; . ./init.cgi)
(cd ..; . ./getargs.cgi)

c=`dirname "$SCRIPT_FILENAME" | egrep -c 'halfjaaroverzicht|biannual_overview'`
if [ $c = 1 ]; then
    NPERYEAR=2
else
    c=`dirname "$SCRIPT_FILENAME" | egrep -c 'seizoensoverzicht|seasonal_overview'`
    if [ $c = 1 ]; then
        NPERYEAR=4
    else
        c=`dirname "$SCRIPT_FILENAME" | egrep -c 'jaaroverzicht|annual_overview'`
        if [ $c = 1 ]; then
            NPERYEAR=1
        else
            NPERYEAR=12
        fi
    fi
fi
if [ -z "$FORM_mon1" -a -z "$FORM_year1" ]; then
    FORM_mon1=`date -d "1 month ago" "+%b" | tr "[:upper:]" "[:lower:]"`
    FORM_year1=`date -d "1 month ago" "+%Y"`
    if [ ! -s $FORM_year1/t2m_ghcncams_$FORM_mon1$FORM_year1.png ]; then
        FORM_mon1=`date -d "2 months ago" "+%b" | tr "[:upper:]" "[:lower:]"`
        FORM_year1=`date -d "2 months ago" "+%Y"`
    fi
fi
if [ -z "$FORM_mon1" ]; then
    FORM_mon1=`date -d "1 month ago" "+%b" | tr "[:upper:]" "[:lower:]"`
fi
if [ -z "$FORM_year1" ]; then
    FORM_year1=`date -d "1 month ago" "+%Y"`
fi
if [ $NPERYEAR = 1 ]; then
    case "$FORM_mon1" in
        DJF|MAM|jan|feb|mar|apr|may) FORM_mon1=dec; FORM_year1=$((FORM_year1-1));;
        JJA|SON|jul|aug|sep|oct|nov) FORM_mon1=jun;;
    esac
fi
if [ $NPERYEAR = 4 ]; then
    case "$FORM_mon1" in
        nov|dec)     FORM_mon1=SON;;
        jan)             FORM_mon1=SON;FORM_year1=$((FORM_year1-1));;
        feb|mar|apr) FORM_mon1=DJF;;
        may|jun|jul) FORM_mon1=MAM;;
        aug|sep|oct) FORM_mon1=JJA;;
    esac
fi
if [ $NPERYEAR = 12 ]; then
    case "$FORM_mon1" in
        DJF) FORM_mon1=feb;;
        MAM) FORM_mon1=may;;
        JJA) FORM_mon1=aug;;
        SON) FORM_mon1=nov;;
        winter) FORM_mon1=mar;;
        summer) FORM_mon1=sep;;
    esac
fi
[ -z "$FORM_var" ] && FORM_var="t2m_ghcncams_w"
[ -z "$FORM_anomalie" ] && FORM_anomalie=ja
[ -z "$FORM_kort" ] && FORM_kort=nee
[ -z "$FORM_expert" ] && FORM_expert=nee
dir=`dirname "$SCRIPT_FILENAME"` 
if [ "${dir%weather}" != "$dir" ]; then
    FORM_lang=en
else
    FORM_lang=nl
fi
if [ "$FORM_lang" = nl ]; then
    lang_ext="_nl"
    mjan=januari
    mfeb=februari
    mmar=maart
    mapr=april
    mmay=mei
    mjun=juni
    mjul=juli
    maug=augustus
    msep=september
    moct=oktober
    mnov=november
    mdec=december
    mDJF="winter (december-februari)"
    mMAM="lente (maart-mei)"
    mJJA="zomer (juni-augustus)"
    mSON="herfst (september-november)"
    mwinter="winterhalfjaar (oktober-maart)"
    msummer="zomerhalfjaar (april-september)"
    afwijking=afwijking
    overzicht_wereldweer="Overzicht wereldweer"
    maandoverzicht_wereldweer="Maandoverzicht wereldweer"
    seizoensoverzicht_wereldweer="Seizoensoverzicht wereldweer"
    halfjaaroverzicht_wereldweer="Halfjaaroverzicht wereldweer"
    jaaroverzicht_wereldweer="Jaaroverzicht wereldweer"
    tijdschaal=Tijdschaal
    maand=Maand
    seizoen=Seizoen
    halfjaar="Half jaar"
    jaar=Jaar
    vol="gemeten waarden"
    relanomalie="relatieve afwijkingen $ano (-1: droog, 0: normaal, 2: drie keer zo veel als normaal)"
    navigatie=Navigatie
    if [ $NPERYEAR = 12 ]; then
        vorigjaar="deze maand vorig jaar"
        volgendjaar="deze maand volgend jaar"
        vorigemaand="vorige maand"
        volgendemaand="volgende maand"
        vorigekalendermaand="vorige kalendermaand"
        volgendekalendermaand="volgende kalendermaand"
    elif [ $NPERYEAR = 4 -o $NPERYEAR = 2 ]; then
        vorigjaar="dit seizoen vorig jaar"
        volgendjaar="dit seizoen volgend jaar"
        vorigemaand="vorig seizoen"
        volgendemaand="volgend seizoen"
        vorigekalendermaand="vorig seizoen"
        volgendekalendermaand="volgend seizoen"
    else
        vorigjaar="vorig jaar"
        volgendjaar="volgend jaar"
        vorigemaand="half jaar eerder"
        volgendemaand="half jaar later"
    fi
    source=Bron
    tm="t/m"
    nu=nu
    helereeks="hele reeks"
    alternatieve_reeksen="Alternatieve reeksen"
else # en
    lang_ext=""
    mjan=January
    mfeb=February
    mmar=March
    mapr=April
    mmay=May
    mjun=June
    mjul=July
    maug=August
    msep=September
    moct=October
    mnov=November
    mdec=December
    mDJF="winter (December-February)"
    mMAM="spring (March-May)"
    mJJA="summer (June-August)"
    mSON="autumn (September-November)"
    mwinter="Winter half year (October-March)"
    msummer="Summer half year (April-September)"
    afwijking=anomaly
    overzicht_wereldweer="Overview world weather"
    maandoverzicht_wereldweer="Monthly overview world weather"
    seizoensoverzicht_wereldweer="Seasonal overview world weather"
    halfjaaroverzicht_wereldweer="Biannual overview world weather"
    jaaroverzicht_wereldweer="Annual overview world weather"
    tijdschaal="Time scale"
    maand=Month
    seizoen=Season
    halfjaar="Half year"
    jaar=Year
    vol="observed values"
    relanomalie="relative anomalies $ano (-1: dry, 0: normal, 2: three times normal)"
    navigatie=Navigation
    if [ $NPERYEAR = 12 ]; then
        vorigjaar="this month last year"
        volgendjaar="this month next year"
        vorigemaand="previous month"
        volgendemaand="next month"
        vorigekalendermaand="previous calendar month"
        volgendekalendermaand="next calendar month"
    elif [ $NPERYEAR = 4 -o $NPERYEAR = 2 ]; then
        vorigjaar="this season last year"
        volgendjaar="this season next year"
        vorigemaand="previous season"
        volgendemaand="next season"
        vorigekalendermaand="previous season"
        volgendekalendermaand="next season"
    else
        vorigjaar="previous year"
        volgendjaar="next year"
        vorigemaand="half year earlier"
        volgendemaand="half year later"
    fi
    source=Source
    tm="up to"
    nu=now
    helereeks="all data"
    alternatieve_reeksen="alternative series"
fi

if [ $NPERYEAR = 12 ]; then
    case "$FORM_mon1" in
        jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) ok=ok;;
        *) FORM_mon1=`date -d "40 days ago" "+%b" | tr "[:upper:]" "[:lower:]"`
    esac

    case "$FORM_mon1" in
        jan) dezemaand=$mjan;next=feb;nextmaand=$mfeb;prev=dec;prevmaand=$mdec;mm1=1;;
        feb) dezemaand=$mfeb;next=mar;nextmaand=$mmar;prev=jan;prevmaand=$mjan;mm1=2;;
        mar) dezemaand=$mmar;next=apr;nextmaand=$mapr;prev=feb;prevmaand=$mfeb;mm1=3;;
        apr) dezemaand=$mapr;next=may;nextmaand=$mmay;prev=mar;prevmaand=$mmar;mm1=4;;
        may) dezemaand=$mmay;next=jun;nextmaand=$mjun;prev=apr;prevmaand=$mapr;mm1=5;;
        jun) dezemaand=$mjun;next=jul;nextmaand=$mjul;prev=may;prevmaand=$mmay;mm1=6;;
        jul) dezemaand=$mjul;next=aug;nextmaand=$maug;prev=jun;prevmaand=$mjun;mm1=7;;
        aug) dezemaand=$maug;next=sep;nextmaand=$msep;prev=jul;prevmaand=$mjul;mm1=8;;
        sep) dezemaand=$msep;next=oct;nextmaand=$moct;prev=aug;prevmaand=$maug;mm1=9;;
        oct) dezemaand=$moct;next=nov;nextmaand=$mnov;prev=sep;prevmaand=$msep;mm1=10;;
        nov) dezemaand=$mnov;next=dec;nextmaand=$mdec;prev=oct;prevmaand=$moct;mm1=11;;
        dec) dezemaand=$mdec;next=jan;nextmaand=$mjan;prev=nov;prevmaand=$mnov;mm1=12;;
    esac

    if [ $prev = dec ]; then
        prevyr=$((FORM_year1-1))
    else
        prevyr=$FORM_year1
    fi
    if [ $next = jan ]; then
        nextyr=$((FORM_year1+1))
    else
        nextyr=$FORM_year1
    fi
    mon1=$FORM_mon1
    prevfile=$prev
    nextfile=$next
elif [ $NPERYEAR = 4 ]; then
    case "$FORM_mon1" in
        DJF|MAM|JJA|SON) ok=ok;;
        *) FORM_mon1=`date -d "40 days ago" "+%b" | tr "[:upper:]" "[:lower:]"`
        case "$FORM_mon1" in
            dec)         FORM_mon1=SON;;
            jan|feb)     FORM_mon1=SON;FORM_year1=$((FORM_year1-1));;
            mar|apr|may) FORM_mon1=DJF;;
            jun|jul|aug) FORM_mon1=MAM;;
            sep|oct|nov) FORM_mon1=JJA;;
        esac
    esac

    case "$FORM_mon1" in
        DJF) dezemaand=$mDJF;next=MAM;nextmaand=$mMAM;prev=SON;prevmaand=$mSON;mm1=1;;
        MAM) dezemaand=$mMAM;next=JJA;nextmaand=$mJJA;prev=DJF;prevmaand=$mDJF;mm1=2;;
        JJA) dezemaand=$mJJA;next=SON;nextmaand=$mSON;prev=MAM;prevmaand=$mMAM;mm1=3;;
        SON) dezemaand=$mSON;next=DJF;nextmaand=$mDJF;prev=JJA;prevmaand=$mJJA;mm1=4;;
    esac

    if [ $prev = SON ]; then
        prevyr=$((FORM_year1-1))
    else
        prevyr=$FORM_year1
    fi
    if [ $next = DJF ]; then
        nextyr=$((FORM_year1+1))
    else
        nextyr=$FORM_year1
    fi
    mon1=$FORM_mon1
    prevfile=$prev
    nextfile=$next
elif [ $NPERYEAR = 2 ]; then
    case "$FORM_mon1" in
        summer|winter) ok=ok;;
        *) FORM_mon1=`date -d "40 days ago" "+%b" | tr "[:upper:]" "[:lower:]"`
        case "$FORM_mon1" in
            sep|oct|nov|dec) FORM_mon1=summer;;
            jan|feb) FORM_mon1=summer;FORM_year1=$((FORM_year1-1));;
            mar|apr|may|jun|jul|aug) FORM_mon1=winter;;
        esac
    esac

    case "$FORM_mon1" in
        winter) dezemaand=$mwinter;next=summer;nextmaand=$msummer;prev=summer;prevmaand=$msummer;mm1=1;;
        summer) dezemaand=$msummer;next=winter;nextmaand=$mwinter;prev=winter;prevmaand=$mwinter;mm1=2;;
    esac

    if [ $prev = summer ]; then
        prevyr=$((FORM_year1-1))
    else
        prevyr=$FORM_year1
    fi
    if [ $next = winter ]; then
        nextyr=$((FORM_year1+1))
    else
        nextyr=$FORM_year1
    fi
    mon1=$FORM_mon1
    prevfile=$prev
    nextfile=$next
else # NPERYEAR = 1
    case "$FORM_mon1" in
        jun|dec) ok=ok;;
        *) FORM_mon1=jun;;
    esac

    case "$FORM_mon1" in
        jun) dezemaand="${mjul}-${mjun}";next=dec;nextmaand="${mjan}-${mdec}";mm1=6
            mon1=yr1;prevfile=yr0;nextfile=yr0;;
        dec) dezemaand="${mjan}-${mdec}";next=jun;nextmaand="${mjul}-${mjun}";mm1=12
            mon1=yr0;prevfile=yr1;nextfile=yr1;;
    esac
    prev=$next
    prevmaand=$nextmaand

    if [ $FORM_mon1 = jun ]; then
        prevyr=$((FORM_year1-1))
    else
        prevyr=$FORM_year1
    fi
    if [ $FORM_mon1 = dec ]; then
        nextyr=$((FORM_year1+1))
    else
        nextyr=$FORM_year1
    fi
fi

if [ "${FORM_var#pr}" != "$var" ]; then
    var=${FORM_var%_frac}
else
    var=${FORM_var%_f}
fi
. ./database.cgi

if [ "$FORM_lang" = nl ]; then
    ano="t.o.v. $interval"
else
    ano="w.r.t. $interval"
fi

if [ -n "$climexpfield" ]; then

if [ -z "$FORM_type" ]; then
    if [ ${FORM_var%eobs} = $FORM_var ]; then
        FORM_type=kaartwereld
    else
        FORM_type=kaarteuropa
    fi
fi

if [ "$FORM_anomalie" = ja ]; then
    if [ "$FORM_lang" = nl ]; then
        naam="$afwijking $naam"
    else
        naam="$naam $afwijking"
    fi
fi

absolute_paths=true
if [ $NPERYEAR = 12 ]; then
    (cd ..; . ./myvinkhead$langext.cgi "$maandoverzicht_wereldweer" "$naam $dezemaand $FORM_year1")
elif [ $NPERYEAR = 4 ]; then
    (cd ..;. ./myvinkhead$langext.cgi "$seizoensoverzicht_wereldweer" "$naam $dezemaand $FORM_year1")
elif [ $NPERYEAR = 2 ]; then
    (cd ..;. ./myvinkheader$langext.cgi "$halfjaaroverzicht_wereldweer" "$naam $dezemaand $FORM_year1")
else
    (cd ..;. ./myvinkheader$langext.cgi "$jaaroverzicht_wereldweer" "$naam $dezemaand $FORM_year1")
fi

field=$var
ext=
if [ "${var#pr}" != "$var" ]; then
    if [ $anomalie = nee ]; then
        if [ "$FORM_anomalie" = ja ]; then
            anomalie=ja
            ext=_frac
        fi
    else
        echo "interne fout, anomalie=$anomalie<br>"
    fi  
else
    if [ $anomalie = ja ]; then
        if [ "$FORM_anomalie" = nee ]; then
            field=${var}_f
            anomalie=nee
        fi
    else
        echo "interne fout, anomalie=$anomalie<br>"
    fi
fi

if [ "$anomalie" != "$FORM_anomalie" ]; then
    echo "interne fout: anomalie=$anomalie, FORM_anomalie=$FORM_anomalie<br>"
fi

###ano="afwijkingen t.o.v. $interval"
case "$anomalie" in
ja) anomalienaam=$ano;anderenaam=$vol;andere=nee;;
nee) anomalienaam=$vol;anderenaam=$ano;andere=ja;;
*) echo "interne fout, anomalie=$anomalie<br>"
esac
if [ "$anomalie" = ja -a \( "$var" = prcp_gpcc -o "$var" = prcp_cmorph \) ]; then
  anomalienaam=$relanomalie
  units=""
fi

echo '<table class="onelinetable" width=451 border=0 cellpadding=0 cellspacing=0><tr class="trcolor">'
echo "<th colspan=3>$navigatie</th></tr><tr><td align=left>"

if [ -s "$((FORM_year1-1))/${field}_${mon1}$((FORM_year1-1))$ext.png" ]; then
    echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$((FORM_year1-1))&anomalie=$anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$vorigjaar</a>"
else
    echo "$vorigjaar"
fi
echo '</td><td align="center">'
if [ "$anomalie" = nee ]; then
    echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$andere&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$ano</a>"
else
    echo "$ano"
fi
echo '</td><td align=right>'
if [ -s "$((FORM_year1+1))/${field}_${FORM_mon1}$((FORM_year1+1))$ext.png" ]; then
    echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$((FORM_year1+1))&anomalie=$anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$volgendjaar</a>"
else
    echo "$volgendjaar"
fi
echo '</td></tr><tr><td align="left">'
if [ -s "${prevyr}/${field}_${prevfile}${prevyr}$ext.png" ]; then
    echo "<a href=index.cgi?var=$var&mon1=$prev&year1=$prevyr&anomalie=$anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$vorigemaand</a>"
else
    echo "$vorigemaand"
fi
echo '</td><td align=center>'
if [ "$anomalie" = nee -o "$var" = tlt_uah ]; then
    echo "$vol"
else
    echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$andere&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$vol</a>"
fi
echo '</td><td align=right>'
if [ -s "${nextyr}/${field}_${nextfile}${nextyr}$ext.png" ]; then
    echo "<a href=index.cgi?var=$var&mon1=$next&year1=$nextyr&anomalie=$anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$volgendemaand</a>"
else
    echo "$volgendemaand"
fi
echo '</td></tr></table>'
    
pngfile=${FORM_year1}/${field}_${mon1}${FORM_year1}$ext.png
if [ ! -s $pngfile ]; then
    if [ "$var" = tlt_uah -a "$anomalie" != ja ]; then
        if [ "$FORM_lang" = nl ]; then
                echo "Van de temperatuur van de lagere troposfeer zijn alleen anomalie&euml;n beschikbaar."
            else
                echo "Only anomalies are available for the temperature of the lower troposphere."
            fi
    elif [ "$FORM_year1" -ge 2010 ]; then
        if [ "$FORM_lang" = nl ]; then
            echo "De $naam figuur is helaas nog niet beschikbaar.<p>"
        else
            echo "Unfortunately the $naam figure is not yet available.<p>"
        fi
    else
        if [ "$FORM_lang" = nl ]; then
            echo "De kaarten hier gaan terug tot $mjan $((FORM_year1+1)).  Eerdere kaarten van dit veld kunt u zelf maken <a href=http://climexp.knmi.nl/plotform.cgi?id=someone@somewhere&field=$climexpfield>op de KNMI Climate Explorer</a>."
        else
            echo "The maps here go back to $mjan $((FORM_year1+1)). You can make maps of earlier dates <a href=http://climexp.knmi.nl/plotform.cgi?id=someone@somewhere&field=$climexpfield>on the KNMI Climate Explorer</a>."
        fi
    fi
else
        width=`file $pngfile | sed -e 's/^.*data, //' -e 's/ x .*$//'`
        if [ $width -gt 455 ]; then
            halfwidth=$((width/2))
            if [ $((2*halfwidth )) != $width ]; then
                    halfwidth=${halfwidth}.5
            fi
        else
            halfwidth=$width
        fi
        ###echo "width=$width, halfwidth=$halfwidth<br>"
    cat <<EOF
<div class="bijschrift">$naam $units $dezemaand $FORM_year1, $anomalienaam ($source: <a href="$url" target="_new">$bron</a>).</div>
<center>
<div style="font-size:10px; width=451px;">
<img src="$pngfile" alt="$naam $dezemaand $year1 $anomalienaam" border=0 class="realimage" width="$halfwidth" hspace=0 vspace=0>
<br clear=all>
</center>
</div>
EOF
fi

if [ "$FORM_lang" = nl ]; then
    txtfile=${FORM_year1}/${field}_${mon1}${FORM_year1}$ext.txt

    if [ -s $txtfile ]; then
        cat $txtfile
    else
        if [ "$field" = sst_ncep_w ]; then
            txtfile=${FORM_year1}/ssta_${mon1}${FORM_year1}$ext.txt
        elif [ "$field" = t2m_ghcncams_w ]; then
            txtfile=${FORM_year1}/t2m_ghcncams_${mon1}${FORM_year1}$ext.txt
        fi
        if [ -s $txtfile ]; then
            cat $txtfile
        fi
    fi
fi

else # not a field but a series

[ -z "$FORM_type" ] && FORM_type=tijdreeks # in case we got here from an external link

if [ $NPERYEAR = 12 ]; then
    if [ "$prefix" != tsi ]; then
        txtfile=`ls -t 201?/i${var}_????[a-z]??.txt|head -1`
    else
        txtfile=`ls -t 201?/i${var}_????"$FORM_mon1".txt|head -1`
        mo="$FORM_mon1"
    fi
    if [ -n "$txtfile" -a -s "$txtfile" ]; then
        yr=`echo $txtfile | sed -e "s@..../i${var}_@@" -e "s/...\.txt//"`
        mo=`echo $txtfile | sed -e "s@..../i${var}_$yr@@" -e "s/\.txt//"`
    else
        yr=""
    fi
    case "$mo" in
        jan) maa=$mjan;;
        feb) maa=$mfeb;;
        mar) maa=$mmar;;
        apr) maa=$mapr;;
        may) maa=$mmay;;
        jun) maa=$mjun;;
        jul) maa=$mjul;;
        aug) maa=$maug;;
        sep) maa=$msep;;
        oct) maa=$moct;;
        nov) maa=$mnov;;
        dec) maa=$mdec;;
        *) echo "error 867yghj"; maa="";;
    esac
    if [ "$prefix" != tsi ]; then
        . ./myvinkheader.cgi "$maandoverzicht_wereldweer" "$naam $tm $maa $yr"
    else
        . ./myvinkheader.cgi "$maandoverzicht_wereldweer" "$maa $naam $tm $yr"
    fi
elif [ $NPERYEAR = 4 ]; then
    if [ "$prefix" != tsi ]; then
        txtfile=`ls -t 20??/i${var}_????[a-z]??.txt|head -1`
    else
        txtfile=`ls -t 20??/i${var}_????"$FORM_mon1".txt|head -1`
        mo="$FORM_mon1"
    fi
    if [ -n "$txtfile" -a -s "$txtfile" ]; then
        yr=`echo $txtfile | sed -e "s@..../i${var}_@@" -e "s/...\.txt//"`
        mo=`echo $txtfile | sed -e "s@..../i${var}_$yr@@" -e "s/\.txt//"`
    else
        yr=""
    fi
    case "$mo" in
        feb|mar|apr) mo=DJF;;
        may|jun|jul) mo=MAM;;
        aug|sep|oct) mo=JJA;;
        nov|dec) mo=SON;;
        jan) mo=SON;yr=$((yr-1));;
        esac
    case "$mo" in
        DJF) maa=$mDJF;;
        MAM) maa=$mMAM;;
        JJA) maa=$mJJA;;
        SON) maa=$mSON;;
        *) echo "error 867yghj"; maa="";;
    esac
    if [ "$prefix" != tsi ]; then
        . ./myvinkheader.cgi "$seizoensoverzicht_wereldweer" "$naam $tm $maa $yr"
    else
        . ./myvinkheader.cgi "$seizoensoverzicht_wereldweer" "$maa $naam $tm $yr"
    fi
    ###echo "txtfile=$txtfile<br>"
    ###echo "mo,yr=$mo,$yr<br>"
elif [ $NPERYEAR = 2 ]; then
    if [ "$prefix" != tsi ]; then
        txtfile=`ls -t 20??/i${var}_????[a-z]??.txt|head -1`
    else
        txtfile=`ls -t 20??/i${var}_????"$FORM_mon1".txt|head -1`
        mo="$FORM_mon1"
    fi
    if [ -n "$txtfile" -a -s "$txtfile" ]; then
        yr=`echo $txtfile | sed -e "s@..../i${var}_@@" -e "s/[a-z]*\.txt//"`
        mo=`echo $txtfile | sed -e "s@..../i${var}_$yr@@" -e "s/\.txt//"`
    else
        yr=""
    fi
    case "$mo" in
        mar|apr|may|jun|jul|aug) mo=winter;;
        sep|oct|nov|dec) mo=summer;;
        jan|feb) mo=summer;yr=$((yr-1));;
        esac
    case "$mo" in
        winter) maa=$mwinter;;
        summer) maa=$msummer;;
        *) echo "error 867yghj"; maa="";;
    esac
    if [ "$prefix" != tsi ]; then
        . ./myvinkheader.cgi "$halfjaaroverzicht_wereldweer" "$naam $tm $maa $yr"
    else
        . ./myvinkheader.cgi "$halfjaaroverzicht_wereldweer" "$maa $naam $tm $yr"
    fi
    ###echo "txtfile=$txtfile<br>"
    ###echo "mo,yr=$mo,$yr<br>"
else # NPERYEAR = 1
    if [ $mon1 = yr0 -o $mon1 = yr1 ]; then
        txtfile=`ls -t 20??/i${var}_???????_$mon1.txt|head -1`
    else
        txtfile=`ls -t 20??/i${var}_????$mon1.txt|head -1`
    fi
    if [ -n "$txtfile" -a -s "$txtfile" ]; then
        yr=`echo $txtfile | sed -e "s@..../i${var}_@@" -e "s/..._yr[01]\.txt//"`
        mo=`echo $txtfile | sed -e "s@..../i${var}_$yr@@" -e "s/_yr[01]\.txt//"`
        case $mo in
            dec) maa=${mjan}-${mdec};;
            jun) maa=${mjul}-${mjun};;
            *) echo "error ce4q21<p>";;
        esac
    else
        yr=""
    fi
    . ./myvinkheader.cgi "$jaaroverzicht_wereldweer" "$naam $tm $maa $yr"
fi

if [ $var != maunaloa_ch4 ]; then
    echo '<table class="onelinetable" width=451 border=0 cellpadding=0 cellspacing=0><tr class="trcolor">'
    echo "<th align=left colspan=3>$navigatie</th></tr><tr><td>&nbsp</td><td align=center>"
    if [ "$prefix" = tsi -a $NPERYEAR != 1 ]; then
        naam="$dezemaand $naam"
        if [ "$FORM_kort" = ja ] ; then
            pngfile=i${var}_1975_now_$mon1.png
            extra="1975-$nu"
            echo "1975-$nu"
        else
            pngfile=i${var}_$mon1.png
            extra="$helereeks"
            echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$FORM_anomalie&kort=ja&expert=$FORM_expert&type=$FORM_type>1975-$nu</a>"
        fi
        echo "</td><td>&nbsp</td></tr><tr><td align=left><a href=index.cgi?var=$var&mon1=$prev&year1=$prevyr&anomalie=$FORM_anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$vorigekalendermaand</td><td align=center>"
        if [ "$FORM_kort" = ja ]; then
            echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$FORM_anomalie&kort=nee&expert=$FORM_expert&type=$FORM_type>$helereeks</a>"
        else
            echo "$helereeks"
        fi
        echo "</td><td align=right>"
        echo "<a href=index.cgi?var=$var&mon1=$next&year1=$nextyr&anomalie=$FORM_anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$volgendekalendermaand"
    elif [ $NPERYEAR != 1 ]; then # no separate months
        if [ "$FORM_kort" = ja ] ; then
            period=_1975_now
            echo "1975-$nu"
            extra="1975-$nu"
        else
            period=""
            extra="$helereeks"
            echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$FORM_anomalie&kort=ja&expert=$FORM_expert&type=$FORM_type>1975-$nu</a>"
        fi
        echo '</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td align=center>'
        if [ "$FORM_kort" = ja ] ; then
            echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$FORM_anomalie&kort=nee&expert=$FORM_expert&type=$FORM_type>$helereeks</a>"
        else
            echo "$helereeks"
        fi
        echo "</td><td>&nbsp;"
        if [ $NPERYEAR = 12 ]; then
            pngfile=i${var}${period}.png
        else # NPERYEAR is 2 or 4
            pngfile=i${var}${period}_mean${NPERYEAR}_90.png
        fi
    else # NPERYEAR = 1
        if [ "$mon1" = yr0 ] ; then
            pngfile=i${var}_yr0.png
            echo "${mjan}-${mdec}"
            extra="${mjan}-${mdec}"
        else
            pngfile=i${var}_yr1.png
            extra="${mjul}-${mjun}"
            echo "<a href=index.cgi?var=$var&mon1=dec&anomalie=$FORM_anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>${mjan}-${mdec}</a>"
        fi
        echo '</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td align=center>'
        if [ "$mon1" = yr0 ] ; then
            echo "<a     href=index.cgi?var=$var&mon1=jun&anomalie=$FORM_anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>${mjul}-${mjun}</a>"
        else
            echo "${mjul}-${mjun}"
        fi
        echo "</td><td>&nbsp;"
    fi
    echo '</td></tr></table>'
else # variables without 1975-now series
    pngfile=i${var}.png
fi
width=`file $pngfile | sed -e 's/^.*data, //' -e 's/ x .*$//'`
if [ $width -gt 455 ]; then
    halfwidth=$((width/2))
    if [ $((2*halfwidth )) != $width ]; then
        halfwidth=${halfwidth}.5
    fi
else
    halfwidth=$width
fi

cat <<EOF
<div class="bijschrift">$naam $units $extra ($source: <a href="$url" target="_new">$bron</a>).</div>
<center>
<div style="font-size:10px; width=451px;">
<img src="$pngfile" alt="$naam" border=0 class="realimage" width="$halfwidth" hspace=0 vspace=0>
<br clear=all>
</center>
</div>
EOF

if [ "$naam" = "wereldgemiddelde temperatuur" \
  -o "$naam" = "wereldgemiddelde landtemperatuur" \
  -o "$naam" = "global mean temperature" \
  -o "$naam" = "global mean land temperature" ]; then
    echo '<table class="onelinetable" width=451 border=0 cellpadding=0 cellspacing=0><tr class="trcolor"><td>'
    echo "$alternatieve_reeksen: "
    if [ "$naam" = "wereldgemiddelde temperatuur" \
      -o "$naam" = "global mean temperature" ]; then
        vars="giss_al_gl_m hadcrut4110_ns_avg ncdc_gl erai_t2msst_gl"
    else
        vars="giss_land crutem4gl ncdc_gl_land erai_t2m_landnoice"
    fi
    for alt in $vars
    do
        if [ $alt = $var ]; then
            . ./database.cgi
            echo "$bron"
        else
            bewaar=$var
            var=$alt
            . ./database.cgi
            echo "<a href=index.cgi?var=$var&mon1=$FORM_mon1&year1=$FORM_year1&anomalie=$FORM_anomalie&kort=$FORM_kort&expert=$FORM_expert&type=$FORM_type>$bron</a>"
            var=$bewaar
        fi
    done
    echo '</td></tr></table>'
fi

if [ "$FORM_lang" = nl ]; then
    if [ -s $txtfile ]; then
        echo "<div class=datumtijd>$maa $yr</div>"
        cat $txtfile
    fi
fi

fi

. ./myvinkfooter.cgi
