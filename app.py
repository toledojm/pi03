import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


phemex= ccxt.phemex() # utilizo phemex Exchange Markets
symbol='BTCUSD' # simbolo de la moneda
timeframe='1d'
limit=500
bars=phemex.fetch_ohlcv(symbol,timeframe=timeframe,limit=limit) #fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
df_market=pd.DataFrame(bars, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')


# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=1, subplot_titles=('OHLC', 'Volume'), 
               row_width=[0.5, 1])

# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=df_market.timestamp,
                    open=df_market.open,
                    high=df_market.high,
                    low=df_market.low,
                    close=df_market.close, 
                    name="OHLC"), row=1, col=1)

# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=df_market.timestamp,y=df_market.volume,showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
st.plotly_chart(fig)