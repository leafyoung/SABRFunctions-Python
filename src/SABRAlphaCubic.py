"""
#' SABR Alpha Cubic Form for ATM Vols
"""

# pylint:disable=invalid-name, line-too-long

def SABRAlphaCubic(x, F0, ATMVol, tex, Beta, Rho, Nu):
    """
    #' Anonymous function to calculate the SABR Alpha given market inputs, used in calibration processes
    #'
    #' @param x The current value of SABR Alpha
    #' @param F0 Current value of forward rate
    #' @param ATMVol Current value of ATM market volatility corresponding to F0
    #' @param tex Time to expiry of the option, in years
    #' @param Beta Calibrated (or user-selected) Beta parameter defining shape of the forward curve
    #' @param Rho Calibrated correlation coefficient between forward and volatility Wiener processes
    #' @param Nu Calibrated vol-of-vol for stochastic volatility process
    #'
    #' @return Single numeric value corresponding to the ATM Black-76-equivalent volatility for the given Alpha
    #'
    #' @export
    #'
    #' @examples
    #' ### Simple example involving a 3M option on the 10Y swap rate with 50% Beta assumed
    #' SABRAlphaCubic(x = 0.0651, F0 = 0.0266, ATMVol = 0.4084, tex = 0.25, Beta = 0.5, Rho = -0.0356,
    #'  Nu = 1.0504)
    """

    A3 = (((1 - Beta) ** 2 ) * tex) / (24 * F0 ** (2 - 2 * Beta))
    A2 = (Rho * Nu * Beta * tex) / (4 * F0 ** (1 - Beta))
    A1 = 1 + (2 - 3 * Rho ** 2) / 24 * Nu ** 2 * tex
    A0 = -ATMVol * F0 ** (1 - Beta)
    return A3 * x ** 3 + A2 * x ** 2 + A1 * x + A0
