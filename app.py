import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image

symbol_list=['BTC/USD', 'ETH/USD', 'USDT/USD', 'USDC/USD', 'BNB/USD', 'XRP/USD', 'BUSD/USD', 'ADA/USD', 'SOL/USD', 'DOGE/USD']
timeframe_list=['1m', '5m', '15m', '30m', '1h', '1d', '1w', '1M']

image = Image.open('cryptocurrency-coins.jpg')

st.set_page_config(page_icon="📈", page_title="Crypto Dashboard")

st.image(image, caption='cryptocurrency-coins')

# Draw a title and some text to the app:
'''
# Ecosistema de criptomonedas

En este dashborad se abarcará el mundo de las criptomonedas y su análisis
'''
option = st.selectbox(
    'Elejir la cripto para conocer su historial',
    (symbol_list))

'Se eligio:', option




genre = st.radio(
    "elija el intervalo de tiempo para graficar el historial",
    timeframe_list, horizontal=True)

ftx= ccxt.ftx() # utilizo phemex Exchange Markets
symbol=option # simbolo de la moneda
timeframe=genre
limit=600
bars=ftx.fetch_ohlcv(symbol,timeframe=timeframe,limit=limit) #fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
df_market=pd.DataFrame(bars, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')

df_market['typical'] = np.round(np.mean([df_market.high,df_market.low,df_market.close],axis=0)) # Typical Price = High price + Low price + Closing Price/3
#VWAP = Cumulative Typical Price x Volume/Cumulative Volume
#Cumulative = total since the trading session opened
df_market['VWAP']=np.round(sum(df_market.typical)*df_market.volume/sum(df_market.volume))

VWAP_var=np.var(df_market.VWAP)

st.metric(option, VWAP_var)


# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.2, subplot_titles=('OHLC', 'Volume'), 
               row_width=[3.8 ,1.8])

# Plot OHLC on 1st row


fig.add_trace(go.Ohlc(x=df_market['timestamp'],
                    open=df_market.open,
                    high=df_market.high,
                    low=df_market.low,
                    close=df_market.close,name="OHLC"), row=1, col=1)


# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=df_market.timestamp,y=df_market.volume,showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=True)
st.plotly_chart(fig)