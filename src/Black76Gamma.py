"""
#' Black-76 Closed-Form Gamma
"""

# pylint:disable=invalid-name, line-too-long

import numpy as np
import scipy.stats as ss

def Black76Gamma(F0, K, Vol, tex, rfr):
    """
    #'
    #' Closed-form solution for the Gamma of a European option on a forward contract or rate, using
    #' the Black-76 formulation. For swaptions, provides the simple Gamma for a European-style exercise
    #' payer or receiver swaption.
    #'
    #' @param F0 Current forward rate
    #' @param K Strike of the option
    #' @param Vol Implied volatility, MUST BE IN LOGNORMAL TERMS, can be taken from SABRTOBLACK76
    #' @param tex Time to expiry, in years, of the option
    #' @param rfr Riskless rate, best taken as either the 10y or 30y government zero rate
    #'
    #' @return Standard Black-76 Gamma of a European option on a forward contract
    #' @export
    #'
    #' @examples Black76Gamma(F0 = 0.0266, K = 0.0250, Vol = 0.4084, tex = 0.25, rfr = 0.02)
    """

    d1 = (np.log(F0 / K) + 0.5 * Vol ** 2  * tex) / (Vol * np.sqrt(tex))
    Gamma = np.exp(-rfr * tex) / (F0 * Vol * np.sqrt(tex)) * ss.norm.pdf(d1)

    return Gamma
