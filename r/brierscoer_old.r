brierscore <- function(data, u, threshold = TRUE, size = 0, bsfile) {
  # Computes the Brier score and its decomposition for an ensemble forecast
  #
  # Usage: brierscore(data, u, threshold, bsfile)
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
  #    threshold: Logical. If TRUE (Default) uses the value u as threshold, if
  #               FALSE u should have the value of the quantile to be computed
  #               (e.g. 50 for the median, 90 for the 90th quantile, etc...)
  #
  #    bsfile: string of charaters with the name of the file where
  #            the value of Brier score, its reliability, resoultion and
  #            uncertainty components and the threshold u will be written 
  #  
  # Author: Chris Ferro <c.a.t.ferro@reading.ac.uk>
 
  # Notes: can use `format' for pretty printing

  source("r/brier_chris.r")
  # set default arguments
  above <- FALSE
  con <- TRUE
  unc <- TRUE
  cover <- 0.95
  boot <- 1000
  simul <- FALSE
  # format data
  data[data == -999.9] <- NA
  x <- data[, 3]            # observations
  y <- data[, 4:ncol(data)] # ensemble forecasts
  # threshold
  if(!threshold)
    u <- quantile(x, u / 100, na.rm = TRUE)
  # ensemble size
  m <- ncol(y)
  if(size == 0)
    size <- m
  # remove missing data
  ok <- !is.na(x) & apply(y, 1, function(y) any(!is.na(y)))
  x <- x[ok]
  y <- y[ok, ]
  # compute Brier score and uncertainty
  temp <- brier.score(rbind(x, t(y)),, u, size, above, con, unc, cover, boot, simul)
  # store output
  bs <- round(temp$scores[1, 1], 3)
  rel <- round(temp$reliability[1], 3)
  res <- round(temp$resolution[1], 3)
  uncer <- round(temp$uncertainty[1], 3)
  # conditional uncertanity
  if(con) {
    ese.con <- round(temp$con$std.err[1, 1], 3)
    if(!is.null(cover)) {
      lo.con <- round(temp$con$point$lower[1, 1], 3)
      up.con <- round(temp$con$point$upper[1, 1], 3)
      Lcon <- paste("Conditional std error   = ", ese.con, ", ", 100*cover, "% CI = (", lo.con, ", ", up.con, ")", sep = "")
    } else {
      Lcon <- paste("Conditional std error   = ", ese.con, sep = "")
    }
  }
  # unconditional uncertainty
  if(unc) {
    ese.unc <- round(temp$unc$std.err[1, 1], 3)
    if(!is.null(cover)) {
      lo.unc <- round(temp$unc$point$lower[1, 1], 3)
      up.unc <- round(temp$unc$point$upper[1, 1], 3)
      Lunc <- paste("Unconditional std error = ", ese.unc, ", ", 100*cover, "% CI = (", lo.unc, ", ", up.unc, ")", sep = "")
    } else {
      Lunc <- paste("Unconditional std error = ", ese.unc, sep = "")
    }
  }
  # output text
  Lth <- paste("Threshold   = ", round(u, 3), sep = "")
  Lbs <- paste("Brier score = ", bs, sep = "")
  Lrel <- paste("Reliability = ", round(rel, 3), sep = "")
  Lres <- paste("Resolution  = ", round(res, 3), sep = "")
  Lcer <- paste("Uncertainty = ", round(uncer, 3), sep = "")
  # write to file
  write(Lth, bsfile, 1, append = FALSE)
  write(Lbs, bsfile, 1, append = TRUE)
  write("", bsfile, 1, append = TRUE)
  write(Lrel, bsfile, 1, append = TRUE)
  write(Lres, bsfile, 1, append = TRUE)
  write(Lcer, bsfile, 1, append = TRUE)
  write("", bsfile, 1, append = TRUE)
  if(con) write(Lcon, bsfile, 1, append = TRUE)
  if(unc) write(Lunc, bsfile, 1, append = TRUE)
  # finished
  c(bs = bs, rel = rel, res = res, uncer = uncer)
} 
