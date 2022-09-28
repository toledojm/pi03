import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import math
import app
import info

ftx= ccxt.ftx() # se instancia el exchange de FTX


now = datetime.now() 
from_ts = ftx.parse8601(now) # busqueda de historial ohlcv para la cripto seleccionada actualizado al momento actual
limit=10000 # cantidad de datos a brindar por el historial ohlcv
ftx_ohlcv = ftx.fetch_ohlcv(symbol=app.symbol, timeframe=app.timeframe, since=from_ts, limit=limit)

# se crea la tabla para graficar el historial ohlcv

ohlcv=pd.DataFrame(ftx_ohlcv, columns=['date','open', 'high', 'low', 'close','volume'])
ohlcv['date']=pd.to_datetime(ohlcv['date'],unit='ms')
ohlcv['typical'] = np.mean([ohlcv.high,ohlcv.low,ohlcv.close],axis=0)


# se crea la tabla de criptomoedas con el TOP 10 por volumen del exchange FTX

tickers = pd.DataFrame(ftx.fetch_tickers(symbols=info.symbol_list)).T
currencies=pd.DataFrame(ftx.fetch_currencies()).T
tickers.drop(['symbol','timestamp','datetime','high','low','bidVolume','askVolume','vwap','open','last','previousClose','change','average','baseVolume','info'],axis=1,inplace=True)
names = currencies[currencies.code.isin(info.code_list)].name
tickers.index=tickers.index.str.replace('/USD','')
tickers=pd.concat([tickers,names],axis=1)
cols = list(tickers.columns)
cols.reverse()
tickers=tickers[cols]

# se buscan los datos para armar los principales KPI's

varianza=np.round(np.var(ohlcv.close),2)
volume=np.round(tickers.quoteVolume.loc[app.option],2)
close=np.round(tickers.close.loc[app.option],2)
typical=np.round(ohlcv.typical.values[-1],2)
var_close=np.round(tickers.percentage.loc[app.option],2)/100

delta_close="{:.2%}".format(var_close) +' var 24hs'

millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
