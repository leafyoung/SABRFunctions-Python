"""
#' Black-76-Equivalent Vols from Parameter Bumps for SABR Inputs
"""

# pylint:disable=invalid-name, line-too-long

from SABRtoBlack76 import SABRtoBlack76

def SABRParamLinearBump(F0, K, tex, Alpha, Beta, Rho, Nu, bump_param, bumpsize = 1 / 20000, bumpdir = 'up'):

    """
    #' Calculates a one-sided bump of 0.5bp by default (user can change the bump size) for the specific
    #'  parameter that the  user wants to alter, for the Black-76-equivalent volatility. Uses a switch
    #'  function to figure out which parameter to bump, and then runs the actual shift.
    #' @param F0 Current forward price
    #' @param K Strike of the option
    #' @param tex Time to expiry, expressed in years, of the option
    #' @param Alpha Calibrated SABR Alpha value from either ATM or FULL calibration methods
    #' @param Beta Shape parameter of SABR schema, EITHER evaluated using historical data OR preset by user
    #' @param Rho Correlation between SABR forward and diffusion processes
    #' @param Nu Vol-of-vol for SABR diffusion process
    #' @param bump_param Specifies which parameter you want to bump. Must be one of the inputs listed above.
    #' @param bumpsize Actual size of the bump, defaults to 0.5bps, but can be increased as required
    #' @param bumpdir Allows for 'up' or 'dn' bumps
    #'
    #' @return Revised Black-76-equivalent SABR implied volatility
    #' @export
    #'
    #' @examples SABRParamLinearBump(F0 = 0.0266, K = 0.0250, tex = 0.25, Alpha = 0.0651, Beta = 0.5,
    #' Rho = -0.0356, Nu = 1.0504, bump_param = 'Alpha', bumpdir = 'dn')
    """

    if bump_param in ['F0', 'Alpha', 'Beta', 'Rho', 'Nu']:
        pass
    else:
        raise ValueError("Bump parameter MUST be one of 'F0', 'Alpha', 'Beta', 'Rho', or 'Nu'!")

    if bumpdir in ['up', 'dn']:
        bumpmult = 1 if bumpdir == 'up' else -1
    else:
      raise ValueError("Bump direction MUST be 'up' or 'dn'!")

    #Calculate the bump:
    bump = bumpmult * bumpsize

    #Switch statement to figure out which actual parameter to bump:
    if bump_param == 'F0':
        BumpedSABRVol = SABRtoBlack76(F0 + bump, K, tex, Alpha, Beta, Rho, Nu)
    elif bump_param == 'Alpha':
        BumpedSABRVol = SABRtoBlack76(F0, K, tex, Alpha + bump, Beta, Rho, Nu)
    elif bump_param == 'Beta':
        BumpedSABRVol = SABRtoBlack76(F0, K, tex, Alpha, Beta + bump, Rho, Nu)
    elif bump_param == 'Rho':
        BumpedSABRVol = SABRtoBlack76(F0, K, tex, Alpha, Beta, Rho + bump, Nu)
    elif bump_param == 'Nu':
        BumpedSABRVol = SABRtoBlack76(F0, K, tex, Alpha, Beta, Rho, Nu + bump)

    #Return the bumped result:
    return BumpedSABRVol
