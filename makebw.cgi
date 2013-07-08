#!/bin/sh
. ./init.cgi
. ./getargs.cgi
# make sure the file is in data/...
FILE=data/`basename "$FORM_file"`
flipcolor="$FORM_color"
format="$FORM_format"
if [ "$format" = pdf ]; then
  command='ps2pdf -'
  echo "Content-Type: application/pdf"
else
  command='gzip -c -'
  echo "Content-Type: application/postscript"
  echo "Content-Encoding: x-gzip"
fi
echo

if [ "$flipcolor" = "3" -o "$flipcolor" = "4" ]; then
# one-sided colour bar
gunzip -c $FILE | sed \
-e 's/blackwhite {false} def/blackwhite {true} def/' \
-e 's/g14 {0.76 g} bdef/g14 {1.0 g} bdef/' \
-e   's/g4 {0.7 g} bdef/g4  {1.0 g} bdef/' \
-e 's/g11 {0.64 g} bdef/g11 {1.0 g} bdef/' \
-e  's/g3 {0.46 g} bdef/g3  {0.8 g} bdef/' \
-e  's/g10 {0.4 g} bdef/g10 {0.8 g} bdef/' \
-e  's/g7 {0.34 g} bdef/g7  {0.6 g} bdef/' \
-e 's/g12 {0.28 g} bdef/g12 {0.6 g} bdef/' \
-e  's/g8 {0.22 g} bdef/g8  {0.4 g} bdef/' \
-e  's/g2 {0.16 g} bdef/g2  {0.4 g} bdef/' \
-e   's/g6 {0.1 g} bdef/g6  {0.2 g} bdef/' \
-e  's/g9 {0.82 g} bdef/g9  {0.2 g} bdef/' \
-e 's/g50 {0.12941 g} bdef/g50 {1.0 g} bdef/' \
-e 's:c1 {g1} def /c2 {g1} def /c3 {g1} def /c4 {g1} def:/c1 {g1} def /c2 {g2} def /c3 {g3} def /c4 {g4} def:' \
-e 's:/c5 {g1} def /c6 {g1} def /c7 {g1} def /c8 {g1} def /c9 {g1} def:/c5 {g5} def /c6 {g6} def /c7 {g7} def /c8 {g8} def /c9 {g9} def:' \
-e 's:/c10 {g1} def /c11 {g1} def /c12 {g1} def /c13 {g1} def /c14 {g1} def:/c10 {g10} def /c11 {g11} def /c12 {g12} def /c13 {g13} def /c14 {g14} def:' \
-e 's:/c15 {g1} def:/c15 {g15} def:' \
-e 's:/c50 {g1} bdef:/c50 {g50} bdef:' \
 | $command
else
# two-sided colour bar
gunzip -c $FILE | sed \
-e 's/blackwhite {false} def/blackwhite {true} def/' \
-e 's/g14 {0.76 g} bdef/g14 {1.0 g} bdef/' \
-e   's/g4 {0.7 g} bdef/g4  {0.9 g} bdef/' \
-e 's/g11 {0.64 g} bdef/g11 {0.8 g} bdef/' \
-e  's/g3 {0.46 g} bdef/g3  {0.6 g} bdef/' \
-e  's/g10 {0.4 g} bdef/g10 {0.95 g} bdef/' \
-e  's/g7 {0.34 g} bdef/g7  {0.95 g} bdef/' \
-e 's/g12 {0.28 g} bdef/g12 {0.5 g} bdef/' \
-e  's/g8 {0.22 g} bdef/g8  {0.4 g} bdef/' \
-e  's/g2 {0.16 g} bdef/g2  {0.2 g} bdef/' \
-e   's/g6 {0.1 g} bdef/g6  {0.0 g} bdef/' \
-e 's/g50 {0.12941 g} bdef/g50 {0.95 g} bdef/' \
-e 's:c1 {g1} def /c2 {g1} def /c3 {g1} def /c4 {g1} def:/c1 {g1} def /c2 {g2} def /c3 {g3} def /c4 {g4} def:' \
-e 's:/c5 {g1} def /c6 {g1} def /c7 {g1} def /c8 {g1} def /c9 {g1} def:/c5 {g5} def /c6 {g6} def /c7 {g7} def /c8 {g8} def /c9 {g9} def:' \
-e 's:/c10 {g1} def /c11 {g1} def /c12 {g1} def /c13 {g1} def /c14 {g1} def:/c10 {g10} def /c11 {g11} def /c12 {g12} def /c13 {g13} def /c14 {g14} def:' \
-e 's:/c15 {g1} def:/c15 {g15} def:' \
-e 's:/c50 {g1} bdef:/c50 {g50} bdef:' \
 | $command
fi
