""" Define the parameters for the plot_atlas_form webpage"""

import logging
import sys
import cgi
import datetime
import os
import re
import ast
from util import month2string


# Region: Predefined (srex)
region_values = [['srex', 'IPCC WG1'],
                 ['ipbes', 'IPBES'],
                 ['countries', 'countries'],
                 ['point', 'place'],
                 ['box', 'box']]
#                ['mask', 'mask']]

srex_values = [['world', 'World'],
               ['worldland', 'World (land)'],
               ['worldsea', 'World (sea)'],
               ['NAmerica', 'North America'],
               ['SAmerica', 'South America'],
               ['Europe', 'Europe'],
               ['Africa', 'Africa'],
               ['Asia', 'Asia'],
               ['Australia', 'Australia'],
               ['Arcticland', 'Arctic (land)'],
               ['Arcticsea', 'Arctic (sea)'],
               ['CGI', 'Canada/Greenland/Iceland'],
               ['NAS', 'North Asia'],
               ['ALA', 'Alaska'],
               ['WNA', 'West North America'],
               ['CNA', 'Central North America'],
               ['ENA', 'Eastern North America'],
               ['CAM', 'Central America'],
               ['Caribbean', 'Caribbean'],
               ['AMZ', 'Amazon'],
               ['NEB', 'North-East Brazil'],
               ['WSA', 'West Coast South America'],
               ['SSA', 'Southeastern South America'],
               ['NEU', 'North Europe'],
               ['CEU', 'Central Europe'],
               ['MED', 'South Europe/Mediterranean'],
               ['SAH', 'Sahara'],
               ['WAF', 'west Africa'],
               ['EAF', 'East Africa'],
               ['SAF', 'Southern Africa'],
               ['WIndian', 'West Indian Ocean'],
               ['WAS', 'West Asia'],
               ['CAS', 'Central Asia'],
               ['TIB', 'Tibetan Plateau'],
               ['EAS', 'Eastern Asia'],
               ['SAS', 'South Asia'],
               ['NIndian', 'North Indian Ocean'],
               ['SEA', 'Southeast Asia (land)'],
               ['SEAsia_sea', 'Southeast Asia (sea)'],
               ['NAU', 'North Australia'],
               ['SAU', 'South Australia/New Zealand'],
               ['NTPacific', 'Northern Tropical Pacific'],
               ['EQPacific', 'Equatorial Pacific'],
               ['STPacific', 'Southern Tropical Pacific'],
               ['Antarcticland', 'Antarctic (land)'],
               ['Antarcticsea', 'Antarctic (sea)']]

country_values = [['Afghanistan', 'Afghanistan'],
               ['Aland', 'Aland'],
               ['Albania', 'Albania'],
               ['Algeria', 'Algeria'],
               ['American_Samoa', 'American Samoa'],
               ['Andorra', 'Andorra'],
               ['Angola', 'Angola'],
               ['Anguilla', 'Anguilla'],
               ['Antigua_and_Barb.', 'Antigua and Barbados'],
               ['Argentina', 'Argentina'],
               ['Armenia', 'Armenia'],
               ['Aruba', 'Aruba'],
               ['Ashmore_and_Cartier_Is.', 'Ashmore and Cartier Is.'],
               ['Australia', 'Australia'],
               ['Australia_A._C._T.', '&nbsp; A. C. T.'],
               ['Australia_New_South_Wales', '&nbsp; New South Wales'],
               ['Australia_Northern_Territory', '&nbsp; Northern Territory'],
               ['Australia_Queensland', '&nbsp; Queensland'],
               ['Australia_South_Australia', '&nbsp; South Australia'],
               ['Australia_Tasmania', '&nbsp; Tasmania'],
               ['Australia_Victoria', '&nbsp; Victoria'],
               ['Australia_Western_Australia', '&nbsp; Western Australia'],
               ['Austria', 'Austria'],
               ['Azerbaijan', 'Azerbaijan'],
               ['Bahamas', 'Bahamas'],
               ['Bahrain', 'Bahrain'],
               ['Bangladesh', 'Bangladesh'],
               ['Barbados', 'Barbados'],
               ['Belarus', 'Belarus'],
               ['Belgium', 'Belgium'],
               ['Belize', 'Belize'],
               ['Benin', 'Benin'],
               ['Bermuda', 'Bermuda'],
               ['Bhutan', 'Bhutan'],
               ['Bolivia', 'Bolivia'],
               ['Bosnia_and_Herz.', 'Bosnia and Herzegovina'],
               ['Botswana', 'Botswana'],
               ['Brazil', 'Brazil'],
               ['British_Virgin_Is.', 'British Virgin Islands'],
               ['Brunei', 'Brunei'],
               ['Bulgaria', 'Bulgaria'],
               ['Burkina_Faso', 'Burkina Faso'],
               ['Burundi', 'Burundi'],
               ['Cambodia', 'Cambodia'],
               ['Cameroon', 'Cameroon'],
               ['Canada', 'Canada'],
               ['Cape_Verde', 'Cape Verde'],
               ['Cayman_Is.', 'Cayman Is.'],
               ['Central_African_Rep.', 'Central African Republic'],
               ['Chad', 'Chad'],
               ['Chile', 'Chile'],
               ['China', 'China'],
               ['Colombia', 'Colombia'],
               ['Comoros', 'Comoros'],
               ['Congo_(Brazzaville)', 'Congo (Brazzaville)'],
               ['Congo_(Kinshasa)', 'Congo (Kinshasa)'],
               ['Cook_Is.', 'Cook Islands'],
               ['Costa_Rica', 'Costa Rica'],
               ['Croatia', 'Croatia'],
               ['Cuba', 'Cuba'],
               ['Curacao', 'Curacao'],
               ['Cyprus', 'Cyprus'],
               ['Czech_Rep.', 'Czech Republic'],
               ['Denmark', 'Denmark'],
               ['Djibouti', 'Djibouti'],
               ['Dominica', 'Dominica'],
               ['Dominican_Rep.', 'Dominican Republic'],
               ['East_Timor', 'East Timor'],
               ['Ecuador', 'Ecuador'],
               ['Egypt', 'Egypt'],
               ['El_Salvador', 'El Salvador'],
               ['Eq._Guinea', 'Equatorial Guinea'],
               ['Eritrea', 'Eritrea'],
               ['Estonia', 'Estonia'],
               ['Ethiopia', 'Ethiopia'],
               ['Falkland_Is.', 'Falkland Islands'],
               ['Faroe_Is.', 'Faroe Islands'],
               ['Fiji', 'Fiji'],
               ['Finland', 'Finland'],
               ['France', 'France'],
               ['France_metropolitan', '&nbsp; France metropolitan'],
               ['France_Guiana', '&nbsp; France Guiana'],
               ['France_Martinique', '&nbsp; France Martinique'],
               ['France_Guadeloupe', '&nbsp; France Guadeloupe'],
               ['France_Reunion', '&nbsp; France Reunion'],
               ['France_Mayotte', '&nbsp; France Mayotte'],
               ['Fr._Polynesia', 'French Polynesia'],
               ['Gabon', 'Gabon'],
               ['Gambia', 'Gambia'],
               ['Gaza', 'Gaza'],
               ['Georgia', 'Georgia'],
               ['Germany', 'Germany'],
               ['Ghana', 'Ghana'],
               ['Greece', 'Greece'],
               ['Greenland', 'Greenland'],
               ['Grenada', 'Grenada'],
               ['Guam', 'Guam'],
               ['Guatemala', 'Guatemala'],
               ['Guernsey', 'Guernsey'],
               ['Guinea', 'Guinea'],
               ['Guinea_Bissau', 'Guinea Bissau'],
               ['Guyana', 'Guyana'],
               ['Haiti', 'Haiti'],
               ['Honduras', 'Honduras'],
               ['Hong_Kong', 'Hong Kong'],
               ['Hungary', 'Hungary'],
               ['Iceland', 'Iceland'],
               ['India', 'India'],
               ['Indonesia', 'Indonesia'],
               ['Iran', 'Iran'],
               ['Iraq', 'Iraq'],
               ['Ireland', 'Ireland'],
               ['Isle_of_Man', 'Isle of Man'],
               ['Israel', 'Israel'],
               ['Italy', 'Italy'],
               ['Ivory_Coast', 'Ivory Coast'],
               ['Jamaica', 'Jamaica'],
               ['Japan', 'Japan'],
               ['Jersey', 'Jersey'],
               ['Jordan', 'Jordan'],
               ['Kazakhstan', 'Kazakhstan'],
               ['Kenya', 'Kenya'],
               ['Kiribati', 'Kiribati'],
               ['Kosovo', 'Kosovo'],
               ['Kuwait', 'Kuwait'],
               ['Kyrgyzstan', 'Kyrgyzstan'],
               ['Laos', 'Laos'],
               ['Latvia', 'Latvia'],
               ['Lebanon', 'Lebanon'],
               ['Lesotho', 'Lesotho'],
               ['Liberia', 'Liberia'],
               ['Libya', 'Libya'],
               ['Liechtenstein', 'Liechtenstein'],
               ['Lithuania', 'Lithuania'],
               ['Luxembourg', 'Luxembourg'],
               ['Macau', 'Macau'],
               ['Macedonia', 'Macedonia'],
               ['Madagascar', 'Madagascar'],
               ['Malawi', 'Malawi'],
               ['Malaysia', 'Malaysia'],
               ['Maldives', 'Maldives'],
               ['Mali', 'Mali'],
               ['Malta', 'Malta'],
               ['Marshall_Is.', 'Marshall Islands'],
               ['Mauritania', 'Mauritania'],
               ['Mauritius', 'Mauritius'],
               ['Mexico', 'Mexico'],
               ['Micronesia', 'Micronesia'],
               ['Moldova', 'Moldova'],
               ['Monaco', 'Monaco'],
               ['Mongolia', 'Mongolia'],
               ['Montenegro', 'Montenegro'],
               ['Montserrat', 'Montserrat'],
               ['Morocco', 'Morocco'],
               ['Mozambique', 'Mozambique'],
               ['Myanmar', 'Myanmar'],
               ['N._Korea', 'North Korea'],
               ['N._Mariana_Is.', 'Norhern Mariana Islands'],
               ['Namibia', 'Namibia'],
               ['Nauru', 'Nauru'],
               ['Nepal', 'Nepal'],
               ['Netherlands', 'Netherlands'],
               ['Netherlands_without_Caribbean', '&nbsp; Netherlands without Caribbean'],
               ['Netherlands_Bonaire', '&nbsp; Bonaire'],
               ['Netherlands_Saba_St_Eustasius', '&nbsp; Saba St Eustasius'],
               ['New_Caledonia', 'New Caledonia'],
               ['New_Zealand', 'New Zealand'],
               ['Nicaragua', 'Nicaragua'],
               ['Niger', 'Niger'],
               ['Nigeria', 'Nigeria'],
               ['Niue', 'Niue'],
               ['Norfolk_Island', 'Norfolk Island'],
               ['Norway', 'Norway'],
               ['Oman', 'Oman'],
               ['Pakistan', 'Pakistan'],
               ['Palau', 'Palau'],
               ['Panama', 'Panama'],
               ['Papua_New_Guinea', 'Papua New Guinea'],
               ['Paraguay', 'Paraguay'],
               ['Peru', 'Peru'],
               ['Philippines', 'Philippines'],
               ['Pitcairn_Is.', 'Pitcairn Islands'],
               ['Poland', 'Poland'],
               ['Portugal', 'Portugal'],
               ['Portugal_without_islands', '&nbsp; Portugal without islands'],
               ['Portugal_Azores', '&nbsp; Azores'],
               ['Portugal_Madeira', '&nbsp; Madeira'],
               ['Puerto_Rico', 'Puerto Rico'],
               ['Qatar', 'Qatar'],
               ['Romania', 'Romania'],
               ['Russia', 'Russia'],
               ['Rwanda', 'Rwanda'],
               ['S._Korea', 'South Korea'],
               ['S._Sudan', 'South Sudan'],
               ['Saint_Helena', 'Saint Helena'],
               ['Saint_Lucia', 'Saint Lucia'],
               ['Samoa', 'Samoa'],
               ['San_Marino', 'San Marino'],
               ['Sao_Tome_and_Principe', 'Sao Tome and Principe'],
               ['Saudi_Arabia', 'Saudi Arabia'],
               ['Senegal', 'Senegal'],
               ['Serbia', 'Serbia'],
               ['Seychelles', 'Seychelles'],
               ['Sierra_Leone', 'Sierra Leone'],
               ['Singapore', 'Singapore'],
               ['Sint_Maarten', 'Sint Maarten'],
               ['Slovakia', 'Slovakia'],
               ['Slovenia', 'Slovenia'],
               ['Solomon_Is.', 'Solomon Islands'],
               ['Somalia', 'Somalia'],
               ['Somaliland', 'Somaliland'],
               ['South_Africa', 'South Africa'],
               ['Spain', 'Spain'],
               ['Spain_Europe', '&nbsp; Spain (Europe)'],
               ['Spain_Canary_islands', '&nbsp; Spain Canary Islands'],
               ['Sri_Lanka', 'Sri Lanka'],
               ['St._Barthelemy', 'St. Barthelemy'],
               ['St._Kitts_and_Nevis', 'St. Kitts and Nevis'],
               ['St._Martin', 'St. Martin'],
               ['St._Pierre_and_Miquelon', 'St. Pierre and Miquelon'],
               ['St._Vin._and_Gren.', 'St. Vincent and the Grenasdines'],
               ['Sudan', 'Sudan'],
               ['Suriname', 'Suriname'],
               ['Swaziland', 'Swaziland'],
               ['Sweden', 'Sweden'],
               ['Switzerland', 'Switzerland'],
               ['Switzerland_North', '&nbsp; North'],
               ['Switzerland_South', '&nbsp; South'],
               ['Syria', 'Syria'],
               ['Tajikistan', 'Tajikistan'],
               ['Tanzania', 'Tanzania'],
               ['Thailand', 'Thailand'],
               ['Togo', 'Togo'],
               ['Tonga', 'Tonga'],
               ['Trinidad_and_Tobago', 'Trinidad and Tobago'],
               ['Tunisia', 'Tunisia'],
               ['Turkey', 'Turkey'],
               ['Turkmenistan', 'Turkmenistan'],
               ['Turks_and_Caicos_Is.', 'Turks and Caicos Islands'],
               ['U.S._Virgin_Is.', 'U.S. Virgin Islands'],
               ['Uganda', 'Uganda'],
               ['Ukraine', 'Ukraine'],
               ['United_Arab_Emirates', 'United Arab Emirates'],
               ['United_Kingdom', 'United Kingdom'],
               ['United_States', 'United States'],
               ['United_States_contiguous', '&nbsp; United States contiguous'],
               ['US_Alabama', '&nbsp; Alabama'],
               ['US_Alaska', '&nbsp; Alaska'],
               ['US_Arizona', '&nbsp; Arizona'],
               ['US_Arkansas', '&nbsp; Arkansas'],
               ['US_California', '&nbsp; California'],
               ['US_Colorado', '&nbsp; Colorado'],
               ['US_Connecticut', '&nbsp; Connecticut'],
               ['US_Delaware', '&nbsp; Delaware'],
               ['US_Florida', '&nbsp; Florida'],
               ['US_Georgia', '&nbsp; Georgia'],
               ['US_Hawaii', '&nbsp; Hawaii'],
               ['US_Idaho', '&nbsp; Idaho'],
               ['US_Illinois', '&nbsp; Illinois'],
               ['US_Indiana', '&nbsp; Indiana'],
               ['US_Iowa', '&nbsp; Iowa'],
               ['US_Kansas', '&nbsp; Kansas'],
               ['US_Kentucky', '&nbsp; Kentucky'],
               ['US_Louisiana', '&nbsp; Louisiana'],
               ['US_Maine', '&nbsp; Maine'],
               ['US_Maryland', '&nbsp; Maryland'],
               ['US_Massachusetts', '&nbsp; Massachusetts'],
               ['US_Michigan', '&nbsp; Michigan'],
               ['US_Minnesota', '&nbsp; Minnesota'],
               ['US_Mississippi', '&nbsp; Mississippi'],
               ['US_Missouri', '&nbsp; Missouri'],
               ['US_Montana', '&nbsp; Montana'],
               ['US_Nebraska', '&nbsp; Nebraska'],
               ['US_Nevada', '&nbsp; Nevada'],
               ['US_New_Hampshire', '&nbsp; New Hampshire'],
               ['US_New_Jersey', '&nbsp; New Jersey'],
               ['US_New_Mexico', '&nbsp; New Mexico'],
               ['US_New_York', '&nbsp; New York'],
               ['US_North_Carolina', '&nbsp; North Carolina'],
               ['US_North_Dakota', '&nbsp; North Dakota'],
               ['US_Ohio', '&nbsp; Ohio'],
               ['US_Oklahoma', '&nbsp; Oklahoma'],
               ['US_Oregon', '&nbsp; Oregon'],
               ['US_Pennsylvania', '&nbsp; Pennsylvania'],
               ['US_Rhode_Island', '&nbsp; Rhode Island'],
               ['US_South_Carolina', '&nbsp; South Carolina'],
               ['US_South_Dakota', '&nbsp; South Dakota'],
               ['US_Tennessee', '&nbsp; Tennessee'],
               ['US_Texas', '&nbsp; Texas'],
               ['US_Utah', '&nbsp; Utah'],
               ['US_Vermont', '&nbsp; Vermont'],
               ['US_Virginia', '&nbsp; Virginia'],
               ['US_Washington', '&nbsp; Washington'],
               ['US_West_Virginia', '&nbsp; West Virginia'],
               ['US_Wisconsin', '&nbsp; Wisconsin'],
               ['US_Wyoming', '&nbsp; Wyoming'],
               ['Uruguay', 'Uruguay'],
               ['Uzbekistan', 'Uzbekistan'],
               ['Vanuatu', 'Vanuatu'],
               ['Vatican', 'Vatican'],
               ['Venezuela', 'Venezuela'],
               ['Vietnam', 'Vietnam'],
               ['W._Sahara', 'Western Sahara'],
               ['Wallis_and_Futuna', 'Wallis and Futuna'],
               ['West_Bank', 'West Bank'],
               ['Yemen', 'Yemen'],
               ['Zambia', 'Zambia'],
               ['Zimbabwe', 'Zimbabwe']]

ipbes_values = [['IPBES_Africa', 'IPBES Africa'],
               ['IPBES_Americas', 'IPBES Americas'],
               ['IPBES_Asia', 'IPBES Asia'],
               ['IPBES_Europe_and_Central_Asia', 'IPBES Europe and Central Asia'],
               ['IPBES_Caribbean', 'IPBES Caribbean'],
               ['IPBES_Central_Africa', 'IPBES Central Africa'],
               ['IPBES_Central_Asia', 'IPBES Central Asia'],
               ['IPBES_Central_Europe', 'IPBES Central Europe'],
               ['IPBES_East_Africa_and_adjacent_islands', 'IPBES East Africa and adjacent islands'],
               ['IPBES_Eastern_Europe', 'IPBES Eastern Europe'],
               ['IPBES_Mesoamerica', 'IPBES Mesoamerica'],
               ['IPBES_North-East_Asia', 'IPBES North-East Asia'],
               ['IPBES_North_Africa', 'IPBES North Africa'],
               ['IPBES_North_America', 'IPBES North America'],
               ['IPBES_Oceania', 'IPBES Oceania'],
               ['IPBES_South-East_Asia', 'IPBES South-East Asia'],
               ['IPBES_South_America', 'IPBES South America'],
               ['IPBES_South_Asia', 'IPBES South Asia'],
               ['IPBES_Southern_Africa', 'IPBES Southern Africa'],
               ['IPBES_West_Africa', 'IPBES West Africa'],
               ['IPBES_Western_Asia', 'IPBES Western Asia'],
               ['IPBES_Western_Europe', 'IPBES Western Europe']]


mon_values = [['1', 'Jan'],
              ['2', 'Feb'],
              ['3', 'Mar'],
              ['4', 'Apr'],
              ['5', 'May'],
              ['6', 'Jun'],
              ['7', 'Jul'],
              ['8', 'Aug'],
              ['9', 'Sep'],
              ['10', 'Oct'],
              ['11', 'Nov'],
              ['12', 'Dec']]

dataset_values = [['CMIP5one', 'GCM: CMIP5 (IPCC AR5 Atlas subset)'],
                  ['CMIP5', 'GCM: CMIP5 (full set)'],
                  ['CMIP5extone', 'GCM: CMIP5 extremes (one ensemble member)'],
                  ['CMIP5ext', 'GCM: CMIP5 extremes (full set)'],
                  ['CMIP3', 'GCM: CMIP3'],
#                 ['RT2b', 'RCM: ENSEMBLES (Europe) GCM-driven'],
#                 ['RT3', 'RCM: ENSEMBLES (Europe) ERA40-driven'],
                 ['ERAi', 'ERA-interim reanalysis'],
                 ['ERA20C', 'ERA-20C reanalysis'],
                 ['20CR', '20C reanalysis'],
                 ['obs', 'Observations']]

cmip5_var_values = [['tas', 'near-surface temperature'],
              ['tasmin', 'minimum near-surface temperature'],
              ['tasmax', 'maximum near-surface temperature'],
              ['pr', 'precipitation'],
              ['evspsbl', 'evaporation, transpiration, sublimation'],
              ['pme', 'P-E, net water flux'],
              ['mrso', 'moisture content of soil layer'],
              ['huss', 'specific humidity near the surface'],
              ['hurs', 'relative humidity near the surface'],
              ['rsds', 'downward solar radiation at the surface'],
              ['psl', 'air pressure at sea-level']]

cmip5_extreme_values = [['altcdd','CDD: maximum length of dry spell'],
              ['altcwd','CWD: maximum length of wet spell'],
              ['csdi','CSDI: cold spell duration index'],
              ['dtr','DTR: daily temperature range'],
              ['fd','FD: number of frost days'],
              ['id','ID: number of icing days'],
              ['gsl','GSL: growing season length'],
              ['prcptot','PRCPTOT: annual total precipitation in wet days'],
              ['r1mm','R1mm: annual count of days when PRCP &ge; 1mm'],
              ['r10mm','R10mm: annual count of days when PRCP &ge; 10mm'],
              ['r20mm','R20mm: annual count of days when PRCP &ge; 20mm'],
              ['r95p','R95pTOT: annual total PRCP when RR &gt; 95p'],
              ['r99p','R99pTOT: annual total PRCP when RR &gt; 99p'],
              ['rx1day','Rx1day: annual maximum 1-day precipitation'],
              ['rx5day','Rx5day: annual maximum consecutive 5-day precipitation'],
              ['sdii','SDII: simple precipitation intensity index'],
              ['tn10p','TN10p: percentage of days when TN &lt; 10th percentile'],
              ['tn90p','TN90p: percentage of days when TN &gt; 90th percentile'],
              ['tnn','TNn: annual minimum value of daily minimum temperature'],
              ['tnx','TNx: annual maximum value of daily minimum temperature'],
              ['tx10p','TX10p: percentage of days when TX &lt; 10th percentile'],
              ['tx90p','TX90p: percentage of days when TX &gt; 90th percentile'],
              ['txn','TXn: annual minimum value of daily maximum temperature'],
              ['txx','TXx: annual maximum value of daily maximum temperature']]

cmip3_var_values = [['tas', 'near-surface temperature'],
              ['pr', 'precipitation'],
              ['psl', 'air pressure at sea-level']]

erai_var_values =[['t2m', 'near-surface temperature'],
              ['tmin', 'minimum near-surface temperature'],
              ['tmax', 'maximum near-surface temperature'],
              ['tp', 'precipitation'],
              ['evap', 'evaporation, transpiration, sublimation'],
              ['pme', 'P-E, net water flux'],
              ['huss', 'specific humidity near the surface'],
              ['ssr', 'net solar radiation at the surface'],
              ['msl', 'air pressure at sea-level']]

era20c_var_values =[['t2m', 'near-surface temperature'],
              ['tmin', 'minimum near-surface temperature'],
              ['tmax', 'maximum near-surface temperature'],
              ['tp', 'precipitation'],
              ['evap', 'evaporation, transpiration, sublimation'],
              ['pme', 'P-E, net water flux'],
              ['huss', 'specific humidity near the surface'],
              ['ssr', 'net solar radiation at the surface'],
              ['msl', 'air pressure at sea-level']]

c20cr_var_values =[['air', 'near-surface temperature'],
              ['tmin', 'minimum near-surface temperature'],
              ['tmax', 'maximum near-surface temperature'],
              ['prate', 'precipitation'],
              ['evap', 'evaporation, transpiration, sublimation'],
              ['pme', 'P-E, net water flux'],
              ['shum2m', 'specific humidity near the surface'],
              ['dswrf', 'downward solar radiation at the surface'],
              ['prmsl', 'air pressure at sea-level']]

obs_var_values =[['tas', 'near-surface temperature'],
              ['tasmin', 'minimum near-surface temperature'],
              ['tasmax', 'maximum near-surface temperature'],
              ['pr', 'precipitation'],
              ['psl', 'air pressure at sea-level']]

output_values = [['map', 'map'],
                 ['series', 'time series']]
#                ['histogram', 'histogram']]
#                ['scatter', 'scatter plots']

transparency_values = [['on', 'on'],
                 ['off', 'off']]

sum_values = [str(el) for el in range(1, 13)]    # ['1', '2', ..., '12']

regr_values = [['time', 'Linear trend in time'],
               ['co2eq45', 'Proportional to RCP4.5 effective CO2 concentration'],
               ['co2eq85', 'Proportional to RCP8.5 effective CO2 concentration'],
               ['obstglobal', 'Proportional to observed Tglobal']]
#              ['modtglobal', 'Proportional to modelled Tglobal']]

scenario_cmip5_values = [['rcp26', 'Historical + RCP2.6'],
                         ['rcp45', 'Historical + RCP4.5'],
                         ['rcp60', 'Historical + RCP6.0'],
                         ['rcp85', 'Historical + RCP8.5'],
                         ['rcp45to85', 'Historical + RCP4.5/RCP6.0/RCP8.5']]

obs_tas_values = [['giss_temp_1200', 'GISTEMP 1200'],
                  ['ncdc_temp', 'NCDC MOST'],
                  ['hadcrut4', 'HadCRUT4.2.0.0'],
                  ['cru_tmp', 'CRU TS 3.23']]

obs_tasmin_values = [['cru_tmn', 'CRU TS 3.23']]

obs_tasmax_values = [['cru_tmx', 'CRU TS 3.23']]

obs_pr_values = [['gpcc_25_n1', 'GPCC v6'],
                 ['prca', 'NCDC anomalies'],
                 ['cru_pre', 'CRU TS 3.23']]

obs_psl_values = [['trenberthslp', 'UCAR ds010 (NH only)'],
                  ['hadslp2r', 'HadSLP2r']]

measure_values = [['diff', 'Difference of two periods'],
                  ['regr', 'Linear or non-linear trend']]

plotvar_values = [['mean', 'mean'],
                  ['p025', '2.5%'],
                  ['p05', '5%'],
                  ['p10', '10%'],
                  ['p17', '17%'],
                  ['p25', '25%'],
                  ['p50', '50%'],
                  ['p75', '75%'],
                  ['p83', '83%'],
                  ['p90', '90%'],
                  ['p95', '95%'],
                  ['p975', '97.5%']]



class FormParameters:
    """Object to collect the parameters from the Atlas HTML formular."""

    def __init__(self, form=None, logLevel=logging.INFO, isLogFormatHTML=True):
        """Initialize the object."""

        # Create a logger
        self.log = logging.getLogger('FormParameters')
        self.log.setLevel(logLevel)

        # Configure the logger to log in the HTML page
#        self.hdlr = logging.StreamHandler(sys.stdout)
#        self.hdlr.setFormatter(util.JavascriptFormatter())
#        self.log.addHandler(self.hdlr)

        if not isLogFormatHTML:
            hdlr = logging.StreamHandler(sys.stdout)
        #            hdlr.setFormatter(logging.Formatter('%(name)s: %(message)s'))
            hdlr.setFormatter(logging.Formatter('\033[1;31m%(name)s:\033[1;0m \033[1;1m%(message)s\033[1;0m'))
        else:
            hdlr = logging.StreamHandler(sys.stdout)
            hdlr.setFormatter(logging.Formatter('<b>%(name)s</b>: <i>%(message)s</i><br>'))

        self.log.addHandler(hdlr)

        if form is None:
            form = cgi.FieldStorage()

        # defaults
        self.EMAIL = 'someone@somewhere'
        self.FORM_resubmitted = ""
        self.FORM_region = 'srex'
        self.FORM_srex = 'world'
        self.FORM_ipbes = ''
        self.FORM_country = ''
        self.FORM_masktype = 'all'
        self.FORM_mon = '1'
        self.FORM_sum = '12'
        self.FORM_dataset = 'CMIP5one'
        self.FORM_var = 'tas'
        self.FORM_output = 'map'
        self.FORM_scenario_cmip5 = 'rcp45'
        self.FORM_scenario_cmip3 = 'sresa1b'
        self.FORM_scenario_rt2b = 'sresa1b'
        self.FORM_obs_tas = 'giss_temp_1200'
        self.FORM_obs_tasmin = 'cru_tmn'
        self.FORM_obs_tasmax = 'cru_tmx'
        self.FORM_obs_pr = 'gpcc_25_n1'
        self.FORM_obs_psl = 'hadslp2r'
        self.FORM_measure = 'diff'
        self.FORM_regr = 'time'
        self.FORM_plotvar = 'mean'
        self.FORM_transparency = 'on'
        self.FORM_begin = '1900'
        self.FORM_end = '2100'
        self.FORM_begin1 = '1986'
        self.FORM_end1 = '2005'
        self.FORM_begin2 = '2081'
        self.FORM_end2 = '2100'
        self.FORM_begin_fit = '1950'
        self.FORM_end_fit = '2100'
        self.FORM_lon = ''
        self.FORM_lat = ''
        self.FORM_lon1 = ''
        self.FORM_lat1 = ''
        self.FORM_lon2 = ''
        self.FORM_lat2 = ''
        self.FORM_normsd = ''
        self.FORM_rcp26 = ''
        self.FORM_rcp45 = ''
        self.FORM_rcp60 = ''
        self.FORM_rcp85 = ''
        self.FORM_anomaly = ''
        self.FORM_anom1 = ''
        self.FORM_anom2 = ''
        self.FORM_transparency = ''

        # first a few that are needed
        self.DO_ACTION = form.getfirst('doAction', '')
        self.EMAIL = form.getfirst('id', 'someone@somewhere')
        if self.EMAIL[:3] == 'id=': # this sometimes happens :-(
            self.EMAIL = self.EMAIL[3:]
        self.REMOTE_ADDR = os.environ["REMOTE_ADDR"]

        # overwrite with values last time the form was called
        if self.EMAIL != "someone@somwehere" and self.EMAIL != "":
            prefs = "prefs/" + self.EMAIL + ".atlas"
            if os.path.exists(prefs):
                with open(prefs, 'r') as f:
                    pat = re.compile('^FORM_[a-z0-9]* = "[-0-9a-zA-Z.]*";$')
                    for line in f:
                        if pat.match(line):
                            ###print line
                            exec('self.'+line[:-2])
                            ###ast.literal_eval('self.'+line[:-2])

        # overwrite with actual values
        pat = re.compile('[^-._A-Za-z0-9]')
        self.FORM_resubmitted = form.getfirst('region', "")
        self.FORM_region = form.getfirst('region', self.FORM_region)
        self.FORM_region = pat.sub('',self.FORM_region)
        self.FORM_srex = form.getfirst('srex', self.FORM_srex)
        self.FORM_srex = pat.sub('',self.FORM_srex)
        self.FORM_ipbes = form.getfirst('ipbes', self.FORM_ipbes)
        self.FORM_ipbes = pat.sub('',self.FORM_ipbes)
        self.FORM_country = form.getfirst('country', self.FORM_country)
        self.FORM_country = pat.sub('',self.FORM_country)
        self.FORM_lon = form.getfirst('lon', self.FORM_lon)
        self.FORM_lon = pat.sub('',self.FORM_lon)
        self.FORM_lat = form.getfirst('lat', self.FORM_lat)
        self.FORM_lat = pat.sub('',self.FORM_lat)
        self.FORM_lon1 = form.getfirst('lon1', self.FORM_lon1)
        self.FORM_lon1 = pat.sub('',self.FORM_lon1)
        self.FORM_lon2 = form.getfirst('lon2', self.FORM_lon2)
        self.FORM_lon2 = pat.sub('',self.FORM_lon2)
        self.FORM_lat1 = form.getfirst('lat1', self.FORM_lat1)
        self.FORM_lat1 = pat.sub('',self.FORM_lat1)
        self.FORM_lat2 = form.getfirst('lat2', self.FORM_lat2)
        self.FORM_lat2 = pat.sub('',self.FORM_lat2)
        self.FORM_masktype = form.getfirst('masktype', self.FORM_masktype)
        self.FORM_masktype = pat.sub('',self.FORM_masktype)
        self.FORM_mon = form.getfirst('mon', self.FORM_mon)
        self.FORM_mon = pat.sub('',self.FORM_mon)
        self.FORM_sum = form.getfirst('sum', self.FORM_sum)
        self.FORM_sum = pat.sub('',self.FORM_sum)
        self.FORM_dataset = form.getfirst('dataset', self.FORM_dataset)
        self.FORM_dataset = pat.sub('',self.FORM_dataset)
        self.FORM_var = form.getfirst('var', self.FORM_var)
        self.FORM_var = pat.sub('',self.FORM_var)
        self.FORM_normsd = form.getfirst('normsd', self.FORM_normsd)
        self.FORM_normsd = pat.sub('',self.FORM_normsd)
        if self.FORM_normsd != "normsd":
            self.FORM_normsd = ""
        self.FORM_output = form.getfirst('output', self.FORM_output)
        self.FORM_output = pat.sub('',self.FORM_output)
        self.FORM_scenario_cmip5 = form.getfirst('scenario_cmip5', self.FORM_scenario_cmip5)
        self.FORM_scenario_cmip5 = pat.sub('',self.FORM_scenario_cmip5)
        self.FORM_scenario_cmip3 = form.getfirst('scenario_cmip3', self.FORM_scenario_cmip3)
        self.FORM_scenario_cmip3 = pat.sub('',self.FORM_scenario_cmip3)
        self.FORM_scenario_rt2b = form.getfirst('scenario_rt2b', self.FORM_scenario_rt2b)
        self.FORM_scenario_rt2b = pat.sub('',self.FORM_scenario_rt2b)
        self.FORM_measure = form.getfirst('measure', self.FORM_measure)
        self.FORM_measure = pat.sub('',self.FORM_measure)
        self.FORM_regr = form.getfirst('regr', self.FORM_regr)
        self.FORM_regr = pat.sub('',self.FORM_regr)
        self.FORM_plotvar = form.getfirst('plotvar', self.FORM_plotvar)
        self.FORM_plotvar = pat.sub('',self.FORM_plotvar)
        self.FORM_obs_tas = form.getfirst('obs_tas', self.FORM_obs_tas)
        self.FORM_obs_tas = pat.sub('',self.FORM_obs_tas)
        self.FORM_obs_tasmin = form.getfirst('obs_tasmin', self.FORM_obs_tasmin)
        self.FORM_obs_tasmin = pat.sub('',self.FORM_obs_tasmin)
        self.FORM_obs_tasmax = form.getfirst('obs_tasmax', self.FORM_obs_tasmax)
        self.FORM_obs_tasmax = pat.sub('',self.FORM_obs_tasmax)
        self.FORM_obs_pr = form.getfirst('obs_pr', self.FORM_obs_pr)
        self.FORM_obs_pr = pat.sub('',self.FORM_obs_pr)
        self.FORM_obs_psl = form.getfirst('obs_psl', self.FORM_obs_psl)
        self.FORM_obs_psl = pat.sub('',self.FORM_obs_psl)
        if self.FORM_resubmitted:
            # ignore defaults
            self.FORM_rcp26 = ""
            self.FORM_rcp45 = ""
            self.FORM_rcp60 = ""
            self.FORM_rcp85 = ""
        self.FORM_rcp26 = form.getfirst('rcp26', self.FORM_rcp26)
        self.FORM_rcp26 = pat.sub('',self.FORM_rcp26)
        self.FORM_rcp45 = form.getfirst('rcp45', self.FORM_rcp45)
        self.FORM_rcp45 = pat.sub('',self.FORM_rcp45)
        self.FORM_rcp60 = form.getfirst('rcp60', self.FORM_rcp60)
        self.FORM_rcp60 = pat.sub('',self.FORM_rcp60)
        self.FORM_rcp85 = form.getfirst('rcp85', self.FORM_rcp85)
        self.FORM_rcp85 = pat.sub('',self.FORM_rcp85)
        self.FORM_anomaly = form.getfirst('anomaly', self.FORM_anomaly)
        self.FORM_anomaly = pat.sub('',self.FORM_anomaly)
        self.FORM_anom1 = form.getfirst('anom1', self.FORM_anom1)
        self.FORM_anom1 = pat.sub('',self.FORM_anom1)
        self.FORM_anom2 = form.getfirst('anom2', self.FORM_anom2)
        self.FORM_anom2 = pat.sub('',self.FORM_anom2)
        self.FORM_transparency = form.getfirst('transparency', self.FORM_transparency)
        self.FORM_transparency = pat.sub('',self.FORM_transparency)

###        self.FORM_region_old = form.getfirst('region_old', ''))
###        self.FORM_dataset_old = form.getfirst('dataset_old', ''))
###        self.FORM_var_old = form.getfirst('var_old', ''))
###        self.FORM_measure_old = form.getfirst('measure_old', ''))
###        self.FORM_output_old = form.getfirst('output_old', ''))

        self.var_ok = False
        self.dataset_ok = False

        self.offset = 0

        self.dumptypes = None
        self.endhistory = None

        self.log.debug("Init.")

    def adjustBeginEnd(self, begin, end):
        
        if end > self.yr2:
            begin = self.yr2 - end + begin
            if begin < self.yr1:
                begin = self.yr1
            end = self.yr2

        if begin < self.yr1:
            end = self.yr1 + end - begin
            if end > self.yr2:
                end = self.yr2
            begin = self.yr1

        return begin, end

    def get_winter_offset(self, mon1,sum):

        mon2 = mon1 + sum - 1
        if mon2 > 12:
            offset = -1
        else:
            offset = 0
    
        return offset

    def calculateDate(self, form=None):
        """Calculate dates."""

        self.log.debug('CalculateDate')

        if form is None:
            form = cgi.FieldStorage()

        # Find yr1 and yr2
        thisYear = datetime.date.today() - datetime.timedelta(days=31)
        thisYear = thisYear.year

        self.dumptypes, self.endhistory = [0], thisYear

        if self.FORM_dataset in ['CMIP5', 'CMIP5one', 'CMIP5ext', 'CMIP5extone']:
            self.yr1, self.yr2 = 1861, 2100
            self.dumptypes, self.endhistory = [0, 1], 2005
        elif self.FORM_dataset == 'CMIP3':
            self.yr1, self.yr2 = 1900, 2099
            self.dumptypes, self.endhistory = [0, 1], 2000
        elif self.FORM_dataset == 'RT2b':
            self.yr1, self.yr2 = 1950, 2100
            self.dumptypes, self.endhistory = [0, 1], 2000
        elif self.FORM_dataset == 'RT3':
            self.yr1, self.yr2 = 1960, 2000
        elif self.FORM_dataset == '20CR':
            self.yr1, self.yr2 = 1878, 2010
        elif self.FORM_dataset == 'ERA20C':
            self.yr1, self.yr2 = 1900, 2010
        elif self.FORM_dataset in ['ERAi']:
            self.yr1 = 1979
            self.yr2 = thisYear
            self.log.debug('FORM_dataset == ERAi, yr1=%i, yr2=%i', self.yr1, self.yr2)
        elif self.FORM_dataset == 'obs':
            self.dataset_ok = True
            self.var_ok = False
            if self.FORM_var in ['tas', 'pr', 'psl']:
                self.var_ok = True

            if self.FORM_var == 'tas':
                self.yr1 = 1880
            else:
                self.yr1 = 1901
            self.yr2 = thisYear

        # do not overwrite values from the defaults file
        if self.FORM_begin == None:
            self.FORM_begin = '1900'
        if self.FORM_end == None:
            self.FORM_end = '2100'
        if self.FORM_begin1 == None:
            self.FORM_begin1 = '1986'
        if self.FORM_end1 == None:
            self.FORM_end1 = '2005'
        if self.FORM_begin2 == None:
            self.FORM_begin2 = str(self.yr2 - 19)
        if self.FORM_end2 == None:
            self.FORM_end2 = str(self.yr2)
        if self.FORM_begin_fit == None:
            self.FORM_begin_fit = '1950'
        if self.FORM_end_fit == None:
            self.FORM_end_fit = str(self.yr2)

        # finally, form values overrule everything else
        pat = re.compile('[^-._A-Za-z0-9]')
        self.FORM_begin = form.getfirst('begin', self.FORM_begin)
        self.FORM_begin = int(pat.sub('',self.FORM_begin))
        self.FORM_end = form.getfirst('end', self.FORM_end)
        self.FORM_end = int(pat.sub('',self.FORM_end))
        self.FORM_begin1 = form.getfirst('begin1', self.FORM_begin1)
        self.FORM_begin1 = int(pat.sub('',self.FORM_begin1))
        self.FORM_end1 = form.getfirst('end1', self.FORM_end1)
        self.FORM_end1 = int(pat.sub('',self.FORM_end1))
        self.FORM_begin2 = form.getfirst('begin2', self.FORM_begin2)
        self.FORM_begin2 = int(pat.sub('',self.FORM_begin2))
        self.FORM_end2 = form.getfirst('end2', self.FORM_end2)
        self.FORM_end2 = int(pat.sub('',self.FORM_end2))
        self.FORM_begin_fit = form.getfirst('begin_fit', self.FORM_begin_fit)
        self.FORM_begin_fit = int(pat.sub('',self.FORM_begin_fit))
        self.FORM_end_fit = form.getfirst('end_fit', self.FORM_end_fit)
        self.FORM_end_fit = int(pat.sub('',self.FORM_end_fit))

        mon1 = int(self.FORM_mon)
        sum = int(self.FORM_sum)
        self.log.debug("mon1 = %i<br>", mon1)
        self.log.debug("sum = %i<br>", sum)

        self.offset = self.get_winter_offset(mon1, sum)

        self.FORM_begin, self.FORM_end = self.adjustBeginEnd(self.FORM_begin, self.FORM_end)
        self.FORM_begin1, self.FORM_end1 = self.adjustBeginEnd(self.FORM_begin1, self.FORM_end1)
        self.FORM_begin2, self.FORM_end2 = self.adjustBeginEnd(self.FORM_begin2, self.FORM_end2)
        self.FORM_begin_fit, self.FORM_end_fit = self.adjustBeginEnd(self.FORM_begin_fit, self.FORM_end_fit)

        if self.FORM_measure == 'regr':
            if self.FORM_end_fit > self.yr2:
                self.FORM_end_fit = self.yr2

            if self.FORM_begin_fit < self.yr1:
                self.FORM_begin_fit = self.yr1
            self.log.debug('FORM_measure == regr, FORM_begin_fit=%i, FORM_end_fit=%i',  
                self.FORM_begin_fit, self.FORM_end_fit)
                

    def dump(self):
        """Display all parameters."""

        paramsLst = ["EMAIL                 = '%s'" % self.EMAIL,
                     "",
                     "# Select a region",
                     "FORM_region           = '%s'" % self.FORM_region,
                     "FORM_srex             = '%s'" % self.FORM_srex,
                     "FORM_ipbes            = '%s'" % self.FORM_ipbes,
                     "FORM_country          = '%s'" % self.FORM_country,
                     "",
                     "FORM_lon1             = '%s'" % self.FORM_lon1,
                     "FORM_lon2             = '%s'" % self.FORM_lon2,
                     "FORM_lat1             = '%s'" % self.FORM_lat1,
                     "FORM_lat2             = '%s'" % self.FORM_lat2,
                     "",
                     "FORM_masktype         = '%s'" % self.FORM_masktype,
                     "",
                     "# Select a season",
                     "FORM_mon              = '%s'" % self.FORM_mon,
                     "FORM_sum              = '%s'" % self.FORM_sum,
                     "",
                     "# Select a dataset and variable"
                     "FORM_dataset          = '%s'" % self.FORM_dataset,
                     "FORM_var              = '%s'" % self.FORM_var,
                     "FORM_normsd           = '%s'" % self.FORM_normsd,
                     "FORM_output           = '%s'" % self.FORM_output,
                     "",
                     "# Map options",
                     "FORM_scenario_cmip5   = '%s'" % self.FORM_scenario_cmip5,
                     "FORM_scenario_cmip3   = '%s'" % self.FORM_scenario_cmip3,
                     "FORM_scenario_rt2b    = '%s'" % self.FORM_scenario_rt2b,
                     "FORM_begin1           = '%s'" % self.FORM_begin1,
                     "FORM_end1             = '%s'" % self.FORM_end1,
                     "FORM_begin2           = '%s'" % self.FORM_begin2,
                     "FORM_end2             = '%s'" % self.FORM_end2,
                     "FORM_plotvar          = '%s'" % self.FORM_plotvar,
                     "",
                     "# Series option",
                     "FORM_rcp26            = '%s'" % self.FORM_rcp26,
                     "FORM_rcp45            = '%s'" % self.FORM_rcp45,
                     "FORM_rcp60            = '%s'" % self.FORM_rcp60,
                     "FORM_rcp85            = '%s'" % self.FORM_rcp85,
                     "FORM_begin            = '%s'" % self.FORM_begin,
                     "FORM_end              = '%s'" % self.FORM_end,
                     "FORM_anomaly          = '%s'" % self.FORM_anomaly,
                     "FORM_anom1            = '%s'" % self.FORM_anom1,
                     "FORM_anom2            = '%s'" % self.FORM_anom2,
                     "",
                     "FORM_measure          = '%s'" % self.FORM_measure,
                     "FORM_regr             = '%s'" % self.FORM_regr,
                     "FORM_obs_tas          = '%s'" % self.FORM_obs_tas,
                     "FORM_obs_pr           = '%s'" % self.FORM_obs_pr,
                     "FORM_obs_psl          = '%s'" % self.FORM_obs_psl,
                     "FORM_lon              = '%s'" % self.FORM_lon,
                     "FORM_lat              = '%s'" % self.FORM_lat,
                     "yr1                   = '%s'" % self.yr1,
                     "yr2                   = '%s'" % self.yr2,
                     "FORM_begin_fit        = '%s'" % self.FORM_begin_fit,
                     "FORM_end_fit          = '%s'" % self.FORM_end_fit]

        return paramsLst


def get_season_name(params):
    
    mon1 = int(params.FORM_mon)
    form_sum = int(params.FORM_sum)

    mon2 = mon1 + form_sum - 1
    if mon2 > 12:
        mon2 -=  12
    
    cmon1 = month2string(mon1)
    
    if form_sum == 1:
        sname = cmon1
    else:
        cmon2 = month2string(mon2)
        sname = "{cmon1}-{cmon2}".format(cmon1=cmon1, cmon2=cmon2)

    return sname
