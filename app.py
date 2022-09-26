import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import matplotlib 
from plotly.subplots import make_subplots

phemex= ccxt.phemex() # utilizo phemex Exchange Markets
symbol='BTCUSD' # simbolo de la moneda
timeframe='1d'
limit=500
bars=phemex.fetch_ohlcv(symbol,timeframe=timeframe,limit=limit) #fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
df_market=pd.DataFrame(bars, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')


candlesticks = go.Candlestick(
    x=df_market.timestamp,
    open=df_market.open,
    high=df_market.high,
    low=df_market.low,
    close=df_market.close,
    showlegend=False
)

volume_bars = go.Bar(
    x=df_market.timestamp,
    y=df_market.volume,
    showlegend=False,
    marker={
        "color": "rgba(128,128,128,0.5)",
    }
)

fig = go.Figure(candlesticks)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(candlesticks, secondary_y=True)
fig.add_trace(volume_bars, secondary_y=False)
fig.update_layout(title="ETH/USDC pool after Uniswap v3 deployment", height=800)
fig.update_yaxes(title="Price $", secondary_y=True, showgrid=True)
fig.update_yaxes(title="Volume $", secondary_y=False, showgrid=False)
st.plotly_chart(fig)