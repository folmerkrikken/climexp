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
  library(verification)
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts


  if(threshold) u<- u
  else u<-quantile(x,u/100)

  bsall <- mean((apply(y <= u, 1, mean, na.rm=TRUE) - (x <= u))^2)

  probfcsts <- apply(y <= u, 1, mean, na.rm=TRUE)                             
  binobs <- (x <= u)                                              
  obar <- mean(binobs, na.rm=TRUE)
  n<-length(probfcsts)                                            

  h<-hist(probfcsts,breaks=seq(0,1,1/nbins),plot=F)$counts        


  g<-hist(probfcsts[binobs==1],breaks=seq(0,1,1/nbins),plot=F)$counts
  
  obari <- g/h                                                    
  ###obari[is.na(obari)]<-0
  
  # Computes reliability,resolution and uncertainty components of the 
  # Brier score 
  yi <- seq((1/nbins)/2,1,1/nbins)
  
  reliab <- sum(h*((yi-obari)^2), na.rm=TRUE)/n
  resol <- sum(h*((obari-obar)^2), na.rm=TRUE)/n
  uncert<-obar*(1-obar)

  bs<-reliab-resol+uncert
  
  reliability.plot(yi,obari,h,titl=maintitle,legend.names="forecast")

  out<-cbind(yi,obari,h)
  
  write.table(round(u,2), file=reliabfile)
  write.table(round(out,2),file=graphvaluefile)
}
