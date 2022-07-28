import imp
import sys
import boto3
import shutil
import time
from datetime import datetime, timedelta
import os
from turtle import clear
import numpy as np
import pandas as pd
import yfinance as yf
from io import StringIO # python3; python2: BytesIO
import matplotlib.pyplot as plt 


day_of_data = "2022-07-27"
end_date = "2022-07-28"
#ticker = "TSLA"
# print(d)

def get_data(ticker):
    d1 = yf.download(tickers=ticker, start=day_of_data , end=end_date, interval="1m", progress=False)
    last_day_data = yf.download(tickers=ticker, period="2d", interval="1d", progress=False).head(1)
    day_open = d1.head(1)['Open'].item()
    print('day_open = '+str(day_open))
    avg = list()
    dt = list()
    t_point = list()
    last_day_close = list()
    DayAvg = list()
    CloseOpenDiff = list()
    CloseOpenDiffPrcnt = list()
    UpDown = list()
    Last3 = list()
    # last5 = list()
    lowOpenRatio = list()
    lowOpenDiffPrcnt = list()
    meanToLastDayCloseRatio = list()
    # movingAvg10 = list()
    # movingAvg50 = list()
    # movingAvg300 = list()
    # movingAvg10Grad = list()
    # movingAvg50Grad = list()
    # movingAvg300Grad = list()


    # d = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False).tail(10)
    # last_day_data = yf.download(tickers=tickers_list, period="2d", interval="1d", progress=False).head(1)

    time_point = 1

    for i in range(0,d1.shape[0]):
        dt.append(1)
        t_point.append(time_point)
        time_point = time_point + 1
        last_day_close.append(float(last_day_data["Close"][0]))
        DayAvg.append((last_day_data["Close"][0]-last_day_data["Open"][0])/2+last_day_data["Open"][0])
        
        avg.append((d1["High"][i]-d1["Low"][i])/2+d1["Low"][i])
        CloseOpenDiff.append(d1["Close"][i]-day_open)
        CloseOpenDiffPrcnt.append(100*(d1["Close"][i]-day_open)/day_open)
        if CloseOpenDiffPrcnt[i]>0:
            UpDown.append(1)
        else:
            UpDown.append(0)

        if i > 2:
            diff2 = d1["Open"][i-2]-d1["Open"][i-3]
            diff1 = d1["Open"][i-1]-d1["Open"][i-2]
            diff0 = d1["Open"][i-0]-d1["Open"][i-1]
            if (diff2 > 0) and (diff1 > 0) and (diff0 > 0):
                Last3.append(2)
            else:
                if (diff2 <= 0) and (diff1 > 0) and (diff0 > 0):
                    Last3.append(1)
                else:
                    if (diff2 > 0) and (diff1 <= 0) and (diff0 <= 0):
                        Last3.append(-1)
                    else:
                        if (diff2 <= 0) and (diff1 <= 0) and (diff0 <= 0):
                            Last3.append(-2)
                        else:
                            Last3.append(0)
        else:
            Last3.append(-7)

        lowOpenRatio.append(d1["Low"][i]/d1["Open"][i])
        lowOpenDiffPrcnt.append(100*(d1["Low"][i]-d1["Open"][i])/d1["Open"][i])
        meanToLastDayCloseRatio.append(((d1["Close"][i]-d1["Open"][i])/2+d1["Open"][i])/last_day_close[i])

    d1['dt'] = dt
    d1['time_point'] = t_point
    d1['last_day_close'] = last_day_close
    d1['DayAvg'] = DayAvg
    d1['avg'] = avg
    d1['CloseOpenDiff'] = CloseOpenDiff
    d1['CloseOpenDiffPrcnt'] = CloseOpenDiffPrcnt
    d1['UpDown'] = UpDown
    d1['Last3'] = Last3
    d1['lowOpenRatio'] = lowOpenRatio
    d1['lowOpenDiffPrcnt'] = lowOpenDiffPrcnt
    d1['meanToLastDayCloseRatio'] = meanToLastDayCloseRatio


    # print(d)
    # day = datetime(0 , 0 , 1 , 0, 0, 0, 0)
    return(d1)

tsla_data = get_data("TSLA")
nflx_data = get_data("NFLX")

tsla_xpoints = tsla_data['time_point']
tsla_ypoints = tsla_data['CloseOpenDiffPrcnt']
nflx_ypoints = nflx_data['CloseOpenDiffPrcnt']

plt.plot( tsla_xpoints, tsla_ypoints,tsla_xpoints, nflx_ypoints)
# plt.plot(xpoints, y1points , xpoints, y2points)
plt.show()