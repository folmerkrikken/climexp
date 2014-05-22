"""define_functions_atlas"""

class DefineVarError(Exception):
    """Raised when a error occured in class DefineVar."""
    pass


class DefineVar:

    def __init__(self, var, normsd):
        """define the properties of the variables"""

        # defaults
        self.varname = None
        self.Varname = None

        self.type = 'Amon'
        self.diffvar = 'diff'
        self.cbar = 0
        self.fac = 1
        self.units = ""
        self.notimeseries = ""
        self.standardunits = ""
        self.norelative = False
        self.sdvar = var

        if var in ['tas', 'tasmin', 'tasmax', 't2m', 'tmin', 'tmax', 'air', 'tnn', 'tnx', 'txn', 'txx']:
            if var in ['tas', 't2m', 'air']:
                self.varname = "temperature"
                self.Varname = "Temperature"
                self.sdvar = 'tas'
            elif var in ['tasmin', 'tmin']:
                self.varname = "Tmin"
                self.Varname = "Tmin"
                self.sdvar = 'tasmin'
            elif var in ['tasmax', 'tmax']:
                self.varname = "Tmax"
                self.Varname = "Tmax"
                self.sdvar = 'tasmax'
            elif var in ['tnn', 'tnx', 'txn', 'txx']:
                self.varname = var[:-1].upper() + var[-1:]
                self.Varname = self.varname

            self.cbar = 0 # for GrADS
            self.cmin = -2
            self.cmax = 8.0
            self.cint = 0.5
            self.rgbcbar = 'tas.txt' # for NCL
            self.cnlevels = "(/-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.,3.,4.,5.,7.,9.,11./)"
            self.units = "[Celsius]"
            self.norelative = True

        elif var in ['pr', 'evspsbl', 'pme', 'tp', 'evap', 'prate', 'prcptot', 'r95p', 'r99p', 'rx1day', 'rx5day', 'sdii']:
            self.standardunits = 'standardunits' # I prefer mm/day
            if var in ['pr', 'tp', 'prate']:
                self.varname = "precipitation"
                self.Varname = "Precipitation"
                self.sdvar = 'pr'
            elif var in ['evspsbl', 'evap']:
                self.varname = "evaporation"
                self.Varname = "Evaporation"
                self.sdvar = 'evspsbl'
            elif var == 'pme':
                self.varname = "P-E"
                self.Varname = "P-E"
            elif var == 'prcptot':
                self.varname = 'PRCPTOT'
                self.Varname = self.varname
            elif var == 'r95p':
                self.varname = 'P95pTOT'
                self.Varname = self.varname
            elif var == 'r99p':
                self.varname = 'P99pTOT'
                self.Varname = self.varname
            elif var == 'rx1day':
                self.varname = 'Rx1day'
                self.Varname = self.varname
            elif var == 'rx5day':
                self.varname = 'Rx5day'
                self.Varname = self.varname
            else:
                self.varname = var.upper()
                self.Varname = self.varname

            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.rgbcbar = 'pr.txt'
                self.cmin = -50
                self.cmax = 50
                self.cint = 10
                if var in ['r95p', 'r99p']:
                    self.cnlevels = "(/-200.,-100.,-50.,-20.,-10.,0.,10.,20.,50.,100.,200./)"
                else:
                    self.cnlevels = "(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.rgbcbar = 'pr.txt'
                self.cmin = -1
                self.cmax = 1
                self.cint = 0.2
                self.units = "[mm/dy]"
                self.fac = 1
                self.standardunits = 'standardunits' # I prefer mm/day
                if var in ['r95p', 'r99p']:
                    self.cnlevels = "(/-200.,-100.,-50.,-20.,-10,0.,10.,20.,50.,100.,200./)"
                    # a) standardunits not recognised b) makes no sense either
                    self.standardunits = ''
                    self.units = "[mm/yr]"
                elif var == 'rx1day':
                    self.cnlevels = "(/-20.,-10.,-5,-2,-1,0.,1.,2.,5.,10.,20./)"
                elif var == 'rx5day':
                    self.cnlevels = "(/-50.,-20.,-10.,-5,-2,0.,2.,5.,10.,20.,50./)"
                    self.standardunits = '' # keep in mm/5dy
                    self.units = "[mm/5dy]"
                else:
                    self.cnlevels = "(/-2.,-1.,-0.5,-0.2,-0.1,0.,0.1,0.2,0.5,1.,2./)"

        elif var in ['huss', 'shum2m']:
            self.varname = "specific humidity"
            self.Varname = "Specific humidity"
            self.sdvar = 'huss'
            self.rgbcbar = 'huss.txt'
            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.cmin = -50
                self.cmax = 50
                self.cint = 10
                self.cnlevels = "(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.cmin = -0.0025
                self.cmax =  0.0025
                self.cint =  0.0005
                self.cnlevels = "(/-0.0025,-0.0020,-0.0015,-0.0010,-0.0005,0.,0.0005,0.0010,0.0015,0.0020,0.0025/)"
                self.diffvar = 'diff'
                self.units = "[1]"

        elif var in ['hurs', 'rhum2m']:
            self.varname = "relative humidity"
            self.Varname = "Relative humidity"
            self.sdvar = 'hurs'
            self.rgbcbar = 'huss.txt'
            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.cmin = -25
                self.cmax = 25
                self.cint = 5
                self.cnlevels = "(/-10.,-8.,-6.,-4.,-2.,0.,2.,4.,6.,8.,10./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.cmin = -25
                self.cmax = 25
                self.cint = 5
                self.cnlevels = "(/-5.,-4.,-3.,-2.,-1.,0.,1.,2.,3.,4.,5./)"
                self.units = "[%]"
                self.diffvar = 'diff'

        elif var in ['rsds', 'ssr', 'dswrf']:
            self.varname = "surface solar radation"
            self.Varname = "Surface solar radiation"
            self.rgbcbar = 'psl.txt'
            self.sdvar = 'rsds'
            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.cmin = -10
                self.cmax = 10
                self.cint = 2
                self.cnlevels = "(/-10.,-8.,-6.,-4.,-2.,0.,2.,4.,6.,8.,10./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.cmin = -10
                self.cmax =  10
                self.cint =   2
                self.cnlevels = "(/-10.,-8.,-6.,-4.,-2.,0.,2.,4.,6.,8.,10./)"
                self.diffvar = 'diff'
                self.units = "[W/m2]"

        elif var in ['psl', 'msl', 'prmsl']:
            self.varname = "surface pressure"
            self.Varname = "Surface pressure"
            self.sdvar = 'psl'
            self.standardunits = 'standardunits' # I prefer hPa
            self.rgbcbar = 'psl.txt'
            self.cmin = -2.5
            self.cmax =  2.5
            self.cint =  0.5
            self.cnlevels = "(/-2.5,-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.,2.5/)"
            self.units = "[hPa]"
            self.norelative = True

        elif var == 'mrso':
            self.type = 'Lmon'
            self.varname = "soil moisture"
            self.Varname = "Soil moisture"
            self.sdvar = 'mrso'
            self.rgbcbar = 'pr.txt'
            if normsd == "normsd":
                self.units = "[%]"
                self.cmin = -30
                self.cmax = 30
                self.cint = 5
                self.cnlevels = "(/-50.,-25.,-10.,-5,-2.5,-1.,0.,1.,2.5,5.,10.,25.,50./)"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.units = "[kg/m2]"
                self.cmin = -1
                self.cmax = 1
                self.cint = 0.2
                self.cnlevels = "(/-100,-80,-60,-40,-20,0.,20,40,60,80,100/)"

        elif var in ['mrro', 'mrros']:
            self.type = 'Lmon'
            if var == 'mrro':
                self.varname = "runoff"
                self.Varname = "Runoff"
            else:
                self.varname = "surface runoff"
                self.Varname = "Surface runoff"

            self.diffvar = 'reldiff'
            self.units = "[%]"
            self.fac = 100
            self.cmin = -30
            self.cmax = 30
            self.cint = 5
            self.cbar = 1
            self.rgbcbar = 'precipg.rgb'
            self.cnlevels = "(/-80.-40.,-20.,-10.,-5.,-2.5,0.,2.5,5.,10.,20.,40.,80./)"
            self.notimeseries = True

        elif var in ['cdd','altcdd','cwd','altcwd','csdi','tn10p','tn90p','tx10p','tx90p']:
            self.type = 'yr'
            if var in ['tn10p','tn90p','tx10p','tx90p']:
                self.varname = var[:-1].upper() + 'p'
                self.Varname = self.varname
                self.norelative = True
            else:
                self.varname = var.upper()
                self.Varname = var.upper()
            if var in ['cdd','altcdd']:
                self.rgbcbar = 'prm.txt'
            elif var in ['cwd','altcwd']:
                self.rgbcbar = 'pr.txt'
            elif var in ['csdi', 'tn10p', 'tx10p']:
                self.rgbcbar = 'tasmm.txt'
                self.norelative = True
            elif var in ['tn90p', 'tx90p']:
                self.rgbcbar = 'tas.txt'
            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.cmin = -10
                self.cmax = 10
                self.cint = 2
                if var in ['csdi', 'tn10p', 'tx10p']:
                    self.cnlevels = "(/-100.,-90.,-80.,-70.,-60.,-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                elif var in ['tn90p', 'tx90p']:
                    self.cnlevels = "(/-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100./)"
                else:
                    self.cnlevels = "(/-25.,-20.,-15.,-10.,-5.,0.,5.,10.,15.,20.,25./)"
                    self.cnlevels = "(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.cmin = -10
                self.cmax =  10
                self.cint =   2
                self.diffvar = 'diff'
                if var in ['tn10p', 'tx10p']:
                    self.units = "[%]"
                    self.cnlevels = "(/-10.,-9.,-8.,-7.,-6.,-5.,-4.,-3.,-2.,-1.,0.,1.,2.,3.,4.,5./)"
                elif var in ['tn90p', 'tx90p']:
                    self.units = "[%]"
                    self.cnlevels = "(/-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100./)"
                else:
                    self.units = "[dy]"
                    self.cnlevels = "(/-10.,-8.,-6.,-4.,-2.,0.,2.,4.,6.,8.,10./)"
    
        elif var in ['fd','id', 'gsl', 'r1mm', 'r10mm', 'r20mm']:
            self.type = 'yr'
            self.varname = var.upper()
            self.Varname = var.upper()
            if var in ['fd', 'id']:
                self.rgbcbar = 'tasmm.txt'
            elif var == 'gsl':
                self.rgbcbar = 'tas.txt'
            elif var in ['r1mm', 'r10mm', 'r20mm']:
                self.rgbcbar = 'pr.txt'
            if normsd == "normsd":
                self.varname = "relative " + self.varname
                self.cmin = -10
                self.cmax = 10
                self.cint = 2
                if var in ['fd', 'id']:
                    self.cnlevels = "(/-100.,-90.,-80.,-70.,-60.,-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                elif var == 'gsl':
                    self.cnlevels = "(/-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100./)"
                elif var in ['r10mm', 'r20mm']:
                    self.cnlevels = "(/-250.,-200.,-150.,-100.,-50.,0.,50.,100.,150.,200.,250./)"
                else:
                    self.cnlevels = "(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
                self.units = "[%]"
                self.fac = 100
                self.diffvar = 'reldiff'
            else:
                self.cmin = -10
                self.cmax =  10
                self.cint =   2
                if var in ['r1mm', 'r10mm']:
                    self.cnlevels = "(/-25.,-20.,-15.,-10.,-5.,0.,5.,10.,15.,20.,25./)"
                elif var == 'r20mm':
                    self.cnlevels = "(/-10.,-8.,-6.,-4.,-2.,0.,2.,4.,6.,8.,10./)"
                elif var == 'gsl':
                    self.cnlevels = "(/-40.,-30.,-20.,-10.,0.,10.,20.,30., 40.,50.,60.,80.,100.,120.,140./)"
                else:
                    self.cnlevels = "(/-140.,-120.,-100.,-80.,-60.,-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40./)"
                self.diffvar = 'diff'
                self.units = "[dy]"
        elif var in ['dtr']:
            self.type = 'yr'
            self.varname = var.upper()
            self.Varname = var.upper()
            self.cbar = 0 # for GrADS
            self.cmin = -2.5
            self.cmax = 2.
            self.cint = 0.5
            self.rgbcbar = 'tasp.txt' # for NCL
            self.cnlevels = "(/-2.5,-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.,2.5/)"
            self.units = "[Celsius]"
            self.norelative = True
        else:
            # TODO: raise an exception
            print "DefineVar: error: unknown variable {var}".format(var=var)
    #        exit -1;;
            pass

        if self.units == '[%]':
            # columns and factor 100 for percentages for gnuplot
            self.s2 = "(100*$2)"
            self.s5 = "(100*$5)"
            self.s8 = "(100*$8)"
            self.s10 = "(100*$9)"
            self.s12 = "(100*$10)"
            self.s15 = "(100*$13)"
            pass
        else:
            # just columns
            self.s2 = 2
            self.s5 = 5
            self.s8 = 8
            self.s10 = 9
            self.s12 = 10
            self.s15 = 13


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


def month2string(m):

    monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    # TODO: emit an exception if not in dict
    cm = monthDict[m]
    return cm


