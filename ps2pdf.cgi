#!/bin/sh
echo "Content-Type: application/pdf"
echo

. ./init.cgi
. ./getargs.cgi
epsfile=data/`basename $FORM_file .gz`
pdffile=${epsfile%.eps}.pdf
gunzip -c $epsfile.gz > $epsfile
convert $epsfile $pdffile
cat $pdffile
