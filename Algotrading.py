import requests
import numpy as np
import time
from sklearn import linear_model

# proxy_servers = {
#    # 'http': '81.200.157.225:17100',
#     'https': '81.200.157.149:17100'
#     #'http://secureproxy.sample.com:8080',
# }

def get_price():
    url = 'https://api.binance.com/api/v3/ticker/price'
    params_eth = {'symbol': 'ETHUSDT'}
    params_btc = {'symbol': 'BTCUSDT'}
    response_eth = requests.get(url, params=params_eth)#, proxies=proxy_servers)
    response_btc = requests.get(url, params=params_btc)#, proxies=proxy_servers)
    data_eth = response_eth.json()
    data_btc = response_btc.json()
    price_eth = float(data_eth['price'])
    price_btc = float(data_btc['price'])
    return price_eth, price_btc

def get_historical_data():
    url = 'https://api.binance.com/api/v3/klines'
    params_eth = {'symbol': 'ETHUSDT', 'interval': '1h', 'limit': 1000}
    params_btc = {'symbol': 'BTCUSDT', 'interval': '1h', 'limit': 1000}
    response_eth = requests.get(url, params=params_eth)#, proxies=proxy_servers)
    response_btc = requests.get(url, params=params_btc)#, proxies=proxy_servers)
    data_eth = response_eth.json()
    data_btc = response_btc.json()
    eth_prices = []
    btc_prices = []

    for h in data_eth:
        eth_prices.append(float(h[4]))

    for h in data_btc:
        btc_prices.append(float(h[4]))

    return eth_prices, btc_prices

def linreg():
    eth_prices, btc_prices = get_historical_data()
    btc_np = np.array(btc_prices)
    eth_np = np.array(eth_prices)
    X = btc_np.reshape((-1, 1))
    Y = eth_np
    model = linear_model.LinearRegression()
    model.fit(X, Y)
    predictions = model.predict(X)
    residual = Y - predictions
    return residual

while True:
    price_eth, price_btc = get_price()
    print(f'Price ETHUSDT: {price_eth} USD, Price BTCUSDT: {price_btc} USD')
    residual = linreg()
    last_5min_residual = residual[-12:]
    last_residual = last_5min_residual[-1]
    change_pct = abs(last_residual / price_eth) * 100
    if change_pct > 1:
        print(f'Price ETHUSDT has moved by {change_pct:.2f}% in the last 5 minutes')

    time.sleep(5)