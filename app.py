import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image

symbol_list=['BTCUSD', 'ETHUSD', 'USDTUSD', 'USDCUSD', 'BNBUSD', 'XRPUSD', 'BUSDUSD', 'ADAUSD', 'SOLUSD', 'DOGEUSD']

from PIL import Image
image = Image.open('https://superyou.co.id/blog/wp-content/uploads/2021/03/cryptocurrency-coins.jpg')

st.image(image, caption='cryptocurrency-coins')

# Draw a title and some text to the app:
'''
# Ecosistema de criptomonedas

En este dashborad se abarcará el mundo de las criptomonedas y sus mercados.
'''

option = st.selectbox(
    'Elejir la cripto para conocer su historial',
    (symbol_list))

'You selected:', option

genre = st.radio(
    "elija el intervalo de tiempo para graficar el historial",
    ('1m', '5m', '15m', '30m', '1h', '1d', '1w', '1M'))

phemex= ccxt.phemex() # utilizo phemex Exchange Markets
symbol=option # simbolo de la moneda
timeframe=genre
limit=500
bars=phemex.fetch_ohlcv(symbol,timeframe=timeframe,limit=limit) #fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
df_market=pd.DataFrame(bars, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')


# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.06, subplot_titles=('OHLC', 'Volume'), 
               row_width=[0.4, 1.4])

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
fig.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig)