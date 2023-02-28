"""
#' SABR First-Order Risk Against Correlation Changes
"""

# pylint:disable=invalid-name, line-too-long

from SABRtoBlack76 import SABRtoBlack76
from SABRtoBlack76 import SABRtoBlack76
from SABRParamLinearBump import SABRParamLinearBump
from Black76Vega import Black76Vega

def SABRVanna(F0, K, tex, rfr, Alpha, Beta, Rho, Nu):
    """
    #' Calculates the first-order risk with respect to changes in the correlation parameter, using a
    #' mixture of analytical and numerical estimation methods. Assumes that all parameters provided are
    #'  ALREADY CALIBRATED, i.e. does not attempt to run any calibrations first. Using the calibrated
    #'  parameters, first calculates the Black-76-equivalent volatility, then calculates the Vega risk of the option
    #'  given the input parameters using the analytical form for Black-76 Vega, and finally calculates the adjustment
    #'  required for the bump of SABR Rho.
    #'
    #' @param F0 Current forward rate
    #' @param K Strike rate of the option
    #' @param tex Time ot expiry of the option, measured in years
    #' @param rfr Riskless rate, best taken as either the 10y or 30y government zero rate
    #' @param Alpha Diffusion parameter in the SABR scheme, calibrated as a result of using one of two methods
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data, OR preset by user
    #' @param Rho Correlation between SABR forward and diffusion processes
    #' @param Nu Vol-of-vol parameter for SABR diffusion process
    #'
    #' @return First-order risk against changes in the Rho (correlation) parameter
    #' @export
    #'
    #' @examples SABRVanna(F0 = 0.0266, K = 0.0250, tex = 0.25, rfr = 0.02, Alpha = 0.0651, Beta = 0.5,
    #' Rho = -0.0356, Nu = 1.0504)
    """

    #Calculate Black-76-equivalent volatility for provided inputs:
    SABRImpVol = SABRtoBlack76(F0, K, tex, Alpha, Beta, Rho, Nu)

    #Calculate Black-76 Vega:
    Black76VegaPart = Black76Vega(F0, K, SABRImpVol, tex, rfr)

    #Calculate the numerical correction term:
    SABRBumpRhoUp = SABRParamLinearBump(F0, K, tex, Alpha, Beta, Rho, Nu, 'Rho', bumpdir = 'up')
    SABRBumpRhoDn = SABRParamLinearBump(F0, K, tex, Alpha, Beta, Rho, Nu, 'Rho', bumpdir = 'dn')

    #Calculate CENTRAL DIFFERENCE for predicted change:
    SABRCorrectionFactor = (SABRBumpRhoUp - SABRBumpRhoDn) / 0.0001 #0.5bp up+ 0.5bp dn = 1bp total bump

    #Calculate final value:
    FinalVanna = Black76VegaPart * SABRCorrectionFactor

    return FinalVanna
