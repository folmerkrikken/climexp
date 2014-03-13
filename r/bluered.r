
# Generate a Colour Scale for Plotting
#
# Description:
#
#      Returns a colour scale corresponding to specified data values.
#
# Usage:
#
#      bluered(data, scale = "equal", white = median(data), yellow = 0,
#          cyan = 0, invert = FALSE, format = "hex")
#
# Arguments:
#
#   data: A vector of distinct data values corresponding to the colours.
#
#  scale: Controls the colour gradients (see Details). Must be either
#         `"equal"' (the default), `"linear"' or `"split"' (or any
#         unique partial match).
#
#  white: The data value corresponding to the colour white.
#
# yellow: A number between 0 and 1 indicating the amount of yellow to
#         insert between white and red. If 0 (the default) then no yellow
#         is used. Larger values indicate more yellow.
#
#   cyan: A number between 0 and 1 indicating the amount of cyan to
#         insert between white and blue. If 0 (the default) then no cyan
#         is used. Larger values indicate more cyan. Not implemented.
#
# invert: Logical: if `TRUE', negative data values are red and positive
#         values are blue; if `FALSE' (the default) then vice-versa.
#
# format: The format in which the colours are returned (see Value). Must
#         be either `"hex"' (the default) or `"rgb"' (or any unique
#         partial match).
#
# Details:
#
#      One colour is created for each value in `data'. Colours range from
#      blue for data values less than `white' to red for data values
#      greater than `white'. If `scale' equals `"linear"' then colour
#      intensity scales linearly with absolute data value: highest
#      intensity corresponding to the maximum absolute value of `data'.
#      If `scale' equals `"split"' then linear intensity scales are
#      constructed separately for blue and red colours so that the
#      maximum intensity is attained by both blue and red. If `scale'
#      equals `"equal"' then intensities are equally spaced regardless of
#      the data values.
#
# Value:
#
#      If `format' is `"hex"' then returns a character vector of
#      hexadecimal RGB numbers. If `format' is `"rgb"' then returns a
#      matrix with three columns containing RGB intensities.
#
# See Also:
#
#      `col2rgb', `colours', `rgb'
#
# Author:
#
#      Chris Ferro <c.a.t.ferro@reading.ac.uk> 4 May 2005
#
# Examples:
#
#      image(volcano, col = bluered(seq(100, 200, 10), "linear"))

bluered <- function(data, scale = c("equal", "linear", "split"), white = median(data), yellow = 0, cyan = 0, invert = FALSE, format = c("hex", "rgb")) {
  scale <- match.arg(scale)
  format <- match.arg(format)
  data <- unique(data) - white
  if(invert) data <- -data
  data <- sort(data)
  nb <- sum(data < 0)
  nr <- sum(data > 0)
  n <- length(data)
  if(scale == "equal") {
    if(nb == 0) r <- rep(1, n)
    else r <- pmin(1:n - 1, nb) / nb
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(n - 1:n, nr) / nr
  } else if(scale == "linear") {
    dmax <- max(abs(data))
    if(nb == 0) r <- rep(1, n)
    else r <- pmin(data + dmax, dmax) / dmax
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(dmax - data, dmax) / dmax
  } else {
    if(nb == 0) r <- rep(1, n)
    else r <- pmax(data[1] - data, data[1]) / data[1]
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(data[n] - data, data[n]) / data[n]
  }
  g <- pmin(r, b)
  y <- min(max(yellow, 0), 1)
  g[b < 1] <- 1 - (1 - y) * (1 - b[b < 1]) - y * (1 - b[b < 1])^2
  b <- 1 - (1 + y) * (1 - b) + y * (1 - b)^2
#  c <- min(max(cyan, 0), 1)
#  g[r < 1] <- 1 - (1 - c) * (1 - r[r < 1]) - c * (1 - r[r < 1])^2
#  r <- 1 - (1 + c) * (1 - r) + c * (1 - r)^2
  if(invert) {
    r <- rev(r)
    g <- rev(g)
    b <- rev(b)
  }
  if(format == "hex") return(rgb(r, g, b))
  cbind(r, g, b)
}


bluered.old <- function(data, scale = c("equal", "linear", "split"), white = median(data), yellow = 0, green = 0, invert = FALSE, format = c("hex", "rgb")) {
  scale <- match.arg(scale)
  format <- match.arg(format)
  data <- unique(data)
  data <- data - white
  if(invert) data <- -data
  data <- sort(data)
  nb <- sum(data < 0)
  nr <- sum(data > 0)
  n <- length(data)
  if(scale == "equal") {
    if(nb == 0) r <- rep(1, n)
    else r <- pmin(1:n - 1, nb) / nb
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(n - 1:n, nr) / nr
  } else if(scale == "linear") {
    dmax <- max(abs(data))
    if(nb == 0) r <- rep(1, n)
    else r <- pmin(data + dmax, dmax) / dmax
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(dmax - data, dmax) / dmax
  } else {
    if(nb == 0) r <- rep(1, n)
    else r <- pmax(data[1] - data, data[1]) / data[1]
    if(nr == 0) b <- rep(1, n)
    else b <- pmin(data[n] - data, data[n]) / data[n]
  }
  g <- pmin(r, (1 + max(yellow, 0)) * b)
  if(invert) {
    r <- rev(r)
    g <- rev(g)
    b <- rev(b)
  }
  if(format == "hex") return(rgb(r, g, b))
  cbind(r, g, b)
}


bluered.older <- function(data, scale = c("equal", "linear", "split"), white = median(data), yellow = FALSE, green = FALSE, invert = FALSE, format = c("hex", "rgb")) {
  scale <- match.arg(scale)
  format <- match.arg(format)
  data <- unique(data)
  data <- data - white
  if(invert) data <- -data
  data <- sort(data)
  nb <- sum(data < 0)
  nw <- sum(data == 0)
  nr <- sum(data > 0)
  ny <- floor(nr / 2)
  n <- length(data)
  if(scale == "equal") {
    if(nb == 0) {
      r <- c(rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c(rep(1, nw + ny), ((nr - ny - 1):0) / (nr - ny))
      else
        g <- c(rep(1, nw), ((nr-1):0) / nr)
      b <- c(rep(1, nw), ((nr-1):0) / nr)
    } else if(nr == 0) {
      r <- c((0:(nb-1)) / nb, rep(1, nw))
      g <- c((0:(nb-1)) / nb, rep(1, nw))
      b <- c(rep(1, nb), rep(1, nw))
    } else {
      r <- c((0:(nb-1)) / nb, rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c((0:(nb-1)) / nb, rep(1, nw + ny), ((nr - ny - 1):0) /(nr - ny))
      else
        g <- c((0:(nb-1)) / nb, rep(1, nw), ((nr-1):0) / nr)
      b <- c(rep(1, nb), rep(1, nw), ((nr-1):0) / nr)
    }
  } else if(scale == "linear") {
    dmax <- max(abs(data))
    if(nb == 0) {
      r <- c(rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c(rep(1, nw + ny), 1 - (data[(n-nr+ny+1):n] - data[n-nr+ny]) / (dmax - data[n-nr+ny]))
      else
        g <- c(rep(1, nw), 1 - data[(n-nr+1):n] / dmax)
      b <- c(rep(1, nw), 1 - data[(n-nr+1):n] / dmax)
    } else if(nr == 0) {
      r <- c(1 + data[1:nb] / dmax, rep(1, nw))
      g <- c(1 + data[1:nb] / dmax, rep(1, nw))
      b <- c(rep(1, nb), rep(1, nw))
    } else {
      r <- c(1 + data[1:nb] / dmax, rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c(1 + data[1:nb] / dmax, rep(1, nw + ny), 1 - (data[(n-nr+ny+1):n] - data[n-nr+ny]) / (dmax - data[n-nr+ny]))
      else
        g <- c(1 + data[1:nb] / dmax, rep(1, nw), 1 - data[(n-nr+1):n] / dmax)
      b <- c(rep(1, nb), rep(1, nw), 1 - data[(n-nr+1):n] / dmax)
    }
  } else {
    if(nb == 0) {
      r <- c(rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c(rep(1, nw + ny), 1 - (data[(n-nr+ny+1):n] - data[n-nr+ny]) / (data[n] - data[n-nr+ny]))
      else
        g <- c(rep(1, nw), 1 - data[(n-nr+1):n] / data[n])
      b <- c(rep(1, nw), 1 - data[(n-nr+1):n] / data[n])
    } else if(nr == 0) {
      r <- c(1 - data[1:nb] / data[1], rep(1, nw))
      g <- c(1 - data[1:nb] / data[1], rep(1, nw))
      b <- c(rep(1, nb), rep(1, nw))
    } else {
      r <- c(1 - data[1:nb] / data[1], rep(1, nw), rep(1, nr))
      if(yellow)
        g <- c(1 - data[1:nb] / data[1], rep(1, nw + ny), 1 - (data[(n-nr+ny+1):n] - data[n-nr+ny]) / (data[n] - data[n-nr+ny]))
      else
        g <- c(1 - data[1:nb] / data[1], rep(1, nw), 1 - data[(n-nr+1):n] / data[n])
      b <- c(rep(1, nb), rep(1, nw), 1 - data[(n-nr+1):n] / data[n])
    }
  }
  if(format == "hex") {
    out <- rgb(r, g, b)
    if(invert)
      return(rev(out))
  } else {
    out <- cbind(r, g, b)
    if(invert)
      return(out[nrow(out):1, ])
  }
  out
}
