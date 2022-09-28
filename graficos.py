import plotly.graph_objects as go
from plotly.subplots import make_subplots
import app
import tablas
import info

# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.25, subplot_titles=(str("Valores Históricos de "+info.dic_name[app.option]), 'Volúmen'),
               row_width=[0.4 ,0.8])
# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=tablas.ohlcv['date'],
                    open=tablas.ohlcv.open,
                    high=tablas.ohlcv.high,
                    low=tablas.ohlcv.low,
                    close=tablas.ohlcv.close, showlegend=False), row=1, col=1)
# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=tablas.ohlcv.date,y=tablas.ohlcv.volume,showlegend=False), row=2, col=1)
# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=True)
fig.update_layout(autosize=False,width=800,height=700)

