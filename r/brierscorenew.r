brierscorenew <- function(data, u, bsfile) {
  # Computes the Brier score for an ensemble forecast
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
  #    u: threshold below which observed and forecast event occurs
  #    bsfile: string of charaters with the name of the file where
  #            the Brier score will be written 
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts
  bs <- mean((apply(y <= u, 1, mean) - (x <= u))^2) 
  
  probfcsts <- apply(y <= u, 1, mean)                             #temp
  binobs <- (x <= u)                                              #temp3
  obar <- mean(binobs)
  n<-length(probfcsts)                                            #n
  h<-hist(probfcsts,breaks=seq(0,1,0.001),plot=F)$counts            #temp1
  g<-hist(probfcsts[binobs==1],breaks=seq(0,1,0.001),plot=F)$counts #temp2
  obari <- g/h                                                    #obar
  obari[is.na(obari)]<-0
  # Computes reliability,resolution and uncertainty components
  # of the Brier score 
  yi <- seq(0.0005,1,0.001)
  reliab <- sum(h*((yi-obari)^2))/n
  resol <- sum(h*((obari-obar)^2))/n
  uncert<-obar*(1-obar)
  bsnew<-reliab-resol+uncert
  out <- c(bsnew,reliab,resol,uncert)  
  write.table(round(out,2), file=bsfile)
  list(bs=bs,reliab=reliab,resol=resol,uncert=uncert,bsnew=bsnew)
} 
