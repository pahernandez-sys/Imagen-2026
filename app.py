import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Visor Pro - Google Drive", layout="wide")

# Función mágica para que Drive muestre la imagen directamente
def convertir_link(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return None
    # Extrae el ID del link de Drive
    match = re.search(r'[-\w]{25,}', str(url))
    if match:
        return f"https://drive.google.com/uc?export=view&id={match.group()}"
    return None

@st.cache_data
def cargar_datos():
    # Lee el Excel que acabas de subir con los links
    return pd.read_excel("Datos.xlsx")

df = cargar_datos()

st.title("📂 Visor de Evidencias - Prueba Drive")

# Filtros
area_sel = st.sidebar.selectbox("AREA", ["Todas"] + sorted(df['AREA'].unique().tolist()))
busqueda = st.sidebar.text_input("Buscar Folio:")

df_filtrado = df.copy()
if area_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['AREA'] == area_sel]
if busqueda:
    df_filtrado = df_filtrado[df_filtrado['Folio'].astype(str).str.contains(busqueda)]

# Mostrar registros
for _, fila in df_filtrado.head(10).iterrows():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            st.subheader(f"Folio: {fila['Folio']}")
            st.write(f"**AREA:** {fila['AREA']}")
            st.write(f"**TIPO:** {fila['TIPO']}")

        with col2:
            link_a = convertir_link(fila.get('Link_Antes'))
            if link_a:
                st.image(link_a, caption="Antes", use_container_width=True)
            else:
                st.info("Sin link 'Antes'")

        with col3:
            link_d = convertir_link(fila.get('Link_Despues'))
            if link_d:
                st.image(link_d, caption="Después", use_container_width=True)
            else:
                st.info("Sin link 'Después'")
        st.divider()
