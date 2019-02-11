from bokeh.plotting import figure, output_file, show
import pandas as pd

# output to static HTML file
output_file("line.html")


df = pd.read_csv("data/csv/indicators/merged/merged_indicators_ALL_tf.csv")
print(df.tail(5))

ind_1h = []
ind_3h = []
ind_6h = []
ind_1D = []
columns = list(df.columns.values)
for col in columns:
    if col.startswith('ema50_dist'):
        if 'usd' not in col:
            if col.endswith('1h'):
                ind_1h.append(col)
                #print(type(col))
            if col.endswith('3h'): ind_3h.append(col)
            if col.endswith('6h'): ind_6h.append(col)
            if col.endswith('1D'): ind_1D.append(col)

print(ind_1h)
print(type(ind_1h))
string = '\'' + '\',\''.join(ind_1h) + '\''
print(string)
df_1h = df[[coin for coin in ind_1h]]
print(df_1h.tail())
df_3h = df[[coin for coin in ind_3h]]
df_6h = df[[coin for coin in ind_6h]]
df_1D = df[[coin for coin in ind_1D]]

x = df_6h.iloc[-1]
y = df_1D.iloc[-1]

p = figure(plot_width=400, plot_height=400, x_range=(0, 1), y_range=(0, 1)) #sizing_mode='scale_width')

# add a circle renderer with a size, color, and alpha
p.circle(x, y, size=5, color="navy", alpha=0.5)

p2 = figure(plot_width=800, plot_height=600, x_axis_type="datetime")

p2.line(df_1D.index,
        df_1D['ema50_dist_ltc_btc_1D'], color='red', alpha=1)
p2.line(df_1D.index,
        df_1D['ema50_dist_eth_btc_1D'], color='blue', alpha=1)

# show the results
show(p2)