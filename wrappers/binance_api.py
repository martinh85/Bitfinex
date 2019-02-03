from binance.client import Client
# info: https://python-binance.readthedocs.io/en/latest/market_data.html

client = Client(api_key='rpDyJOR9w2Y4LaLk05RKuRONQ4kh5HrkdWe2Uox5QIKkq8DZV0UbXKvDEB2EoOZA',
                api_secret='tG4c0tZict5oD8VpaIrgJgPutatBBKrEnMFugIL7Jjj9Iwbf3UrcaCzhvsBVEn9r')

# OCHLV
# client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "2 minute ago UTC")
def minute_last_binance(symbol, comparison_symbol):
    data = client.get_historical_klines(str(symbol)+str(comparison_symbol), Client.KLINE_INTERVAL_1MINUTE, "2 minute ago UTC")
    data = data[0][:6]
    data = [float(i) for i in data]
    data[0] = int(data[0])
    # Set predefined order of price data - TOCHLV
    newOrder = [0, 1, 4, 2, 3, 5]
    data = [data[i] for i in newOrder]
    return data



