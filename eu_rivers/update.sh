#!/bin/sh

# From http://www.eea.europa.eu/data-and-maps/data/wise-river-basin-districts-rbds

file=RBD_F1v3
if [ ! -s $file.gml -o $file.gml -ot $file.shp ]; then
    ogr2ogr -f GML -t_srs "EPSG:4326" $file.gml $file.shp
fi
rm *.txt
./gml2txt.py $file.gml 0
# names too long
mv FR_Adour,_Garonne,_Dordogne,_Charente_and_coastal_waters_of_aquitania.txt FR_Adour,_Garonne,_Dordogne,_Charente_and.txt
mv FR_Scheldt,_Somme_and_coastal_waters_of_the_Channel_and_the_North_Sea.txt FR_Scheldt,_Somme_and_coastal_waters.txt
mv FI_Teno-,_Naatamo-_and_Paatsjoki_\(Finnish_part\).txt FI_Teno-,_Naatamo-_and_Paatsjoki.txt
mv FI_Kokemaenjoki-Archipelago_Sea-Bothnian_Sea.txt FI_Kokemaenjoki-Archipelago_Sea-Bothnian.txt
# insert breaks
for file in *.txt
do
    cp $file $file.org
    if [ $file != CH_Rhone.txt \
      -a $file != CY_Cyprus.txt \
      -a $file != NL_Rhine.txt ]; then
        ./insert_breaks.py $file
        mv ${file%.txt}_new.txt $file
    fi
    ./make_coarse.py $file
    mv ${file%.txt}_coarse.txt $file
    if [ $file = DE_Elbe.txt ]; then
        ./separate_polygons.py $file 8.2 16 48 55 > aap.txt
        mv aap.txt $file
    fi
    if [ $file = ___Danube.txt ]; then
        ./separate_polygons.py ___Danube.txt 14 24 42 47 > ___Danube.1.txt
        ./separate_polygons.py ___Danube.txt 22 30 45 50 > ___Danube.2.txt
        rm $file
    fi
done

