"""
#' Convert from SABR to Black-76 Volatility
"""

# pylint:disable=invalid-name, line-too-long

import numpy as np

def SABRtoBlack76(F0, K, tex, Alpha, Beta, Rho, Nu):
    """
    #' Returns the Black-76 EQUIVALENT volatility after calibrating for SABR Alpha, Beta, Rho, and Nu, using the formulation found in
    #' Eqn 2.17 of 'Managing Smile Risk' by Hagan et al, 2002. Base function for all other calibrations
    #'
    #' @param F0 Current forward rate
    #' @param K Strike rate of the option
    #' @param tex Time ot expiry of the option, measured in years
    #' @param Alpha Diffusion parameter in the SABR scheme, calibrated as a result of using one of two methods
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data, OR preset by user
    #' @param Rho Correlation between SABR forward and diffusion processes
    #' @param Nu Vol-of-vol parameter for SABR diffusion process
    #'
    #' @return Black-76-equivalent volatility that can then be plugged into usual Black-76 closed-form option price
    #' @export
    #'
    #' @examples
    #' ### Example for ITM option
    #' SABRtoBlack76(F0 = 0.0266, K = 0.0250, tex = 0.25, Alpha = 0.0651, Beta = 0.5, Rho = -0.0356,
    #'  Nu = 1.0504)
    #'
    #' @examples
    #' ### Example for ATM option
    #' SABRtoBlack76(F0 = 0.0266, K = 0.0266, tex = 0.25, Alpha = 0.0651, Beta = 0.5, Rho = -0.0356,
    #'  Nu = 1.0504)
    """

    #Setup a series of coefficients that will then be multiplied together:
    k1 = (F0 * K) ** ((1 - Beta) / 2)
    k2 = 1 + (1 - Beta)**2 / 24 * (np.log(F0 / K)) **2 + (1 - Beta)**4 / 1920 * np.log(F0 / K) ** 4
    z = Nu / Alpha * (F0 * K) ** ((1 - Beta) / 2) * np.log(F0 / K)
    xz = np.log((np.sqrt(1 - 2 * Rho * z + z **2) + z - Rho) / (1 - Rho))
    k3 = (1 - Beta) **2 / 24 * Alpha **2 / ((F0 * K) ** ( 1 - Beta))
    k4 = 1 / 4 * Rho * Beta * Nu * Alpha / (((F0 * K) ** ((1 - Beta) / 2)))
    k5 = (2 - 3 * Rho ** 2) / 24 * Nu ** 2

    if F0 != K:
        try:
            return (Alpha / (k1 * k2)) * (z / xz) * (1 + tex *(k3 + k4 + k5))
        except:
            breakpoint()
            raise

    return (Alpha / (k1 * k2) * 1 * (1 + tex *(k3 + k4 + k5)))
