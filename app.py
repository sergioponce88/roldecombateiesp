import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai

# CONFIGURACIÓN DE IA (Gemini)
# Reemplaza 'TU_API_KEY_AQUI' con tu clave de Google AI Studio
genai.configure(api_key="TU_API_KEY_AQUI")
model_ia = genai.GenerativeModel('gemini-pro')

# CONFIGURACIÓN DE GOOGLE SHEETS
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# Cambia esto por el nombre EXACTO de tu archivo en Google Drive
NOMBRE_EXCEL = "Base_Datos_IESP" 
sheet = client.open("ROL DE COMBATE").sheet1

st.set_page_config(page_title="Sistema de Sanciones I.E.S.P.", layout="wide")
st.title("👮 Sistema de Registro Disciplinario - I.E.S.P.")

# --- FORMULARIO ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre y Apellido del Cadete")
        dni = st.text_input("DNI del Cadete")
        año = st.selectbox("Año de Cursado", ["I° Año", "II° Año", "III° Año"])
    
    with col2:
        fecha_novedad = st.date_input("Fecha del hecho")
        oficial_actuante = st.text_input("Oficial que sanciona", value="Of. Aux. Sergio Edgardo Ponce")

    borrador = st.text_area("Describa lo ocurrido (Borrador informal):", height=150)

    # BOTÓN PARA MEJORAR CON IA
    if st.button("✨ Mejorar Redacción con IA"):
        if borrador:
            prompt = f"""
            Actúa como un Oficial de la Policía de Tucumán experto en redacción administrativa.
            Transforma el siguiente borrador en una sanción disciplinaria formal para el I.E.S.P.
            
            Usa esta estructura obligatoria:
            'El causante se hace pasible del presente correctivo disciplinario, en razón de que en fecha [FECHA], siendo horas [HORA] aproximadamente, [DESCRIPCIÓN TÉCNICA DEL HECHO]. Haciendo constar que se trata de un cadete de {año}, amplio conocedor del Reglamento Disciplinario de este I.E.S.'
            
            Borrador: {borrador}
            """
            respuesta = model_ia.generate_content(prompt)
            st.session_state['texto_mejorado'] = respuesta.text
        else:
            st.warning("Escribe algo en el borrador primero.")

    # Mostrar resultado de la IA
    cuerpo_final = st.text_area("Cuerpo de la Sanción (Final):", 
                                value=st.session_state.get('texto_mejorado', ''), 
                                height=200)

    # BOTÓN DE GUARDAR
    if st.button("💾 Guardar y Sincronizar con Drive"):
        if nombre and cuerpo_final:
            try:
                sheet.append_row([str(fecha_novedad), nombre, dni, año, oficial_actuante, cuerpo_final])
                st.success(f"✅ Sanción de {nombre} guardada en el Excel correctamente.")
                # Limpiar el estado después de guardar
                if 'texto_mejorado' in st.session_state:
                    del st.session_state['texto_mejorado']
            except Exception as e:
                st.error(f"Error al conectar con Drive: {e}")
        else:
            st.error("Faltan datos obligatorios (Nombre o Cuerpo de la sanción).")
