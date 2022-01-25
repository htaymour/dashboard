# from binance.spot import Spot
from binance import Client
import pandas as pd

#client = Spot()
# print(client.time())

# client = Spot(key='LYL3DSi8nr7WK9O2k4DXUO8jqeb4ZkzZJ6djakO9awHj24pFDsaloon2UCPVAkLR', secret='MBbOS784jdh9JpPndugGtZaKMmTAoHny23xSZQJKFHKKoWk7gEZ3eqivhiUg88Yy')
# print(client.account())

#api_key = 'LYL3DSi8nr7WK9O2k4DXUO8jqeb4ZkzZJ6djakO9awHj24pFDsaloon2UCPVAkLR'
#api_secret = 'MBbOS784jdh9JpPndugGtZaKMmTAoHny23xSZQJKFHKKoWk7gEZ3eqivhiUg88Yy'

# TESTNET SPOT
api_key = 'v7qLX9erMafm29cabyeTKfGxYSvsb7M4GwjXWPoJZzXMFhLC5lS7nbGMX1MVUFta'
api_secret = '2xunD6Z1mMWHkXjMrDI3wtu3773huMAmuVLN9SgCWHe4poIYXwnX0yxeOFqC7kdP'


client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'   # for TESTNET SPOT
tickers = client.get_all_tickers()
ticker_df = pd.DataFrame(tickers)
ticker_df.set_index('symbol', inplace=True)
float(ticker_df.loc['ETHBTC']['price'])
depth = client.get_order_book(symbol='BTCUSDT')  # market depth means the bids that happened to certain coin pain
depth_df = pd.DataFrame(depth['asks'])
depth_df.columns = ['Price', 'Volume']
depth_df.head()

# GET HISTORICAL DATA
#  [[
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore.
#   ]]


historical = client.get_historical_klines('ETHBTC', Client.KLINE_INTERVAL_15MINUTE, '1 Aug 2021')
hist_df = pd.DataFrame(historical)
print(hist_df.head())
hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
print(hist_df.head())
print(hist_df)
print(hist_df.dtypes)

hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
print(hist_df.info())
print(hist_df.describe())


import mplfinance as mpf
print(hist_df.set_index('Close Time').tail(100))
mpf.plot(hist_df.set_index('Close Time').tail(120), 
        type='candle', style='charles', 
        volume=True, 
        title='ETHBTC Last 120 Days', 
        mav=(10,20))  

print("\n".join(dir(client))) 



