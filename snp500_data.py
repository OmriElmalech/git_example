# import imp
import sys
import boto3
import shutil
import time
from datetime import datetime, timedelta
import os
from turtle import clear
import numpy as np
import numpy.fft as fft
import pandas as pd
import yfinance as yf
from io import StringIO # python3; python2: BytesIO
import matplotlib.pyplot as plt 
from urllib.request import Request, urlopen
import squeeze_mom_benchmark as sm

start_time = time.time()

day_of_data = datetime.now()-timedelta(days=365)
# day_of_data = "2022-07-28"
end_date = "2022-07-29"
#ticker = "TSLA"
# print(d)

def get_data(ticker):
    d1 = yf.download(tickers=ticker, start=day_of_data , interval="1d", progress=False)
    # last_day_data = yf.download(tickers=ticker, period="2d", interval="1d", progress=False).head(1)
    return(d1)

# print(get_data("^GSPC"))

# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# print(table)
count = 0
snp500_ticker_list = pd.DataFrame()
sym = list()
change_mean = list()
change_stdev = list()
left_3sig = list()
period_change = list()
sm_chng = list()

######        squeeze momentum parameters       #########
boll_lookback = 20
boll_vol = 2
kelt_lookback = 20
kelt_vol = 1.5
#########################################################

req = Request('https://www.slickcharts.com/sp500', headers={'User-Agent': 'Mozilla/5.0'})
table=pd.read_html(urlopen(req))

for row in table[0]['Symbol']:
    change_prctg = list()
    if row == 'BRK.B':
        continue
    else:
        data = get_data(row)
    # print('change % = '+str(sm.buy_sell(sm.squeeze(data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))
    try:
        sm_chng.append(sm.buy_sell(sm.squeeze(data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4)))
    except ValueError:
        continue
    
    sym.append(row)
    # print(data.shape[0])
    for i in range(0,data.shape[0]):
        if i==0:
            start_price = data["Open"][i]
            
        if i==(data.shape[0]-1):
            end_price = data["Close"][i]

#         change_prctg.append(100*(data["Close"][i]-data["Open"][i])/data["Open"][i])
#     # print('year long days change mean = '+str(np.mean(change_prctg)))
#     # print('year long days change stdv = '+str(np.std(change_prctg)))
#     data['change_prctg'] = change_prctg
    period_change.append(100*(end_price-start_price)/start_price)
#     change_mean.append(np.mean(change_prctg))
#     change_stdev.append(np.std(change_prctg))
#     left_3sig.append(np.mean(change_prctg)-3*np.std(change_prctg))
#     # snp500_ticker_list.append(row)
    count = count + 1
    print('count = '+str(count))
    if count == 100:
        break


snp500_ticker_list['symbol'] = sym
snp500_ticker_list['period_change'] = period_change
snp500_ticker_list['Squeeze Momentum change'] = sm_chng
# snp500_ticker_list['year_long_days_change_mean'] = change_mean
# snp500_ticker_list['year_long_days_change_stdev'] = change_stdev
# snp500_ticker_list['left_3sig'] = left_3sig

print(snp500_ticker_list.nlargest(10,'Squeeze Momentum change'))
snp500_ticker_list.to_csv('snp500_ticker_list.csv', sep='\t')

# print(snp500_ticker_list)
# print('max left_3sig: '+str(max(snp500_ticker_list['left_3sig'])))
# print(snp500_ticker_list.loc[snp500_ticker_list['left_3sig'] == max(snp500_ticker_list['left_3sig'])])
# print('max period_change: '+str(max(snp500_ticker_list['period_change'])))
# print(snp500_ticker_list.loc[snp500_ticker_list['period_change'] == max(snp500_ticker_list['period_change'])])
# print('min period_change: '+str(min(snp500_ticker_list['period_change'])))
# print(snp500_ticker_list.loc[snp500_ticker_list['period_change'] == min(snp500_ticker_list['period_change'])])

# # print(get_data(snp500_ticker_list[0]))
# print(time.time-start_time)
