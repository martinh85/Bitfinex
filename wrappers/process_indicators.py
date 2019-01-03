import talib

# Get candle data for coin and output a indicator values for last timeframe
def process_indicators(df_price, timeframe):
    closes = df_price.close.values
    lows = df_price.low.values
    highs = df_price.high.values
    opens = df_price.open.values
    volumetos = df_price.volumeto.values

    # EMA
    ema50 = talib.EMA(closes, timeperiod=50)
    ema200 = talib.EMA(closes, timeperiod=200)
    # Distance in %, close to ema50, ema200
    ema50_dist = ema50 / closes - 1
    ema200_dist = ema200 / closes - 1

    # BBands
    upperband, middleband, lowerband = talib.BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # Distance in %, close to upper/lower band
    upper_bb_dist = upperband / closes - 1
    lower_bb_dist = lowerband / closes - 1
    # Width of BBands compared to price in %
    width_bb = (upperband - lowerband) / middleband

    # RSI
    rsi = talib.RSI(closes, timeperiod=14) / 100

    # StochRSI
    stoch_rsi_fastk, stoch_rsi_fastd = talib.STOCHRSI(closes, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    stoch_rsi_fastk = stoch_rsi_fastk / 100
    stoch_rsi_fastd = stoch_rsi_fastd / 100

    # Kijun, Tenkan
    kijun = (max(highs[-60:]) + min(lows[-60:])) / 2
    tenkan = (max(highs[-20:]) + min(lows[-20:])) / 2
    # Distance in %, close to kijun, tenkan
    kijun_dist = kijun / closes - 1
    tenkan_dist = tenkan / closes - 1

    # Returns dict of last elements of the calculated indicators
    return {'ema50_dist_'+ timeframe: ema50_dist[-1],
            'ema200_dist_'+ timeframe: ema200_dist[-1],
            'upper_bb_dist_'+ timeframe: upper_bb_dist[-1],
            'lower_bb_dist_'+ timeframe: lower_bb_dist[-1],
            'width_bb_'+ timeframe: width_bb[-1],
            'rsi_'+ timeframe: rsi[-1],
            'stoch_rsi_fastk_'+ timeframe: stoch_rsi_fastk[-1],
            'stoch_rsi_fastd_'+ timeframe: stoch_rsi_fastd[-1],
            'kijun_dist_'+ timeframe: kijun_dist[-1],
            'tenkan_dist_'+ timeframe: tenkan_dist[-1]
            }

