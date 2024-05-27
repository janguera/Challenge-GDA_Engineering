import streamlit as st
import pandas as pd
from PIL import Image
import altair as alt
import bokeh
import bokeh.models
import bokeh.layouts
from numerize.numerize import numerize
# import asyncio
import logging
import datetime

# import sys
# sys.path.append('./app/')
# sys.path.append('/app/')
from graficos import *
# from datos_graficos import Paralelizar_apis
from importar_datos_apis import Obtener_maestro_skus, Obtener_datos_skus

from generar_excel import descargar_graficos_excel


ACTIONS = ["Lista productos prioritarios", "Revisión producto en profundidad", "Validación datos de mercado"]

st.set_page_config(layout="wide")


       
        

def actualiza_session_state(session_state, prefijo: str):
    """Actualiza los estados de la sesión para que no se pierdan al jugar con los parametros
    Se conservan todos los estados que tengan el prefijo indicado
    
    Arguments:
        session_state {dict} -- Diccionario con los estados de la sesión, ejemplo: st.session_state
        prefijo {str} -- Prefijo para identificar los estados de la sesión que se quieren conservar
    
    """
    for k in session_state.keys():
        session_state[k] = session_state[k]
def on_change_radio_button(event):
    pass
def main() -> None:
    TIMEPO_INICIO = datetime.datetime.now()

    # Inicializamos los datos de session state para que no se pierdan al jugar con los parametros
    actualiza_session_state(session_state=st.session_state, prefijo='revision_producto_en_profundidad')

    
    # logo_AG = Image.open('./images/logo_ahumada.png')
    logo_Solver = Image.open('./images/logo_solver.png')
    st.sidebar.image(logo_Solver, width=250)


    _set_block_container_style()

    # Opciones panel lateral
    st.set_option('deprecation.showfileUploaderEncoding', False) 

    
    st.session_state['OPT'] = None # deshabilito opción de procesamiento de datos original del código. Todo el procesamiento se hace en este bloque ELIF

    prefijo_estado = 'revision_producto_en_profundidad'
    # Define estados de la sesión
    st.session_state[f'{prefijo_estado}_previsualizar_comparativa'] = False
    
    

    # Asigna el título de la página
    st.title('Revisión producto en profundidad')
    st.subheader('Evolución semanal de los indicadores más relevantes del producto')
    # print(f'{datetime.datetime.now()} - Ejecutnado revisión producto')

    # st.session_state['obtener_datos'] = False
    with st.spinner('Obteniendo datos...'):
        data_maestro_skus               = Obtener_maestro_skus()['df_data']
        dict_skus_para_cuadro_sleccion  = Obtener_maestro_skus()['dict_skus_para_cuadro_sleccion']


    # Seleccionar por SKU o por descripción
    opcion_busqueda = st.sidebar.radio(key=f'{prefijo_estado}_opcion_busqueda', label="Seleccionar por", options=['SKU', 'Nombre Producto'], index=0
                                       )

    # Si la selección es por descripción, entonces se muestra el cuadro de búsqueda por descripción (claves del diccionario dict_skus_para_cuadro_sleccion)
    # Si la selección es por SKU, entonces se muestra el cuadro de búsqueda por SKU (valores del diccionario dict_skus_para_cuadro_sleccion)
    # el selectbox siempre es por DESCRIPCION y solo se altera lo que se muestra en el cuadro de búsqueda, de esta forma pareciera quetengo 2 cuadros de búsqueda, pero siempre es el mismo
    # Esto permite también que si intercambio la selección de SKU a descripción, el cuadro de búsqueda se actualice con la descripción del SKU seleccionado y viceversa
    if opcion_busqueda == 'SKU':
        format_func = lambda x: x
    else:
        format_func = lambda x: dict_skus_para_cuadro_sleccion[x] if x != '' else ''
        

    sku = st.sidebar.selectbox(key=f'{prefijo_estado}_sku',
                                    label="Seleccionar SKU",
                                    options = [''] + list(dict_skus_para_cuadro_sleccion.keys()), 
                                    index=0,
                                    format_func=format_func,
                                    )
    

    

    VISTA_TEMPORAL_DICT    = {'Semanal': 'W', 'Mensual': 'MS', 'Trimestral': 'Q'}
    vista_temporal_graficos = st.sidebar.selectbox(key=f'{prefijo_estado}_vista_temporal_graficos', 
                                                            label="Cambiar la agrupación temporal de los gráficos", 
                                                            options=VISTA_TEMPORAL_DICT.keys(),                                                               
                                                            index=0)
    
    # sku = dict_skus_para_cuadro_sleccion[sku] if sku != '' else ''
    if sku != '':
        datos_de_maestro_para_sku = data_maestro_skus.loc[sku]
        with st.expander(f'Datos de maestro de producto para SKU: **{sku} - {datos_de_maestro_para_sku["Descriptor"]} - {datos_de_maestro_para_sku["Proveedor"]}**'):
            st.write(datos_de_maestro_para_sku)

        # Obtengo la configuración actual del SKU para construir los parámetros de la lista de productos prioritarios
        with st.spinner('Obteniendo datos...'):
            df_datos_detalle, df_kpis_sku = Obtener_datos_skus(sku, frecuencia=VISTA_TEMPORAL_DICT[vista_temporal_graficos])        
            

        st.sidebar.text("")

        # Muestra datos
        df_datos_detalle['Fecha'] = pd.to_datetime(df_datos_detalle['Fecha'])

        revision_producto_en_profundidad(df_datos_detalle, sku, df_kpis_sku.fillna(0), vista_temporal_graficos)
        # # Descarga gráficos en Excel


        descargar_graficos = st.sidebar.button('Generar archivo gráficos')
        if descargar_graficos:
            descargar_graficos_excel(df_datos_detalle.sort_values(by='Fecha').reset_index(drop=True).fillna(0), sku)

            with open(f'analisis_{sku}.xlsx', 'rb') as my_file:
                st.sidebar.download_button(label = 'Pulsar para descargar archivo', 
                                data = my_file,
                                file_name = f'analisis_{sku}.xlsx',
                                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                )

    

    st.write(f"TIEMPO USADO: {datetime.datetime.now() - TIMEPO_INICIO}")
