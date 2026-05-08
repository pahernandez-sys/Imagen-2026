import streamlit as st
import pandas as pd
import re

# 1. Configuración de página
st.set_page_config(page_title="Imagen Telmex 2026", layout="wide")

# 2. CSS Avanzado: Títulos Fijos y Optimización
st.markdown("""
    <style>
    /* Fijar el encabezado superior */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 1000;
        padding: 10px 20px;
        border-bottom: 2px solid #005596;
    }
    
    /* Espaciado para que el contenido no quede debajo del título fijo */
    .main-content {
        margin-top: 150px;
    }

    .stApp { background-color: #FFFFFF; }
    .main-title { color: #005596 !important; font-family: 'Segoe UI', sans-serif; font-size: 2.2rem; font-weight: 800; margin: 0; }
    
    [data-testid="stSidebar"] { background-color: #005596 !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: white !important; }
    
    .contador-registros { 
        color: #005596 !important; 
        font-weight: 700; 
        background-color: #E8F0F8; 
        padding: 8px; 
        border-radius: 4px;
        display: inline-block;
    }
    
    .evidencia-container { background-color: #F8FAFC; border-radius: 12px; margin-bottom: 25px; border: 1px solid #D1DBE5; overflow: hidden; }
    .folio-header { background-color: #005596; color: white !important; padding: 8px 15px; font-size: 1.1rem; font-weight: 700; }
    .info-label { color: #005596; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .info-value { color: #333333; font-size: 0.9rem; background-color: white; padding: 3px 8px; border-radius: 4px; border: 1px solid #E2E8F0; }
    </style>
    """, unsafe_allow_html=True)

# 3. Función de procesamiento de links
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
        return df.dropna(how='all')
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = cargar_datos()

if df is not None:
    # --- BARRA LATERAL ---
    st.sidebar.title("🔍 FILTROS")
    
    col_area = 'AREA' if 'AREA' in df.columns else df.columns[0]
    areas = sorted([str(x) for x in df[col_area].dropna().unique()])
    area_sel = st.sidebar.selectbox("Área:", ["Todas"] + areas)
    
    col_tipo = 'TIPO' if 'TIPO' in df.columns else df.columns[1]
    tipos = sorted([str(x) for x in df[col_tipo].dropna().unique()])
    tipo_sel = st.sidebar.selectbox("Tipo:", ["Todos"] + tipos)
    
    busqueda = st.sidebar.text_input("Buscar Folio:")

    # Filtrado
    df_f = df.copy()
    if area_sel != "Todas": df_f = df_f[df_f[col_area].astype(str) == area_sel]
    if tipo_sel != "Todos": df_f = df_f[df_f[col_tipo].astype(str) == tipo_sel]
    if busqueda:
        col_fol = 'FOLIO' if 'FOLIO' in df.columns else df.columns[0]
        df_f = df_f[df_f[col_fol].astype(str).str.contains(busqueda)]

    # --- ENCABEZADO FIJO ---
    # Usamos un contenedor normal de Streamlit pero con el CSS sticky aplicado
    st.markdown(f"""
        <div class="sticky-header">
            <h1 class="main-title">🔵 Imagen Telmex 2026</h1>
            <div class="contador-registros">Registros: {len(df_f)}</div>
        </div>
        <div class="main-content"></div>
    """, unsafe_allow_html=True)

    # --- RENDERIZADO OPTIMIZADO (Paginación de 50 en 50) ---
    # Esto evita que la app se trabe
    if len(df_f) == 0:
        st.warning("Sin resultados.")
    else:
        # Solo mostramos los primeros 50. Si necesitas más, el usuario puede filtrar.
        # Esto es vital para que la app no se muera con 20k registros.
        registros_a_mostrar = df_f.head(50) 
        
        for _, fila in registros_a_mostrar.iterrows():
            with st.container():
                st.markdown(f'<div class="evidencia-container"><div class="folio-header">FOLIO: {fila.get("FOLIO", "N/A")}</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1.2, 2, 2])
                
                with c1:
                    st.markdown(f'<p class="info-label">📍 ÁREA</p><p class="info-value">{fila.get("AREA", "N/A")}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="info-label">🛠️ TIPO</p><p class="info-value">{fila.get("TIPO", "N/A")}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="info-label">📝 ESTADO</p><p class="info-value">{fila.get("ESTADO", "N/A")}</p>', unsafe_allow_html=True)
                
                with c2:
                    link_a = procesar_link(fila.get('LINK_ANTES'))
                    if link_a: st.image(link_a, caption="ANTES", use_container_width=True)
                    else: st.info("Sin foto Antes")
                
                with c3:
                    link_d = procesar_link(fila.get('LINK_DESPUES'))
                    if link_d: st.image(link_d, caption="DESPUÉS", use_container_width=True)
                    else: st.info("Sin foto Después")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        if len(df_f) > 50:
            st.info(f"Mostrando los primeros 50 de {len(df_f)} resultados. Por favor, usa los filtros para refinar la búsqueda.")
