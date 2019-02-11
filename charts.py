from bokeh.plotting import figure
import pandas as pd

import numpy as np

from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure
from bokeh.sampledata.stocks import AAPL


df = pd.read_csv("data/csv/indicators/merged_indicators.csv")

time = df.timestamp.values
ema1 = df.rsi_eth_usd_1h.values
ema2 = df.rsi_xrp_usd_1h.values
ema3 = df.rsi_ltc_usd_1h.values
ema4 = df.rsi_xmr_usd_1h.values
ema5 = df.rsi_eos_usd_1h.values

print(ema1[-20:])



dates = np.array(df.timestamp.values, dtype=np.datetime64)
source = ColumnDataSource(data=dict(date=dates, close=df.rsi_eth_usd_1h, close2=df.rsi_eth_usd_1h.values))

p = figure(plot_height=150, plot_width=250, tools="", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(dates[200], dates[400]))

p.line('date', 'close', source=source)
p.line('date', 'close2', source=source)
p.yaxis.axis_label = 'Price'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=100, plot_width=200, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

show(column(p, select))

