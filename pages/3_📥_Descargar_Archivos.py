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

def render_page():
    data_dir = 'data'
    st.set_page_config(
        layout='wide', 
        initial_sidebar_state='expanded',
        page_title='Dragón',
        page_icon='🐉'
    )
    
    fm = FileManager()
    fc = FileCleaner(data_dir=data_dir)

    with open(f'static_data/style.css') as f:
        # Cargamos el estilo de css (estoy utilizando uno de internet)
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.write('''
        <p class="paragraph">
            En esta sección puedes descargar los <b>archivos originales</b> que subieron para procesar.
        </p>
    ''', unsafe_allow_html=True)

    type_of_file = st.sidebar.radio('Elige el tipo de archivo a descargar', ['Inventario', 'Forecast', 'Transferencias'])

    if type_of_file == 'Inventario':
        download_inventarios(fm, fc, data_dir=data_dir)

    elif type_of_file == 'Forecast':
        download_forecasts(fm, data_dir=data_dir)

    elif type_of_file == 'Transferencias':
        download_transfers(fm, fc, data_dir=data_dir)

def download_inventarios(fm: FileManager, fc: FileCleaner, data_dir:str):
    st.markdown("### Descarga Inventarios")
    dir_location = f'{data_dir}/raw_data/inventarios'
    files = fm.get_files_on_directory(dir_location)
    files = fc.ordena_lista_nombres_con_fecha(files)
    file_name = st.selectbox('Elige el inventario', files, label_visibility="hidden")

    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)

def download_forecasts(fm: FileManager, data_dir:str):
    st.markdown("### Descarga Forecasts")
    dir_location = f'{data_dir}/raw_data/forecasts'
    files = fm.get_files_on_directory(dir_location)
    file_name = st.selectbox('Elige el inventario', files, label_visibility="hidden")

    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)

def download_transfers(fm: FileManager, fc: FileCleaner, data_dir:str):
    st.markdown("### Descarga Transferencias")
    dir_location = f'{data_dir}/raw_data/transferencias'
    files = fm.get_files_on_directory(dir_location)
    files = fc.ordena_lista_transferencias(files)
    file_name = st.selectbox('Elige el inventario', files, label_visibility="hidden")

    bytes_data, _ = fm.download_file(f'{dir_location}/{file_name}')
    download_button(bytes_data, file_name)
    

if __name__ == "__main__":
    render_page()