import streamlit as st
import pandas as pd
import re

# 1. Configuración visual de la página
st.set_page_config(
    page_title="Visor de Evidencias Pro - Cloud",
    page_icon="📂",
    layout="wide"
)

# Estilos CSS personalizados para mejorar la apariencia
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .evidencia-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stImage { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Función para convertir links de Drive a imágenes directas
def convertir_link_drive(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return None
    # Extraemos el ID del archivo usando una expresión regular
    match = re.search(r'[-\w]{25,}', str(url))
    if match:
        file_id = match.group()
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return None

# 3. Carga de datos optimizada
@st.cache_data
def cargar_datos():
    # El archivo debe llamarse Datos.xlsx en GitHub
    try:
        data = pd.read_excel("Datos.xlsx")
        # Limpieza rápida: quitar espacios en los nombres de las columnas
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception as e:
        st.error(f"Error al cargar Datos.xlsx: {e}")
        return None

df = cargar_datos()

if df is not None:
    # 4. Barra Lateral - Filtros
    st.sidebar.title("🔍 Panel de Filtros")
    
    # Filtro por AREA (según tu Excel actual)
    areas = ["Todas"] + sorted(df['AREA'].unique().tolist())
    area_sel = st.sidebar.selectbox("Seleccionar Área:", areas)
    
    # Filtro por TIPO
    tipos = ["Todos"] + sorted(df['TIPO'].unique().tolist())
    tipo_sel = st.sidebar.selectbox("Seleccionar Tipo:", tipos)
    
    # Buscador por Folio
    busqueda = st.sidebar.text_input("Buscar por Folio:")

    # Aplicar la lógica de filtrado
    df_final = df.copy()
    if area_sel != "Todas":
        df_final = df_final[df_final['AREA'] == area_sel]
    if tipo_sel != "Todos":
        df_final = df_final[df_final['TIPO'] == tipo_sel]
    if busqueda:
        df_final = df_final[df_final['Folio'].astype(str).str.contains(busqueda)]

    # 5. Cuerpo Principal
    st.title("📂 Visor de Evidencias (Cloud)")
    st.write(f"Mostrando **{len(df_final)}** registros encontrados.")

    # Paginación simple para no saturar la web (mostramos los primeros 50)
    registros_a_mostrar = df_final.head(50)

    for _, fila in registros_a_mostrar.iterrows():
        with st.container():
            # Creamos 3 columnas: Info | Antes | Después
            col_info, col_antes, col_desp = st.columns([1, 1.5, 1.5])
            
            with col_info:
                st.subheader(f"Folio: {fila['Folio']}")
                st.write(f"**📍 Área:** {fila['AREA']}")
                st.write(f"**🛠️ Tipo:** {fila['TIPO']}")
                st.write(f"**📝 Estado:** {fila['ESTADO']}")
                
            with col_antes:
                # Verificamos si existe la columna y el link
                if 'Link_Antes' in fila and pd.notnull(fila['Link_Antes']):
                    url_directa = convertir_link_drive(fila['Link_Antes'])
                    if url_directa:
                        st.image(url_directa, caption="EVIDENCIA ANTES", use_container_width=True)
                    else:
                        st.warning("Link de Drive inválido")
                else:
                    st.info("Sin link 'Antes'")

            with col_desp:
                if 'Link_Despues' in fila and pd.notnull(fila['Link_Despues']):
                    url_directa_d = convertir_link_drive(fila['Link_Despues'])
                    if url_directa_d:
                        st.image(url_directa_d, caption="EVIDENCIA DESPUÉS", use_container_width=True)
                    else:
                        st.warning("Link de Drive inválido")
                else:
                    st.info("Sin link 'Después'")
            
            st.divider()

else:
    st.warning("Por favor, asegúrate de que 'Datos.xlsx' esté en tu repositorio de GitHub.")
