rocrclim <- function(data, u, threshold = TRUE, rocfile,maintitle="") {
   # Computes the Brier score for an ensemble forecast
   #
   # Usage: rocrclim(data, u, threshold, rocfile, maintitle)
   #
   # Arguments:
   #    data: a table with the following structure
   #           first  column = year
   #         second column = month
   #         third  column = observation
   #         forth  column = ensemble member 1
   #         fith   column = ensemble member 2
   #         .
   #         .
   #         .
   #         last   column = ensemble member k
   #
   #    u: threshold value or quantile (e.g. u=50 for the 0.5 quantile,
   #       i.e. the median of the observations) that defined the event of
   #       interest to be forecast
   #
   #    threshold: Logical. If TRUE (Default) uses the value u as threshold, if
   #               FALSE u should have the value of the quantile to be computed
   #
   #    rocfile: string of charaters with the name of the file where
   #            the ROC area value and the threshold u will be written
   #
   #    maintitle: String containing the text for the ROC diagram title
   #
   # Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>

   library(verification)

   x <- data[,3] # extracts observation column
   x[x==-999.9]<-NA
   y <- data[,4:(dim(data)[2])] # extracts ensemble forecasts
   y[y==-999.9]<-NA

   if(threshold) u<- u
   else u<-quantile(x,u/100,na.rm=T)

   probfcsts <- apply(y <= u, 1, mean,na.rm=T)
   binobs <- (x <= u)

   index <- !(is.na(probfcsts) | is.na(binobs))

   roc.plot(binobs[index],probfcsts[index],main=maintitle)
   ra<-roc.area(binobs[index],probfcsts[index])$A.tild
   out<-c(ra,u)
   write.table(round(out,2), file=rocfile)

   list(ra=ra,u=u)
}

