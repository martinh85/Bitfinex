import requests
import datetime
import pandas as pd

def daily_price_query(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def hourly_price_query(symbol, comparison_symbol, limit, aggregate, exchange):
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def minute_price_query(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

#https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=2000&aggregate=1&toTs=1500000000
def hourly_price_query_hist(symbol, comparison_symbol, limit, date, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit=2000&aggregate={}&toTs={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, date)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    print(data)
    return data

# Function for merging dataframes of all historical hourly price data, returns final dataframe
def get_1h_price_historical(symbol, comparison_symbol, limit, exchange, from_date, to_date):
    """ Get historical price data between two dates. """
    date = to_date
    holder = []
    # While the earliest date returned is later than the earliest date requested, keep on querying the API
    # and adding the results to a list.
    while date > from_date:
        data = hourly_price_query_hist(symbol=symbol, comparison_symbol=comparison_symbol,
            limit=limit, exchange=exchange, date=date)

        print(data)
        holder.append(pd.DataFrame(data['Data']))
        # Set datestamp to last queried line
        date = data['TimeFrom'] - 1
    # Join together all of the API queries in the list.
    df = pd.concat(holder, axis = 0)
    # Remove rows with no values
    df = df[df['close'] != 0]
    # Remove data points from before from_date
    # df = df[df['time']>from_date]
    # Convert to timestamp to readable date format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Make the DataFrame index the time
    df.set_index('time', inplace=True)
    # And sort it so its in time order
    df.sort_index(ascending=False, inplace=True)
    # Export dataframe to csv file
    timeframe = str(limit) + 'h'
    df.to_csv('datasets/' + symbol + '_'
              + comparison_symbol + '_' + timeframe + '.csv')
    return df

# Query used for loading all historical minute price data
def minute_price_query_hist(symbol, comparison_symbol, limit, date, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=2000&aggregate={}&toTs={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, date)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data

# Function for merging dataframes of all historical minute price data, returns final dataframe
def get_1m_price_historical(symbol, comparison_symbol, limit, exchange, from_date, to_date):
    """ Get historical price data between two dates. """
    date = to_date
    holder = []
    # While the earliest date returned is later than the earliest date requested, keep on querying the API
    # and adding the results to a list.
    while date > from_date:
        data = minute_price_query_hist(symbol=symbol, comparison_symbol=comparison_symbol,
            limit=limit, date=date, exchange=exchange )

        print(data)
        holder.append(pd.DataFrame(data['Data']))
        # Set datestamp to last queried line
        date = data['TimeFrom'] - 1
    # Join together all of the API queries in the list.
    df = pd.concat(holder, axis = 0)
    # Remove rows with no values
    df = df[df['close'] != 0]
    # Remove data points from before from_date
    # df = df[df['time']>from_date]
    # Convert to timestamp to readable date format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Make the DataFrame index the time
    df.set_index('time', inplace=True)
    # And sort it so its in time order
    df.sort_index(ascending=False, inplace=True)
    # Export dataframe to csv file
    timeframe = str(aggregate) + 'm'
    df.to_csv('datasets/' + symbol + '_'
              + comparison_symbol + '_' + timeframe + '.csv')
    return df

