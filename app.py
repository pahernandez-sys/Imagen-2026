import streamlit as st
import pandas as pd
import re

# 1. Configuración de página con Título Corporativo
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. Estilos CSS Corporativos (Fondo claro, azules y grises)
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp {
        background-color: #F4F7F9;
    }
    
    /* Títulos principales */
    h1 {
        color: #005596 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    
    /* Tarjeta de cada folio */
    .evidencia-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid #E1E8ED;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Etiquetas de información */
    .info-label {
        color: #5F6368;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 2px;
    }
    
    .info-value {
        color: #202124;
        font-size: 1rem;
        margin-bottom: 10px;
        border-bottom: 1px solid #F1F3F4;
    }
    
    /* Personalización de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #005596;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Función para convertir links de Drive
def convertir_link_drive(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return None
    match = re.search(r'[-\w]{25,}', str(url))
    if match:
        id_foto = match.group()
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w1000"
    return None

# 4. Carga de Datos
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel("Datos.xlsx")
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return None

df = cargar_datos()

if df is not None:
    # --- BARRA LATERAL ---
    st.sidebar.title("🔍 PANEL DE CONTROL")
    
    lista_areas = ["Todas"] + sorted(df['AREA'].unique().tolist())
    area_sel = st.sidebar.selectbox("Área Operativa:", lista_areas)
    
    lista_tipos = ["Todos"] + sorted(df['TIPO'].unique().tolist())
    tipo_sel = st.sidebar.selectbox("Tipo de Infraestructura:", lista_tipos)
    
    busqueda = st.sidebar.text_input("Buscar Folio Específico:")

    # Filtros
    df_f = df.copy()
    if area_sel != "Todas": df_f = df_f[df_f['AREA'] == area_sel]
    if tipo_sel != "Todos": df_f = df_f[df_f['TIPO'] == tipo_sel]
    if busqueda: df_f = df_f[df_f['Folio'].astype(str).str.contains(busqueda)]

    # --- CUERPO PRINCIPAL ---
    st.title("🔵 Imagen Telmex 2026")
    st.markdown(f"**Gestión de Evidencias Digitales** | Registros activos: `{len(df_f)}`")
    st.divider()

    for _, fila in df_f.head(50).iterrows():
        # Usamos HTML para crear la tarjeta corporativa
        st.markdown('<div class="evidencia-container">', unsafe_allow_html=True)
        
        col_info, col_a, col_d = st.columns([1.2, 2, 2])
        
        with col_info:
            st.markdown(f"### Folio: {fila['Folio']}")
            
            # Formato de datos con estilo limpio
            datos = [
                ("📍 ÁREA", fila['AREA']),
                ("🛠️ TIPO", fila['TIPO']),
                ("📝 ESTADO", fila['ESTADO']),
                ("📞 DISTRITO / TEL", fila.get('DISTRITO TELEFONO', 'N/A')),
                ("📢 CAMPAÑA", fila.get('Vinil o lateral instalado ?', 'N/A')),
                ("🔢 VINILES", fila.get('Numero de Viniles o laterales Instalados', '0'))
            ]
            
            for label, value in datos:
                st.markdown(f'<p class="info-label">{label}</p><p class="info-value">{value}</p>', unsafe_allow_html=True)
            
        with col_a:
            col_ant = [c for c in df.columns if 'Antes' in c][0]
            link_a = convertir_link_drive(fila[col_ant])
            if link_a:
                st.image(link_a, caption="SITUACIÓN ANTERIOR", use_container_width=True)
            else:
                st.info("Sin registro 'Antes'")

        with col_d:
            col_des = [c for c in df.columns if 'Despues' in c][0]
            link_d = convertir_link_drive(fila[col_des])
            if link_d:
                st.image(link_d, caption="SITUACIÓN FINAL", use_container_width=True)
            else:
                st.info("Sin registro 'Después'")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()

else:
    st.error("Archivo 'Datos.xlsx' no detectado.")
