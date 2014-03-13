import logging
import sys


class DefineRegion:

    regions = ['world', 'arctic', 'highlatitudes', 'westnorthamerica', 'eastnorthamerica',
               'centralamerica', 'northsouthamerica', 'southsouthamerica', 'northeurope',
               'mediterranean', 'weafrica', 'southafrica', 'centralasia', 'eastasia',
               'southasia', 'southeastasia', 'australia', 'pacific', 'antarctica']

    def __init__(self, region):
        """define list of regions."""

#        self.log = logging.getLogger('DefineRegion')
#        self.log.setLevel(logging.DEBUG)
#
#        hdlr = logging.StreamHandler(sys.stdout)
#        hdlr.setFormatter(logging.Formatter('%(name)s: %(message)s'))
#        self.log.addHandler(hdlr)
#
#        self.log.debug('')
#        self.log.debug('DefineRegion, region = %s' % region)

        # define properties of the regions
        self.labelx = 0.77
        self.labely = 0.67
        self.abbr = [""]*4
        self.country = [""]*4
        self.npoly = [0]*4
        self.shortname = [""]*4
        self.lon1 = [0]*4
        self.lon2 = [0]*4
        self.lat1 = [0]*4
        self.lat2 = [0]*4
        self.name = [""] * 4
        self.lsmask = [""] * 4
        self.area = [""] * 4

        self.firstpage = 8
        self.subregions = [1, 2]
        self.prmin_winter2 = ""
        self.prmax_winter2 = ""
        self.prmin_summer2 = ""
        self.prmax_summer2 = ""

        self.tasmin_JJA = ""

        if region == 'world':
            # home-defined
            self.name[0] = "World"
            self.lon1[0] = -170;self.lon2[0] = 190;self.lat1[0] = -90;self.lat2[0] = 90;self.lsmask[0] = 'all'
            self.name[1] = "World (land)"
            self.shortname[1] = "worldland"
            self.area[1] = ""
            self.lon1[1] = -170;self.lon2[1] = 190;self.lat1[1] = -90;self.lat2[1] = 90;self.lsmask[1] = 'land'
            self.name[2] = "World (sea)"
            self.lon1[2] = -170;self.lon2[2] = 190;self.lat1[2] = -90;self.lat2[2] = 90;self.lsmask[2] = 'sea'
            self.area[2] = ""
            self.shortname[2] = "worldsea"
            self.name[3] = "World"
            self.shortname[3] = 'world'
            self.lon1[3] = -170;self.lon2[3] = 190;self.lat1[3] = -90;self.lat2[3] = 90;self.lsmask[3] = 'all'
            self.area[3] = ""
            self.subregions = [1, 2, 3]
            self.labely = 0.63
            self.xwidth = 0.33
            # TODO: fix this
            self.page = self.firstpage
            #self.page = $((self.firstpage+0))
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"
            self.tascross = "9.4.1, 9.4.2, 10.3, 11.3.2.2, 11.3.3.1, Box 11.2, 12.4.3 and 12.4.7"
            self.prcross = "9.4.4, 11.3.2.3, Box 11.2, 12.4.5"
        elif region == 'NAmerica':
            # continents (KNMI Atlas only)
            self.name[0] = "North America"
            self.lon1[0] = -170;self.lon2[0] = -15;self.lat1[0] = 5;self.lat2[0] = 85;self.lsmask[0] = 'land'
            self.name[1] = "North America"
            self.shortname[1] = "NAmerica"
            self.area[1] = ""
            self.lon1[1] = -170;self.lon2[1] = -15;self.lat1[1] = 5;self.lat2[1] = 85;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"
        elif region == 'SAmerica':
            self.name[0] = "South America"
            self.lon1[0] = -90;self.lon2[0] = -30;self.lat1[0] = -60;self.lat2[0] = 15;self.lsmask[0] = 'land'
            self.name[1] = "South America"
            self.shortname[1] = "SAmerica"
            self.area[1] = ""
            self.lon1[1] = -90;self.lon2[1] = -30;self.lat1[1] = -60;self.lat2[1] = 15;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"

        elif region == 'Europe':
            self.name[0] = "Europe"
            self.lon1[0] = -25;self.lon2[0] = 45;self.lat1[0] = 35;self.lat2[0] = 72.5;self.lsmask[0] = 'land'
            self.name[1] = "Europa"
            self.shortname[1] = "Europe"
            self.area[1] = ""
            self.lon1[1] = -25;self.lon2[1] = 45;self.lat1[1] = 35;self.lat2[1] = 72.5;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"
        elif region == 'Africa':
            self.name[0] = "Africa"
            self.lon1[0] = -20;self.lon2[0] = 52.5;self.lat1[0] = -37.5;self.lat2[0] = 37.5;self.lsmask[0] = 'land'
            self.name[1] = "Africa"
            self.shortname[1] = "Africa"
            self.area[1] = ""
            self.lon1[1] = -20;self.lon2[1] = 52.5;self.lat1[1] = -37.5;self.lat2[1] = 37.5;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"
        elif region == 'Asia':
            self.name[0] = "Aisa"
            self.lon1[0] = 40;self.lon2[0] = 190;self.lat1[0] = -10;self.lat2[0] = 80;self.lsmask[0] = 'land'
            self.name[1] = "Asia"
            self.shortname[1] = "Asia"
            self.area[1] = ""
            self.lon1[1] = 40;self.lon2[1] = 190;self.lat1[1] = -10;self.lat2[1] = 80;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"

        elif region == 'Australia':
            self.name[0] = "Australia"
            self.lon1[0] = 110;self.lon2[0] = 180;self.lat1[0] = -47.5;self.lat2[0] = -10;self.lsmask[0] = 'land'
            self.name[1] = "Australia"
            self.shortname[1] = "Australia"
            self.area[1] = ""
            self.lon1[1] = 110;self.lon2[1] = 180;self.lat1[1] = -47.5;self.lat2[1] = -10;self.lsmask[1] = 'land'
            self.subregions = [1]
            self.labely = 0.63
            self.xwidth = 0.33
            self.page = self.firstpage
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-15"
            self.prmax_winter = "25"
            self.prmin_summer = "-15"
            self.prmax_summer = "25"

        elif region == 'arctic':
            # home-defined
            self.lon1[0] = -180;self.lon2[0] = 180;self.lat1[0] = 67.5;self.lat2[0] = 90;self.lsmask[0] = 'all'
            self.name[1] = "Arctic (land)"
            self.shortname[1] = "Arcticland"
            self.area[1] = "67.5dg--90dg N"
            self.lon1[1] = -180;self.lon2[1] = 180;self.lat1[1] = 67.5;self.lat2[1] = 90;self.lsmask[1] = 'land'
            self.name[2] = "Arctic (sea)"
            self.shortname[2] = "Arcticsea"
            self.lon1[2] = -180;self.lon2[2] = 180;self.lat1[2] = 67.5;self.lat2[2] = 90;self.lsmask[2] = 'sea'
            self.area[2] = ""
            self.labelx = 0.79
            self.labely = 0.79
            self.xwidth = 0.213
            self.page = self.firstpage
            self.tasmin_DJF = "-12.5"
            self.tasmax_DJF = "27.5"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-40"
            self.prmax_winter = "140"
            self.prmin_summer = "-30"
            self.prmax_summer = "100"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.2"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.2"

        elif region == 'highlatitudes':
            # CGI + NAS
            self.lon1[0] = -180;self.lon2[0] = 180;self.lat1[0] = 50;self.lat2[0] = 90;self.lsmask[0] = 'land'
            self.name[1] = "Canada/Greenland/Iceland"
            self.area[1] = "50dg--85dg N, 105dg--10dg W"
            self.lon1[1] = -105;self.lon2[1] = -10;self.lat1[1] = 50;self.lat2[1] = 85;self.lsmask[1] = 'land'
            self.abbr[1] = "CGI";self.npoly[1] = 4
            self.name[2] = "North Asia"
            self.area[2] = "50dg--70dg N, 40dg--180dg E"
            self.lon1[2] = 40;self.lon2[2] = 180;self.lat1[2] = 50;self.lat2[2] = 70;self.lsmask[2] = 'land'
            self.abbr[2] = "NAS";self.npoly[2] = 4
            self.labelx = 0.79
            self.labely = 0.79
            self.xwidth = 0.213
            self.page = self.firstpage+8
            self.tasmin_DJF = "-10"
            self.tasmax_DJF = "17.5"
            self.tasmin_JJA = "-5"
            self.tasmax_JJA = "11"
            self.prmin_winter = "-30"
            self.prmax_winter = "100"
            self.prmin_summer = "-25"
            self.prmax_summer = "50"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.8"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.8"

        elif region == 'westnorthamerica':
            # ALA + WNA
            self.lon1[0] = -170;self.lon2[0] = -105;self.lat1[0] = 30;self.lat2[0] = 70;self.lsmask[0] = 'land'
            self.name[1] = "Alaska/NW Canada"
            self.lon1[1] = -168.0220;self.lon2[1] = -105;self.lat1[1] = 60;self.lat2[1] = 72.5540;self.lsmask[1] = 'land'
            self.area[1] = "60dg--72.6dg N, 168dg--105dg W"
            self.abbr[1] = "ALA";self.npoly[1] = 4
            self.name[2] = "West North America"
            self.lon1[2] = -130;self.lon2[2] = -105;self.lat1[2] = 28.5660;self.lat2[2] = 60;self.lsmask[2] = 'land'
            self.area[2] = "28.6dg--60dg N, 130dg--105dg W"
            self.abbr[2] = "WNA";self.npoly[2] = 4
            self.page = self.firstpage+12
            self.labely = 0.678
            self.xwidth = 0.33
            self.tasmin_DJF = "-12.5"
            self.tasmax_DJF = "22.5"
            self.tasmin_JJA = "-5"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-50"
            self.prmax_winter = "125"
            self.prmin_summer = "-30"
            self.prmax_summer = "70"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.3"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.3"

        elif region == 'eastnorthamerica':
            # CNA + ENA
            self.name[0] = "North America East"
            self.lon1[0] = -105;self.lon2[0] = -60;self.lat1[0] = 25;self.lat2[0] = 50;self.lsmask[0] = 'land'
            self.name[1] = "Central North America"
            self.lon1[1] = -105;self.lon2[1] = -85;self.lat1[1] = 28.5660;self.lat2[1] = 50;self.lsmask[1] = 'land'
            self.area[1] = "28.6dg--50dg N, 105dg--85dg W"
            self.abbr[1] = "CNA";self.npoly[1] = 4
            self.name[2] = "Eastern North America"
            self.lon1[2] = -85;self.lon2[2] = -60;self.lat1[2] = 25;self.lat2[2] = 50;self.lsmask[2] = 'land'
            self.area[2] = "25dg--50dg N, 85dg--60dg W"
            self.abbr[2] = "ENA";self.npoly[2] = 4
            self.page = self.firstpage + 16
            self.labely = 0.716
            self.xwidth = 0.27
            self.tasmin_DJF = "-7.5"
            self.tasmax_DJF = "12.5"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-60"
            self.prmax_winter = "90"
            self.prmin_summer = "-60"
            self.prmax_summer = "60"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.3"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.3"

        elif region == 'centralamerica':
            # CAM + home-defined
            self.lon1[0] = -115;self.lon2[0] = -60;self.lat1[0] = 0;self.lat2[0] = 30;self.lsmask[0] = 'land'
            self.name[1] = "Central America"
            self.lsmask[1] = 'land'
            self.area[1] = "68.8dg W,11.4dg N; 79.7dg W, 1.2dg S; 116.3dg W,28.6dg N; 90.3dg W,28.6dg N"
            self.abbr[1] = "CAM";self.npoly[1] = 4
            self.shortname[2] = "Caribbean"
            self.name[2] = "Caribbean (land and sea)"
            self.lon1[2] = -85;self.lon2[2] = -60;self.lat1[2] = 10;self.lat2[2] = 25;self.lsmask[2] = 'all'
            self.area[2] = "10dg--25dg N, 85dg--60dg W"
            self.labely = 0.665
            self.xwidth = 0.33
            self.page = self.firstpage + 20
            self.tasmin_DJF = "-2.5"
            self.tasmax_DJF = "7.5"
            self.tasmin_JJA = "-2.5"
            self.tasmax_JJA = "7.5"
            self.prmin_winter = "-100"
            self.prmax_winter = "100"
            self.prmin_summer = "-100"
            self.prmax_summer = "150"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.4"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.4"

        elif region == 'northsouthamerica':
            # AMZ + NEB
            self.lon1[0] = -80;self.lon2[0] = -35;self.lat1[0] = -20;self.lat2[0] = 10;self.lsmask[0] = 'land'
            self.name[1] = "Amazon"
            self.lsmask[1] = 'land'
            self.area[1] = "20dg S--10dg N, 82.5dg--60dg W"
            self.abbr[1] = "AMZ";self.npoly[1] = 5
            self.name[2] = "North-East Brazil"
            self.lon1[2] = -50;self.lon2[2] = -34;self.lat1[2] = -20;self.lat2[2] = 0;self.lsmask[2] = 'land'
            self.area[2] = "20dg S--EQ, 50dg--34dg W"
            self.abbr[2] = "NEB";self.npoly[2] = 4
            self.labely = 0.693
            self.xwidth = 0.315
            self.page = self.firstpage + 24
            self.tasmin_DJF = "-4"
            self.tasmax_DJF = "12"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "10"
            self.prmin_winter = "-80"
            self.prmax_winter = "120"
            self.prmin_summer = "-100"
            self.prmax_summer = "150"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.5"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.5"

        elif region == 'southsouthamerica':
            # WSA + SSA
            self.name[0] = "Southern South America"
            self.lon1[0] = -82.5;self.lon2[0] = -35;self.lat1[0] = -55;self.lat2[0] = -4;self.lsmask[0] = 'land'
            self.name[1] = "West Coast South America"
            self.lsmask[1] = 'land'
            self.area[1] = "79.7dg W,1.2dg S; 66.4dg W,20dg S; 72.1dg W,50dg S; 67.3dg W56.7dg S; 82.0dg W 56.7dg S; 82.2dg W,0.5dg N"
            self.abbr[1] = "WSA";self.npoly[1] = 6
            self.name[2] = "Southeastern South America"
            self.lsmask[2] = 'land'
            self.area[2] = "39.4dg W,20dg S; 39.4dg W,56.6dg S; 67.3dg W,56.7dg S; 72.1dg W,50dg S; 66dg W,20dg S"
            self.abbr[2] = "SSA";self.npoly[2] = 5
            self.labelx = 0.77
            self.labely = 0.785
            self.xwidth = 0.2025
            self.page = self.firstpage + 28
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "8"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "7"
            self.prmin_winter = "-50"
            self.prmax_winter = "70"
            self.prmin_summer = "-60"
            self.prmax_summer = "100"
            self.tascross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.5"
            self.prcross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.5"
        elif region == 'northeurope':
            # NEU + CEU
            self.name[0] = "North and Central Europe"
            self.lon1[0] = -10;self.lon2[0] = 40;self.lat1[0] = 45;self.lat2[0] = 75;self.lsmask[0] = 'land'
            self.name[1] = "North Europe"
            self.lsmask[1] = 'land'
            self.area[1] = "10dg W,48dg N; 10dg W,75dg N; 40dg E,75dg N; 40dg E,61.3dg N"
            self.abbr[1] = "NEU";self.npoly[1] = 4
            self.name[2] = "Central Europe"
            self.lsmask[2] = 'land'
            self.area[2] = "10dg W, 45dg N; 10dg W,48dg N; 40dg E, 61.3dg N; 40dg E,45dg N"
            self.abbr[2] = "CEU";self.npoly[2] = 4
            self.labely = 0.67
            self.xwidth = 0.33
            self.page = self.firstpage + 32
            self.tasmin_DJF = "-12.5"
            self.tasmax_DJF = "15"
            self.tasmin_JJA = "-5"
            self.tasmax_JJA = "12.5"
            self.prmin_winter = "-50"
            self.prmax_winter = "75"
            self.prmin_summer = "-60"
            self.prmax_summer = "80"
            self.tascross = "9.6.1, 10.3, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.6"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.6"

            # MED + SAH
        elif region == 'mediterranean':
            self.name[0] = "Mediterranean and Sahara"
            self.lon1[0] = -20;self.lon2[0] = 40;self.lat1[0] = 15;self.lat2[0] = 45;self.lsmask[0] = 'land'
            self.name[1] = "South Europe/Mediterranean"
            self.lon1[1] = -10;self.lon2[1] = 40;self.lat1[1] = 30;self.lat2[1] = 45;self.lsmask[1] = 'land'
            self.area[1] = "30dg--45dg N, 10dg W--40dg E"
            self.abbr[1] = "MED";self.npoly[1] = 4
            self.name[2] = "Sahara"
            self.lon1[2] = -20;self.lon2[2] = 40;self.lat1[2] = 15;self.lat2[2] = 30;self.lsmask[2] = 'land'
            self.area[2] = "15dg--30dg N, 20dg W--40dg E"
            self.abbr[2] = "SAH";self.npoly[2] = 4
            self.labely = 0.655
            self.xwidth = 0.33
            self.page = self.firstpage + 36
            self.tasmin_DJF = "-4"
            self.tasmax_DJF = "10"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-60"
            self.prmax_winter = "60"
            self.prmin_winter2 = "-100"
            self.prmax_winter2 = "1000"
            self.prmin_summer = "-100"
            self.prmax_summer = "100"
            self.prmin_summer2 = "-100"
            self.prmax_summer2 = "350"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.6"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.6"

            # WAF + EAF
        elif region == 'weafrica':
            self.name[0] = "West and East Africa"
            self.lon1[0] = -20;self.lon2[0] = 55;self.lat1[0] = -10;self.lat2[0] = 15
            self.name[1] = "west Africa"
            self.lon1[1] = -20;self.lon2[1] = 25;self.lat1[1] = -11.3650;self.lat2[1] = 15;self.lsmask[1] = 'land'
            self.area[1] = "11.4dg S--15dg N, 20dg W--25dg E"
            self.abbr[1] = "WAF";self.npoly[1] = 4
            self.name[2] = "East Africa"
            self.lon1[2] = 25;self.lon2[2] = 52;self.lat1[2] = -11.3650;self.lat2[2] = 15;self.lsmask[2] = 'land'
            self.area[2] = "11.3dg S--15dg N, 25dg--52dg E"
            self.abbr[2] = "EAF";self.npoly[2] = 4
            self.labely = 0.608
            self.xwidth = 0.33
            self.page = self.firstpage + 40
            self.tasmin_DJF = "-4"
            self.tasmax_DJF = "8"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "8"
            self.prmin_winter = "-60"
            self.prmax_winter = "80"
            self.prmin_summer = "-40"
            self.prmax_summer = "80"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.7"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.7"

            # SAF + home-grown
        elif region == 'southafrica':
            self.name[0] = "Southern Africa and West Indian Ocean"
            self.lon1[0] = -10;self.lon2[0] = 75;self.lat1[0] = -35;self.lat2[0] = 10
            self.name[1] = "Southern Africa"
            self.lon1[1] = -10;self.lon2[1] = 52;self.lat1[1] = -35;self.lat2[1] = -11.3650;self.lsmask[1] = 'land'
            self.area[1] = "35dg--11.4dg S, 10dg W--52dg E"
            self.abbr[1] = "SAF";self.npoly[1] = 4
            self.shortname[2] = 'WIndian'
            self.name[2] = 'West Indian Ocean'
            self.lon1[2] = 52;self.lon2[2] = 75;self.lat1[2] = -25;self.lat2[2] = 5;self.lsmask[2] = 'sea'
            self.area[2] = "25dg S--5dg N, 52dg--75dg E"
            self.labely = 0.663
            self.xwidth = 0.33
            self.page = self.firstpage + 44
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "9"
            self.prmin_winter = "-40"
            self.prmax_winter = "60"
            self.prmin_summer = "-100"
            self.prmax_summer = "100"
            self.tascross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.7"
            self.prcross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.7"

            # WAS + CAS
        elif region == 'centralasia':
            self.name[0] = "West and Central Asia"
            self.lon1[0] = 40;self.lon2[0] = 75;self.lat1[0] = 15;self.lat2[0] = 50;self.lsmask[0] = 'land'
            self.name[1] = "West Asia"
            self.lon1[1] = 40;self.lon2[1] = 60;self.lat1[1] = 15;self.lat2[1] = 50;self.lsmask[1] = 'land'
            self.area[1] = "15dg--50dg N, 40dg--60dg E"
            self.abbr[1] = "WAS";self.npoly[1] = 4
            self.name[2] = "Central Asia"
            self.lon1[2] = 60;self.lon2[2] = 75;self.lat1[2] = 30;self.lat2[2] = 50;self.lsmask[2] = 'land'
            self.area[2] = "30dg--50dg N, 60dg--75dg E"
            self.abbr[2] = "CAS";self.npoly[2] = 4
            self.labely = 0.76
            self.xwidth = 0.24
            self.page = self.firstpage + 48
            self.tasmin_DJF = "-7.5"
            self.tasmax_DJF = "12.5"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-100"
            self.prmax_winter = "250"
            self.prmin_summer = "-100"
            self.prmax_summer = "250"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.8"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.8"

            # TIB + EAS
        elif region == 'eastasia':
            self.name[0] = "Eastern Asia and Tibetan Plateau"
            self.lon1[0] = 75;self.lon2[0] = 145;self.lat1[0] = 20;self.lat2[0] = 50
            self.name[1] = "Eastern Asia"
            self.lon1[1] = 100;self.lon2[1] = 145;self.lat1[1] = 20;self.lat2[1] = 50;self.lsmask[1] = 'land'
            self.area[1] = "20dg--50dg N, 100dg--145dg E"
            self.abbr[1] = "EAS";self.npoly[1] = 4
            self.name[2] = "Tibetan Plateau"
            self.lon1[2] = 75;self.lon2[2] = 100;self.lat1[2] = 30;self.lat2[2] = 50;self.lsmask[2] = 'land'
            self.area[2] = "30dg--50dg N, 75dg--100dg E"
            self.abbr[2] = "TIB";self.npoly[2] = 4
            self.labely = 0.635
            self.xwidth = 0.33
            self.page = self.firstpage + 52
            self.tasmin_DJF = "-8"
            self.tasmax_DJF = "12"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "12"
            self.prmin_winter = "-50"
            self.prmax_winter = "100"
            self.prmin_summer = "-50"
            self.prmax_summer = "100"
            self.tascross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.9"
            self.prcross = "9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.9"

            # SAS + homegrown sea self.area
        elif region == 'southasia':
            self.name[0] = "South Asia"
            self.lon1[0] = 60;self.lon2[0] = 100;self.lat1[0] = 5;self.lat2[0] = 30
            self.name[1] = "South Asia"
            self.lsmask[1] = 'land'
            self.area[1] = "60dg E,5dg N; 60dg E,30dg N; 100dg E,30dg N; 100dg E,20dg E; 95dg E,20dg N; 95dg E,5dg N"
            self.abbr[1] = "SAS";self.npoly[1] = 6
            self.shortname[2] = 'NIndian'
            self.name[2] = 'North Indian Ocean'
            self.lon1[2] = 60;self.lon2[2] = 95;self.lat1[2] = 5;self.lat2[2] = 30;self.lsmask[2] = 'sea'
            self.area[2] = "5dg--30dg N, 60dg--95dg E"
            self.labely = 0.683
            self.xwidth = 0.3175
            self.page = self.firstpage + 56
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "9"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "8"
            self.prmin_winter = "-100"
            self.prmax_winter = "200"
            self.prmin_summer = "-60"
            self.prmax_summer = "100"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.10"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.10"

            # SEA
        elif region == 'southeastasia':
            self.name[0] = "Southeast Asia"
            self.lon1[0] = 95;self.lon2[0] = 155;self.lat1[0] = -10;self.lat2[0] = 20;self.lsmask[0] = 'land'
            self.name[1] = 'Southeast Asia (land)'
            self.lon1[1] = 95;self.lon2[1] = 155;self.lat1[1] = -10;self.lat2[1] = 20;self.lsmask[1] = 'land'
            self.area[1] = "10dg S--20dg N, 95dg--155dg E"
            self.abbr[1] = "SEA";self.npoly[1] = 4
            self.shortname[2] = 'SEAsia_sea'
            self.name[2] = 'Southeast Asia (sea)'
            self.lon1[2] = 95;self.lon2[2] = 155;self.lat1[2] = -10;self.lat2[2] = 20;self.lsmask[2] = 'sea'
            self.area[2] = ""
            self.labely = 0.653
            self.xwidth = 0.33
            self.page = self.firstpage + 60
            self.tasmin_DJF = "-2"
            self.tasmax_DJF = "7"
            self.tasmin_JJA = "-2"
            self.tasmax_JJA = "7"
            self.prmin_winter = "-60"
            self.prmax_winter = "60"
            self.prmin_summer = "-40"
            self.prmax_summer = "80"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.11"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.11"

            # NAU + SAU
        elif region == 'australia':
            self.name[0] = "Australia and New Zealand"
            self.lon1[0] = 110;self.lon2[0] = 180;self.lat1[0] = -47.5;self.lat2[0] = -10;self.lsmask[0] = 'land'
            self.name[1] = "North Australia"
            self.lon1[1] = 110;self.lon2[1] = 155;self.lat1[1] = -30;self.lat2[1] = -10;self.lsmask[1] = 'land'
            self.area[1] = "30dg--10dg S, 110dg--155dg E"
            self.abbr[1] = "NAU";self.npoly[1] = 4
            self.name[2] = "South Australia/New Zealand"
            self.lon1[2] = 110;self.lon2[2] = 180;self.lat1[2] = -50;self.lat2[2] = -30;self.lsmask[2] = 'land'
            self.area[2] = "50dg--30dg S, 110dg--180dg E"
            self.abbr[2] = "SAU";self.npoly[2] = 4
            self.labely = 0.665
            self.xwidth = 0.33
            self.page = self.firstpage + 64
            self.tasmin_DJF = "-4"
            self.tasmax_DJF = "8"
            self.tasmin_JJA = "-4"
            self.tasmax_JJA = "8"
            self.prmin_winter = "-100"
            self.prmax_winter = "200"
            self.prmin_summer = "-100"
            self.prmax_summer = "350"
            self.tascross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.12"
            self.prcross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.12"

            # Pacific Island (home-grown)
        elif region == 'pacific':
            self.name[0] = "Pacific Islands region"
            self.lon1[0] = 155;self.lon2[0] = 230;self.lat1[0] = -25;self.lat2[0] = 25;self.lsmask[0] = 'all'
            self.shortname[1] = "NTPacific"
            self.name[1] = "Northern Tropical Pacific"
            self.lon1[1] = 155;self.lon2[1] = 210;self.lat1[1] = 5;self.lat2[1] = 25;self.lsmask[1] = 'all'
            self.area[1] = "5dg--25dg N, 155dg E--150dg W"
            self.shortname[2] = "EQPacific"
            self.name[2] = "Equatorial Pacific"
            self.lon1[2] = 155;self.lon2[2] = 210;self.lat1[2] = -5;self.lat2[2] = 5;self.lsmask[2] = 'all'
            self.area[2] = "5dg S--5dg N, 155dg E--150dg W"
            self.shortname[3] = "STPacific"
            self.name[3] = "Southern Tropical Pacific"
            self.lon1[3] = 155;self.lon2[3] = 230;self.lat1[3] = -25;self.lat2[3] = -5;self.lsmask[3] = 'all'
            self.area[3] = "25dg--5dg S, 155dg E--130dg W"
            self.labely = 0.698
            self.xwidth = 0.325
            self.page = self.firstpage + 68
            self.subregions = [1, 2, 3]
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "5"
            self.tasmin_JJA = "-3"
            self.tasmax_JJA = "5"
            self.prmin_winter = "-100"
            self.prmax_winter = "300"
            self.prmin_summer = "-100"
            self.prmax_summer = "150"
            self.tascross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.13"
            self.prcross = "9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.13"

            # home-grown
        elif region == 'antarctica':
            self.name[0] = "Antarctica"
            self.lon1[0] = -180;self.lon2[0] = 180;self.lat1[0] = -90;self.lat2[0] = -50;self.lsmask[0] = 'all'
            self.name[1] = 'Antarctica (land)'
            self.shortname[1] = "Antarcticland"
            self.area[1] = "90dg--50dg S"
            self.lon1[1] = -180;self.lon2[1] = 180;self.lat1[1] = -90;self.lat2[1] = -50;self.lsmask[1] = 'land'
            self.name[2] = 'Antarctica (sea)'
            self.shortname[2] = "Antarcticsea"
            self.lon1[2] = -180;self.lon2[2] = 180;self.lat1[2] = -90;self.lat2[2] = -50;self.lsmask[2] = 'sea'
            self.area[2] = ""
            self.labelx = 0.79
            self.labely = 0.79
            self.xwidth = 0.213
            self.page = self.firstpage + 72
            self.tasmin_DJF = "-3"
            self.tasmax_DJF = "7"
            self.tasmin_JJA = "-5"
            self.tasmax_JJA = "10"
            self.prmin_winter = "-30"
            self.prmax_winter = "70"
            self.prmin_summer = "-30"
            self.prmax_summer = "70"
            self.tascross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.14"
            self.prcross = "9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.14"
        else:
            print 'unknown region {region}'.format(region)
            # TODO: generate an exception

        self.prmin_winter2 = self.prmin_winter
        self.prmax_winter2 = self.prmax_winter
        self.prmin_summer2 = self.prmin_summer
        self.prmax_summer2 = self.prmax_summer

