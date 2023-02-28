"""
#' ATM Calibration Procedure for SABR Parameters
"""

# pylint:disable=invalid-name, line-too-long, pointless-string-statement

import numpy as np
import scipy.optimize as spopt
from ATMVolToSABRAlpha import ATMVolToSABRAlpha
from SABRtoBlack76 import SABRtoBlack76

def SABRATMCalib(F0, ATMVol, Strikes, MarketVols, tex, Beta, guess_Rho, guess_Nu):
    """
    #' Calibrates Rho and Nu such that sum of square errors between Black-76-equivalent SABR vols and market observed vols are minimized.
    #' For a given Rho and Nu, calculates ATM SABR Alpha from this, then calculates the resulting Black-76 vol, then takes SSE.
    #' Minimizes SSE function using non-linear optimization.
    #'
    #' @param F0 Current forward rate
    #' @param ATMVol Current lognormal ATM volatility corresponding to F0 in the market
    #' @param Strikes VECTOR of strike prices
    #' @param MarketVols VECTOR of LOGNORMAL (i.e. Black-76) market-quoted implied volatilities
    #' @param tex Time to expiry of option, measured in years
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data OR preset by user
    #' @param guess_Rho Initial user-defined guess of Rho value, MUST be bounded between -1 and 1
    #' @param guess_Nu Initial user-defined guess of Nu value, MUST be non-zero
    #'
    #' @return List of outputs from the constrOptim function that includes the parameters for calibrated Rho/Nu
    #' @export
    #'
    #' @examples
    #' data(sabrcalibdata)
    #' calibrun = sabrcalibdata[sabrcalibdata$Point == '3M10Y',]
    #' SABRATMCalib(F0 = 0.0266, ATMVol = 0.4084, Strikes = calibrun$Strike,
    #' MarketVols = calibrun$BlackVol,  tex = 0.25, Beta = 0.5, guess_Rho = 0.05,
    #'  guess_Nu = 0.5)
    """

    # Some basic error-checking:
    if len(Strikes) != len(MarketVols):
        raise ValueError('Strikes vector must be same length as market data!')

    if np.abs(guess_Rho) > 1:
        raise ValueError('Correlation parameter Rho must be between -1 and 1!')

    if guess_Nu <= 0:
        raise ValueError('Vol-of-vol parameter must be non-zero!')

    #Create empty vector of vols for calibration:
    n = len(Strikes)

    CalibVols = np.zeros(n)

    #Define the internal sum of square errors (SSE) function:
    def SSE(calibparams,
            F0 = F0,
            ATMVol = ATMVol,
            Strikes = Strikes,
            tex = tex,
            Beta = Beta,
            MarketVols = MarketVols):

        v1 = calibparams[0]
        v2 = calibparams[1]

        # Calculate ATM SABR Alpha from initial values:
        ATMAlpha = ATMVolToSABRAlpha(F0, ATMVol, tex, Beta, v1, v2)

        for i in range(n):
            CalibVols[i] = SABRtoBlack76(F0, Strikes[i], tex, ATMAlpha, Beta, v1, v2)

        y = ((CalibVols - MarketVols) ** 2).sum()
        return y

    #Define matrix and vector of constraints
    #We must setup the constraints such that:
    #rho >= -1
    #rho <= 1
    #nu > 0

    """
    # Global optimization
    grid = (-10, 10, 0.1)
    xmin_global = optimize.brute(f, (grid, ))
    print("Global minima found %s" % xmin_global)

    # Constrain optimization
    xmin_local = optimize.fminbound(f, 0, 10)
    print("Local minimum found %s" % xmin_local)
    """

    #Pass in the vector of initial parameter guesses:
    init_params = (guess_Rho, guess_Nu)
    bnds = ((-1, 1), (0, None))
    CalibSet = spopt.minimize(SSE, init_params,bounds=bnds)

    return CalibSet
