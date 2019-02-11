import pandas as pd

# # Prepare dataframe for merged indicators, all pairs
df_merged_ind_ALL_timeframes = pd.DataFrame()

# Merge ALL timeframes --- ALL pairs, ALL indicators
for tf in ['1h', '3h', '6h', '1D']:
        df = pd.read_csv("data/csv/indicators/merged/merged_indicators_" + tf + ".csv")
        df.set_index(['timestamp'], inplace=True)
        if df_merged_ind_ALL_timeframes.empty:
                df_merged_ind_ALL_timeframes = df
        else:
                df_merged_ind_ALL_timeframes = pd.merge(df_merged_ind_ALL_timeframes, df,
                                          left_index=True, right_index=True, how='outer')

df_merged_ind_ALL_timeframes.fillna(method='ffill', inplace=True)
df_merged_ind_ALL_timeframes.to_csv("data/csv/indicators/merged/merged_indicators_ALL_tf.csv")