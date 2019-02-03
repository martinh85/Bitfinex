from  wrappers.get_price_data import get_price_data
# Import list of traded pairs
from inputs import ALLpairs

import psycopg2
from config import config


timeframe = '1h'


#if timeframe == '1m':
    #for pair in ALLpairs:
        # Load list of dataframes with price data of all trading pairs
        #df = get_1m_price_historical(symbol, comparison_symbol, limit=1, exchange, from_date, to_date)

#if timeframe == '1h':
for pair in ALLpairs:
#pair = ['ETH', 'USD']
# Load list of dataframes with price data of all trading pairs
    df = get_price_data(pair, timeframe, hist=True)


# Database
# !/usr/bin/python


#if __name__ == '__main__':
#     connect()
