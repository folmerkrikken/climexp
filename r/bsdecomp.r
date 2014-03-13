#data<-read.table("/usr/people/caio/public_html/climexp/data/iens_cfs_prcp_jan_-1.2E_51.7N_i_++15102.table",header=T)
#source("relargs.r")
#a<-relargs(data,50)
#reliability.plot(seq(0,1,0.1),a$y,a$probs,a$obar)

#b<-hist(a$probs,breaks=seq(0,1,0.1))

#b$counts

#reliability.plot(seq(0,1,0.1),a$y,b$counts,a$obar)


bsdecomp <- function(data, u) {
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
  
  #library(verification)
  
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts
  
  bsall <- mean((apply(y <= u, 1, mean) - (x <= u))^2)
  
  probfcsts <- apply(y <= u, 1, mean)                             #temp
  
  binobs <- (x <= u)                                              #temp3
  
  obar <- mean(binobs)
  
  n<-length(probfcsts)                                            #n

  #h<-hist(probfcsts,breaks=seq(0,1,0.1),plot=F)$counts            #temp1
  #h<-hist(probfcsts,breaks=seq(0,1,0.000001),plot=F)$counts            #temp1
  h<-hist(probfcsts,breaks=seq(0,1,0.001),plot=F)$counts            #temp1


  #g<-hist(probfcsts[binobs==1],breaks=seq(0,1,0.1),plot=F)$counts #temp2
  #g<-hist(probfcsts[binobs==1],breaks=seq(0,1,0.000001),plot=F)$counts #temp2
  g<-hist(probfcsts[binobs==1],breaks=seq(0,1,0.001),plot=F)$counts #temp2
   
  obari <- g/h                                                    #obar
  obari[is.na(obari)]<-0
  
  # Computes reliability component of the Brier score 
  #yi <- 0.05
  #yi <- 0.0000005
  yi <- 0.0005
  
  #yinew <- seq(0.05,0.95,0.1)
  #yinew <- seq(0.0000005,1,0.000001)
  yinew <- seq(0.0005,1,0.001)
  
  reliabnew <- sum(h*((yinew-obari)^2))/n
  resolnew <- sum(h*((obari-obar)^2))/n
  
  reliabaux <-0

  #for (i in 1:10){
  #for (i in 1:1000000){
  for (i in 1:1000){
  reliabaux <- reliabaux+(h[i]*(yi-obari[i])^2)
  #yi <- yi+0.1
  #yi <- yi+0.000001
  yi <- yi+0.001
  }

  reliab <- reliabaux/n

  # Computes resolution component of the Brier score 

  resolaux <- 0

  #for (i in 1:10){
  #for (i in 1:1000000){
  for (i in 1:1000){
  resolaux <- resolaux+(h[i]*(obari[i]-obar)^2)
  }

  resol <- resolaux/n

  uncert<-obar*(1-obar)

  bs<-reliab-resol+uncert
  
  #library(verification)
  #reliability.plot(yinew,obari,h)
  #  roc.plot(binobs,probfcsts)
  # ra<-roc.area(binobs,probfcsts)$A.tild
 
 
list(bsall=bsall,obari=obari,bs=bs,reliab=reliab,reliabnew=reliabnew,resol=resol,resolnew=resolnew,uncert=uncert,yi=yi)
#list(bsall=bsall,bs=bs,reliab=reliab,reliabnew=reliabnew,resol=resol,resolnew=resolnew,uncert=uncert,yi=yi)

}  
#0.4875391
