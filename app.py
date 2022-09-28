import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from datetime import datetime
from PIL import Image
import math



timeframe_list=['1m', '5m', '15m', '1h', '1d', '1w', '1M']
BTC='Bitcoin es una criptomoneda descentralizada presentada originalmente en un documento técnico en 2008 por una persona, o grupo de personas, utilizando el alias Satoshi Nakamoto. Se lanzó poco después, en enero de 2009.El bitcoin es una moneda en línea peer-to-peer, lo que significa que todas las transacciones ocurren directamente entre los participantes, iguales e independientes, de la red sin la necesidad de que ningún intermediario les de permiso o les facilite las operaciones. Bitcoin se creó, de acuerdo con las propias palabras de Nakamoto, para permitir que “los pagos en línea se pudieran enviar directamente de una parte a otra sin pasar por una institución financiera.Existen algunos conceptos que describen un tipo similar de moneda electrónica descentralizada antes del BTC, pero Bitcoin tiene la distinción de ser la primera criptomoneda en entrar en uso.'
#BTC='Moneda digital pionera. En 2008 fue creada por varias personas bajo el nombre de Satoshi Nakamoto. Por supuesto, en su lanzamiento no tenía el valor que posee ahora y la mayoría tampoco podía llegar a pensar que alcanzaría estos datos.Sin duda esta moneda se ha posicionado como líder en el mercado digital. Sin embargo, ha sufrido grandes altibajos y resulta complicado saber cuándo va a subir o a bajar. Pese a que muchos gestores consideran que el Bitcoin es el nuevo oro digital, sigue teniendo grandes variaciones de precio y volatilidades muy elevadas.El funcionamiento de la red Bitcoin es relativamente simple (de ahí gran parte de su virtud) pero asombrosamente segura.'
ETH='Ethereum no es una divisa, es una plataforma de computación descentralizada. Podríamos representarla como un gran ordenador que está repartido en múltiples ordenadores a la vez y trabaja de forma simultánea. Esta red de computación permite ejecutar aplicaciones en esta red distribuida y las operaciones se alimentan con la divisa de la red, el ether (ETH). Ethereum se considera como una blockchain de 2º generación, lo cuál significa que se ha construido en base al sistema de funcionamiento de Bitcoin pero con grandes diferencias. Ambas redes son utilizadas para usarlas como dinero digital, pero la red de Ethereum es programable, lo que significa que tiene muchas más funcionalidades.ETH es la moneda de las aplicaciones de la red Ethereum, similar a Bitcoin en su naturaleza.'
ADA='Cardano es una plataforma de blockchain de prueba de participación cuyo objetivo es permitir que los usuarios que sean "pioneros, innovadores y visionarios" traigan consigo un cambio global positivo a la red.Este proyecto de código abierto también pretende “redistribuir el poder de las estructuras contables entre los individuos marginados", ayudando a crear una sociedad más segura, transparente y justa. Cardano fue fundada en 2017, y las token de ADA están diseñadas para asegurar que los propietarios puedan participar en el funcionamiento de la red. Debido a esto, los que poseen esta criptomoneda tienen derecho a votar sobre cualquier cambio propuesto en el software.'
USDT='Tether es una criptomoneda cuyas fichas son emitidas por Tether Limited. Anteriormente desde la compañía afirmaron que cada token estaba respaldado por un dólar estadounidense, pero el 14 de marzo de 2019 cambió el respaldo para incluir préstamos a empresas afiliadas. El intercambio de Bitfinex fue acusado por el fiscal general de Nueva York de usar los fondos de Tether para cubrir $850 millones en fondos faltantes desde mediados de 2018. Tether se considera una moneda estable porque originalmente se diseñó para que valiera siempre $1.00, manteniendo $1.00 en reservas por cada Tether emitido. Sin embargo, la compañía afirma que los propietarios de amarres no tienen ningún derecho contractual, otros reclamos legales o garantía de que los amarres se canjearán o cambiarán por dólares. El 30 de abril de 2019, el abogado de Tether Limited afirmó que cada atadura estaba respaldada por solo $0,74 en efectivo y equivalentes de efectivo.'
BNB= 'BNB se lanzó a través de una oferta inicial de monedas en 2017, 11 días antes de que el exchange de criptomonedas Binance se pusiera en marcha. Originalmente se emitió como un token ERC-20 que se ejecutaba en la red de Ethereum, con un suministro total limitado a 200 millones de monedas y 100 millones de BNB ofrecidos en la ICO. Sin embargo, las monedas BNB ERC-20 se intercambiaron con BEP2 BNB en una proporción de 1:1 en abril de 2019 con el lanzamiento de la red principal de Binance Chain, y ahora ya no están alojadas en Ethereum.BNB se puede utilizar como método de pago, un token de utilidad para pagar las tarifas en el exchange de Binance y para participar en las ventas de tokens en la plataforma de lanzamiento de Binance. BNB también alimenta a Binance DEX (exchange descentralizado).'
XRP= 'XRP es la criptomoneda nativa de Ripple, un sistema de pago de criptomonedas creado por Ripple Labs Inc. XRP es su "activo digital creado para pagos globales", lo que implica que Ripple planea rivalizar con las transferencias de dinero que generalmente realiza el sistema bancario. XRP permitirÁ a los usuarios enviar dinero a un costo muy bajo, atrayendo el interés potencial de clientes minoristas y bancos por igual. Una propuesta de valor clave de Ripple es su minúsculo costo de transacción al tiempo que ofrece una finalidad de transacción de menos de cinco segundos'
SOL='Solana es un proyecto de código abierto altamente funcional que se basa en la naturaleza sin permiso de la tecnología blockchain para proporcionar soluciones financieras descentralizadas (DeFi). Si bien la idea y el trabajo inicial en el proyecto comenzaron en 2017, Solana fue lanzada oficialmente en marzo de 2020 por la Fundación Solana con sede en Ginebra, Suiza.El protocolo Solana está diseñado para facilitar la creación de aplicaciones descentralizadas (DApp). Su objetivo es mejorar la escalabilidad introduciendo un consenso de prueba de historia (PoH) combinado con el consenso de prueba de participación (PoS) subyacente de la cadena de bloques.Debido al innovador modelo de consenso híbrido, Solana disfruta del interés tanto de los pequeños comerciantes como de los comerciantes institucionales. Un enfoque importante para la Fundación Solana es hacer que las finanzas descentralizadas sean accesibles a mayor escala.'
DOGE='Dogecoin (DOGE) se basa en el popular meme de Internet "doge" y tiene un Shiba Inu en su logotipo. La moneda digital de código abierto fue creada por Billy Markus de Portland, Oregon y Jackson Palmer de Sydney, Australia, y se bifurcó de Litecoin en diciembre de 2013. Los creadores de Dogecoin la vieron como una criptomoneda divertida y alegre que tendría un mayor atractivo más allá de la audiencia principal de Bitcoin, ya que se basó en un meme de perro. El CEO de Tesla, Elon Musk, publicó varios tuits en las redes sociales en los que decía que Dogecoin era su moneda favorita.'

symbol_list=['BTC/USD','ETH/USD','XRP/USD','SOL/USD','USDT/USD','ETHW/USD','BNB/USD','LINK/USD','FTT/USD','ATOM/USD']
dic_symbol={'BTC':'BTC/USD','ETH':'ETH/USD','XRP':'XRP/USD','SOL':'SOL/USD','USDT':'USDT/USD','ETHW':'ETHW/USD','BNB':'BNB/USD','LINK':'LINK/USD','FTT':'FTT/USD','ATOM':'ATOM/USD'}
code_list=['BTC', 'ETH','XRP','SOL','USDT','ETHW', 'BNB', 'LINK','FTT', 'ATOM']
dic_descripcion={'BTC':BTC,'ETH':ETH,'USDT':USDT,'BNB':BNB,'XRP':XRP,'SOL':SOL}
dic_name={'ATOM':'Atom','BNB':'Binance Coin','BTC':'Bitcoin','ETH':'Ethereum','ETHW':'Ethereum','FTT':'FTX Token','LINK':'ChainLink Token','SOL':'Solana','XRP':'XRP'}
image = Image.open('cripto_image.jpg')

st.set_page_config(page_icon="📈", page_title="Ecosistema de criptomonedas",layout = 'wide')

st.image(image,use_column_width=True)

# Draw a title and some text to the app:

'''# Ecosistema de criptomonedas'''
'_Análisis del TOP 10 por volúmen de compra de criptomonedas de la plataforma de exchange FTX_'
'---------------------------------------------------------------------------------------------'
option = st.selectbox(
        'Seleccionar la criptomoneda a analizar',
        (code_list))

'La selección fue:', dic_name[option]

expander = st.expander("información detallada de la criptomoneda seleccionada")
expander.write(dic_descripcion[option])

genre = st.radio(
    "Seleccionar el intervalo de tiempo",
    timeframe_list, horizontal=True)
'------------------------------------------------------------------------------------------'


ftx= ccxt.ftx() # se instancia el exchange de FTX
symbol=dic_symbol[option] # simbolo de la criptomoneda seleccionada por usuario
timeframe=genre # intervalo de tiempo seleccionado por usuario

now = datetime.now() 
from_ts = ftx.parse8601(now) # busqueda de historial ohlcv para la cripto seleccionada actualizado al momento actual
limit=10000 # cantidad de datos a brindar por el historial ohlcv
ftx_ohlcv = ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=from_ts, limit=limit)

# se crea la tabla para graficar el historial ohlcv

ohlcv=pd.DataFrame(ftx_ohlcv, columns=['timestamp','open', 'high', 'low', 'close','volume'])
ohlcv['timestamp']=pd.to_datetime(ohlcv['timestamp'],unit='ms')
ohlcv['typical'] = np.mean([ohlcv.high,ohlcv.low,ohlcv.close],axis=0)


# se crea la tabla de criptomoedas con el TOP 10 por volumen del exchange FTX

tickers = pd.DataFrame(ftx.fetch_tickers(symbols=symbol_list)).T
currencies=pd.DataFrame(ftx.fetch_currencies()).T
tickers.drop(['symbol','timestamp','datetime','high','low','bidVolume','askVolume','vwap','open','last','previousClose','change','average','baseVolume','info'],axis=1,inplace=True)
names = currencies[currencies.code.isin(code_list)].name
tickers.index=tickers.index.str.replace('/USD','')
tickers=pd.concat([tickers,names],axis=1)
cols = list(tickers.columns)
cols.reverse()
tickers=tickers[cols]

# se buscan los datos para armar los principales KPI's

varianza=np.round(np.var(ohlcv.close),2)
volume=np.round(tickers[option].quoteVolume,2)
close=np.round(tickers[option].close,2)
typical=np.round(ohlcv.typical.values[-1],2)
var_close=np.round(tickers[option].percentage,2)


label_price='Precio $'
label_var='Varianza 📈'
label_volume='Volúmen $'
label_typical='Media Móvil 📈'

delta_close="{:.2%}".format(var_close)



millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

col1, col2, col3, col4= st.columns(4)
col1.metric(label_price, close,delta_close)
col2.metric(label_volume, millify(volume))
col3.metric(label_var, millify(varianza))
col4.metric(label_typical, typical) 
'------------------------------------------------------------------------------------------'
# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.25, subplot_titles=('OHLC', 'Volume'),
               row_width=[0.4 ,0.8])
# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=ohlcv['timestamp'],
                    open=ohlcv.open,
                    high=ohlcv.high,
                    low=ohlcv.low,
                    close=ohlcv.close,name="OHLC", showlegend=False), row=1, col=1)
# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=ohlcv.timestamp,y=ohlcv.volume,showlegend=False), row=2, col=1)
# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=True)
fig.update_layout(autosize=False,width=800,height=700)




tab1, tab2, tab3 , tab4= st.tabs(["Tabla Criptomonedas","Calculadora","Gráfico Histórico", "Tabla Histórica"])

with tab1:
    st.dataframe(tickers,use_container_width=True)
with tab2:
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
with tab3:
    st.plotly_chart(fig,use_container_width=True)
    expander = st.expander("See explanation")
    expander.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
with tab4:
    st.dataframe(ohlcv,use_container_width=True)
    