from app import *

# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.25, subplot_titles=(str("Valores Históricos de "+dic_name[option]), 'Volúmen'),
               row_width=[0.4 ,0.8])
# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=ohlcv['date'],
                    open=ohlcv.open,
                    high=ohlcv.high,
                    low=ohlcv.low,
                    close=ohlcv.close, showlegend=False), row=1, col=1)
# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=ohlcv.date,y=ohlcv.volume,showlegend=False), row=2, col=1)
# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=True)
fig.update_layout(autosize=False,width=800,height=700)

