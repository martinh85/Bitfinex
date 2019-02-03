from bitfinex import WssClient, ClientV2, ClientV1
# info: https://bitfinex.readthedocs.io/en/latest/restv2.html

bfx_client = ClientV2(key='nJKOHF9lPF5sx2HyIxl2YsWTY4zITMe6u7vsdv1Xhet',secret='QpTdEuHaREhH8lKBM0DRpYxwNLvE56iCqa3B3sitrCl')

# OCHLV
def minute_last_bitfinex(symbol, comparison_symbol):
    data = bfx_client.candles("1m", "t" + str(symbol)+str(comparison_symbol), "hist", limit='2')
    data = data[1]
    return data
