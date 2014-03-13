rps <- function(data, rpsfile) {
  # Computes the Ranked probability score for tercile categories
  # for an ensemble forecast
  #
  # Usage: rps(data, rpsfile)
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
  #    rpsfile:  string of charaters with the name of the file where
  #              the value of the Ranked probaility score will be written 
  #  
  # Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>

  data[data == -999.9] <- NA
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts

  u1<- quantile(x,p=1/3,na.rm=TRUE)
  u2<- quantile(x,p=2/3,na.rm=TRUE)
   
  bs1 <- mean((apply(y <= u1, 1, mean,na.rm=TRUE) - (x <= u1))^2,na.rm=TRUE) 
  bs2 <- mean((apply(y <= u2, 1, mean,na.rm=TRUE) - (x <= u2))^2,na.rm=TRUE) 

  rps <- bs1+bs2

  write.table(round(rps,3), file=rpsfile)
  list(rps)
} 
