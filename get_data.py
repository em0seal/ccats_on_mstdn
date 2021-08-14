import datetime
import requests

import pandas as pd


# Return DataFrame of Bitcoin historical data
# https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataHistoday
def get_crypto_hist_from_cryptocompare(
        from_symbol='BTC',      # other ex. ETH
        target_symbol='USD',    # other ex. JPY, EUR
        exchange=None,          # default -> cccagg_or_exchange(cryptocompare original)
                                # other ex. 'bitFlyer'
        limit=1,
        aggregate=1,
        allData='true'):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}&allData={}'\
        .format(from_symbol.upper(), target_symbol.upper(), limit, aggregate, allData)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


def save_df(df, file_name, suffix):
    file_name = file_name+'.'+suffix
    if suffix == 'csv':
        df.to_csv(file_name)
    if suffix == 'html':
        df.to_html(file_name)
    if suffix == 'json':
        df.to_json(file_name)


def get_data(save_filename, suffix):
    df_btc2usd = get_crypto_hist_from_cryptocompare()
    save_df(df_btc2usd, save_filename, suffix)
