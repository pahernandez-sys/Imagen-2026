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

# 2. Carga de Datos (Asegúrate de que el archivo en GitHub se llame Datos.xlsx)
@st.cache_data
def cargar_datos():
    # Usamos Datos.xlsx con D mayúscula como aparece en tu repositorio
    return pd.read_excel("Datos.xlsx")

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al leer Datos.xlsx: {e}")
    st.stop()

# 3. Barra Lateral con Filtros corregidos según tu imagen
st.sidebar.title("🛠️ Panel de Control")

st.sidebar.subheader("Filtrar Registros")

# Filtro por AREA (en mayúsculas)
area_list = ["Todas"] + sorted(df['AREA'].unique().tolist())
area_sel = st.sidebar.selectbox("Por AREA:", area_list)

# Filtro por TIPO (en mayúsculas)
tipo_list = ["Todos"] + sorted(df['TIPO'].unique().tolist())
tipo_sel = st.sidebar.selectbox("Por TIPO:", tipo_list)

# Buscador por Folio
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
st.write(f"Mostrando **{len(df_final)}** registros de la columna AREA: **{area_sel}**")

# Control de paginación
if 'num_items' not in st.session_state:
    st.session_state.num_items = 20

df_muestra = df_final.head(st.session_state.num_items)

for _, fila in df_muestra.iterrows():
    with st.container():
        c_info, c_antes, c_desp = st.columns([1, 1.5, 1.5])
        
        with c_info:
            st.subheader(f"Folio: {fila['Folio']}")
            st.write(f"**AREA:** {fila['AREA']}")
            st.write(f"**TIPO:** {fila['TIPO']}")
            st.write(f"**ESTADO:** {fila['ESTADO']}")
            
        with c_antes:
            # Asegúrate que la carpeta en GitHub se llame miniaturas
            foto_1 = f"miniaturas/{fila['Folio']}_antes.jpg"
            if os.path.exists(foto_1):
                st.image(foto_1, caption="Antes", use_container_width=True)
            else:
                st.info("Sin foto 'Antes'")

        with c_desp:
            foto_2 = f"miniaturas/{fila['Folio']}_desp.jpg"
            if os.path.exists(foto_2):
                st.image(foto_2, caption="Después", use_container_width=True)
            else:
                st.info("Sin foto 'Después'")
        
        st.divider()

if st.session_state.num_items < len(df_final):
    if st.button("Ver más registros ⬇️"):
        st.session_state.num_items += 20
        st.rerun()
