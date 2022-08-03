from datetime import datetime, timedelta
import squeeze_mom_benchmark as sm
import yfinance as yf
import pandas as pd

day_of_data = datetime.now()-timedelta(days=183)
ticker = "NVDA"
boll_lookback = 20
boll_vol = 2
kelt_lookback = 20
kelt_vol = 1.5

snp500_ticker_list = pd.DataFrame()
sym = list()
period_change = list()
sm_chng = list()
sm_last_day_sig = list()

sym.append("NVDA")
nvda_data = yf.download(tickers="NVDA", start="2021-11-08",end="2022-08-01", interval="1d", progress=False)
start_price = 281.84
end_price = nvda_data.tail(1)["Close"][0]
print('NVDA: start_price = '+str(start_price)+'    end_price = '+str(end_price))
period_change.append(100*(end_price-start_price)/start_price)
[sm_chng_prct,last_day_sig] = sm.buy_sell(sm.squeeze(nvda_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))
sm_chng.append(sm_chng_prct)
sm_last_day_sig.append(last_day_sig)

sym.append("AMD")
amd_data = yf.download(tickers="AMD", start="2021-11-08",end="2022-08-01", interval="1d", progress=False)
start_price = 130.44
end_price = amd_data.tail(1)["Close"][0]
print('AMD: start_price = '+str(start_price)+'    end_price = '+str(end_price))
period_change.append(100*(end_price-start_price)/start_price)
[sm_chng_prct,last_day_sig] = sm.buy_sell(sm.squeeze(amd_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))
sm_chng.append(sm_chng_prct)
sm_last_day_sig.append(last_day_sig)

sym.append("AAPL")
aapl_data = yf.download(tickers="AAPL", start="2022-01-24",end="2022-08-01", interval="1d", progress=False)
start_price = 156.63
end_price = aapl_data.tail(1)["Close"][0]
print('AAPL: start_price = '+str(start_price)+'    end_price = '+str(end_price))
period_change.append(100*(end_price-start_price)/start_price)
[sm_chng_prct,last_day_sig] = sm.buy_sell(sm.squeeze(aapl_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))
sm_chng.append(sm_chng_prct)
sm_last_day_sig.append(last_day_sig)

sym.append("TSLA")
tsla_data = yf.download(tickers="TSLA", start="2022-01-24",end="2022-08-01", interval="1d", progress=False)
start_price = 871.35
end_price = tsla_data.tail(1)["Close"][0]
print('TSLA: start_price = '+str(start_price)+'    end_price = '+str(end_price))
period_change.append(100*(end_price-start_price)/start_price)
[sm_chng_prct,last_day_sig] = sm.buy_sell(sm.squeeze(tsla_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))
sm_chng.append(sm_chng_prct)
sm_last_day_sig.append(last_day_sig)

sym.append("NFLX")
nflx_data = yf.download(tickers="NFLX", start="2022-04-21",end="2022-08-01", interval="1d", progress=False)
start_price = 224.9
print(nflx_data.tail(1)["Close"][0])
end_price = nflx_data.tail(1)["Close"][0]
print('NFLX: start_price = '+str(start_price)+'    end_price = '+str(end_price))
period_change.append(100*(end_price-start_price)/start_price)
[sm_chng_prct,last_day_sig] = sm.buy_sell(sm.squeeze(nflx_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))
sm_chng.append(sm_chng_prct)
sm_last_day_sig.append(last_day_sig)

snp500_ticker_list['symbol'] = sym
snp500_ticker_list['period_change'] = period_change
snp500_ticker_list['Squeeze Momentum change'] = sm_chng
snp500_ticker_list['sm last day sig'] = sm_last_day_sig

# print(snp500_ticker_list.nlargest(10,'Squeeze Momentum change'))
print(snp500_ticker_list)

sum1 = 0
for i in range(0,5):
    sum1 = sum1 + 25000*(1+snp500_ticker_list['period_change'][i]/100)

# print('current holdings value is '+str(sum1)+'  --> '+str(100*(sum1-125000)/125000)+r'% change')
print('current holdings value  --> '+str(float(f'{100*(sum1-125000)/125000:.2f}'))+r'% change')

sum2 = 0
for i in range(0,5):
    sum2 = sum2 + 25000*(1+snp500_ticker_list['Squeeze Momentum change'][i]/100)
# print('possible holdings Squeeze-Momentum value is '+str(sum2)+'  --> '+str(100*(sum2-125000)/125000)+r'% change')
print('possible holdings Squeeze-Momentum value  --> '+str(float(f'{100*(sum2-125000)/125000:.2f}'))+r'% change')

# for i in range(0,nvda_data.shape[0]):
#     if i==0:
#         start_price = nvda_data["Open"][i]
        
#     if i==(nvda_data.shape[0]-1):
#         end_price = nvda_data["Close"][i]
# period_change = (100*(end_price-start_price)/start_price)

# print('NVDA change % = '+str(sm.buy_sell(sm.squeeze(nvda_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))
# print('AMD change % = '+str(sm.buy_sell(sm.squeeze(amd_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))
# print('AAPL change % = '+str(sm.buy_sell(sm.squeeze(aapl_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))
# print('TSLA change % = '+str(sm.buy_sell(sm.squeeze(tsla_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))
# print('NFLX change % = '+str(sm.buy_sell(sm.squeeze(nflx_data.to_numpy(), boll_lookback, boll_vol, kelt_lookback, kelt_vol, 3, 4))))