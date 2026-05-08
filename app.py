import streamlit as st
import pandas as pd
import re

# 1. Configuración de página
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. Estilos CSS Corporativos
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main-title { color: #005596 !important; font-family: 'Segoe UI', sans-serif; font-size: 2.8rem; font-weight: 800; margin-bottom: 0px; }
    
    /* Barra Lateral Azul */
    [data-testid="stSidebar"] { background-color: #005596 !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: white !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] h1 { color: white !important; }
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="base-input"] > input { background-color: white !important; color: black !important; }
    
    /* Contador de registros fijo */
    .contador-registros { 
        color: #005596 !important; 
        font-size: 1.1rem; 
        font-weight: 700; 
        padding: 12px; 
        border-left: 5px solid #005596; 
        background-color: #E8F0F8; 
        margin-top: 10px;
        margin-bottom: 20px; 
        border-radius: 4px; 
    }
    
    /* Contenedor de Tarjetas */
    .evidencia-container { background-color: #F8FAFC; border-radius: 12px; margin-bottom: 35px; border: 1px solid #D1DBE5; overflow: hidden; box-shadow: 0 4px 10px rgba(0, 85, 150, 0.06); }
    .folio-header { background-color: #005596; color: white !important; padding: 12px 20px; font-size: 1.3rem; font-weight: 700; }
    .info-label { color: #005596; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 2px; }
    .info-value { color: #333333; font-size: 0.95rem; background-color: white; padding: 5px 10px; border-radius: 4px; margin-bottom: 10px; border: 1px solid #E2E8F0; }
    </style>
    """, unsafe_allow_html=True)

# 3. Función para procesar links de Drive
def procesar_link(url):
    if pd.isna(url) or str(url).strip() == "": return None
    url_str = str(url)
    if "thumbnail?id=" in url_str: return url_str
    match = re.search(r'[-\w]{25,}', url_str)
    if match:
        id_foto = match.group()
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w1000"
    return None

# 4. Carga de Datos
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel("Datos.xlsx")
        df.columns = [str(c).strip().upper() for c in df.columns]
        df = df.dropna(how='all')
        return df
    except Exception as e:
        st.error(f"Error cargando Datos.xlsx: {e}")
        return None

df = cargar_datos()

if df is not None:
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.title("🔍 FILTROS")
    
    col_area = 'AREA' if 'AREA' in df.columns else df.columns[0]
    areas_disponibles = sorted([str(x) for x in df[col_area].dropna().unique()])
    area_sel = st.sidebar.selectbox("Área Operativa:", ["Todas"] + areas_disponibles)
    
    col_tipo = 'TIPO' if 'TIPO' in df.columns else df.columns[1]
    tipos_disponibles = sorted([str(x) for x in df[col_tipo].dropna().unique()])
    tipo_sel = st.sidebar.selectbox("Tipo de Infraestructura:", ["Todos"] + tipos_disponibles)
    
    busqueda = st.sidebar.text_input("Buscar por Folio:")

    # Filtrado
    df_f = df.copy()
    if area_sel != "Todas":
        df_f = df_f[df_f[col_area].astype(str) == area_sel]
    if tipo_sel != "Todos":
        df_f = df_f[df_f[col_tipo].astype(str) == tipo_sel]
    if busqueda:
        col_folio = 'FOLIO' if 'FOLIO' in df.columns else df.columns[0]
        df_f = df_f[df_f[col_folio].astype(str).str.contains(busqueda)]

    # --- CUERPO PRINCIPAL (ESTÁTICO) ---
    st.markdown('<h1 class="main-title">🔵 Imagen Telmex 2026</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="contador-registros">Registros encontrados: {len(df_f)}</div>', unsafe_allow_html=True)

    # --- CONTENEDOR CON SCROLL (DINÁMICO) ---
    # La altura de 750px es ideal para laptops. Si se filtra, vuelve al inicio.
    with st.container(height=750):
        if len(df_f) == 0:
            st.warning("No se encontraron resultados con los filtros aplicados.")
        else:
            for _, fila in df_f.iterrows():
                folio_val = fila.get('FOLIO', 'N/A')
                st.markdown(f'<div class="evidencia-container"><div class="folio-header">FOLIO: {folio_val}</div>', unsafe_allow_html=True)
                
                col_info, col_a, col_d = st.columns([1.5, 2, 2])
                with col_info:
                    campos = [
                        ("📍 ÁREA", fila.get('AREA', 'N/A')),
                        ("🛠️ TIPO", fila.get('TIPO', 'N/A')),
                        ("📝 ESTADO", fila.get('ESTADO', 'N/A')),
                        ("📞 DISTRITO", fila.get('DISTRITO TELEFONO', 'N/A')),
                        ("📢 CAMPAÑA", fila.get('VINIL O LATERAL INSTALADO ?', 'N/A'))
                    ]
                    for label, value in campos:
                        st.markdown(f'<p class="info-label">{label}</p><p class="info-value">{value}</p>', unsafe_allow_html=True)
                    
                with col_a:
                    link_a = procesar_link(fila.get('LINK_ANTES'))
                    if link_a: st.image(link_a, caption="ANTES", use_container_width=True)
                    else: st.info("Sin foto Antes")

                with col_d:
                    link_d = procesar_link(fila.get('LINK_DESPUES'))
                    if link_d: st.image(link_d, caption="DESPUÉS", use_container_width=True)
                    else: st.info("Sin foto Después")
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Archivo 'Datos.xlsx' no detectado en el repositorio.")
