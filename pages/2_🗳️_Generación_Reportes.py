import streamlit as st
from scripts.file_cleaner import FileCleaner
from scripts.file_manager import FileManager

def download_button(data, file_name):
    if data is not None:
        st.download_button(
            label='📥 Descargar Datos',
            data=data,
            file_name=file_name
        )

def show_available_inventarios(fm: FileManager):
    st.markdown('## Inventarios')
    dir_location = 'transformed_data/inventarios'
    files = fm.get_files_on_directory(dir_location)
    files = FileCleaner().ordena_lista_nombres_con_fecha(files)
    file_name = st.selectbox('Elige el archivo', files)
    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)


def show_available_forecasts(fm: FileManager):
    st.markdown('## Forecasts')
    dir_location = 'transformed_data/forecasts'
    files = fm.get_files_on_directory(dir_location)
    file_name = st.selectbox('Elige el archivo', files)
    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)


def show_available_transferencias(fm: FileManager):
    st.markdown('## Transferencias')
    dir_location = 'transformed_data/transferencias'
    files = fm.get_files_on_directory(dir_location)
    orderd_files = FileCleaner().ordena_lista_nombres_con_fecha(files)
    file_name = st.selectbox('Elige el archivo', orderd_files)
    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)


def click_button():
    st.session_state.clicked = True

def unclick_button():
    st.session_state.clicked = False

def click_crear_reporte():
    st.session_state.crear_reporte = True

def unclick_crear_reporte():
    st.session_state.crear_reporte = False

def reset_session_state():
    unclick_button()
    unclick_crear_reporte()

def show_available_back_orders(fm: FileManager):
    st.markdown('## Back Orders')
    fc = FileCleaner()

    # Permitimos generar nuevos reportes
    if st.sidebar.button('Generar Reporte de Hoy', on_click=unclick_crear_reporte):
        # Quitamos la persistencia de los otros botones en caso de que sigan ahí
        st.session_state.clicked = False
        datos = fc.genera_reporte_back_order()
        st.sidebar.write('''
            <p class="paragraph">
                Estos son los datos que se usaron para generar el reporte
            </p>
        ''', unsafe_allow_html=True)
        st.sidebar.json(datos, expanded=False)


    st.sidebar.button('Genera Reporte Específico', on_click=click_button)

    if st.session_state.clicked:

        # Tengo que darle la oportunidad de elegir los archivos que desee
        transfers_dir = 'transformed_data/transferencias'
        forecasts_dir = 'transformed_data/forecasts'
        inventario_dir = 'transformed_data/inventarios'
        
        # Leemos los diccionarios
        transfers_files = fm.get_files_on_directory(transfers_dir)
        transfers_files = fc.ordena_lista_nombres_con_fecha(transfers_files)
        forecasts_files = fm.get_files_on_directory(forecasts_dir)
        inventario_files = fm.get_files_on_directory(inventario_dir)
        inventario_files = fc.ordena_lista_nombres_con_fecha(inventario_files)

        transfers = st.selectbox('Transferencias', transfers_files, on_change=unclick_crear_reporte)
        inventario = st.selectbox('Inventario', inventario_files, on_change=unclick_crear_reporte)
        forecast = st.selectbox('Forecasts', forecasts_files, on_change=unclick_crear_reporte)

        st.button('Crear reporte', on_click=click_crear_reporte)

        if st.session_state.crear_reporte:
            # Tenemos que asegurarnos de que las fechas coincidan en los archivos, para hacerle saber al usuario en caso contrario
            date_numbers_inventario = "_".join(fc.encontrar_numeros_en_cadena(inventario))
            date_numbers_transfers = "_".join(fc.encontrar_numeros_en_cadena(transfers))
            if date_numbers_transfers != date_numbers_inventario:
                st.warning(f'Las fechas de los archivos no coinciden, se usará {date_numbers_inventario}')
                if st.button('Deseo continuar'):
                    datos = fc.genera_reporte_back_order_especifico({'forecast':forecast, 'inventario':inventario, 'transfers':transfers})
                    st.sidebar.write('''
                        <p class="paragraph">
                            Estos son los datos que se usaron para generar el reporte
                        </p>
                    ''', unsafe_allow_html=True)
                    st.sidebar.json(datos, expanded=False)
            else:
                datos = fc.genera_reporte_back_order_especifico({'forecast':forecast, 'inventario':inventario, 'transfers':transfers})
                st.sidebar.write('''
                    <p class="paragraph">
                        Estos son los datos que se usaron para generar el reporte
                    </p>
                ''', unsafe_allow_html=True)
                st.sidebar.json(datos, expanded=False)

        st.write('<hr>', unsafe_allow_html=True)



    # Permitimos descargar nuevos reportes
    dir_location = 'transformed_data/back_orders'
    files = fm.get_files_on_directory(dir_location)
    files = fc.ordena_lista_nombres_con_fecha(files)
    file_name = st.selectbox('Elige el archivo que deseas descargar', files, label_visibility='visible')
    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)

def render_page():
    # Permitamos generar reportes con archivos específicos
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    if 'crear_reporte' not in st.session_state:
        st.session_state.crear_reporte = False

    fm = FileManager()

    with open('static_data/style.css') as f:
        # Cargamos el estilo de css (estoy utilizando uno de internet)
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.write('''
        <p class="paragraph">
            En esta sección puedes descargar los <b>archivos que se generaron</b> al cargar tus archivos.
        </p>
    ''', unsafe_allow_html=True)
    
    type_of_file = st.sidebar.radio('Elige el tipo de archivo a subir', ['Inventario', 'Forecast', 'Transferencias', 'Back Orders'], on_change=reset_session_state)

    if type_of_file == 'Inventario':
        show_available_inventarios(fm)
    elif type_of_file == 'Forecast':
        show_available_forecasts(fm)
    elif type_of_file == 'Transferencias':
        show_available_transferencias(fm)
    elif type_of_file == 'Back Orders':
        show_available_back_orders(fm)   

if __name__ == "__main__":
    render_page()