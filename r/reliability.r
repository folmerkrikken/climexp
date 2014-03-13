reliability <- function(data, u, nbins=10, threshold = TRUE,reliabfile,graphvaluefile,maintitle="") {
  # Plot reliability diagram for an ensemble forecast
  #
  # Usage: reliability(data, u, nbins, threshold, reliabfile,maintitle)
  #
  # Arguments:
  #    data: a table with the following structure
  #           first  column = year
  #	     second column = month
  #	     third  column = observation
  #	     forth  column = ensemble member 1
  #	     fith   column = ensemble member 2
  #	     .
  #	     .
  #	     .
  #	     last   column = ensemble member k
  #
  #    u: threshold value or quantile (e.g. u=50 for the 0.5 quantile, 
  #       i.e. the median of the observations) that defined the event of 
  #       interest to be forecast
  #
  #    nbins: number of probability bins 
  #
  #    threshold: Logical. If TRUE (Default) uses the value u as threshold, if
  #               FALSE u should have the value of the quantile to be computed
  #  
  #
  #    reliabfile: string of charaters with the name of the file where
  #            the threshold value or quantile u will be written
  #
  # graphvaluefile: string of charaters with the name of the file where
  #                 the data used to produce reliability diagram plot will
  #                 be written
  #                   
  #    maintitle: String containing the text for the reliability diagram title
  #
  # Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>

  data[data == -999.9] <- NA

  observations <- data[,3]
  observations <- observations - mean(observations)

  ensemble <- as.matrix(data[,4:(dim(data)[2])])
  ensemble <- ensemble - mean(ensemble,na.rm=TRUE)

  if (threshold)
      thresh <- u
  else
      thresh <- quantile(observations,u/100.0,na.rm=TRUE)

  p <- rowMeans(ensemble <= thresh,na.rm=TRUE)
  y <- 1*(observations <= thresh)

  rd <- SpecsVerification::ReliabilityDiagram(probs=p,obs=y,bins=((0:nbins)/nbins),plot=TRUE,nboot=500,mc.cores=8)
  
  write.table(round(rd,4),file=reliabfile)
  write.table(round(rd,4),file=graphvaluefile)
}
