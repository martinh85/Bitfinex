from wrappers.get_price_data import get_price_data
import wrappers.process_indicators as process_indicators

import time
import psycopg2
from config import config

# Import list of traded pairs form get_timeframe_data file
from inputs import ALLpairs

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    for pair in ALLpairs:
        last1m = list(get_price_data(pair, '1m', hist=False))
        holder = int(str(last1m[0])[:-3])
        ts = time.gmtime(holder)
        last1m[0] = time.strftime("%Y-%m-%d %H:%M", ts)
        print(last1m)
        print(pair[0])
        cur.execute("DROP TABLE IF EXISTS data_1m_" + str(pair[0]) + "_" + str(pair[1]))
        cur.execute("CREATE TABLE IF NOT EXISTS data_1m_" + str(pair[0]) + "_" + str(pair[1]) + """(
                        timestamp timestamp PRIMARY KEY,
                        open DECIMAL(13,8),
                        close DECIMAL(13,8),
                        high DECIMAL(13,8),
                        low DECIMAL(13,8),
                        volume DECIMAL(13,8));""")
        cur.execute("INSERT INTO data_1m_" +
                        str(pair[0]) + "_" + str(pair[1]) +
                        " VALUES(%s, %s, %s, %s, %s, %s)", last1m)
        conn.commit()
    conn.close()

### Save to 1m database

# Get actual time
#time = time.gmtime()

# Get 5m price data
#if time[4] % 5 == 0:
### Query database for last x entries
# save to dataframe
# process indicators
# save indicators to pickle

### for every timeframe change, reload new plots

### ! just for strategies from ML, for every timeframe change, reload combination of pickles for all timeframes


# Get 5m minute price data

    # Update database


# Get 15m price data
#if time[4] % 15 == 0:

# Get 1h price data
#if time[4] % 60 == 0:

# Get 4h price data
#if time[4] % 60 == 0 and time[3] % 4 == 0:

# Get 1d price data
#if time[4] % 60 == 0 and time[3] % 24 == 0:
