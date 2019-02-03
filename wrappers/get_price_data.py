import wrappers.cryptocompare_wrapper as cc
import wrappers.bitfinex_api as bf
import wrappers.binance_api as bn
from inputs import from_date, to_date

# Process timeframe input ('1m', '5m', '15m', '1h', '4h', '1d') to prepare
# parameters for API query - tf (timeframe), limit (how many time-series is
# loaded for each timeframe, max. 2000 per 1 call,
# it is possible to ask for all historical data)

def get_price_data(pair, timeframe, hist):

    # Convert timeframe to be used as parameter for api call
    tf = int(timeframe[:-1])

    # Set how many time-series is loaded for each timeframe,
    # max. 2000 per 1 call, possible to ask for all historical data
    if tf == 1:
        limit = 200
    if tf == 4:
        limit = 800
    if tf == 5:
        limit = 1000
    if tf == 15:
        limit = 2000


    # Process trading pair input list (['ETH', 'USD'],..) to prepare
    # parameter for API query - exchange:
    # BTC/USD - Coinbase
    # USD pairs - LLweb_data
    # BTC pairs - Binance
    if pair[0] == 'BTC':
        exchange = 'coinbase'
    if pair[0] != 'BTC' and pair[1] == 'USD':
        exchange = 'bitfinex'
    if pair[1] == 'BTC':
        exchange = 'binance'

    if hist == False:
        # Load 1 minute timeframe price data,
        # 1m, 5m, 15m and 30m data is boundled from 1m price data
        if timeframe == '1m':
            if exchange == 'bitfinex':
                return  bf.minute_last_bitfinex(pair[0], pair[1])
                #cc.minute_price_query(
                #pair[0], pair[1], limit=limit, aggregate=tf, exchange=exchange)
            if exchange == 'binance':
                return  bn.minute_last_binance(pair[0], pair[1])

        if timeframe in ['1m,', '5m', '15m']:
            return cc.minute_price_query(
                pair[0], pair[1] , limit=limit, aggregate=tf, exchange=exchange)

        # Load 1 hour timeframe price data,
        # 1h, 4h and 12h data is boundled from 1h price data
        if timeframe in ['1h', '4h']:
            return cc.hourly_price_query(
                pair[0], pair[1], limit=limit, aggregate=tf, exchange=exchange)

        # Load 1 day timeframe price data
        if timeframe == '1d':
            return cc.daily_price_query(
            pair[0], pair[1], limit=limit, aggregate = tf, exchange=exchange)


    if hist == True:

        if timeframe == '1m':
            return cc.get_1m_price_historical(pair[0], pair[1], limit=1, exchange=exchange, from_date=from_date, to_date=to_date)

        if timeframe == '1h':
            return cc.get_1h_price_historical(pair[0], pair[1], limit=1, exchange=exchange, from_date=from_date, to_date=to_date)
    print(pair[0], '/', pair[1], 'on', timeframe, 'timeframe loaded.')

if __name__ == "__main__":
    pair = int(sys.argv[1])
    timeframe = int(sys.argv[2])
    load_price_data(pair, timeframe)