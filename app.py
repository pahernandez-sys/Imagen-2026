import streamlit as st
import pandas as pd
import re

# 1. Configuración de página
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. Estilos CSS Corporativos (Corregidos para no afectar iconos)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Titulo Principal en Azul */
    .main-title {
        color: #005596 !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    /* Contador de registros */
    .contador-registros {
        color: #005596 !important;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 12px;
        border-left: 5px solid #005596;
        background-color: #E8F0F8;
        margin-bottom: 25px;
        border-radius: 4px;
    }
    
    /* Tarjeta de registro */
    .evidencia-container {
        background-color: #F8FAFC; 
        border-radius: 12px;
        margin-bottom: 35px;
        border: 1px solid #D1DBE5;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0, 85, 150, 0.06);
    }
    
    /* Encabezado de Folio en Azul */
    .folio-header {
        background-color: #005596;
        color: white !important;
        padding: 12px 20px;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .card-body {
        padding: 20px;
    }
    
    /* Labels de datos */
    .info-label {
        color: #005596;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 1px;
    }
    
    .info-value {
        color: #333333;
        font-size: 0.95rem;
        background-color: white;
        padding: 5px 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        border: 1px solid #E2E8F0;
    }

    /* Barra lateral - Solo afectamos el fondo y textos específicos */
    [data-testid="stSidebar"] {
        background-color: #005596;
    }
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Función de conversión de links
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
    st.sidebar.title("🔍 FILTROS")
    lista_areas = ["Todas"] + sorted(df['AREA'].unique().tolist())
    area_sel = st.sidebar.selectbox("Área Operativa:", lista_areas)
    
    lista_tipos = ["Todos"] + sorted(df['TIPO'].unique().tolist())
    tipo_sel = st.sidebar.selectbox("Tipo:", lista_tipos)
    
    busqueda = st.sidebar.text_input("Folio:")

    df_f = df.copy()
    if area_sel != "Todas": df_f = df_f[df_f['AREA'] == area_sel]
    if tipo_sel != "Todos": df_f = df_f[df_f['TIPO'] == tipo_sel]
    if busqueda: df_f = df_f[df_f['Folio'].astype(str).str.contains(busqueda)]

    # --- CUERPO PRINCIPAL ---
    
    # Título Azul usando una clase específica (main-title) para no romper el resto
    st.markdown('<h1 class="main-title">🔵 Imagen Telmex 2026</h1>', unsafe_allow_html=True)
    
    # Contador de registros
    st.markdown(f'<div class="contador-registros">Número de registros encontrados: {len(df_f)}</div>', unsafe_allow_html=True)

    for _, fila in df_f.head(50).iterrows():
        st.markdown(f'''
            <div class="evidencia-container">
                <div class="folio-header">FOLIO: {fila['Folio']}</div>
                <div class="card-body">
        ''', unsafe_allow_html=True)
        
        col_info, col_a, col_d = st.columns([1.3, 2, 2])
        
        with col_info:
            campos = [
                ("📍 ÁREA", fila['AREA']),
                ("🛠️ TIPO", fila['TIPO']),
                ("📝 ESTADO", fila['ESTADO']),
                ("📞 DISTRITO / TEL", fila.get('DISTRITO TELEFONO', 'N/A')),
                ("📢 CAMPAÑA", fila.get('Vinil o lateral instalado ?', 'N/A')),
                ("🔢 VINILES", fila.get('Numero de Viniles o laterales Instalados', '0'))
            ]
            
            for label, value in campos:
                st.markdown(f'<p class="info-label">{label}</p><p class="info-value">{value}</p>', unsafe_allow_html=True)
            
        with col_a:
            col_ant_list = [c for c in df.columns if 'Antes' in c]
            if col_ant_list:
                link_a = convertir_link_drive(fila[col_ant_list[0]])
                if link_a:
                    st.image(link_a, caption="SITUACIÓN ANTERIOR", use_container_width=True)
                else:
                    st.info("Sin registro 'Antes'")

        with col_d:
            col_des_list = [c for c in df.columns if 'Despues' in c]
            if col_des_list:
                link_d = convertir_link_drive(fila[col_des_list[0]])
                if link_d:
                    st.image(link_d, caption="SITUACIÓN FINAL", use_container_width=True)
                else:
                    st.info("Sin registro 'Después'")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

else:
    st.error("Archivo 'Datos.xlsx' no detectado.")
