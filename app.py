# --- CUERPO PRINCIPAL (ESTÁTICO) ---
st.markdown('<h1 class="main-title">🔵 Imagen Telmex 2026</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="contador-registros">Registros encontrados: {len(df_f)}</div>', unsafe_allow_html=True)

# --- CONTENEDOR CON SCROLL PARA LOS REGISTROS ---
# Al usar 'height', Streamlit crea automáticamente la barra de desplazamiento interna
# y al cambiar los filtros, el contenedor vuelve automáticamente al inicio.
with st.container(height=700): 
    if len(df_f) == 0:
        st.warning("No se encontraron registros con los filtros seleccionados.")
    else:
        for _, fila in df_f.iterrows(): # Quitamos el .head(100) si quieres ver todos en el scroll
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
                if link_a: st.image(link_a, caption="SITUACIÓN ANTERIOR", use_container_width=True)
                else: st.info("Sin foto Antes")

            with col_d:
                link_d = procesar_link(fila.get('LINK_DESPUES'))
                if link_d: st.image(link_d, caption="SITUACIÓN FINAL", use_container_width=True)
                else: st.info("Sin foto Después")
            
            st.markdown('</div>', unsafe_allow_html=True)
