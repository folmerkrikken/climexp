##########################################################################
##########################################################################
# Fair Brier score for 3d fields
# function that computes fair Brier score for two given fields
# (observations and forecasts)
#
# Usage: fairbrierscore(data,threshold,is.value,fbsfile)
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
# threshold: threshold for which the fair Brier score will be computed
#
# is.value: TRUE if the threshold is a value, FALSE if it is a percentage
#
# fbsfile: string of characters with the name of the file where
#            the fair Brier score will be written
#                   
# Author: Camiel Severijns <c.severijns@knmi.nl>
#

fairbrierscore <- function(data,threshold,is.value,fbsfile) {
    data[data == -999.9] <- NA
    observations <- data[,3]
    ensemble     <- data[,4:(dim(data)[2])]
    if (is.value)
        tau <- threshold
    else
        tau <- quantile(observations, threshold/100.0,na.rm=TRUE)
    fbs <- mean(SpecsVerification::FairBrier(ens=ensemble,obs=observations,tau=tau))
    write(paste("Fair Brier score",fbs,sep="="),fbsfile,1,append=FALSE)
}
