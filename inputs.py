
# Watched timeframes
timeframes = ['5m', '15m', '30m', '1h', '4h', '12h', '1D']

# Traded coins
symbols = ['ETH', 'XRP', 'LTC', 'EOS', 'IOT', 'XMR',
            'ZEC', 'NEO',
            'ETC', 'DSH', 'OMG', 'TRX']

# Prepare trading pairs in format ETH/BTC: ['ETH', 'BTC']
USDpairs = []
for coin in symbols:
    list = [coin]
    list.append('USD')
    USDpairs.append(list)

BTCpairs = []
for coin in symbols:
    if coin == 'IOT':
        coin = 'IOTA'
    if coin == 'DSH':
        coin = 'DASH'
    if coin == 'BCH':
        coin = 'BCHABC'
    list = [coin]
    list.append('BTC')
    BTCpairs.append(list)

ALLpairs = USDpairs + BTCpairs

# Set date range for historical queries
from_date = 1430000000
to_date = 1446700000

