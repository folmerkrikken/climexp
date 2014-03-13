brierscore <- function(data, u, threshold = TRUE, nbins = 10, bsfile) {
  # Computes the Brier score and its decomposition for an ensemble forecast
  #
  # Usage: brierscore(data, u, threshold, nbins, bsfile)
  #
  # Arguments:
  #    data: a table with the following structure
  #          first  column = year
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
  #    threshold: Logical. If TRUE uses the value u as threshold, if
  #               FALSE u should have the value of the quantile to be computed
  #               (e.g. 50 for the median, 90 for the 90th quantile, etc...)
  #
  #    nbins: number of bins used to compute the Brier score
  #
  #    bsfile: the name of the file where the value of Brier score,
  #            its reliability, resoultion and uncertainty components
  #            will be written 
  #  
  # Author: Camiel Severijns <c.severijns@knmi.nl>
 
    require(parallel)


    data[data == -999.9] <- NA
    observations <- data[,3]
    ensemble     <- data[,4:ncol(data)]

    if (!threshold) u <- quantile(observations,u/100.0,na.rm=TRUE)

    # remove missing data
    ok <- !is.na(observations) & apply(ensemble, 1, function(y) any(!is.na(y)))
    observations <- observations[ok]
    ensemble <- ensemble[ok,]

    p <- ( ensemble <= u )
    p <- apply(p,1:2,mean)
    y <- ( observations <= u )

    #terms <- SpecsVerification::BrierScoreDecomposition(
    #    p=p,y=y,calibration=list(method="bin",bins=((0:nbins)/nbins)) )
    child <- mcparallel( SpecsVerification::BrierScoreDecomposition(
        p=p,y=y,calibration=list(method="bin",bins=((0:nbins)/nbins)) ) )
    i <- 0
    n <- 100
    repeat {
        result <- mccollect(child,wait=FALSE,timeout=10)
        if (length(result) > 0) break
        i <- i + 1
        .Fortran("rkeepalive",i=as.integer(i),n=as.integer(n))
    }
    terms <- result[[1]]
  
    bs  <- sum(terms)
    rel <- terms[1]
    res <- terms[2]
    unc <- terms[3]

    write(paste("Brier score",bs ,sep="="),bsfile,1,append=FALSE)
    write(paste("Reliability",rel,sep="="),bsfile,1,append=TRUE)
    write(paste("Resolution ",res,sep="="),bsfile,1,append=TRUE)
    write(paste("Uncertainty",unc,sep="="),bsfile,1,append=TRUE)

    c(bs=bs,rel=rel,res=res,unc=unc)
}
