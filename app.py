import streamlit as st
from PIL import Image
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from info import *

CURRENT_THEME = "dark"
IS_DARK_THEME = True

st.set_page_config(page_icon="📈", page_title="Ecosistema de criptomonedas",layout = "centered", menu_items={
        'About': "Este dashboard correponde al PI 03 del cohorte 03 de la carrera de Data Science en Henry."
        })

image = Image.open('cripto_image.png')
st.image(image)


'''# Ecosistema de criptomonedas'''
'_Análisis del TOP 10 por volúmen de compra de criptomonedas de la plataforma de exchange FTX_'
'---------------------------------------------------------------------------------------------'
# se arma la lista para elección de la cripto
option = st.selectbox(
        'Seleccionar la criptomoneda a analizar',
        (code_list))

'La selección fue:', dic_name[option]

expander = st.expander("información detallada de la criptomoneda seleccionada")
expander.write(dic_info[option])

genre = st.radio(
    "Seleccionar el intervalo de tiempo",
    timeframe_list, horizontal=True)
'------------------------------------------------------------------------------------------'



symbol=dic_symbol[option] # simbolo de la criptomoneda seleccionada por usuario
timeframe=genre # intervalo de tiempo seleccionado por usuario

ftx= ccxt.ftx() # se instancia el exchange de FTX

now = datetime.now() 
from_ts = ftx.parse8601(now) # busqueda de historial ohlcv para la cripto seleccionada actualizado al momento actual
limit=10000 # cantidad de datos a brindar por el historial ohlcv
ftx_ohlcv = ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=from_ts, limit=limit)# se busca el registro histórico

# se crea la tabla para graficar el historial ohlcv

ohlcv=pd.DataFrame(ftx_ohlcv, columns=['date','open', 'high', 'low', 'close','volume'])
ohlcv['date']=pd.to_datetime(ohlcv['date'],unit='ms')
ohlcv['media'] = ohlcv.close.rolling(30).mean()

# se crea la tabla de criptomoedas con el TOP 10 por volumen del exchange FTX

tickers = pd.DataFrame(ftx.fetch_tickers(symbols=symbol_list)).T
currencies=pd.DataFrame(ftx.fetch_currencies()).T
tickers.drop(['symbol','timestamp','datetime','high','low',
            'bidVolume','askVolume','vwap','open','last','previousClose',
            'change','average','baseVolume','info'],axis=1,inplace=True)
names = currencies[currencies.code.isin(code_list)].name
tickers.index=tickers.index.str.replace('/USD','')
tickers=pd.concat([tickers,names],axis=1)
cols = list(tickers.columns)
cols.reverse()
tickers=tickers[cols]

# se buscan los datos para armar los principales KPI's

varianza=np.round(np.var(ohlcv.close),2)
volume=np.round(tickers.quoteVolume.loc[option],2)
close=np.round(tickers.close.loc[option],2)
media=np.round(ohlcv.media.values[-1],2)
var_close=np.round(tickers.percentage.loc[option],2)/100

delta_close="{:.2%}".format(var_close) +' var 24hs'

millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

# se crean los KPIs
label_price='Precio u$s'
label_var='Varianza u$s'
label_volume='Volúmen u$s'
label_media='Media Móvil u$s'

col1, col2, col3, col4= st.columns(4)
col1.metric(label_price, close,delta_close)
col2.metric(label_volume, millify(volume))
col3.metric(label_var, millify(varianza))
col4.metric(label_media, media) 

#se crea el historail para un segunda cripto comparable




'------------------------------------------------------------------------------------------'
# se crea el grafico tipo candle con el historico de precio y media movil y volúmen
fig = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.1, 
                    subplot_titles=(str("Valores Históricos en u$s del "+dic_name[option]), 'Volúmen en u$s'),
                    row_width=[0.4 ,0.8])
# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=ohlcv.date,
                    open=ohlcv.open,
                    high=ohlcv.high,
                    low=ohlcv.low,
                    close=ohlcv.close,showlegend=False), row=1, col=1)

fig.add_trace(go.Scatter(x=ohlcv.date, 
                        y=ohlcv.media,
                        mode='lines',
                        marker_color='#A9A9A9',
                        showlegend=False,
                        line=dict(width=0.5)),
                        row=1, col=1)

fig.add_trace(go.Bar(x=ohlcv.date,
                    y=ohlcv.volume,
                    showlegend=False,
                    marker_color='#ff0000'), 
                    row=2, col=1)

fig.update(layout_xaxis_rangeslider_visible=False)
fig.update_layout(autosize=False,width=800,height=700)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='#F2D7D5')



# se crean las tabs para mostrar las tablas, caluculadora y gráficos

tab1, tab2, tab3 , tab4,tab5= st.tabs(["Tabla Criptomonedas","Calculadora","Gráfico Histórico", "Gráfico Comparable","Tabla Histórica"])

with tab1:
    st.dataframe(tickers,use_container_width=True)
with tab2:
    col1, col2= st.columns(2)
    with col1:
        'calculadora de criptomoneda a u$s'
        cripto = st.number_input('Insertar el valor en criptomoneda')
        conversion_cripto=cripto*close
        'El valor de la critomoneda en u$s es:',conversion_cripto
    with col2:
        'calculadora de u$s a  criptomoneda'
        usd = st.number_input('Insertar el valor en moneda u$s')
        conversion_usd=usd/close
        'El valor de u$s en la criptomoneda es:',conversion_usd
with tab3:
    st.plotly_chart(fig,use_container_width=True)
    expander = st.expander(str("Hitos en la historia de "+dic_name[option]))
    hitos=dic_hitos[option]
    expander.write(hitos)
with tab4:
    symbol2 = st.radio(
    "Seleccionar una criptomoneda para comparar su tendencia",
    code_list, horizontal=True)

    comp=dic_symbol[symbol2]
    
    ftx_ohlcv_2 = ftx.fetch_ohlcv(symbol=comp, timeframe=timeframe, since=from_ts, limit=limit)# se busca el registro histórico
    ohlcv_2=pd.DataFrame(ftx_ohlcv, columns=['date','open', 'high', 'low', 'close','volume'])
    ohlcv_2['date']=pd.to_datetime(ohlcv['date'],unit='ms')
    ohlcv_2=pd.DataFrame(ohlcv_2, columns=['date','open', 'high', 'low', 'close','volume'])
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=ohlcv.date, 
                        y=ohlcv.media,
                        mode='lines',
                        marker_color='#A9A9A9',
                        name=symbol,
                        line=dict(width=1)))

    fig2.add_trace(go.Scatter(x=ohlcv_2.date, 
                        y=ohlcv.close,
                        mode='lines',
                        marker_color='#F2D7D5',
                        name=symbol2,
                        line=dict(width=1)))


with tab5:
    st.dataframe(ohlcv,use_container_width=True)

'                                                                                             '
'                                                                                             ''                                                                                             '
'                                                                                             ''                                                                                             '
'                                                                                             '
'---------------------------------------------------------------------------------------------'

st.markdown("libreria ccxt de criptomonedas:https://pypi.org/project/ccxt/  \nmercado exchange:https://ftx.com/  \ninfo mercado criptomonedas:https://coinmarketcap.com/")