

##########################################################################################################################################
#############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####################################
#############################                                                                        #####################################   
#############################     DDDDDDD       OOOOOOO         N    NNN    OOOOOOO   TTTTTTTTTT     #####################################
#############################     DD     DD    OO     OO        N   NN N   OO     OO      TT         #####################################
#############################     DD      DD  O         O       N  NN  N  O         O     TT         #####################################
#############################     DD     DD    OO     OO        N NN   N   OO     OO      TT         #####################################
#############################     DDDDDDD       OOOOOOO         NN     N    OOOOOOO       TT         #####################################
#############################                                                                        #####################################
#############################                                                                        #####################################
#############################            EEEEEEEEE  DDDDDDD     IIIIII  TTTTTTTTTT    !!!            #####################################
#############################            EE         DD     DD     II        TT       !!!!!           #####################################
#############################            EEEEEEE    DD      DD    II        TT        !!!            #####################################
#############################            EE         DD     DD     II        TT         !             #####################################
#############################            EEEEEEEEE  DDDDDDD     IIIIII      TT         O             #####################################
#############################                                                                        #####################################
#############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####################################
##########################################################################################################################################


import pandas as pd
import numpy as np

import time
import matplotlib.pyplot as plt 

import yfinance as yf
from datetime import datetime, timedelta

def adder(Data, n):
    Data = np.append(Data,np.zeros((Data.shape[0],n)),axis=1)
    return Data

def deleter(Data, where, n):
    Data = np.append(Data[:,0:where],Data[:,(where+n):],axis=1)
    return Data


def ma(Data, lookback, what, where):
    for i in range(len(Data)):
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, what].mean())
        except IndexError:
            pass
    
    print('ma data in column '+str(where)) 
    return Data


def volatility(Data, lookback, what, where):
    
    for i in range(20,len(Data)):
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, what].std())
        except IndexError:
            pass
        
    print('volatility data in column '+str(where)) 
    
    return Data


def BollingerBands(Data, boll_lookback, standard_distance, what, where):
       
    # Calculating mean 
    ma(Data, boll_lookback, what, where)                          
    # Calculating volatility
    volatility(Data, boll_lookback, what, where + 1)
    
    Data[:, where + 2] = Data[:, where] + (standard_distance *  Data[:, where + 1])
    Data[:, where + 3] = Data[:, where] - (standard_distance * Data[:, where + 1])

    print('BollingerBands data in columns '+str(where + 2)+' and '+str(where + 3))  
        
    return Data

# Using the function to calculate a 20-period Bollinger Band with 2 Standard Deviations

# Data = BollingerBands(Data, 20, 2, 3, 4)

def atr(Data, lookback, high, low, close, where, genre = 'Smoothed'):
    # Adding the required columns
    Data = adder(Data, 1)
    # True Range Calculation
    for i in range(len(Data)):
        try:
            Data[i, where] = max(Data[i, high] - Data[i, low],
                            abs(Data[i, high] - Data[i - 1, close]),
                            abs(Data[i, low] - Data[i - 1, close]))
            
        except ValueError:
            pass
        
    Data[0, where] = 0   
    
    print('MAX data in columns '+str(where))  

    if genre == 'Smoothed':
        
        # Average True Range Calculation
        Data = ema(Data, 2, lookback, where, where + 1)
        print('ema data in columns '+str(where+1))  
    
    if genre == 'Simple':
    
        # Average True Range Calculation
        Data = ma(Data, lookback, where, where + 1)
        print('ma data in columns '+str(where+1))  
    
    # Cleaning
    Data = deleter(Data, where, 1)
    # Data = jump(Data, lookback)
    return Data

def ema(Data, alpha, lookback, what, where):

    alpha = alpha / (lookback + 1.0)
    beta  = 1 - alpha
    
    # First value is a simple SMA
    Data = ma(Data, lookback, what, where)
    
    # Calculating first EMA
    Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)
    # Calculating the rest of EMA
    for i in range(lookback + 2, len(Data)):
            try:
                Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)
        
            except IndexError:
                pass 
    return Data

def keltner_channel(Data, ma_lookback, atr_lookback, multiplier, what, where):
    
    Data = ema(Data, 2, ma_lookback, what, where)
    print('keltner ema data in columns '+str(where))  
    Data = atr(Data, atr_lookback, 1, 2, 3, where + 1)
    print('keltner atr data in columns '+str(where+1))  
    
    Data[:, where + 2] = Data[:, where] + (Data[:, where + 1] * multiplier)
    Data[:, where + 3] = Data[:, where] - (Data[:, where + 1] * multiplier)  
    print('keltner_channel data in columns '+str(where + 2)+' and '+str(where + 3))  
    return Data

def squeeze(Data, boll_lookback, boll_vol, kelt_lookback, kelt_vol, close, where):
    
    # Adding Columns
    Data = np.append(Data,np.zeros((Data.shape[0],20)),axis=1)
    
    # Adding Bollinger Bands
    Data = BollingerBands(Data, boll_lookback, boll_vol, close, where)
    # Adding Keltner Channel
    Data = keltner_channel(Data, kelt_lookback, kelt_lookback, kelt_vol, close, where + 4)
    
    # Donchian Middle Point
    for i in range(len(Data)):
    
        try:
            Data[i, where + 8] = max(Data[i - boll_lookback + 1:i + 1, 2])
        except ValueError:
            pass

    for i in range(len(Data)):
        try:
            Data[i, where + 9] = min(Data[i - boll_lookback + 1:i + 1, 1])
    
        except ValueError:
            pass

    print('Donchian max & min Point data in columns '+str(where + 7)+' and '+str(where + 8))  

    Data[:, where + 9] = (Data[:, where + 7] + Data[:, where + 8]) / 2
    
    print('Donchian Middle Point data in columns '+str(where + 9))  
    # Data = deleter(Data, where + 4, 2)
    
    # Calculating Simple Moving Average on the Market
    Data = ma(Data, boll_lookback, close, where + 10)
    print('Simple Moving Average on the Market data in columns '+str(where + 10))  
    # Calculating Delta
    for i in range(len(Data)):
        Data[i, where + 11] = Data[i, close] - ((Data[i, where + 9] + Data[i, where + 10]) / 2)
    
    print('delta between close and avg of Donchian Middle Point and moving avg in columns '+str(where + 11))  

    # Final Smoothing
    Data = ma(Data, boll_lookback, where + 11, where + 12)
    print('moving avg of delta in columns '+str(where + 12))  

    # Cleaning
    
    # Data = deleter(Data, where + 4, 3)
    
    # Squeeze Detection
    for i in range(len(Data)):
        
        if Data[i, where] < Data[i, where + 2] and Data[i, where + 1] > Data[i, where + 3]:
            Data[i, where + 13] = 0.001
    
    print('Squeeze Detection data in columns '+str(where + 13)) 
    
    return Data

boll_lookback = 20
boll_vol = 2
kelt_lookback = 20
kelt_vol = 1.5

# day_of_data = datetime.now()-timedelta(days=450)
# ticker = "AMZN"
# end_date = "2022-07-29"

# my_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv').to_numpy()[:,1:5]

# my_data = yf.download(tickers=ticker, start=day_of_data , interval="1d", progress=False).to_numpy()
# print(my_data[0:10,:])

# my_data = squeeze(my_data, boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4)

def indicator_plot_squeeze(Data, window = 250):
    fig, ax = plt.subplots(3, figsize = (10, 5))
    Chosen = Data[-window:, ]
    # Chosen = Data
        
    for i in range(len(Chosen)):
        ax[0].vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
        # print('i = '+str(i)+' ;  low = '+str(Chosen[i, 2])+' ;  high = '+str(Chosen[i, 1]))
        ax[1].vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  

    ax[0].grid() 
    ax[0].plot(my_data[-window:, 4], color = 'red') 
    ax[0].plot(my_data[-window:, 6], color = 'green') 
    
    ax[1].grid()   
    ax[0].plot(my_data[-window:, 10], color = 'blue') 
    ax[0].plot(my_data[-window:, 11], color = 'pink')
    
    col1 = 16
    col2 = 17

    for i in range(len(Chosen)):
        if Chosen[i, col1] > 0:
            ax[2].vlines(x = i, ymin = 0, ymax = Chosen[i, col1], color = 'black', linewidth = 1)
        if Chosen[i, col1] < 0:
            ax[2].vlines(x = i, ymin = Chosen[i, col1], ymax = 0, color = 'black', linewidth = 1)
        if Chosen[i, col1] == 0:
            ax[2].vlines(x = i, ymin = Chosen[i, col1], ymax = 0, color = 'black', linewidth = 1)  
            
    ax[2].grid() 
    ax[2].axhline(y = 0, color = 'black', linewidth = 1.0, linestyle = '--')

    for i in range(len(Chosen)):
            if Chosen[i, col2] == 0.001:
                x = i
                y = Chosen[i, col1] #+ (-Chosen[i, 8])
                ax[2].annotate(' ', xy = (x, y), arrowprops = dict(width = 5, headlength = 3, headwidth = 3, facecolor = 'red', color = 'red'))
            elif Chosen[i, col2] == 0:
                x = i
                y = Chosen[i, col1] #+ (-Chosen[i, 8])
                ax[2].annotate(' ', xy = (x, y), arrowprops = dict(width = 5, headlength = 3, headwidth = 3, facecolor = 'green', color = 'green'))
    
    ax[0].legend(loc="upper left")
    fig.savefig('full_figure.png')
    fig.show()

# indicator_plot_squeeze(my_data)

def signal(Data):
    for i in range(len(Data)):   
       # Bullish Signal
       if Data[i, 9] != 0.001 and Data[i - 1, 9] == 0.001 and Data[i, 8] > 0: 
            Data[i, 10] = 1 
                
       # Bearish Signal
       elif Data[i, 9] != 0.001 and Data[i - 1, 9] == 0.001 and Data[i, 8] < 0:            
            Data[i, 11] = -1

def buy_sell(Data):
    money_avail_flag = 1
    buy_price = 0
    sell_price = 0
    limit = 0

    money = 100000
    red = 4
    green = 6
    blue = 10
    pink = 11
    signal = 'hold'
    print(np.size(Data,axis=0))
    Data = Data[-(min(250,np.size(Data,axis=0)-1)):, ]
    n_days = min(250,np.size(Data,axis=0)-1)
    for i in range(2,n_days):   
        # buy Signal
        if Data[i, 1] > limit*1.05:
            limit = Data[i, 1]

        if Data[i, 1] > Data[i,green]:
            signal = 'Buy'
        elif ((Data[i, 2] < Data[i,blue] and ((Data[i-1,16]-Data[i-2,16])/Data[i-2,16])<(-0.05)) or (Data[i, 2]<limit*0.995)):
            signal = 'sell'
        else:
            signal = 'hold'

        # if Data[i, 1] > Data[i,6] and ((Data[i-1,16]-Data[i-2,16])/Data[i-2,16])>(-0.1) and money_avail_flag == 1: 
        if signal == 'Buy' and money_avail_flag == 1: 
                Data[i, 17] = 1
                money_avail_flag = 0
                buy_price = Data[i, 2]
                limit = buy_price
                # print(str(i)+':  buy_price= '+str(buy_price))
                    
        # sell Signal
        elif signal == 'sell' and money_avail_flag == 0:
                Data[i, 17] = -1
                money_avail_flag = 1
                sell_price = Data[i, 2]
                # print(str(i)+':  sell_price= '+str(sell_price)+'   and col16: '+str(Data[i-1,16]-Data[i-2,16]))
                # print('cng % = '+str(100*(sell_price-buy_price)/buy_price))
                money = money*(1+(sell_price-buy_price)/buy_price)
                # print(100*(money-10000)/100000)

        # print(Data[i, 17])
    print(signal)
    print('change % = '+str(100*(money-100000)/100000))
    return [100*(money-100000)/100000,signal]

