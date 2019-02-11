from binance.client import Client
# info: https://python-binance.readthedocs.io/en/latest/market_data.html

import pandas as pd
import datetime

client = Client(
    api_key='rpDyJOR9w2Y4LaLk05RKuRONQ4kh5HrkdWe2Uox5QIKkq8DZV0UbXKvDEB2EoOZA',
    api_secret='tG4c0tZict5oD8VpaIrgJgPutatBBKrEnMFugIL7Jjj9Iwbf3UrcaCzhvsBVEn9r')

# OCHLV
# client.get_historical_klines
# ("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "2 minute ago UTC")
def binance_candles(symbol, comparison_symbol, timeframe, limit):
    pair = symbol + comparison_symbol
    if timeframe == '5m':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_5MINUTE,
        "2 days ago UTC")#"2 days ago UTC")
    if timeframe == '15m':
        data = client.get_historical_klines(
            pair, Client.KLINE_INTERVAL_15MINUTE,
        "5 days ago UTC") #5
    if timeframe == '30m':
        data = client.get_historical_klines(
            pair, Client.KLINE_INTERVAL_30MINUTE,
        "10 days ago UTC") #10
    if timeframe == '1h':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_1HOUR,
        "20 days ago UTC") #20
    if timeframe == '3h':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_4HOUR,
        "80 days ago UTC") #80
    if timeframe == '6h':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_6HOUR,
        "110 days ago UTC") #110
    if timeframe == '12h':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_12HOUR,
        "220 days ago UTC") #220
    if timeframe == '1D':
        data = client.get_historical_klines(
        pair, Client.KLINE_INTERVAL_1DAY,
        "420 days ago UTC") #420
    # Remove unnecessary data from query
    data = [row[:6] for row in data]
    # Prepare final dataframe
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = [int(str(timestamp)[:-3]) for timestamp in df.timestamp]
    df['timestamp'] = [datetime.datetime.fromtimestamp(timestamp)
                       for timestamp in df.timestamp]

    # Set standardized order of columns
    df = df[['timestamp', 'open', 'close', 'high', 'low', 'volume']]

    # Set numeric types for columns
    df[['open', 'close', 'high', 'low', 'volume']] = df[[
        'open', 'close', 'high', 'low', 'volume']].apply(pd.to_numeric)

    # Drop duplicate values in timestamp column
    df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)

    df['volume'] = df['volume'].round(2)
    df.set_index(['timestamp'], inplace=True)
    print(symbol, comparison_symbol, df.head(1))
    return df



