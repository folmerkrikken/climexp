#!/bin/csh -f
#
set station = $1
set season = $2
set scen = $3

if ( "$scen" == "" ) then
  echo "usage: $0 station season scenario"
  exit -1
endif

if ($scen == "GG" ) then
  set dyr=110
  switch ( $season )
  case MAM:
    echo "NOT YET READY";exit
    breaksw
  case JJA:
    set WDFfut  = -0.032
    set MPWDfut = 9.2
    set Q99fut  = 24.8
    breaksw
  case SON:
    echo "NOT YET READY";exit
    breaksw
  case DJF:
    set WDFfut  =  0.002
    set MPWDfut = 7.2
    set Q99fut  = 8.6
    breaksw
  endsw

else if ($scen == "GG+" ) then
  set dyr=110
  switch ( $season )
  case MAM:
    echo "NOT YET READY";exit
    breaksw
  case JJA:
    set WDFfut  = -0.192
    set MPWDfut = 0.2
    set Q99fut  = 12.4
    breaksw
  case SON:
    echo "NOT YET READY";exit
    breaksw
  case DJF:
    set WDFfut  =  0.018
    set MPWDfut = 12.0
    set Q99fut  = 11.2
    breaksw
  endsw

else if ($scen == "WW" ) then
  set dyr=110
  switch ( $season )
  case MAM:
    echo "NOT YET READY";exit
    breaksw
  case JJA:
    set WDFfut  = -0.066
    set MPWDfut = 18.2
    set Q99fut  = 49.6
    breaksw
  case SON:
    echo "NOT YET READY";exit
    breaksw
  case DJF:
    set WDFfut  =  0.004
    set MPWDfut = 14.2
    set Q99fut  = 17.2
    breaksw
  endsw

else if ($scen == "WW+" ) then
  set dyr=110
  switch ( $season )
  case MAM:
    echo "NOT YET READY";exit
    breaksw
  case JJA:
    set WDFfut  = -0.386
    set MPWDfut = 0.6
    set Q99fut  = 24.6
    breaksw
  case SON:
    echo "NOT YET READY";exit
    breaksw
  case DJF:
    set WDFfut  =  0.038
    set MPWDfut = 24.2
    set Q99fut  = 22.4
    breaksw
  endsw

else if ($scen == "G" ) then
  set dyr=60
  switch ( $season )
  case MAM: 
    set WDFfut  = -0.019
    set MPWDfut = 3.6
    set Q99fut  = 6.7
    breaksw
  case JJA:
    set WDFfut  = -0.016
    set MPWDfut = 4.6 
    set Q99fut  = 12.4
    breaksw
  case SON:
    set WDFfut  = -0.045
    set MPWDfut = 2.4
    set Q99fut  = 6.5
    breaksw
  case DJF:
    set WDFfut  =  0.001
    set MPWDfut = 3.6
    set Q99fut  = 4.3
    breaksw
  endsw

else if ($scen == "G+" ) then
  set dyr=60
  switch ( $season )
  case MAM: 
    set WDFfut  = -0.007			
    set MPWDfut = 5.1
    set Q99fut  = 6.7
    breaksw
  case JJA:
    set WDFfut  = -0.096    		
    set MPWDfut = 0.1
    set Q99fut  = 6.2
    breaksw
  case SON:
    set WDFfut  = -0.019			
    set MPWDfut = 4.6
    set Q99fut  = 7.1
    breaksw
  case DJF:
    set WDFfut  = 0.009			
    set MPWDfut = 6.0
    set Q99fut  = 5.6
    breaksw
  endsw

else if ($scen == "W" ) then
  set dyr=60
  switch ( $season )
  case MAM: 
    set WDFfut  = -0.039		
    set MPWDfut = 7.3
    set Q99fut  = 13.3
    breaksw
  case JJA:
    set WDFfut  = -0.033    	
    set MPWDfut = 9.1 
    set Q99fut  = 24.8
    breaksw
  case SON:
    set WDFfut  = -0.089		
    set MPWDfut = 4.8
    set Q99fut  = 13.0
    breaksw
  case DJF:
    set WDFfut  = 0.002		
    set MPWDfut = 7.1
    set Q99fut  = 8.6
    breaksw
  endsw

else if ($scen == "W+" ) then
  set dyr=60
  switch ( $season )
  case MAM: 
    set WDFfut  = -0.014
    set MPWDfut = 10.2
    set Q99fut  = 13.4
    breaksw
  case JJA:
    set WDFfut  = -0.193     		
    set MPWDfut = 0.3
    set Q99fut  = 12.3
    breaksw
  case SON:
    set WDFfut  = -0.037			
    set MPWDfut = 9.2
    set Q99fut  = 14.3
    breaksw
  case DJF:
    set WDFfut  = 0.019			
    set MPWDfut = 12.1
    set Q99fut  = 11.2
    breaksw
  endsw

else if ($scen == "0" ) then
  set dyr=0
  set WDFfut  = 0
  set MPWDfut = 0
  set Q99fut  = 0
endif


cat << EOF
# prcp [mm/day] at station $station under scenario $scen
# a complete description can be found at the <a href="http://www.knmi.nl/scenarios">KNMI web pages</a>
# This data can be distributed freely as long as this header is kept intact.
EOF

./Scenarios/sepmonth.sh Scenarios/S${station}_obs.txt $season |\
./Scenarios/WDFchange -f - -WDF $WDFfut -thres 0.1 |\
./Scenarios/changeMPfinale -f - -Q99fut $Q99fut -MPWDfut $MPWDfut |\
./Scenarios/adjustdate $dyr
