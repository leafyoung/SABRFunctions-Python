import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd

np.seterr(all='raise')

import warnings
warnings.filterwarnings( "ignore", module = "pandas\..*" )

import sys
sys.path.insert(0, '../src')

cmap = plt.colormaps.get_cmap('Dark2')
colors = cmap.colors  # type: list
cmap

from SABRVolsFromFullCalib import SABRVolsFromFullCalib

strikes = np.array([0.5271, 1.0271, 1.5271, 1.7771, 2.0271, 2.2771, 2.4021,
              2.5271, 2.6521, 2.7771, 3.0271, 3.2771, 3.5271, 4.0271, 4.5271,
              5.5271]) / 100

LogNormalVols = np.array([15.785344, 14.305103, 13.073869, 12.550007, 12.088721,
              11.691661, 11.517660, 11.360133, 11.219058, 11.094293, 10.892464,
              10.750834, 10.663653, 10.623862, 10.714479, 11.103755]) / 100

full_calib = SABRVolsFromFullCalib(2.5271/100, strikes, LogNormalVols, tex=10, Beta=0.5,
                                   guess_Alpha=0.001,
                                   guess_Rho=0.1,
                                   guess_Nu=0.01)

print(full_calib)

from pysabr import Hagan2002LognormalSABR
import numpy as np
sabrLognormal = Hagan2002LognormalSABR(f=2.5271/100, shift=0, t=10, beta=0.5)
[alpha, rho1, volvol1] = sabrLognormal.fit(strikes, LogNormalVols * 100)
print("Fitted  alpha, rho, volvol: ", [alpha, rho1, volvol1])

