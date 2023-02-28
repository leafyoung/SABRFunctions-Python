library(SABRFunctions)
library(ggplot2)
library(dplyr)

View(sabrcalibdata)

data('histratevoldata')

View(histratevoldata)

data("sabrcalibdata")
library(dplyr)
sabr3m10y <- sabrcalibdata %>% filter(Point == '3M10Y')

sabr3m10y

#Setup SABR params
F0 <- sabr3m10y$Strike[1]          #ATM Forward Rate
K <- sabr3m10y$Strike              #Vector of strikes
MarketVols <- sabr3m10y$BlackVol   #Vector of vols

t <- 0.25                          #Assume 3M to expiry of option

#Initialise SABR parameters
Alpha <- 0.05                      #Best guess of initial Alpha
Beta <- 0.5                        #Assume simple 0.5 Beta
Rho <- 0.1                         #Guess value must be between -1 and 1
Nu <- 0.7                          #Guess value must be greater than 0

SABR3M10YFullCalib <- SABRVolsFromFullCalib(F0, K, MarketVols, t, Beta, Alpha, Rho, Nu)
SABR3M10YFullCalib

list(F0, K, MarketVols, t, Beta, Alpha, Rho, Nu)

SABR3M10YFullCalib$SABR_Vols
Fitted3M10YData$Value[Fitted3M10YData$Method == 'FULL']
Fitted3M10YData$Value[Fitted3M10YData$Method == 'FULL'] - SABR3M10YFullCalib$SABR_Vols

Fitted3M10YData$Strike[Fitted3M10YData$Method == 'ATM'] - SABR3M10YFullCalib$SABR_Strikes
Fitted3M10YData$Value[Fitted3M10YData$Method == 'ATM'] - SABR3M10YFullCalib$SABR_Vols





sabrfitteddata %>% filter(Point == '3M10Y')

data("sabrfitteddata")
library(ggplot2)
library(dplyr)
Fitted3M10YData <- sabrfitteddata %>% filter(Point == '3M10Y') %>% select(Method, Strike, Value)
ATM <- Fitted3M10YData$Strike[Fitted3M10YData$Method == 'MARKET'][1] * 100
ATMVOL <- Fitted3M10YData$Value[Fitted3M10YData$Method == 'MARKET'][1] * 100
ggplot(data = Fitted3M10YData, aes(x = Strike * 100, y = Value * 100, colour = Method)) +
  geom_point(aes(x = ATM, y = ATMVOL), colour = 'red', size = 5, stroke = 1, fill = 'yellow', shape = 21) +
  geom_point() +
  geom_line() +
  labs(x = 'Swaption Strike (%)', y = 'Swaption Implied Black-76 (Lognormal) Volatility (%)',
       title = 'Comparison of 3M10Y Swaption Volatilities Against Fitted Values',
       subtitle = 'ATM and Full Calibration of SABR, with Actual ATM Highlighted')


###

data("sabrcalibdata")
library(dplyr)
sabr3m10y <- sabrcalibdata %>% filter(Point == '3M10Y')

#Setup SABR params
F0 <- sabr3m10y$Strike[1]          #ATM Forward Rate
ATMVol <- sabr3m10y$BlackVol[1]    #ATM Black vol quoted in market
K <- sabr3m10y$Strike              #Vector of strikes
MarketVols <- sabr3m10y$BlackVol   #Vector of vols

t <- 0.25                          #Assume 3M to expiry of option

#Initialise SABR parameters
Beta <- 0.5                        #Assume simple 0.5 Beta
Rho <- 0.1                         #Guess value must be between -1 and 1
Nu <- 0.7                          #Guess value must be greater than 0

list(F0, ATMVol, K, MarketVols, t, Beta, Rho, Nu)

SABR3M10YATMCalib <- SABRVolsFromATMCalib(F0, ATMVol, K, MarketVols, t, Beta, Rho, Nu)
SABR3M10YATMCalib
