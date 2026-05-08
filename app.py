import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(page_title="Visor de Evidencias Pro", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stImage { border-radius: 8px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Carga de Datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("Datos.xlsx")

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al leer Datos.xlsx: {e}")
    st.stop()

# 3. Barra Lateral con Filtros
st.sidebar.title("🛠️ Panel de Control")
st.sidebar.subheader("Filtrar Registros")

area_list = ["Todas"] + sorted(df['AREA'].unique().tolist())
area_sel = st.sidebar.selectbox("Por AREA:", area_list)

tipo_list = ["Todos"] + sorted(df['TIPO'].unique().tolist())
tipo_sel = st.sidebar.selectbox("Por TIPO:", tipo_list)

busqueda = st.sidebar.text_input("Buscar por Folio:")

# Aplicar filtros
df_final = df.copy()
if area_sel != "Todas":
    df_final = df_final[df_final['AREA'] == area_sel]
if tipo_sel != "Todos":
    df_final = df_final[df_final['TIPO'] == tipo_sel]
if busqueda:
    df_final = df_final[df_final['Folio'].astype(str).str.contains(busqueda)]

# 4. Cuerpo Principal
st.title("📂 Galería de Evidencias")
st.write(f"Mostrando **{len(df_final)}** registros.")

# Control de paginación
if 'num_items' not in st.session_state:
    st.session_state.num_items = 20

df_muestra = df_final.head(st.session_state.num_items)

# RUTA DE LA CARPETA (Corregida según tu imagen)
ruta_fotos = "IMAGEN 2026-miniaturas"

for _, fila in df_muestra.iterrows():
    with st.container():
        c_info, c_antes, c_desp = st.columns([1, 1.5, 1.5])
        
        with c_info:
            st.subheader(f"Folio: {fila['Folio']}")
            st.write(f"**AREA:** {fila['AREA']}")
            st.write(f"**TIPO:** {fila['TIPO']}")
            st.write(f"**ESTADO:** {fila['ESTADO']}")
            
        with c_antes:
            # Nombre de archivo corregido: _antes.jpg
            foto_1 = f"{ruta_fotos}/{fila['Folio']}_antes.jpg"
            if os.path.exists(foto_1):
                st.image(foto_1, caption="Antes", use_container_width=True)
            else:
                st.info(f"No existe: {fila['Folio']}_antes.jpg")

        with c_desp:
            # Nombre de archivo corregido: _despues.jpg (según tu foto de GitHub)
            foto_2 = f"{ruta_fotos}/{fila['Folio']}_despues.jpg"
            if os.path.exists(foto_2):
                st.image(foto_2, caption="Después", use_container_width=True)
            else:
                st.info(f"No existe: {fila['Folio']}_despues.jpg")
        
        st.divider()

if st.session_state.num_items < len(df_final):
    if st.button("Ver más registros ⬇️"):
        st.session_state.num_items += 20
        st.rerun()
