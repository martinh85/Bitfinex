import wrappers.cryptocompare_wrapper as cc
import wrappers.bitfinex_api as bf
import wrappers.binance_api as bn
from inputs import from_date, to_date
from wrappers.process_indicators import process_indicators

def get_price_data(pair, timeframe, cur, hist):

    # Request data limited to date
    if hist == False:
        # Load price data form exchange
        if pair[1] == 'USD':
            df = bf.bitfinex_candles(pair[0], pair[1], timeframe, limit=420)
        if pair[1] == 'BTC':
            df = bn.binance_candles(pair[0], pair[1], timeframe, limit=420)


        # --- PRICE DATA ---

        # Prepare price data file name
        price_data_name = "price_data_" + "_" + str(pair[0]).lower() \
                          + "_" + str(pair[1]).lower() + "_" + timeframe
        # Optionally drop the table
        # cur.execute("DROP TABLE " + price_data_name)
        # Prepare price data table if data is loaded for the first time
        cur.execute("CREATE TABLE IF NOT EXISTS " + price_data_name + """(
                                    timestamp timestamp PRIMARY KEY,
                                    open DECIMAL(13,8),
                                    close DECIMAL(13,8),
                                    high DECIMAL(13,8),
                                    low DECIMAL(13,8),
                                    volume DECIMAL(13,2));""")
        # Select last recorded timestamp of price data table in database
        cur.execute("SELECT MAX(timestamp) FROM " + price_data_name)
        last = cur.fetchone()
        # Prepare upload to database based on whether table is empty or not
        if last[0] != None:
            # Prepare dataframe with price data not loaded to database yet
            df_recent = df.loc[df.index > last[0]]
            # Export data to csv
            df_recent.to_csv("data/csv/price_data/" + price_data_name + ".csv")
        else:
            # Export data to csv
            df.to_csv("data/csv/price_data/" + price_data_name + ".csv")
        # Load price data to database
        with open("data/csv/price_data/" + price_data_name + ".csv") as f:
            cur.copy_expert("COPY " + price_data_name + " FROM STDIN WITH CSV HEADER", f)

        # --- INDICATORS ---

        # Prepare indicators file name
        indicators_name = "indicators_" + "_" + str(pair[0]).lower() \
                          + "_" + str(pair[1]).lower() + "_" + timeframe
        # Compute indicators, load to dataframe
        df_indicators = process_indicators(df, pair, timeframe)
        # Prepare string for SQL query CREATE TABLE with indicators imported from dataframe's columns
        # Get indicator names from dataframe
        indicators = list(df_indicators.dtypes.index)
        db_values_import_string = str()
        # Append string for each
        for ind in indicators:
            db_values_import_string += ', ' + ind
            # Enable specific type for indicator
            # if ind == :
            # db_values_import_string += ' DECIMAL(13,8),'
            # break
            db_values_import_string += ' DECIMAL(5,2)'
        # Prepare indicators data table if data is loaded for the first time
        # Optionally drop the table
        # cur.execute("DROP TABLE " + indicators_name)
        cur.execute("CREATE TABLE IF NOT EXISTS " + indicators_name +
                    "(timestamp timestamp PRIMARY KEY" +
                    db_values_import_string + ");")
        # Select last recorded timestamp of indicators data table in database
        cur.execute("SELECT MAX(timestamp) FROM " + indicators_name)
        last = cur.fetchone()
        # Prepare upload to database based on whether table is empty or not
        if last[0] != None:
            print(last[0])
            # Prepare dataframe with indicators data not loaded to database yet
            df_ind_recent = df_indicators.loc[df_indicators.index > last[0]]
            # Export data to csv
            df_ind_recent.to_csv("data/csv/indicators/" + indicators_name + ".csv")
        else:
            # Export data to csv
            df_indicators.to_csv("data/csv/indicators/" + indicators_name + ".csv")
        # Load indicators data to database
        with open("data/csv/indicators/" + indicators_name + ".csv") as f:
            cur.copy_expert("COPY " + indicators_name + " FROM STDIN WITH CSV HEADER", f)
        return None

    # Request all historical data
    if hist == True:
        if timeframe == '1m':
            return cc.get_1m_price_historical(pair[0], pair[1], limit=1, exchange=exchange, from_date=from_date, to_date=to_date)
        if timeframe == '1h':
            return cc.get_1h_price_historical(pair[0], pair[1], limit=1, exchange=exchange, from_date=from_date, to_date=to_date)
    print(pair[0], '/', pair[1], 'on', timeframe, 'timeframe loaded.')

def save_to_database(df):
    last_candle = df.iloc[1]
    last_candle = last_candle.tolist()
    cur.execute("DROP TABLE IF EXISTS data_5m_" + str(pair[0]) + "_" + str(pair[1]))
    cur.execute("CREATE TABLE IF NOT EXISTS data_5m_" + str(pair[0]) + "_" + str(pair[1]) + """(
                    timestamp timestamp PRIMARY KEY,
                    open DECIMAL(13,8),
                    close DECIMAL(13,8),
                    high DECIMAL(13,8),
                    low DECIMAL(13,8),
                    volume DECIMAL(15,8));""")
    cur.execute("INSERT INTO data_5m_" +
                str(pair[0]) + "_" + str(pair[1]) +
                " VALUES(%s, %s, %s, %s, %s, %s)", last_candle)
def prepare_df(data):
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'close', 'high', 'low', 'volume'])
    df['timestamp'] = [int(str(timestamp)[:-3]) for timestamp in df.timestamp]
    df['timestamp'] = [datetime.datetime.fromtimestamp(timestamp)
                       for timestamp in df.timestamp]
    return df

# Insert last data to database
def insert_last_data(df, timeframe):
    tableName = "data_" + timeframe + "_" + str(pair[0]).lower()\
                + "_" + str(pair[1]).lower()
    last_candle = df.iloc[1]
    last_candle = last_candle.tolist()
    cur.execute("DROP TABLE IF EXISTS " + tableName)  # data_5m_" + str(pair[0]) + "_" + str(pair[1]))
    cur.execute("CREATE TABLE IF NOT EXISTS " + tableName + """(
                                timestamp timestamp PRIMARY KEY,
                                open DECIMAL(13,8),
                                close DECIMAL(13,8),
                                high DECIMAL(13,8),
                                low DECIMAL(13,8),
                                volume DECIMAL(12,2));""")
    cur.execute("INSERT INTO data_5m_" +
                str(pair[0]) + "_" + str(pair[1]) +
                " VALUES(%s, %s, %s, %s, %s, %s)", last_candle)

def insert_data(df, pair, timeframe, cur):
    tableName = "data_" + timeframe + "_" + str(pair[0]).lower()\
                + "_" + str(pair[1]).lower()
    df.to_csv("data/csv/" + tableName + ".csv")
    cur.execute("DROP TABLE IF EXISTS " + tableName)  # data_5m_" + str(pair[0]) + "_" + str(pair[1]))
    cur.execute("CREATE TABLE IF NOT EXISTS " + tableName + """(
                                timestamp timestamp PRIMARY KEY,
                                open DECIMAL(13,8),
                                close DECIMAL(13,8),
                                high DECIMAL(13,8),
                                low DECIMAL(13,8),
                                volume DECIMAL(12,2));""")
    with open("data/csv/" + tableName + ".csv") as f:
        cur.copy_expert("COPY " + tableName + " FROM STDIN WITH CSV HEADER", f)
#if __name__ == "__main__":
#    pair = int(sys.argv[1])
#    timeframe = int(sys.argv[2])
#    load_price_data(pair, timeframe)