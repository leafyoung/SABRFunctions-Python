"""
#' Full Calibration Wrapper Function for SABR Parameters
"""

# pylint:disable=invalid-name, line-too-long

import numpy as np

from SABRFullCalib import SABRFullCalib
from SABRtoBlack76 import SABRtoBlack76


def SABRVolsFromFullCalib(F0, Strikes, MarketVols, tex, Beta, guess_Alpha, guess_Rho, guess_Nu):
    """
    #' Runs the complete calibration against market volatilities and strikes by calling the FULL
    #' calibration method, SABRFULLCALIB.
    #'
    #' @param F0 Current forward rate
    #' @param Strikes VECTOR of strike prices
    #' @param MarketVols VECTOR of LOGNORMAL (i.e. Black-76) market-quoted implied volatilities
    #' @param tex Time to expiry of option, measured in years
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data OR preset by user
    #' @param guess_Alpha Initial user-defined guess of Alpha parameter, MUST be non-zero
    #' @param guess_Rho Initial user-defined guess of Rho value, MUST be bounded between -1 and 1
    #' @param guess_Nu Initial user-defined guess of Nu value, MUST be non-zero
    #'
    #' @return A list object containing each of the 4 calibrated parameters, plus a vector of
    #' the input strikes, and a vector of the calibrated Black-76-equivalent volatilities.
    #' @export
    #'
    #' @examples
    #' data(sabrcalibdata)
    #' calibrun = sabrcalibdata[sabrcalibdata$Point == '3M10Y',]
    #' SABRVolsFromFullCalib(F0 = 0.0266, Strikes = calibrun$Strike, MarketVols = calibrun$BlackVol,
    #' tex = 0.25, Beta = 0.5, guess_Alpha = 0.06, guess_Rho = 0.05, guess_Nu = 0.7)
    """

    #Step 1: Run the calibration for SABR Rho and Nu:
    #Extract Alpha, Rho, and Nu from the calibration process:
    Calib_Alpha, Calib_Rho, Calib_Nu  = SABRFullCalib(F0, Strikes, MarketVols, tex, Beta, guess_Alpha, guess_Rho, guess_Nu).x

    #Step 2: Calculate the calibrated SABR Black-76 equivalent vols:
    n = len(Strikes)
    Calib_SABRVols = np.zeros(n)

    for i in range(n):
        Calib_SABRVols[i] = SABRtoBlack76(F0, Strikes[i], tex, Calib_Alpha, Beta, Calib_Rho, Calib_Nu)

    #Step 4: Combine the results into a list of items to return:
    ResultsList = {'SABR_Alpha': Calib_Alpha,
                   'SABR_Beta': Beta,
                   'SABR_Rho': Calib_Rho,
                   'SABR_Nu': Calib_Nu,
                   'SABR_Strikes': Strikes,
                   'SABR_Vols': Calib_SABRVols}

    return ResultsList
