#!/bin/sh
# various environment variables that come in useful later on
# plus a check on the state of the server
if [ -z "$init_done" ]; then
    if [ "${HTTP_USER_AGENT%megaindex*}" != "${HTTP_USER_AGENT}" ]; then
        echo "Content-Type: text/plain"
        echo
        echo "As MegaIndex does not obey robots.txt nor the nofollow directive it is blocked. Please contact oldenborgh@knmi.nl for details."
        exit
    fi
    if [ -n "$HTTP_X_FORWARDED_FOR" ]; then
        REMOTE_ADDR=$HTTP_X_FORWARDED_FOR
    fi

    if [ -n "$use_uptime" ] ;then
        line=`uptime`
        load=${line##*averages: } # Mac OSX
        load=${load##*average: }  # linux
        load=${load%%.*}
        maxload=20
    else
        load=`ps axuw | fgrep -v upload | egrep -c '\.cgi$'`
        maxload=11 # 1 is the grep, we have 4 cores, correlatefield counts for two
    fi
    if [ ${load:-0} -gt $maxload -a `uname` != Darwin ]; then
        echo 
        echo "Server too busy (load $load &gt; $maxload), try again later"
        echo `date` "Server too busy, load $load > $maxload" >> log/log
        exit
    fi
    if [ -s log/attack-ip.txt ]; then
        c=`fgrep -c $REMOTE_ADDR log/attack-ip.txt`
        if [ $c != 0 ]; then
            echo 'Content/type: text/plain'
            echo
            echo
            echo "IP address $REMOTE_ADDR has been blacklisted" >> log/log
            echo "IP address $REMOTE_ADDR has been blacklisted"
            exit
        fi
    fi

   init_done=done

    function getpngwidth {
        use_exact_pixels=false
        if [ $use_exact_pixels = true ]; then
            if [ -s $pngfile ]; then
                type=`file -b $pngfile`
                if [ "${type#PNG}" != "$type" ]; then
                    width=`echo $type | sed -e 's/^.*data, //' -e 's/ x .*$//'`
                    halfwidth=$((width/2))
                    if [ $((2*halfwidth )) != $width ]; then
                        halfwidth=${halfwidth}.5
                    fi
                else
                    width=0
                    halfwidth=0
                fi
            else
                width=0
                halfwidth=0
            fi
        else
            width="100%"
            halfwidth="100%"
        fi
    }
   # set a standard TTF font for gnuplot.   GNUPLOT_DEFAULT_GDFONT is not used
   # if all is well, but is there as a fall-back.
   export gnuplot_version=`./bin/gnuplot --version`
   if [ "${gnuplot_version#gnuplot 5}" != "$gnuplot_version" ]; then
      export gnuplot_init="set colors classic"
      setxzeroaxis="" # bug in gnuplot 5.0 patchlevel 0
   else
      setxzeroaxis="set xzeroaxis"
   fi
   export GDFONTPATH=`pwd`/truetype
   export GNUPLOT_DEFAULT_GDFONT="DejaVuSansCondensed"
   export gnuplot_png_font_hires="size 1280,960 crop font DejaVuSansCondensed 15"
   export gnuplot_png_font="size 640,480 crop font DejaVuSansCondensed 8.5"
   # R libraries
   export R_LIBS=`pwd`/rpacks
   # netcdf libraries on bhlclim, bvlclim - hard-coded
   export LD_LIBRARY_PATH=/home/oldenbor/lib:/usr/local/free/lib:$LD_LIBRARY_PATH
   # for a few routines this seems needed
   export PATH=./bin:/sw/bin:/usr/local/bin:/usr/local/free/bin:$PATH
   # finally, avoid commas instead of decimal points :-(
   export LANG=C
   # start with modest parallel processing
   host=`uname -a | cut -f 2 -d ' '`
   export OMP_NUM_THREADS=2
   if [ $host = bima ]; then
      export OMP_NUM_THREADS=4
   fi
fi
