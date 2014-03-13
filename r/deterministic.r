deterministic <- function(data, detfile) {
  # Computes correlation, RMSE and MAE for an ensemble forecast
  #  
  # Usage: deterministic(data,detfile)
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
  #    detfile: string of charaters with the name of the file where
  #             the correlation, RMSE and MAE values will be written 
  #  
  # Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
  
  data[data == -999.9] <- NA

  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts
  ensmean <-apply(y,1,mean,na.rm=TRUE)
  corr <- cor(x,ensmean,use="pairwise.complete.obs")
  rmse <- sqrt(mean((ensmean-x)^2,na.rm=TRUE))
  mae <- mean(abs(ensmean-x),na.rm=TRUE)
  out <- c(corr,rmse,mae)
  write.table(out, file=detfile)
  list(out=out)
} 
