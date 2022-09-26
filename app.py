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


fig = make_subplots(rows=2, cols=1)

fig.append_trace(go.Ohlc(x=df_market.timestamp,
                    open=df_market.open,
                    high=df_market.high,
                    low=df_market.low,
                    close=df_market.close), row=1, col=1)

fig.append_trace(go.Bar(x=df_market.timestamp, 
                     y=df_market.volume), row=2, col=1)

fig.update_layout(height=600, width=600, title_text="Stacked Subplots")
st.plotly_chart(fig)