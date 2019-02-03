import pandas as pd
import wrappers.cryptocompare_wrapper as cryptocompare_wrapper
from inputs import ALLpairs`
import datetime

list_df_prices = []

# Returns list of dataframes with all historical price data
# for all trading pairs for selected timeframe
def get_all_data(timeframe, from_date, to_date, hist=False):
    print('Loading price data dataframes:')

    # Load 1 minute timeframe price data,
    # 5m, 15m data is boundled from 1m price data
    if hist == False:
        if timeframe == '1m' or timeframe == '5m' or \
            timeframe == '15m' :

            # Convert timeframe to be used as parameter for api call
            tf = int(timeframe[:-1])

            # Load price dataframes for all pairs, from these exchanges:
            # BTC/USD - Coinbase
            # USD pairs - LLweb_data
            # BTC pairs - Binance
            for pair in ALLpairs:
                if pair[0] == 'BTC':
                    exchange = 'coinbase'
                if pair[0] != 'BTC' and pair[1] == 'USD':
                    exchange = 'bitfinex'
                if pair[1] == 'BTC':
                    exchange = 'binance'

                list_df_prices.append(
                    cryptocompare_wrapper.get_all_minute_price_historical(
                        pair[0], pair[1], aggregate=tf, exchange=exchange,
                        from_date=from_date, to_date=to_date))

                print(pair[0],'/', pair[1])

        # Load 1 hour timeframe price data,
        # 1h, 4h and 12h data is boundled from 1h price data
        if timeframe == '1h' or timeframe == '4h':

            tf = int(timeframe[:-1])

            for pair in ALLpairs:
                if pair[0] == 'BTC':
                    exchange = 'coinbase'
                if pair[0] != 'BTC' and pair[1] == 'USD':
                    exchange = 'bitfinex'
                if pair[1] == 'BTC':
                    exchange = 'binance'

                list_df_prices.append(
                    cryptocompare_wrapper.get_all_hourly_price_historical(
                        pair[0], pair[1], aggregate=tf, exchange=exchange,
                        from_date=from_date, to_date=to_date))

                print(pair[0],'/', pair[1])

        # Load 1 day timeframe price data
        if timeframe == '1d':
            tf = int(timeframe[:-1])
            limit = 200

            for pair in ALLpairs:
                if pair[0] == 'BTC':
                    exchange = 'coinbase'
                if pair[0] != 'BTC' and pair[1] == 'USD':
                    exchange = 'bitfinex'
                if pair[1] == 'BTC':
                    exchange = 'binance'

                list_df_prices.append(
                    cryptocompare_wrapper.get_all_daily_price_historical(
                        pair[0], pair[1], aggregate=tf, exchange=exchange,
                        from_date=from_date, to_date=to_date))
                print(pair[0],'/', pair[1])

        return list_df_prices

    if hist == True:


