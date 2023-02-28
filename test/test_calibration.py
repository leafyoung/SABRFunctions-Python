import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.filterwarnings( "ignore", module = "pandas\..*" )

import sys
sys.path.insert(0, '../src')

cmap = plt.colormaps.get_cmap('Dark2')
colors = cmap.colors  # type: list 
cmap


# Calibrate for all
# sabrfitteddata.query('Point == "3M10Y"')

from SABRVolsFromFullCalib import SABRVolsFromFullCalib
from SABRVolsFromATMCalib import SABRVolsFromATMCalib

sabrfitteddata = pd.read_csv('../data/sabrfitteddata.csv', index_col=0)
sabrcalibdata = pd.read_csv('../data/sabrcalibdata.csv', index_col=0)
all_points = sabrcalibdata.Point.unique()

np.seterr(all='raise')

for point_sel in ['5Y10Y']: # 3M10Y
    print(point_sel)

    sabre3m10y = sabrcalibdata.query('Point == @point_sel')

    display(sabre3m10y)

    # Setup SABR params
    K = sabre3m10y.Strike.to_numpy() #Vector of strikes
    MarketVols = sabre3m10y.BlackVol.to_numpy() #Vector of vols    
    F0 = K[0] #ATM Forward Rate
    ATMVol = MarketVols[0] #ATM Black vol quoted in market

    t = 0.25 #Assume 3M to expiry of option

    #Initialise SABR parameters
    Alpha = 0.05 #Best guess of initial Alpha
    Beta = 0.5   #Assume simple 0.5 Beta
    Rho = 0.1    #Guess value must be between -1 and 1
    Nu = 0.7     #Guess value must be greater than 0

    SABR3M10YFullCalib = SABRVolsFromFullCalib(F0, K, MarketVols, t, Beta, Alpha, Rho, Nu)
    SABR3M10YATMCalib = SABRVolsFromATMCalib(F0, ATMVol, K, MarketVols, t, Beta, Rho, Nu)

    df_market = pd.DataFrame({
        'Point': point_sel,
        'Method': 'MARKET',
        'Strike': K,
        'Value': MarketVols})

    df_atm = pd.DataFrame({
        'Point': point_sel,
        'Method': 'ATM',
        'Strike': SABR3M10YATMCalib['SABR_Strikes'],
        'Value': SABR3M10YATMCalib['SABR_Vols']})

    df_full = pd.DataFrame({
        'Point': point_sel,
        'Method': 'FULL',
        'Strike': SABR3M10YFullCalib['SABR_Strikes'],
        'Value': SABR3M10YFullCalib['SABR_Vols']})

    df_point = pd.concat([df_market, df_atm, df_full]).reset_index()

display(df_point
 .merge(sabrfitteddata,
        on = ['Point', 'Method', 'Strike'],
        suffixes=['_1', '_2'])
 .assign(diff = lambda x: x.Value_1 - x.Value_2))


