brierscore <- function(x, y, u) {
  # Computes the Brier score for an ensemble forecast
  #
  # Arguments:
  #
  #    x: vector of observations
  #    y: matrix of ensemble forecasts (1st dimension equals length(x))
  #    u: threshold below which observed and forecast event occurs
  bs<-mean((apply(y <= u, 1, mean) - (x <= u))^2)
  list(bs=bs)
} 
