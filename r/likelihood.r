likelihood<- function(table,xlab,ylab){  
  # Plot likelihood function for an ensemble forecast (regression of
  # ensemble forecasts on observations)
  #
  # Usage: likelihood(tale,xlab,ylab)
  #
  # Arguments:
  #    table: a table with the following structure
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
  #    xlab: String with the label to be displayed in the x axis
  #
  #    ylab: String with the label to be displayed in the y axis
  #  
  # Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>

    	table[table == -999.9] <- NA

	dims <- dim(table)
	n <- dims[1]
	ncol <- dims[2]

        year <- table[,1]
	nmember <- ncol-3
        obs <- table[,3]

        index <- order(obs)

	yearord <- year[index]
        obsord <- sort(obs)

	ensmean<-apply(table[,4:ncol],1,mean,na.rm=TRUE)
        ensvar<-apply(table[,4:ncol],1,var,na.rm=TRUE)
	ensmeanord <- ensmean[index]
	ensvarord <- ensvar[index]

	tableord <- table[index,4:ncol]
	
	lims<-range(as.vector(tableord),na.rm=TRUE)
        minimum<-lims[1]
	maximum<-lims[2]

	par(mar = c(7., 7., 3, 2.1))
	plot(obsord, ensmeanord, xlab = xlab, ylab
		 = ylab, ylim = c(minimum,
		maximum), type = "n", cex = 1.5)
	
	#if (n >= 100) ensmeanpointsize=1
	#else ensmeanpointsize=1.5
	
	ensmeanpointsize=1.5
		
	points(obsord, ensmeanord, cex = ensmeanpointsize, pch = "O")
	lines(obsord, obsord,lty=2,lwd=2)
	
	regr <- lsfit(obs, ensmean)
	intercept <- regr$coef[1]
	slope <- regr$coef[2]
	abline(intercept, slope, type = "b", lwd = 2)
	rsquared <- summary(lm(ensmean ~ obs))$r.squared

        corr <- cor(ensmean,obs,use="pairwise.complete.obs")
	rmse <- sqrt(mean((ensmean-obs)^2,na.rm=TRUE))
	
	
	mtext(paste("Correlation =",as.character(round(corr,2)),"RMSE =",as.character(round(rmse,2)),sep=" "),3)
        

	#if (n >= 100) pointsize=0.2
	#else pointsize=0.6

        pointsize=0.6

	#for (i in 1:n){
        #.Fortran("rkeepalive",i=as.integer(i),n=as.integer(n))
        #points(rep(obsord[i], nmember), tableord[i,], cex = pointsize ,pch = 16)
	#}
	points(rep(obsord,times=nmember),c(as.matrix(tableord)), cex = pointsize ,pch = 16)
	list(slope=slope, intercept=intercept, rsquared=rsquared,nmember=nmember)
}

