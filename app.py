import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image
import math

symbol_list=['BTC/USD', 'ETH/USD', 'USDT/USD', 'USDC/USD', 'BNB/USD', 'XRP/USD', 'BUSD/USD', 'ADA/USD', 'SOL/USD', 'DOGE/USD']
timeframe_list=['1m', '5m', '15m', '1h', '1d', '1w', '1M']

image = Image.open('cripto_image.jpg')

st.set_page_config(page_icon="📈", page_title="Ecosistema de criptomonedas")

st.image(image,use_column_width=True)

# Draw a title and some text to the app:

'''# Ecosistema de criptomonedas'''
'_Este dashboard analizará 10 criptomonedas de la plataforma de exchange FTX_'
'------------------------------------------------------------------------------------------'
col1, col2 = st.columns(2)
with col1:
    option = st.selectbox(
        'Seleccionar la criptomoneda a analizar',
        (symbol_list))
with col2:
    'La selección fue:', option
'------------------------------------------------------------------------------------------'
genre = st.radio(
    "Seleccionar el intervalo de tiempo",
    timeframe_list, horizontal=True)
'------------------------------------------------------------------------------------------'
ftx= ccxt.ftx() # utilizo phemex Exchange Markets
symbol=option # simbolo de la moneda
timeframe=genre

from datetime import datetime


now = datetime.now()
from_ts = ftx.parse8601(now)
limit=10000
ohlcv_list = []
ohlcv = ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=from_ts, limit=limit)

df_market=pd.DataFrame(ohlcv, columns=['timestamp','open', 'high', 'low', 'close','volume'])
df_market['timestamp']=pd.to_datetime(df_market['timestamp'],unit='ms')
df_market['typical'] = np.mean([df_market.high,df_market.low,df_market.close],axis=0)
df_market['var_close']=df_market.close.pct_change()
df_market['var_volume']=df_market.volume.pct_change()
df_market['var_typical']=df_market.typical.pct_change()

varianza=np.round(np.var(df_market.close),2)
volume=np.round(df_market.volume.values[-1],2)
close=np.round(df_market.close.values[-1],2)
typical=np.round(df_market.typical.values[-1],2)
var_close=np.round(df_market.var_close.values[-2],6)
var_volume=np.round(df_market.var_volume.values[-2],6)
var_typical=np.round(df_market.var_typical.values[-2],6)

label_price='Precio'
label_var='Varianza'
label_volume='Volúmen'
label_typical='Media Móvil'



millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

col1, col2, col3, col4= st.columns(4)
col1.metric(label_price, close,var_close)
col2.metric(label_volume, millify(volume),var_volume)
col3.metric(label_var, millify(varianza))
col4.metric(label_typical, typical, var_typical)
'------------------------------------------------------------------------------------------'
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



tab1, tab2, tab3 = st.tabs(["Calculadora","Gráfico Histórico", "Tabla Histórica"])

with tab1:
    col1, col2= st.columns(2)
    with col1:
        'calculadora de criptomoneda a -> USD'
        cripto = st.number_input('Insertar el valor en criptomoneda')
        conversion_cripto=cripto*close
        'El valor de la critomoneda en USD es:',conversion_cripto
    with col2:
        'calculadora de USD a -> criptomoneda'
        usd = st.number_input('Insertar el valor en moneda USD')
        conversion_usd=usd/close
        'El valor de USD en la criptomoneda es:',conversion_usd
with tab2:
    st.plotly_chart(fig)#use_container_width=True
with tab3:
    st.dataframe(df_market)