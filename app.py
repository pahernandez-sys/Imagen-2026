import streamlit as st
import pandas as pd
import re

# 1. Configuración de página
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. Función para convertir links de Drive a imágenes directas
def convertir_link_drive(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return None
    match = re.search(r'[-\w]{25,}', str(url))
    if match:
        id_foto = match.group()
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w1000"
    return None

# 3. Carga de Datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Datos.xlsx")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = cargar_datos()
    
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.title("🔍 Filtros")
    lista_areas = ["Todas"] + sorted(df['AREA'].unique().tolist())
    area_sel = st.sidebar.selectbox("Seleccionar Área:", lista_areas)
    
    lista_tipos = ["Todos"] + sorted(df['TIPO'].unique().tolist())
    tipo_sel = st.sidebar.selectbox("Seleccionar Tipo:", lista_tipos)
    
    busqueda = st.sidebar.text_input("Buscar por Folio:")

    # Lógica de filtrado
    df_filtrado = df.copy()
    if area_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['AREA'] == area_sel]
    if tipo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['TIPO'] == tipo_sel]
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado['Folio'].astype(str).str.contains(busqueda)]

    # --- CUERPO PRINCIPAL ---
    # Título solicitado
    st.title("📂 Imagen Telmex 2026")
    st.write(f"Resultados: **{len(df_filtrado)}**")
    st.divider()

    for _, fila in df_filtrado.head(50).iterrows():
        with st.container():
            col_info, col_a, col_d = st.columns([1, 1.5, 1.5])
            
            with col_info:
                st.subheader(f"Folio: {fila['Folio']}")
                st.write(f"**📍 Área:** {fila['AREA']}")
                st.write(f"**🛠️ Tipo:** {fila['TIPO']}")
                st.write(f"**📝 Estado:** {fila['ESTADO']}")
                
                # --- NUEVOS CAMPOS SOLICITADOS ---
                st.write(f"**📞 Distrito o Telefono:** {fila.get('DISTRITO TELEFONO', 'N/A')}")
                st.write(f"**📢 Campaña:** {fila.get('Vinil o lateral instalado ?', 'N/A')}")
                st.write(f"**🔢 Numero de Viniles:** {fila.get('Numero de Viniles o laterales Instalados', '0')}")
            
            with col_a:
                col_antes = [c for c in df.columns if 'Antes' in c][0]
                link_a = convertir_link_drive(fila[col_antes])
                if link_a:
                    st.image(link_a, caption="ANTES", use_container_width=True)
                else:
                    st.info("Sin foto 'Antes'")

            with col_d:
                col_desp = [c for c in df.columns if 'Despues' in c][0]
                link_d = convertir_link_drive(fila[col_desp])
                if link_d:
                    st.image(link_d, caption="DESPUÉS", use_container_width=True)
                else:
                    st.info("Sin foto 'Después'")
            
            st.divider()

except Exception as e:
    st.error(f"Error: {e}")
