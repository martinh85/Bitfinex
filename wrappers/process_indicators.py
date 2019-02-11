import talib
from inputs import ALLpairs
import pickle
import pandas as pd

# Get candle data for coin and output a indicator values for last timeframe
def process_indicators(df_price, pair, timeframe):
    timestamp = df_price.index.values
    closes = df_price.close.values
    lows = df_price.low.values
    highs = df_price.high.values
    opens = df_price.open.values
    volumetos = df_price.volume.values

    # EMA
    ema50 = talib.EMA(closes, timeperiod=50)
    ema200 = talib.EMA(closes, timeperiod=200)
    # Distance in %, close to ema50, ema200
    ema50_dist = (ema50 / closes - 1)*100
    ema200_dist = (ema200 / closes - 1)*100

    # BBands
    upperband, middleband, lowerband = talib.BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # Distance in %, close to upper/lower band
    upper_lower_bb_dist = upperband - lowerband
    upper_bb_dist = (upperband / closes - 1)*100
    lower_bb_dist = (lowerband / closes - 1)*100
    # Width of BBands compared to price in %
    width_bb = ((upperband - lowerband) / middleband)*100

    # RSI
    rsi = talib.RSI(closes, timeperiod=14)

    # StochRSI
    stoch_rsi_fastk, stoch_rsi_fastd = talib.STOCHRSI(closes, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    stoch_rsi_fastk = stoch_rsi_fastk
    stoch_rsi_fastd = stoch_rsi_fastd

    # Kijun, Tenkan
    kijun = (max(highs[-60:]) + min(lows[-60:])) / 2
    tenkan = (max(highs[-20:]) + min(lows[-20:])) / 2
    # Distance in %, close to kijun, tenkan
    kijun_dist = (kijun / closes - 1)*100
    tenkan_dist = (tenkan / closes - 1)*100

    # Prepare dict of the calculated indicators for import to dataframe
    str_ind = '_' + pair[0].lower() + '_' + pair[1].lower() + '_' + timeframe
    indicators =  {
            'timestamp': timestamp,
            'ema50_dist' + str_ind: ema50_dist,
            'ema200_dist' + str_ind: ema200_dist,
            'upper_bb_dist' + str_ind: upper_bb_dist,
            'lower_bb_dist' + str_ind: lower_bb_dist,
            'width_bb' + str_ind: width_bb,
            'rsi' + str_ind: rsi,
            'stoch_rsi_fastk' + str_ind: stoch_rsi_fastk,
            'stoch_rsi_fastd' + str_ind: stoch_rsi_fastd,
            'kijun_dist' + str_ind: kijun_dist,
            'tenkan_dist' + str_ind: tenkan_dist
            }

    df = pd.DataFrame(data=indicators)
    df.set_index(['timestamp'], inplace=True)
    df = df.round(2)

    return df

# Not used
def prepade_df_ml(list):
    # Dictionary for merging all timeframes per traded pair
    dict_all_timeframes = {}
    for x in range(4):
        for i in range(0, count(ALLpairs) - 1):
            dict_all_timeframes.update(list[x][i])
        pandas.DataFrame.from_dict(dict_all_timeframes)

# Export indicator into pickle file
def pickle_indicators(tf, list_indicators):
    pickle_filename = 'pickles/' + tf + '_indicators.pickle'
    with open(pickle_filename, 'wb') as handler:
        pickle.dump(list_indicators, handler, protocol=pickle.HIGHEST_PROTOCOL)
    handler.close()

