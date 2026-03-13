import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Legajo Digital IESP", layout="wide")

# Configuración IA (Recuerda poner tu clave real)
genai.configure(api_key="TU_API_KEY_AQUI")

# Conexión a Google Sheets y Google Drive (Fotos)
scope = [
    "https://www.googleapis.com/auth/spreadsheets", 
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file"
]

try:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("ROL DE COMBATE").sheet1
    # Servicio para subir fotos a Drive
    drive_service = build('drive', 'v3', credentials=creds)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# Función para subir la foto a Drive y obtener el link público
def subir_foto_drive(foto_archivo, nombre_cadete):
    try:
        file_metadata = {'name': f"FOTO_{nombre_cadete}_{date.today()}.jpg"}
        media = MediaIoBaseUpload(io.BytesIO(foto_archivo.getvalue()), mimetype='image/jpeg')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        # Permisos de lectura para que el link sea accesible
        drive_service.permissions().create(fileId=file.get('id'), body={'type': 'anyone', 'role': 'reader'}).execute()
        return file.get('webViewLink')
    except:
        return "Error al subir foto"

# --- TÍTULO ---
st.title("📑 SISTEMA DE LEGAJO DIGITAL - I.E.S.P.")
st.markdown("---")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🆔 Identidad", "📍 Localización", "🏥 Salud", 
    "👨‍👩‍👧‍👦 Familia", "🎓 Formación", "👮 Profesional"
])

# --- TAB 1: IDENTIDAD ---
with tab1:
    st.subheader("Fotografía Oficial y Datos Filiatorios")
    
    # REQUISITO DE FOTO (GALA DE VERANO)
    st.warning("📸 **REQUISITO DE FOTOGRAFÍA:** La imagen debe ser del cadete vistiendo **GALA DE VERANO** con todos sus atributos reglamentarios.")
    foto_perfil = st.file_uploader("Cargar fotografía oficial (Formato JPG/PNG)", type=['jpg', 'png', 'jpeg'])
    
    if foto_perfil:
        st.image(foto_perfil, width=150, caption="Vista previa de gala")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        apellido = st.text_input("Apellidos").upper()
        nombre = st.text_input("Nombres").upper()
        dni = st.text_input("DNI Nº")
        cuil = st.text_input("CUIL Nº")
    with c2:
        anio_cursa = st.selectbox("Año que cursa", ["1er Año", "2do Año", "3er Año"])
        estado_act = st.selectbox("Estado Actual", ["ACTIVO", "EN PROCESO", "LICENCIA", "BAJA"])
        prontuario = st.text_input("Prontuario Policial Nº")
        legajo_lp = st.text_input("L.P. Nº (Legajo)")
    with c3:
        f_nac = st.date_input("Fecha de Nacimiento", min_value=date(1980, 1, 1))
        edad = date.today().year - f_nac.year
        st.info(f"Edad Real: {edad} Años")
        lug_nac = st.text_input("Lugar de Nacimiento").upper()
        nacionalidad = st.text_input("Nacionalidad", value="ARGENTINA").upper()

    col_id2, col_id3 = st.columns(2)
    with col_id2:
        sexo = st.selectbox("Sexo (Según DNI)", ["MASCULINO", "FEMENINO", "X"])
        est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "VIUDO/A", "CONVIVIENTE"])
    with col_id3:
        cp = st.text_input("Código Postal")
        mano_habil = st.selectbox("Mano Hábil", ["DIESTRO", "ZURDO", "AMBIDIESTRO"])

    st.markdown("##### 🌐 Redes Sociales (Requisito D.G.I.I.)")
    col_redes1, col_redes2 = st.columns(2)
    with col_redes1:
        ig_user = st.text_input("Instagram (Usuario)").lower()
        fb_user = st.text_input("Facebook (Usuario)").lower()
    with col_redes2:
        tk_user = st.text_input("TikTok (Usuario)").lower()
        otras_redes = st.text_input("Otras Redes").lower()

    st.markdown("##### Biometría")
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        estatura = st.number_input("Estatura (cm)", 140, 220, 170)
        peso = st.number_input("Peso (kg)", 40, 160, 75)
    with cb2:
        imc = round(peso / ((estatura/100)**2), 2)
        estado_imc = "NORMAL" if imc < 25 else "SOBREPESO" if imc < 30 else "OBESIDAD"
        st.metric("IMC", f"{imc}", estado_imc)
    with cb3:
        gs = st.selectbox("Grupo Sanguíneo", ["A", "B", "AB", "0"])
        rh = st.selectbox("Factor RH", ["POSITIVO (+)", "NEGATIVO (-)"])
    senias = st.text_area("Señas Particulares").upper()

# --- TAB 2: LOCALIZACIÓN Y LOGÍSTICA ---
with tab2:
    st.subheader("Residencia y Contacto")
    cl1, cl2 = st.columns(2)
    with cl1:
        ur_destino = st.selectbox("Jurisdicción (UR)", ["U.R. CAPITAL", "U.R. NORTE", "U.R. SUR", "U.R. ESTE", "U.R. OESTE"])
        localidad_res = st.text_input("Localidad de Residencia").upper()
        departamento = st.text_input("Departamento").upper()
        domicilio_perm = st.text_input("Domicilio Permanente (Calle, Nº, Barrio)").upper()
    with cl2:
        comisaria_jur = st.text_input("Comisaría Jurisdiccional").upper()
        cel_particular = st.text_input("Celular Particular")
        tel_familiar = st.text_input("Teléfono Familiar / Allegado")
        movilidad = st.radio("¿Posee Movilidad Propia?", ["SI", "NO"], horizontal=True)

    st.markdown("##### Situación Habitacional y Conducción")
    ch1, ch2 = st.columns(2)
    with ch1:
        convive_txt = st.text_input("¿Con quién vive? (Resumen)").upper()
        alquila = st.selectbox("¿Alquila?", ["NO", "SI"])
        aviso_emerg = st.text_input("Avisar en caso de Emergencia a:").upper()
        tel_emerg = st.text_input("Teléfono de Emergencia")
    with ch2:
        conduce = st.selectbox("¿Conduce Vehículos?", ["SI", "NO"])
        que_conduce = st.text_input("¿Qué Conduce?").upper()
        carnet = st.selectbox("¿Posee Carnet?", ["SI", "NO"])
        clase_carnet = st.text_input("Clase de Licencia").upper()

# --- TAB 3: SALUD ---
with tab3:
    st.subheader("Monitor Clínico")
    with st.expander("🩺 Síntomas y Enfermedades"):
        col_m1, col_m2, col_m3 = st.columns(3)
        lista_enf = ["Tos", "Diarreas", "Diabetes", "Tuberculosis", "Cólicos renales", "Hipertiroidismo", 
                     "Falta de aire", "Infecciones Urinarias", "Hipotiroidismo", "Enfermedades respiratorias", 
                     "Reflujo", "Intoxicaciones", "Escupir sangre", "Acidez", "Asma", "Parasitosis",
                     "Pérdida conocimiento", "Epigastralgias", "Palpitaciones", "Hepatitis", "Hernias", 
                     "Dolor pecho", "Sangre orina", "E.T.S", "Hipertensión", "Dolor cabeza", "Chagas", 
                     "Convulsiones", "Dolores óseos", "Temblores", "Lumbalgias", "Ulceras", "Insomnio"]
        dict_enf = {}
        for i, enf in enumerate(lista_enf):
            target_col = [col_m1, col_m2, col_m3][i % 3]
            dict_enf[enf] = target_col.selectbox(enf, ["NO", "SI"], key=f"enf_{enf}")

    with st.expander("🦴 Antecedentes Traumáticos"):
        zonas = ["Cráneo", "Columna vertebral", "Tórax", "Pelvis", "Miembros Superiores", "Miembros Inferiores"]
        dict_trauma = {}
        for z in zonas:
            c_z1, c_z2 = st.columns([1, 2])
            tuvo = c_z1.selectbox(z, ["NO", "SI"], key=f"t_{z}")
            fec = c_z2.text_input(f"Fecha lesión {z}", key=f"f_{z}")
            dict_trauma[z] = f"{tuvo} ({fec})"
        relato_trauma = st.text_area("Relato del hecho de la lesión").upper()

    ant_fam_txt = st.text_area("Detalle enfermedades familiares").upper()
    tabaco = st.selectbox("Tabaco", ["NO", "SI"])
    alcohol = st.selectbox("Alcohol", ["NO", "SI"])
    act_fisica = st.text_input("Actividad física").upper()
    dieta = st.text_input("Dieta habitual").upper()

# --- TAB 4: FAMILIA Y CONVIVIENTES ---
with tab4:
    st.subheader("Datos Familiares")
    datos_hermanos = []
    for i in range(1, 6):
        with st.expander(f"Hermano N° {i}"):
            h_c1, h_c2 = st.columns(2)
            h_n = h_c1.text_input(f"Nombre (H{i})", key=f"hn_{i}").upper()
            h_d = h_c1.text_input(f"DNI (H{i})", key=f"hd_{i}")
            h_f = h_c2.date_input(f"F. Nac (H{i})", value=date(2000,1,1), key=f"hf_{i}")
            datos_hermanos.append(f"H{i}:{h_n}")

    datos_convivientes = []
    for i in range(1, 6):
        with st.expander(f"Conviviente N° {i}"):
            cv1, cv2 = st.columns(2)
            c_p = cv1.text_input(f"Parentesco (C{i})", key=f"cp_{i}").upper()
            c_n = cv1.text_input(f"Nombre (C{i})", key=f"cn_{i}").upper()
            c_d = cv2.text_input(f"DNI (C{i})", key=f"cd_{i}")
            datos_convivientes.append(f"C{i}:{c_n}({c_p})")

# --- TAB 5 Y 6 ---
with tab5:
    niv_alcanzado = st.selectbox("Nivel Académico", ["SECUNDARIO", "TERCIARIO", "UNIVERSITARIO"])
    titulo_obt = st.text_input("Título Obtenido").upper()

with tab6:
    st.subheader("Situación Profesional")
    otro_trabajo = st.selectbox("¿Tiene otro trabajo?", ["NO", "SI"])
    jerarquia = st.selectbox("Jerarquía Actual", ["CADETE", "CABO C.", "SARGENTO C."])
    arm_prov_m = st.text_input("Arma Marca").upper()
    arm_prov_s = st.text_input("Arma Serie")

# --- BOTÓN DE REGISTRO FINAL (43 CAMPOS) ---
st.markdown("---")
st.warning("⚠️ **DECLARACIÓN JURADA:** Declaro bajo juramento que los datos consignados son verídicos.")
acepto_legales = st.checkbox("Confirmo que los datos ingresados son verídicos.")

if st.button("🚀 REGISTRAR LEGAJO COMPLETO"):
    if acepto_legales and apellido and nombre and dni:
        with st.spinner("Procesando y subiendo legajo..."):
            try:
                # Subida de foto a Drive
                url_foto = subir_foto_drive(foto_perfil, f"{apellido}_{nombre}") if foto_perfil else "Sin Foto"

                # Consolidación de datos complejos
                string_enf = ", ".join([f"{k}" for k, v in dict_enf.items() if v == "SI"])
                string_trauma = ", ".join([f"{k}:{v}" for k, v in dict_trauma.items() if "SI" in v])
                
                # FILA SEGÚN TU ORDEN EXACTO (A-AQ)
                fila = [
                    str(date.today()), apellido, nombre, dni, cuil, str(f_nac), # A-F
                    edad, sexo, est_civil, legajo_lp, prontuario, anio_cursa,   # G-L
                    estatura, peso, imc, estado_imc, f"{gs} {rh}",             # M-Q
                    ur_destino, localidad_res, departamento, domicilio_perm,   # R-U
                    comisaria_jur, cel_particular, ig_user, fb_user, tk_user,  # V-Z
                    str(datos_hermanos), str(datos_convivientes),              # AA-AB
                    string_enf, string_trauma, relato_trauma, ant_fam_txt,     # AC-AF
                    tabaco, alcohol, act_fisica, dieta, niv_alcanzado,         # AG-AK
                    titulo_obt, otro_trabajo, jerarquia, arm_prov_m,           # AL-AP
                    arm_prov_s, url_foto                                       # AQ-AR
                ]
                
                sheet.append_row(fila)
                st.success(f"✅ Legajo de {nombre} {apellido} guardado con éxito.")
                st.balloons()
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("⚠️ Verifique DNI/Nombre y acepte la declaración jurada.")
