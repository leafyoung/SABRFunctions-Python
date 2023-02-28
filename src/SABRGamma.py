"""
#' SABR Second-Order Risk with Backbone Correction
"""

# pylint:disable=invalid-name, line-too-long

from SABRtoBlack76 import SABRtoBlack76
from Black76Gamma import Black76Gamma
from Black76Vega import Black76Vega
from SABRParamLinearBump import SABRParamLinearBump

import numpy as np
import scipy.stats as ss


def SABRGamma(F0, K, tex, rfr, Alpha, Beta, Rho, Nu):
    """
    #' Calculates the second-order risk due to changes in the value of the underlying forward rate
    #' using a mixture of analytical and numerical estimation methods. Assumes that all parameters
    #' provided are ALREADY CALIBRATED, i.e. does not attempt to run any calibrations first. Using
    #' the calibrated parameters, first calculates the Black-76-equivalent volatility, then calculates
    #' the Delta risk of the option given the input parameters using the analytical forms for Black-76
    #' Delta and Vega.
    #'
    #' @param F0 Current forward price
    #' @param K Strike of the option
    #' @param tex Time to expiry, expressed in years, of the option
    #' @param rfr Riskless rate, best taken as either the 10y or 30y government zero rate
    #' @param Alpha Diffusion parameter in SABR scheme, calibrated as a result of using one of two methods
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data OR preset by user
    #' @param Rho Correlation between SABR forward and diffusion processes
    #' @param Nu Vol-of-vol for SABR diffusion process
    #'
    #' @return Corrected second-order risk against changes in the underlying forward rate
    #' @export
    #'
    #' @examples SABRGamma(F0 = 0.0266, K = 0.0250, tex = 0.25, rfr = 0.02, Alpha = 0.0651, Beta = 0.5,
    #' Rho = -0.0356, Nu = 1.0504)
    """

    #Calculate Black-76-equivalent volatility for provided inputs:
    SABRImpVol = SABRtoBlack76(F0, K, tex, Alpha, Beta, Rho, Nu)

    #Calculate the usual d1 term - we'll need this later:
    d1 = (np.log(F0 / K) + 0.5 * SABRImpVol ** 2  * tex) / (SABRImpVol * np.sqrt(tex))

    #Calculate Black-76 Gamma:
    Black76GammaPart = Black76Gamma(F0, K, SABRImpVol, tex, rfr)

    #Calculate Black-76 Vega:
    Black76VegaPart = Black76Vega(F0, K, SABRImpVol, tex, rfr)

    ##Now calculate the various bumps to figure out the multipliers for the Gamma equation
    #Upward bump:
    SABRBumpForwardUp = SABRParamLinearBump(F0, K, tex, Alpha, Beta, Rho, Nu, 'F0', bumpdir = 'up')
    #Downward bump:
    SABRBumpForwardDn = SABRParamLinearBump(F0, K, tex, Alpha, Beta, Rho, Nu, 'F0', bumpdir = 'dn')

    #Calculate first-order central-differences bump:
    Black76FirstOrderChange = (SABRBumpForwardUp - SABRBumpForwardDn) / 0.0001 #0.5bp up + 0.5bp dn = 1bp total bump

    #Calculate second-order central-differences bump:
    Black76SecondOrderChange = (SABRBumpForwardUp - 2 * SABRImpVol + SABRBumpForwardDn) / (0.0001) ** 2 #1bp bump squared for 2nd-order bump

    #Calculate final correction term:
    CorrectionTerm = np.exp(-rfr * tex) * ss.norm.pdf(d1) - K * np.exp(-rfr * tex) * ss.norm.pdf(d1)

    #Put it all together to calculate Gamma:
    FinalGamma = Black76GammaPart + Black76VegaPart * Black76SecondOrderChange + Black76FirstOrderChange * CorrectionTerm

    return FinalGamma
