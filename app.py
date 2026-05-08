import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Visor de Evidencias Pro", layout="wide")

# Función mejorada para forzar la visualización de la imagen
def convertir_link_drive(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return None
    
    # Esta expresión regular busca el ID largo de Google Drive en cualquier tipo de link
    match = re.search(r'[-\w]{25,}', str(url))
    if match:
        id_foto = match.group()
        # Este formato (thumbnail) es mucho más rápido y confiable para Streamlit
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w1000"
    return None

@st.cache_data
def cargar_datos():
    # Cargamos el Excel (Asegúrate que se llame Datos.xlsx en GitHub)
    df = pd.read_excel("Datos.xlsx")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = cargar_datos()
    
    st.title("📂 Visor de Evidencias - Google Drive")
    
    # Filtros
    area_list = ["Todas"] + sorted(df['AREA'].unique().tolist())
    area_sel = st.sidebar.selectbox("Área", area_list)
    
    df_filtrado = df.copy()
    if area_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['AREA'] == area_sel]

    # Mostrar fotos
    for _, fila in df_filtrado.head(10).iterrows():
        with st.container():
            col_info, col_a, col_d = st.columns([1, 2, 2])
            
            with col_info:
                st.subheader(f"Folio: {fila['Folio']}")
                st.write(f"**Estado:** {fila['ESTADO']}")

            # Foto ANTES
            with col_a:
                link_a = convertir_link_drive(fila.get('Link_Antes'))
                if link_a:
                    st.image(link_a, caption="Antes", use_container_width=True)
                else:
                    st.info("Sin link en columna 'Link_Antes'")

            # Foto DESPUÉS
            with col_d:
                link_d = convertir_link_drive(fila.get('Link_Despues'))
                if link_d:
                    st.image(link_d, caption="Después", use_container_width=True)
                else:
                    st.info("Sin link en columna 'Link_Despues'")
            st.divider()

except Exception as e:
    st.error(f"Error: {e}")
