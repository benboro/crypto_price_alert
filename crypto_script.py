from requests import Session
import json
from datetime import datetime
from dateutil import tz
import pandas as pd
import os
from playsound import playsound


def get_current_price(coin='DOGE'):
    """Retrieves the current price for given coing from CoinMarketCap.com using their API"""
    API_KEY = '000-API-KEY-000'
    API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    # get data from CoinMarketCap API
    parameters = {'symbol': coin}
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': API_KEY}
    session = Session()
    session.headers.update(headers)
    response = session.get(API_URL, params=parameters)

    # get only the price and timestamp from the data
    data = json.loads(response.text)['data'][parameters['symbol']]['quote']['USD']
    cprice = data['price']
    ctime = datetime.strptime(data['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ')\
        .replace(tzinfo=tz.gettz('UTC'))\
        .astimezone(tz.tzlocal())
    return cprice, ctime


# get current coin value (in USD)
coin_name = 'DOGE'
coin_price, coin_time = get_current_price(coin=coin_name)
coin_df = pd.DataFrame({'timestamp': [datetime.strftime(coin_time, '%Y-%m-%d %H:%M')], 'price': [coin_price]})

# specify what sounds to play when coin value changes
sound_up = './dmx_bark.mp3'
sound_down = './napalmDeath_youSuffer.mp3'
fpath = './{}_log.csv'.format(coin_name).lower()

# do action if log exists, otherwise create log
if os.path.exists(fpath):

    # get previous value and compare with current value
    past_df = pd.read_csv(fpath)
    last_price = past_df.iloc[-1]['price']
    if coin_price > last_price:
        print('{} is up by {}'.format(coin_name, round(coin_price - last_price, 4)))
        playsound(sound_up)
    else:
        print('{} is down by {}'.format(coin_name, round(last_price - coin_price, 4)))
        playsound(sound_down)

    # append new data to log
    total_df = past_df.append(coin_df, ignore_index=True)
    total_df.to_csv(fpath, index=False)
else:
    coin_df.to_csv(fpath, index=False)


