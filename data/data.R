#' Calibration data for SABRFunctions package
#'
#' Bloomberg implied volatility smile data by strike from May 23, 2022
#'
#'@format A data frame with 56 rows of 3 variables:
#' \describe{
#'    \item{Point}{Name of forward rate, used for filtering}
#'    \item{Strike}{Strike rate of various options traded in the market}
#'    \item{BlackVol}{Implied lognormal volatility of option traded at that strike}
#'  }
#'
#' @source {Created using Bloomberg BVOL data from May 23, 2022}
#'
#' @examples data('sabrcalibdata')  ###Lazy loading
"sabrcalibdata"

#' Results of calibration runs for SABRFunctions package
#'
#' Consolidated market volatilities, ATM SABR Black-76 vols, and Full SABR Black-76 vols, organised
#' by Strike and Method for easy subsetting and filtering.
#'
#'@format A data frame with 168 rows of 4 variables:
#' \describe{
#'    \item{Point}{Name of forward rate, used for filtering}
#'    \item{Method}{Factor detailing what the data actually is - market quote, ATM SABR, Full SABR}
#'    \item{Strike}{Strike rate of various options traded in the market}
#'    \item{Value}{Implied lognormal volatility of option traded at that strike}
#'  }
#'
#' @source {Results from calibration runs from June 6, 2022}
#'
#' @examples data('sabrfitteddata')  ###Lazy loading
"sabrfitteddata"

#' Curve data for SABRFunctions package
#'
#' Bloomberg SOFR swap and zero curve from May 23, 2022
#'
#'@format A data frame in tidy format which contains 66 rows of 3 variables
#' \describe{
#'    \item{Term}{Swap rate maturity in years, e.g. 0.25 means 3M, 1 means 1Y, etc.}
#'    \item{Type}{Text string that tells you whether you are looking at a SOFR (swap) or ZERO (discount) rate}
#'    \item{Value}{Actual value of the corresponding swap or zero rate for the given tenor point}
#' }
#'
#'@source {Created using Bloomberg YCRV function from May 23, 2022}
#'
#'@examples
#'library(ggplot2)
#'data('curves')
#'ggplot(data = curves, aes(x = Term, y = Value, colour = Type)) +
#' geom_line() +
#' geom_point() +
#' labs(x = 'Term (Years)', y = 'Rate (%)',
#'       title = 'USD SOFR Swap and Zero Curves',
#'       subtitle = 'Fixed 30/360 vs SOFR Rates as of May 23 2022',
#'       caption = '(Source: Bloomberg)',
#'       colour = 'Rate Type')
"curves"

#' Historical Rate and Lognormal Vol Data for Beta Estimation
#'
#' Bloomberg swap forward rate and Black-76 implied volatility from May 23, 2022. Used for
#' vignette only.
#'
#' @format A data frame with 36 observations of 4 variables
#'  \describe{
#'    \item{Rate}{Text label describing the particular forward rate, e.g. "3M10Y"}
#'    \item{Forward}{Numerical vector of actual forward rate values}
#'    \item{Date}{Observation date of the forward rate. Only for information.}
#'    \item{BlackVol}{Lognormal ATM implied volatility corresponding to forward rate}
#'  }
#'
#' @source {Created using Bloomberg SWPM - OV pricing function from May 23, 2022}
#'
#' @examples
#' data('histratevoldata')
#' str(histratevoldata)
"histratevoldata"
