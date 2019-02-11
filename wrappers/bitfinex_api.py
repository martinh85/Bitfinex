from bitfinex import WssClient, ClientV2, ClientV1
# info: https://bitfinex.readthedocs.io/en/latest/restv2.html

import pandas as pd
import datetime


bfx_client = ClientV2(key='nJKOHF9lPF5sx2HyIxl2YsWTY4zITMe6u7vsdv1Xhet',
                      secret='QpTdEuHaREhH8lKBM0DRpYxwNLvE56iCqa3B3sitrCl')

def bitfinex_candles(symbol, comparison_symbol, timeframe, limit):
    pair = 't' + symbol + comparison_symbol
    # If queried timeframe is not Bitfinex standard query, aggregated 1h timeframe will be used
    if timeframe in ['4h', '12h']:
        data = bfx_client.candles('1h', pair, 'hist', limit=limit)
        # Prepare final dataframe
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'close', 'high', 'low', 'volume'])
        df['timestamp'] = [int(str(timestamp)[:-3]) for timestamp in df.timestamp]
        df['timestamp'] = [datetime.datetime.fromtimestamp(timestamp)
                           for timestamp in df.timestamp]

        # Drop duplicate values in timestamp column
        df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)

        df['volume'] = df['volume'].round(2)
        df.set_index(['timestamp'], inplace=True)
        df = df.sort_index(ascending=True)

        # Resample data for 12h timeframe
        if timeframe == '12h':
            df = df.resample('12h', closed='right', label='right', loffset='2h').agg({
                'open': lambda s: s[0],
                'close': lambda df: df[-1],
                'high': lambda df: df.max(),
                'low': lambda df: df.min(),
                'volume': lambda df: df.sum()
            })

        if timeframe == '4h':
            df = df.resample('4h', closed='right', label='right').agg({
                'open': lambda s: s[0],
                'close': lambda df: df[-1],
                'high': lambda df: df.max(),
                'low': lambda df: df.min(),
                'volume': lambda df: df.sum()
            })

    else:
        # Make API query
        data = bfx_client.candles(timeframe, pair, 'hist', limit=limit)
        # Prepare final dataframe
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'close', 'high', 'low', 'volume'])
        df['timestamp'] = [int(str(timestamp)[:-3]) for timestamp in df.timestamp]
        df['timestamp'] = [datetime.datetime.fromtimestamp(timestamp)
                           for timestamp in df.timestamp]

        # Drop duplicate values in timestamp column
        df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)

        df['volume'] = df['volume'].round(2)
        df.set_index(['timestamp'], inplace=True)
        df = df.sort_index(ascending=True)

    print(symbol, comparison_symbol, df.head(1))
    return df
