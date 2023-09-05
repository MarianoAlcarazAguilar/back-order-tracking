from scripts.file_cleaner import FileCleaner
from scripts.file_manager import FileManager
import streamlit as st

def update_inventarios(fc: FileCleaner, fm: FileManager):
    st.title('Limpieza de Inventarios')
    uploaded_files = st.file_uploader('Actualización de inventarios', type=['xls', 'xlsx'], accept_multiple_files=True)
    
    if len(uploaded_files) > 0:
        for file in uploaded_files:
            try:
                fc.clean_inventory_file(file, 'transformed_data/inventarios')
                fm.save_file(file, 'raw_data/inventarios')
                st.success(f'{file.name} se cargó exitosamente')
            except:
                # Llamamos también a la función de limpieza de transferencias
                try:
                    fc.clean_transferencias(file, 'transformed_data/transferencias')
                    fm.save_file(file, 'raw_data/transferencias')
                    st.success(f'{file.name} se cargó exitosamente')
                except:
                    st.error(f'Error al cargar {file.name}')


def update_forecasts(fc: FileCleaner, fm:FileManager):
    st.title('Limpieza de Forecasts')
    uploaded_files = st.file_uploader('Actualización de forecasts', type=['xls', 'xlsx'], accept_multiple_files=True)

    if len(uploaded_files) > 0:
        for file in uploaded_files:
            try:
                fc.clean_forecast_file(file, 'transformed_data/forecasts')
                fm.save_file(file, 'raw_data/forecasts')
                st.success(f'{file.name} se cargó exitosamente')
            except:
                st.error(f'Error al cargar {file.name}')

def update_transferencias(fc: FileCleaner, fm: FileManager):
    st.title('Limpieza de Transferencias')
    uploaded_files = st.file_uploader('Actualización de transferencias', type=['xls', 'xlsx'], accept_multiple_files=True)

    if len(uploaded_files) > 0:
        for file in uploaded_files:
            try:
                fc.clean_transferencias(file, 'transformed_data/transferencias')
                fm.save_file(file, 'raw_data/transferencias')
                st.success(f'{file.name} se cargó exitosamente')
            except:
                try:
                    # Intentamos también con el inventario
                    fc.clean_inventory_file(file, 'transformed_data/inventarios')
                    fm.save_file(file, 'raw_data/inventarios')
                    st.success(f'{file.name} se cargó exitosamente')
                except:
                    st.error(f'Error al cargar {file.name}')
    


def mariano_app():
    fc = FileCleaner()
    fm = FileManager()

    with open('static_data/style.css') as f:
        # Cargamos el estilo de css (estoy utilizando uno de internet)
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.write('''
        <p class="paragraph">
            En esta sección puedes <b>cargar losarchivos operacionales</b> para limpiarlos y generar los reportes. Puedes descargar estos mismos archivos en la página de Descargar Archivos.
        </p>
    ''', unsafe_allow_html=True)
        
    type_of_file = st.sidebar.radio('Elige el tipo de archivo a subir', ['Inventario', 'Forecast', 'Transferencias'])

    if type_of_file == 'Inventario':
        update_inventarios(fc, fm)

    elif type_of_file == 'Forecast':
        update_forecasts(fc, fm)

    elif type_of_file == 'Transferencias':
        update_transferencias(fc, fm)


if __name__ == '__main__':
    mariano_app()