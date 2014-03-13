brierscore <- function(data, u) {
  # Computes the Brier score for an ensemble forecast
  #
  # Arguments:
  #    data: a table with the following structure
             first  column = year
	     second column = month
	     third  column = observation
	     forth  column = ensemble member 1
	     fith   column = ensemble member 2
	     .
	     .
	     .
	     last   column = ensemble member k
  #    u: threshold below which observed and forecast event occurs
  x <- data[,3] # extracts observation column
  y <- data[,4:(dim(data)[2]-3)] # extracts ensemble forecasts
  bs <- mean((apply(y <= u, 1, mean) - (x <= u))^2)
  list(bs=bs)
} 
