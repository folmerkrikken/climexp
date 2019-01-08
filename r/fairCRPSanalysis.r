##########################################################################
##########################################################################
# Fair CRPS analysis for 3d fields
# function that computes fair CRPS analysis for two given fields
# (observations and forecasts)
#
# Usage: fairCRPSanalysis(data,fcafile)
#
# Inputs:
#
# data: a table with the following structure
#           first  column = year
#	    second column = month
#	    third  column = observation
#	    forth  column = ensemble member 1
#	    fifth  column = ensemble member 2
#	    .
#	    .
#	    .
#	    last   column = ensemble member k
#
# fcafile: string of characters with the name of the file where
#            the fair CPRS analysis will be written
#                   
# Author: Camiel Severijns <c.severijns@knmi.nl>
#

fairCRPSanalysis <- function(data,fcafile) {
    require(parallel)
    
    data[data == -999.9] <- NA

    observations <- as.vector(data[,3])
    ensemble     <- as.matrix(data[,4:(dim(data)[2])])

    fca <- mean(SpecsVerification::FairCrps(ens=ensemble,obs=observations))

    write(paste("Fair CRPS analysis",fca,sep="="),fcafile,1,append=FALSE)
}
