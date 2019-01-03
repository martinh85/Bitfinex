import wrappers.get_timeframe_data as get_timeframe_data
import wrappers.process_indicators as process_indicators
# Import list of traded pairs form get_timeframe_data file
from wrappers.get_timeframe_data import list_pairs
import pickle

timeframe = '15m'
# Load list of dataframes of all pairs
list_df_prices = get_timeframe_data.check_timeframe(timeframe)

# List for collecting indicator data for all pairs for last timeframe
list_indicators = []

# Compute indicators for all traded pairs for last time frame
for df_price, pair in zip(list_df_prices, list_pairs):
    print('\n', pair[0], '/', pair[1])
    list_indicators.append(process_indicators.process_indicators(df_price, timeframe))
    print(list_indicators[-1])