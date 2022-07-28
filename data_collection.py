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


start_time = time.time()
s3 = boto3.resource('s3')
BUCKET = "oe-algotrading"

today = (str(datetime.now()).split('-')[0] + '-' + str(datetime.now()).split('-')[1] + '-' + str(datetime.now()).split('-')[2].split(' ')[0])
tickers_list = sys.argv[1]
# tickers_list = 'INTC'
run_flag = 'on'
data_avail_flag = 0

if os.path.exists('run_log_'+today+'.txt'):
  os.remove('run_log_'+today+'.txt')
else:
    log_file = open('run_log_'+today+'.txt', 'w')
    log_file.write('run log \n run started: '+str(datetime.now()))
    log_file.close

hist = yf.download(tickers=tickers_list, period="2d", interval="1d", progress=False).head(1)
d = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False).tail(1)
d = pd.concat([hist,d])

out_put_path = "/home/ubuntu/algo_temp/"+tickers_list+"/"+today+"/"
if os.path.exists(out_put_path):
    shutil.rmtree(out_put_path)
    os.makedirs(out_put_path)
else:
    os.makedirs(out_put_path)
local_file_name = ''
count = 0
file_count = 1

trade_flag = 'off'
trade_start = datetime(int(str(datetime.now()).split('-')[0]),int(str(datetime.now()).split('-')[1]),int(str(datetime.now()).split('-')[2].split(' ')[0]), 13, 29, 45, 0)
trade_end = datetime(int(str(datetime.now()).split('-')[0]),int(str(datetime.now()).split('-')[1]),int(str(datetime.now()).split('-')[2].split(' ')[0]), 20, 0, 0)

# trade_start = datetime.now()
# trade_end = datetime.now() + timedelta(minutes=3)

print('now is:')
print(datetime.now())
print('trade starts in:')
print(trade_start - datetime.now())

sleep_time = round((trade_start - datetime.now()).total_seconds())
print('sleeping for additional '+str(sleep_time)+' seconds till trade starts')

while 1:
    while trade_flag == 'off':
        if sleep_time <= 0:
            trade_flag ='on'
            break

        print(datetime.now())
        print(trade_start - datetime.now())
        print((trade_start - datetime.now()).total_seconds())
        sleep_time = round((trade_start - datetime.now()).total_seconds())
        print('trading starts in '+str(trade_start - datetime.now()))
        print("going to sleep till trade open")

        if sleep_time > 1800:
            time.sleep(600)
            print('trading starts in '+str(trade_start - datetime.now()))
        else:
            time.sleep(sleep_time)
            trade_flag = 'on'

    while datetime.now() > trade_start and datetime.now() < trade_end:
        count = count + 1
        # print('count = ',count)
        # print('time = ',datetime.now())
        new_data = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False).tail(2).head(1)
        print(new_data)
        d = pd.concat([d,new_data])
        # d = d.append(new_data)
        next_minute = datetime.now()+timedelta(minutes=1)-timedelta(seconds=datetime.now().second,microseconds=datetime.now().microsecond)
        while datetime.now() < next_minute:
            time.sleep(1)
        data_avail_flag = 1

        if count == 90:
        #if count == 3:
            count = 0
            break

    time.sleep(0.5)

    if data_avail_flag == 1:
        last_day_data = yf.download(tickers=tickers_list, period="2d", interval="1d", progress=False).head(1)
        avg = list()
        dt = list()
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


        for i in range(0,d.shape[0]):
            dt.append(1)
            last_day_close.append(float(last_day_data["Close"][0]))
            DayAvg.append((last_day_data["Close"][0]-last_day_data["Open"][0])/2+last_day_data["Open"][0])
            
            avg.append((d["High"][i]-d["Low"][i])/2+d["Low"][i])
            CloseOpenDiff.append(d["Close"][i]-d["Open"][i])
            CloseOpenDiffPrcnt.append(100*(d["Close"][i]-d["Open"][i])/d["Open"][i])
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

        # print(d.tail(10))

        local_file_name = tickers_list + '_' + str(file_count) + r'.csv'

        (d.head(d.shape[0]-1)).to_csv(out_put_path  + local_file_name)
        print('file: '+ local_file_name +' was saved locally')

        try:
            output_file_name = tickers_list+'_'+ str(datetime.now()) +'_'+str(file_count) +'.csv'
            s3.Bucket(BUCKET).upload_file(out_put_path + local_file_name, "from_ubuntu/hist_data/"+tickers_list+"_hist_daily/"+today+"/"+output_file_name)
            print('file: '+output_file_name+' was written to S3')
        except Exception as no_s3_write:
            log_file = open('run_log_'+today+'.txt', 'a')
            log_file.write('\n'+str(datetime.now())+' -->  '+tickers_list+': '+no_s3_write+'\n')
            log_file.close

        d = d.tail(3)
        if datetime.now() > trade_start and datetime.now() < trade_end:
            run_flag = 'on'
            file_count = file_count + 1
        else:
            time.sleep(10)
            data_avail_flag = 0
            hist = yf.download(tickers=tickers_list, period="2d", interval="1d", progress=False).head(1)
            d = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False).tail(1)
            file_count = 1
            run_flag = 'off'
            
            today = (str(datetime.now() + timedelta(days=1)).split('-')[0] + '-' + str(datetime.now() + timedelta(days=1)).split('-')[1] + '-' + str(datetime.now() + timedelta(days=1)).split('-')[2].split(' ')[0])
            trade_start = trade_start + timedelta(days=1)
            sleep_time = round((trade_start - datetime.now()).total_seconds())
            print("new spleep time: " + str(sleep_time))
            trade_end = trade_end + timedelta(days=1)
            if os.path.exists(out_put_path):
                shutil.rmtree(out_put_path)
                out_put_path = "/home/ubuntu/algo_temp/"+tickers_list+"/"+today+"/"
                os.makedirs(out_put_path)
            else:
                out_put_path = "/home/ubuntu/algo_temp/"+tickers_list+"/"+today+"/"
                os.makedirs(out_put_path)




