"""
#' Black-76 Closed Form Delta
"""

# pylint:disable=invalid-name, line-too-long

import numpy as np
import scipy.stats as ss

def Black76Delta(F0, K, Vol, tex, rfr, CallOrPut):
    """
    #'
    #' Closed-form solution for the Delta of a European call or put on a forward contract or rate,
    #' using the Black-76 formulation. For swaptions, provides the simple Delta for a European-style
    #' exercise payer or receiver swaption.
    #'
    #' @param F0 Current forward rate
    #' @param K Strike of the option
    #' @param Vol Implied volatility, MUST BE IN LOGNORMAL TERMS, can be taken from SABRTOBLACK76
    #' @param tex Time to expiry, in years, of the option
    #' @param rfr Riskless rate, best taken as either the 10y or 30y government zero rate
    #' @param CallOrPut Takes values of 'c' or 'p', and nothing else - determines whether you are pricing a call or put
    #'
    #' @return Standard Black-76 Delta of a European option on a forward contract
    #' @export
    #'
    #' @examples Black76Delta(F0 = 0.0266, K = 0.0250, Vol = 0.4084, tex = 0.25, rfr = 0.02, CallOrPut = 'c')
    """

    if CallOrPut in ['c', 'p']:
        a = 0 if CallOrPut == 'c' else -1
    else:
        raise ValueError('CallOrPut flag can only take values c or p!')

    d1 = (np.log(F0 / K) + 0.5 * Vol ** 2  * tex) / (Vol * np.sqrt(tex))

    Delta = np.exp(-rfr * tex) * (ss.norm.cdf(d1) + a)

    return Delta
