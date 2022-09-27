import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image

symbol_list=['BTC/USD', 'ETH/USD', 'USDT/USD', 'USDC/USD', 'BNB/USD', 'XRP/USD', 'BUSD/USD', 'ADA/USD', 'SOL/USD', 'DOGE/USD']
timeframe_list=['1m', '5m', '15m', '30m', '1h', '1d', '1w', '1M']

image = Image.open('cripto_image.jpg')

st.set_page_config(page_icon="📈", page_title="Crypto Dashboard")

st.image(image,use_column_width=True)

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

from datetime import datetime


now = datetime.now()
from_ts = ftx.parse8601(now)
limit=1000
ohlcv_list = []
ohlcv = ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=from_ts, limit=limit)
ohlcv_list.append(ohlcv)
while(len(ohlcv)==1000):
    from_ts = ohlcv[-1][0]
    new_ohlcv = ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=from_ts, limit=limit)
    ohlcv.extend(new_ohlcv)
df_market=pd.DataFrame(ohlcv, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')
df_market['typical'] = np.mean([df_market.high,df_market.low,df_market.close],axis=0)
df_market['vwap']=sum(df_market.typical*df_market.volume)/sum(df_market.volume)
df_market['var_close']=df_market.close.pct_change()
df_market['var_vwap']=df_market.vwap.pct_change()
df_market['var_varianza']=np.var(df_market.close)

vwap=np.round(df_market.vwap.values[-1],2)
close=np.round(df_market.close.values[-1],4)
var_close=np.round(df_market.var_close.values[-2],4)
var_vwap=np.round(df_market.var_vwap.values[-2],4)
var_varianza=np.round(df_market.var_varianza.values[-2],4)

varianza=np.var(df_market.close)
label_price=str(symbol+' Precio')
label_var='Varianza'
label_vwap='Precio Medio Ponderado \n por Volumen (VWAP)'



col1, col2, col3 = st.columns(3)
col1.metric(label_price, close,var_close)
col2.metric(label_var, varianza,var_varianza)
col3.metric(label_vwap, vwap,var_vwap)

# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.3, subplot_titles=('OHLC', 'Volume'),
               row_width=[0.4 ,0.8])

# Plot OHLC on 1st row


fig.add_trace(go.Ohlc(x=df_market['timestamp'],
                    open=df_market.open,
                    high=df_market.high,
                    low=df_market.low,
                    close=df_market.close,name="OHLC", showlegend=False), row=1, col=1)


# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=df_market.timestamp,y=df_market.volume,showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=True)

fig.update_layout(height=700, width=900)

st.plotly_chart(fig,use_container_width=True)