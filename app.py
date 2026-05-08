import streamlit as st
import pandas as pd
import re

# 1. Configuración de página
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. Estilos CSS Corporativos Avanzados
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Estilo del contador de registros */
    .contador-registros {
        color: #005596;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 10px;
        border-left: 5px solid #005596;
        background-color: #E8F0F8;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    /* Títulos principales */
    h1 {
        color: #005596 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Tarjeta de cada registro (Azul Tenue solicitado) */
    .evidencia-container {
        background-color: #F0F4F8; /* Azul muy tenue */
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        border: 1px solid #D1DBE5; /* Borde azul de contraste */
        box-shadow: 0 4px 12px rgba(0, 85, 150, 0.08);
    }
    
    /* Estilo de la información interna */
    .info-label {
        color: #005596;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    
    .info-value {
        color: #333333;
        font-size: 1rem;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 4px 8px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    
    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #005596;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] label {
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

    # Lógica de filtrado
    df_f = df.copy()
    if area_sel != "Todas": df_f = df_f[df_f['AREA'] == area_sel]
    if tipo_sel != "Todos": df_f = df_f[df_f['TIPO'] == tipo_sel]
    if busqueda: df_f = df_f[df_f['Folio'].astype(str).str.contains(busqueda)]

    # --- CUERPO PRINCIPAL ---
    st.title("🔵 Imagen Telmex 2026")
    
    # Contador de registros con el nuevo estilo
    st.markdown(f'<div class="contador-registros">Número de registros encontrados: {len(df_f)}</div>', unsafe_allow_html=True)

    for _, fila in df_f.head(50).iterrows():
        st.markdown('<div class="evidencia-container">', unsafe_allow_html=True)
        
        col_info, col_a, col_d = st.columns([1.3, 2, 2])
        
        with col_info:
            st.markdown(f"<h2 style='color:#005596; margin-top:0;'>Folio: {fila['Folio']}</h2>", unsafe_allow_html=True)
            
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

else:
    st.error("Archivo 'Datos.xlsx' no detectado.")
