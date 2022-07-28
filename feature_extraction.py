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
ticker = "TSLA"
d = yf.download(tickers=ticker, start=day_of_data , end=end_date, interval="1m", progress=False)
# print(d)

last_day_data = yf.download(tickers=ticker, period="2d", interval="1d", progress=False).head(1)
day_open = d.head(1)['Open'].item()
new_data = yf.download(tickers=ticker, period="1d", interval="1m", progress=False).tail(2).head(1)
print(str(new_data.index).split(",")[0])
print('day open = '+str(day_open))
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

for i in range(0,d.shape[0]):
    dt.append(1)
    t_point.append(time_point)
    time_point = time_point + 1
    last_day_close.append(float(last_day_data["Close"][0]))
    DayAvg.append((last_day_data["Close"][0]-last_day_data["Open"][0])/2+last_day_data["Open"][0])
    
    avg.append((d["High"][i]-d["Low"][i])/2+d["Low"][i])
    CloseOpenDiff.append(d["Close"][i]-day_open)
    CloseOpenDiffPrcnt.append(100*(d["Close"][i]-day_open)/day_open)
    if CloseOpenDiffPrcnt[i]>0:
        UpDown.append(1)
    else:
        UpDown.append(0)

    if i > 2:
        diff2 = d["Open"][i-2]-d["Open"][i-3]
        diff1 = d["Open"][i-1]-d["Open"][i-2]
        diff0 = d["Open"][i-0]-d["Open"][i-1]
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

    lowOpenRatio.append(d["Low"][i]/d["Open"][i])
    lowOpenDiffPrcnt.append(100*(d["Low"][i]-d["Open"][i])/d["Open"][i])
    meanToLastDayCloseRatio.append(((d["Close"][i]-d["Open"][i])/2+d["Open"][i])/last_day_close[i])

d['dt'] = dt
d['time_point'] = t_point
d['last_day_close'] = last_day_close
d['DayAvg'] = DayAvg
d['avg'] = avg
d['CloseOpenDiff'] = CloseOpenDiff
d['CloseOpenDiffPrcnt'] = CloseOpenDiffPrcnt
d['UpDown'] = UpDown
d['Last3'] = Last3
d['lowOpenRatio'] = lowOpenRatio
d['lowOpenDiffPrcnt'] = lowOpenDiffPrcnt
d['meanToLastDayCloseRatio'] = meanToLastDayCloseRatio

xpoints = d['time_point']
y1points = d['avg']
y2points = d['CloseOpenDiffPrcnt']

plt.plot( xpoints, y2points)
# plt.plot(xpoints, y1points , xpoints, y2points)
plt.show()

# print(d)
# day = datetime(0 , 0 , 1 , 0, 0, 0, 0)