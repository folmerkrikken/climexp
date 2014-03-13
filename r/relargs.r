#data<-read.table("/usr/people/caio/public_html/climexp/data/iens_cfs_prcp_jan_-1.2E_51.7N_i_++15102.table",header=T)
#source("relargs.r")
#a<-relargs(data,50)
#reliability.plot(seq(0,1,0.1),a$y,a$probs,a$obar)

#b<-hist(a$probs,breaks=seq(0,1,0.1))

#b$counts

#reliability.plot(seq(0,1,0.1),a$y,b$counts,a$obar)


relargs <- function(data, u) {
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
  
  library(verification)
  
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts
  probs <- apply(y <= u, 1, mean)
  binobs <- (x <= u)
  obar <- mean(binobs)
  

  h<-hist(probs,breaks=seq(0,1,0.1))

  
  index <- (1:dim(data)[1])[probs == 0 & probs <= 0.1]
  
  #y[[1]]<-sum(binobs[index])/length(index)
  y<-sum(binobs[index])/length(index)
  y[is.na(y)]<-0
  
  yy<-NULL
  j<- 0.1 
  for(i in 1:9) {
  index <- (1:dim(data)[1])[probs > j & probs <= j+0.1]
  yy[[i]]<-sum(binobs[index])/length(index)
  j<-j+0.1
  }
  yy[is.na(yy)]<-0
   
  yyy<-c(y,yy)    
  
  #reliability.plot(h$breaks,yyy,h$counts)
  
  reliability.plot(h$mids,yyy,h$counts)
  #attribute(h$mids,yyy,h$counts,obar)
  # roc.plot(binobs,probs)
   ra<-roc.area(binobs,probs)$A.tild
  
  #bs <- mean((apply(y <= u, 1, mean) - (x <= u))^2) 
  #write.table(round(bs,2), file=bsfile)
  list(probs=probs,binobs=binobs,yyy=yyy,obar=obar,ra=ra)
} 
