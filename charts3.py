from math import pi

import pandas as pd

from bokeh.plotting import figure, show, output_file
from bokeh.plotting import figure, output_file, show
import pandas as pd
from bokeh.models import ColumnDataSource, CDSView
from bokeh.embed import components

# output to static HTML file
#output_file("line.html")


df = pd.read_csv("data/csv/price_data/price_data__ltc_usd_1D.csv")
print(df.tail(5))

df = df.iloc[-120:]
#source = ColumnDataSource(df)
df['time'] = df.index
#df = pd.DataFrame(df)[:50]
#df[""] = pd.to_datetime(df["date"])

inc = df.close > df.open
dec = df.open > df.close
w = 0.65 #12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "MSFT Candlestick")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

p.segment(df.time, df.high, df.time, df.low, color="black")
p.vbar(df.time[inc], w, df.open[inc], df.close[inc], fill_color="green", line_color="black")
p.vbar(df.time[dec], w, df.open[dec], df.close[dec], fill_color="red", line_color="black")

output_file("candlestick.html") #, title="candlestick.py example")
show(p)

script, div = components(p)