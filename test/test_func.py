# pylint: disable=line-too-long

"""
test
"""

import sys
sys.path.insert(0, '../src/')

import numpy as np
from Black76Delta import Black76Delta
from Black76Gamma import Black76Gamma
from Black76Vega import Black76Vega
from Black76OptionPrice import Black76OptionPrice

from SABRDelta import SABRDelta
from SABRGamma import SABRGamma
from SABRVega import SABRVega
from SABRVanna import SABRVanna
from SABRVolga import SABRVolga

from SABRtoBlack76 import SABRtoBlack76
from SABRAlphaCubic import SABRAlphaCubic
from ATMVolToSABRAlpha import ATMVolToSABRAlpha

from SABRVolsFromATMCalib import SABRVolsFromATMCalib
from SABRVolsFromFullCalib import SABRVolsFromFullCalib

def test(value, func):
    """
    test and print
    """

    a_val = value
    b_val = func()
    print((a_val, b_val, np.isclose(a_val, b_val)))
    assert np.isclose(a_val, b_val)


if __name__ == '__main__':
    test(0.06562295, lambda: Black76Delta(0.018, 0.025, 0.4084, 0.25, 0.02, "c"))
    test(0.8359315, lambda: Black76Delta(0.03, 0.025, 0.4084, 0.25, 0.02, "c"))

    test(34.71331, lambda: Black76Gamma(0.018, 0.025, 0.4084, 0.25, 0.02))
    test(39.50014, lambda: Black76Gamma(0.03, 0.025, 0.4084, 0.25, 0.02))

    test(0.00114833, lambda: Black76Vega(0.018, 0.025, 0.4084, 0.25, 0.02))
    test(0.003629668, lambda: Black76Vega(0.03, 0.025, 0.4084, 0.25, 0.02))

    test(9.775347e-05, lambda: Black76OptionPrice(0.018, 0.025, 0.4084, 0.25, 0.02, "c"))
    test(0.005539448, lambda: Black76OptionPrice(0.03, 0.025, 0.4084, 0.25, 0.02, "c"))

    # ATM calibrated
    test(0.0840342, lambda: SABRDelta(0.018, 0.025, 0.25, 0.02, "c", 0.06502845, 0.5, 1.798357e-10, 1.062621))
    test(0.8390087, lambda: SABRDelta(0.03, 0.025, 0.25, 0.02, "c", 0.06502845, 0.5, 1.798357e-10, 1.062621))

    test(-0.9109783, lambda: SABRDelta(0.018, 0.025, 0.25, 0.02, "p", 0.06502845, 0.5, 1.798357e-10, 1.062621))
    test(-0.1560038, lambda: SABRDelta(0.03, 0.025, 0.25, 0.02, "p", 0.06502845, 0.5, 1.798357e-10, 1.062621))

    test(40.83423, lambda: SABRGamma(0.018, 0.025, 0.25, 0.02, 0.06502845, 0.5, 1.798357e-10, 1.062621))
    test(40.48232, lambda: SABRGamma(0.03, 0.025, 0.25, 0.02, 0.06502845, 0.5, 1.798357e-10, 1.062621))

    # Full calibrated
    test(0.001823385, lambda: SABRVega(0.018, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))
    test(0.004058561, lambda: SABRVega(0.03, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))

    test(0.0002533987, lambda: SABRVanna(0.018, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))
    test(-0.0002858474, lambda: SABRVanna(0.03, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))

    test(0.0001482841, lambda: SABRVolga(0.018, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))
    test(0.0001387801, lambda: SABRVolga(0.03, 0.025, 0.25, 0.02, 0.06943288, 0.5, 0.02668178, 0.9025896))

    test(0.5165779, lambda: SABRtoBlack76(0.018, 0.025, 0.25, 0.06943288, 0.5, 0.02668178, 0.9025896))
    test(0.435243, lambda: SABRtoBlack76(0.03, 0.025, 0.25, 0.06943288, 0.5, 0.02668178, 0.9025896))

    test(-0.06074962, lambda: SABRAlphaCubic(0.018, 0.025, 0.5, 0.25, 0.5, 0.02668178, 0.9025896))
    test(-0.04854122, lambda: SABRAlphaCubic(0.03, 0.025, 0.5, 0.25, 0.5, 0.02668178, 0.9025896))

    # (K, 0.5, tex, Beta_Full, Rho_Full, Nu_Full)

    test(0.07766273520393163, lambda: ATMVolToSABRAlpha(0.025, 0.5, 0.25, 0.5, 0.02668178, 0.9025896))
    test(0.49728414213467964, lambda: ATMVolToSABRAlpha(0.025+1, 0.5, 0.25, 0.5, 0.02668178, 0.9025896))
    test(0.3558953627524897, lambda: ATMVolToSABRAlpha(0.025+0.5, 0.5, 0.25, 0.5, 0.02668178, 0.9025896))

    atm_calib = SABRVolsFromATMCalib(
        0.0266,
        0.4084,
        [0.0266, 0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0500, 0.0600, 0.0700, 0.0800, 0.0900, 0.1000],
        [0.4084, 0.7376, 0.5685, 0.4668, 0.4154, 0.4048, 0.4161, 0.4347, 0.4734, 0.5072, 0.5358, 0.5602, 0.5813, 0.5998],
        0.25,
        0.5,
        0.1,
        0.7)

    print(atm_calib)

    full_calib = SABRVolsFromFullCalib(
        0.0266,
        [0.0266, 0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0500, 0.0600, 0.0700, 0.0800, 0.0900, 0.1000],
        [0.4084, 0.7376, 0.5685, 0.4668, 0.4154, 0.4048, 0.4161, 0.4347, 0.4734, 0.5072, 0.5358, 0.5602, 0.5813, 0.5998],
        0.25,
        0.5,
        0.05,
        0.1,
        0.7
    )

    print(full_calib)
