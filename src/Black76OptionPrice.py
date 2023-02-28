"""
#' Black-76 Closed-Form Price
"""
# pylint:disable=invalid-name, line-too-long

import numpy as np
import scipy.stats as ss

def Black76OptionPrice(F0, K, Vol, tex, rfr, CallOrPut):
    """
    #' Closed-form solution for the price of a European call or put on a forward contract or rate,
    #' using the Black-76 formulation. For swaptions, provides the simple Price for a European-style
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
    #'
    #' @export
    #'
    #' @examples Black76OptionPrice(F0 = 0.0266, K = 0.0250, Vol = 0.4084, tex = 0.25, rfr = 0.02, CallOrPut = 'c')

    """

    if CallOrPut in ['c', 'p']:
        a = 1 if CallOrPut == 'c' else -1
    else:
        raise ValueError('CallOrPut flag can only take values c or p!')

    d1 = (np.log(F0 / K) + 0.5 * Vol ** 2  * tex) / (Vol * np.sqrt(tex))
    d2 = d1 - Vol * np.sqrt(tex)

    Price = np.exp(-rfr * tex) * a * (F0 * ss.norm.cdf(a * d1) - K * ss.norm.cdf(a * d2))

    return Price
