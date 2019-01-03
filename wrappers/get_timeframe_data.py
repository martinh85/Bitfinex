import pandas as pd
import wrappers.cryptocompare_wrapper as cryptocompare_wrapper

# List of traded pairs
list_pairs = [['BTC','USD'],
            ['ETH','USD'], ['XRP','USD'], ['LTC','USD'], ['EOS','USD'], ['IOT','USD'], ['XMR','USD'], ['ZEC','USD'],
            ['NEO','USD'], ['XLM','USD'], ['ETC','USD'], ['DASH','USD'], ['OMG','USD'],
            ['ETH','BTC'], ['XRP','BTC'], ['LTC','BTC'], ['EOS','BTC'], ['IOT','BTC'], ['XMR','BTC'], ['ZEC','BTC'],
            ['NEO','BTC'], ['XLM','BTC'], ['ETC','BTC'], ['DASH','BTC'], ['OMG','BTC']]
list_df_prices = []

# Load list of dataframes of all pairs candles: 1st BTCUSD, 2nd USD pairs list of dataframes,
# 3rd BTC pairs list of dataframes, 4th list of coin names
def check_timeframe(timeframe):
    print('Loading price data dataframes:')
    # Load minute candles
    if timeframe == '1m' or timeframe == '5m' or timeframe == '15m' or timeframe == '30m':
        tf = int(timeframe[:-1])

        # Set number of candles loaded for each timeframe
        if tf == 1:
            limit = 200
        if tf == 5:
            limit = 1000
        if tf == 15:
            limit = 2000
        if tf == 30:
            limit = 2000

        # Load price dfs for all pairs
        for pair in list_pairs:
            if pair[0] == 'BTC':
                exchange = 'coinbase'
            if pair[0] != 'BTC' and pair[1] == 'USD':
                exchange = 'bitfinex'
            if pair[1] == 'BTC':
                exchange = 'binance'

            list_df_prices.append(cryptocompare_wrapper.minute_price_historical(pair[0], pair[1] , limit=limit,
                                                      aggregate=tf, exchange=exchange))
            print(pair[0],'/', pair[1])
            print(list_df_prices[-1])

    # Load hourly candles
    if timeframe == '1h' or timeframe == '4h':
        tf = int(timeframe[:-1])

        # Set number of candles loaded for each timeframe
        if tf == 1:
            limit = 200
        if tf == 4:
            limit = 800

        # Load price dfs for all pairs
        for pair in list_pairs:
            if pair[0] == 'BTC':
                exchange = 'coinbase'
            if pair[0] != 'BTC' and pair[1] == 'USD':
                exchange = 'bitfinex'
            if pair[1] == 'BTC':
                exchange = 'binance'

            list_df_prices.append(cryptocompare_wrapper.hourly_price_historical(pair[0], pair[1] , limit=limit,
                                                      aggregate=tf, exchange=exchange))
            print(pair[0],'/', pair[1])
            print(list_df_prices[-1])

    # Load daily candles
    if timeframe == '1d':
        tf = int(timeframe[:-1])
        limit = 200

        # Load price dfs for all pairs
        for pair in list_pairs:
            if pair[0] == 'BTC':
                exchange = 'coinbase'
            if pair[0] != 'BTC' and pair[1] == 'USD':
                exchange = 'bitfinex'
            if pair[1] == 'BTC':
                exchange = 'binance'

            list_df_prices.append(cryptocompare_wrapper.daily_price_historical(pair[0], pair[1] , limit=limit,
                                                      aggregate=tf, exchange=exchange))
            print(pair[0],'/', pair[1])
            print(list_df_prices[-1])

    return list_df_prices