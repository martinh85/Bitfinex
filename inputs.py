# Traded coins
symbols = ['ETH', 'XRP',]# 'LTC', 'EOS', 'IOT', 'XMR','ZEC', 'NEO',
            #'ETC', 'DSH', 'OMG', 'TRX', 'REP', 'BCH']

# Prepare trading pairs in format ETH/BTC: ['ETH', 'BTC']
USDpairs = []
for coin in symbols:
    list = [coin]
    list.append('USD')
    USDpairs.append(list)

BTCpairs = []
for coin in symbols:
    list = [coin]
    list.append('BTC')
    BTCpairs.append(list)

ALLpairs = USDpairs + BTCpairs

# Set date range for historical queries
from_date = 1430000000
to_date = 1446700000

