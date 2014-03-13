##########################################################################
##########################################################################
# Rank histogram analysis for 3d fields
# function that computes fair CRPS analysis for two given fields
# (observations and forecasts)
#
# Usage: rankhistogramanalysis(data,graphvaluefile,maintitle)
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
# graphvaluefile: string of charaters with the name of the file where
#                 the data used to produce reliability diagram plot will
#                 be written
#                   
# maintitle: String containing the text for the reliability diagram title
#
# Author: Camiel Severijns <c.severijns@knmi.nl>
#

rankhistogram <- function(data,graphvaluefile,maintitle) {
    data[data == -999.9] <- NA

    observations <- data[,3]
    observations <- observations - mean(observations,rm.na=TRUE)

    ensemble <- as.matrix(data[,4:(dim(data)[2])])
    ensemble <- ensemble - mean(ensemble,rm.na=TRUE)

    rh <- SpecsVerification::Rankhist(ens=ensemble,obs=observations)
    SpecsVerification::PlotRankhist(rh,mode="raw")

    write.table(round(rh,2),file=graphvaluefile)
}
