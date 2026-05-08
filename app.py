import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(page_title="Visor de Evidencias Pro", layout="wide")

# Estilo visual para mejorar la experiencia
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stImage { border-radius: 8px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Carga de Datos
@st.cache_data
def cargar_datos():
    # Cambia 'datos.xlsx' por el nombre real de tu archivo
    return pd.read_excel("datos.xlsx")

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"No se encontró el archivo de Excel o tiene errores: {e}")
    st.stop()

# 3. Barra Lateral con Filtros y Contraseña (Opcional)
st.sidebar.title("🛠️ Panel de Control")

# Filtros
st.sidebar.subheader("Filtrar Registros")
area_list = ["Todas"] + sorted(df['Area'].unique().tolist())
area_sel = st.sidebar.selectbox("Por Area:", area_list)

tipo_list = ["Todos"] + sorted(df['Tipo'].unique().tolist())
tipo_sel = st.sidebar.selectbox("Por Tipo:", tipo_list)

busqueda = st.sidebar.text_input("Buscar por Folio:")

# Aplicar filtros
df_final = df.copy()
if area_sel != "Todas":
    df_final = df_final[df_final['Área'] == area_sel]
if tipo_sel != "Todos":
    df_final = df_final[df_final['Tipo'] == tipo_sel]
if busqueda:
    df_final = df_final[df_final['Folio'].astype(str).str.contains(busqueda)]

# 4. Cuerpo Principal - Lista Infinita
st.title("📂 Galería de Evidencias")
st.write(f"Mostrando **{len(df_final)}** registros filtrados.")

# Control de paginación (Lista infinita)
if 'num_items' not in st.session_state:
    st.session_state.num_items = 20

# Mostrar los registros
df_muestra = df_final.head(st.session_state.num_items)

for _, fila in df_muestra.iterrows():
    with st.container():
        # Crear 4 columnas: Datos, Foto Antes, Foto Después, Espacio
        c_info, c_antes, c_desp = st.columns([1, 1.5, 1.5])
        
        with c_info:
            st.subheader(f"Folio: {fila['Folio']}")
            st.info(f"**Área:** {fila['Área']}\n\n**Tipo:** {fila['Tipo']}")
            
        with c_antes:
            # Ajusta la ruta a tu carpeta de miniaturas
            foto_1 = f"miniaturas/{fila['Folio']}_antes.jpg"
            if os.path.exists(foto_1):
                st.image(foto_1, caption="Evidencia Antes", use_container_width=True)
            else:
                st.warning("Sin foto 'Antes'")

        with c_desp:
            foto_2 = f"miniaturas/{fila['Folio']}_desp.jpg"
            if os.path.exists(foto_2):
                st.image(foto_2, caption="Evidencia Después", use_container_width=True)
            else:
                st.warning("Sin foto 'Después'")
        
        st.divider()

# Botón para cargar más (Efecto lista infinita)
if st.session_state.num_items < len(df_final):
    if st.button("Ver más registros ⬇️"):
        st.session_state.num_items += 20
        st.rerun()
