#!/bin/bash
. ./init.cgi
. ./getargs.cgi

echo "Content-Type: text/html"
echo
. ./myvinkhead.cgi "Generating PDF file"

epsfile=data/`basename $FORM_file .gz`
if [ ! \( -s $epsfile.gz -o -s $epsfile \) ]; then
    epsfile=`echo $epsfile | tr '%' '+'`
    if [ ! \( -s $epsfile.gz -o -s $epsfile \) ]; then
        echo "Error: cannot find file $epsfile[.gz]"
        exit
    fi
fi
pdffile=${epsfile%.eps}.pdf
[ ! -s $epsfile ] && gunzip -c $epsfile.gz > $epsfile
[ ! -s $pdffile ] && epstopdf $epsfile

echo "Please download the <a href=$pdffile>PDF file here</a>"

. ./myvinkfoot.cgi