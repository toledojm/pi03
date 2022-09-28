import streamlit as st
from PIL import Image
import info
import tablas
import graficos



image = Image.open('cripto_image.png')

st.set_page_config(page_icon="📈", page_title="Ecosistema de criptomonedas",layout = 'wide')

st.image(image)

# Draw a title and some text to the app:

'''# Ecosistema de criptomonedas'''
'_Análisis del TOP 10 por volúmen de compra de criptomonedas de la plataforma de exchange FTX_'
'---------------------------------------------------------------------------------------------'
option = st.selectbox(
        'Seleccionar la criptomoneda a analizar',
        (info.code_list))

'La selección fue:', info.dic_name[option]

expander = st.expander("información detallada de la criptomoneda seleccionada")
expander.write(info.dic_info[option])

genre = st.radio(
    "Seleccionar el intervalo de tiempo",
    info.timeframe_list, horizontal=True)
'------------------------------------------------------------------------------------------'

symbol=info.dic_symbol[option] # simbolo de la criptomoneda seleccionada por usuario
timeframe=genre # intervalo de tiempo seleccionado por usuario

label_price='Precio u$s'
label_var='Varianza u$s'
label_volume='Volúmen u$s'
label_typical='Media Móvil u$s'

col1, col2, col3, col4= st.columns(4)
col1.metric(label_price, tablas.close,tablas.delta_close)
col2.metric(label_volume, tablas.millify(tablas.volume))
col3.metric(label_var, tablas.millify(tablas.varianza))
col4.metric(label_typical, tablas.typical) 
'------------------------------------------------------------------------------------------'


tab1, tab2, tab3 , tab4= st.tabs(["Tabla Criptomonedas","Calculadora","Gráfico Histórico", "Tabla Histórica"])

with tab1:
    st.dataframe(tablas.tickers,use_container_width=True)
with tab2:
    col1, col2= st.columns(2)
    with col1:
        'calculadora de criptomoneda a u$s'
        cripto = st.number_input('Insertar el valor en criptomoneda')
        conversion_cripto=cripto*tablas.close
        'El valor de la critomoneda en u$s es:',conversion_cripto
    with col2:
        'calculadora de u$s a  criptomoneda'
        usd = st.number_input('Insertar el valor en moneda u$s')
        conversion_usd=usd/tablas.close
        'El valor de u$s en la criptomoneda es:',conversion_usd
with tab3:
    st.plotly_chart(graficos.fig,use_container_width=True)
    expander = st.expander("See explanation")
    expander.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
with tab4:
    st.dataframe(tablas.ohlcv,use_container_width=True)
    