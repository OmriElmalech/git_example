
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

minute = datetime(int(str(datetime.now()).split('-')[0]),int(str(datetime.now()).split('-')[1]),int(str(datetime.now()).split('-')[2].split(' ')[0]), 0, 1, 0, 0)

d = yf.download(tickers="TSLA", period="1d", interval="1m", progress=False).tail(2).head(1)
print(d)

# day = datetime(0 , 0 , 1 , 0, 0, 0, 0)