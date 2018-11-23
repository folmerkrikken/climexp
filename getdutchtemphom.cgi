#!/bin/sh
export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

WMO="$FORM_WMO"
TYPE=thom
STATION="$FORM_STATION"
NPERYEAR=366
NAME="homogenised_temperature"
NPERYEAR=12

    case $WMO in
	240) name="Amsterdam Schiphol"
	    homfile=temp_Schiphol_hom
        lat="52.30"; lon="4.77"; lev=" -4.4";;
	260) name="De Bilt"
	    homfile=temp_De_Bilt_hom
        lat="52.10"; lon="5.18"; lev="  2.0";;
	280) name="Groningen/Eelde"
	    homfile=temp_Groningen_Eelde_hom
        lat="53.13"; lon="6.58"; lev="  3.5";;
	344) name="Rotterdam"
	    homfile=temp_Rotterdam_hom
        lat="51.95"; lon="4.45"; lev=" -4.8";;
	370) name="Eindhoven"
	    homfile=temp_Eindhoven_hom
        lat="51.45"; lon="5.42"; lev=" 22.4";;
	380) name="Maastricht/Beek"
	    homfile=temp_Maastricht_Beek_hom
        lat="50.92"; lon="5.78"; lev="114.0";;
	283) name="Winterswijk/Hupsel"
	    homfile=temp_Winterswijk_Hupsel_hom
	    lat="52.07";lon="6.65";lev="29.0";;
	350) name="Oudenbosch/Gilze-Rijen"
	    homfile=temp_Oudenbosch_Gilze-Rijen_hom
	    lat="51.57";lon="4.93",lev="11.0";;
	375) name="Gemert/Volkel"
	    homfile=temp_Gemert_Volkel_hom
	    lat="51.65";lon="5.70";lev="20.1";;
	275) name="Deelen"
	    homfile=temp_Deelen_hom
	    lat="52.07";lon="5.88";lev="50.0";;
	*) echo 'HELP! UNKNOWN STATION ' $station; exit -1;;
    esac

TYPE=
WMO="KNMIData/$homfile"
PROG="getindices"
LASTMODIFIED=`stat $homfile.dat | fgrep Modify | cut -b 8-27`
LASTMODIFIED=`date -R -d "$LASTMODIFIED"`

. $DIR/getdata.cgi
