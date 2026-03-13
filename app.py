import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import google.generativeai as genai

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Legajo Digital IESP", layout="wide")

# Configuración IA (Recuerda poner tu clave real)
genai.configure(api_key="TU_API_KEY_AQUI")

# Conexión a Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
try:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("ROL DE COMBATE").sheet1
except:
    st.error("Error de conexión. Revisa los Secrets y el nombre del Excel.")

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
    st.subheader("Datos Filiatorios y Biometría")
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

    # REDES SOCIALES (NUEVO REQUISITO D.G.I.I.)
    st.markdown("##### 🌐 Redes Sociales (Requisito D.G.I.I.)")
    col_redes1, col_redes2 = st.columns(2)
    with col_redes1:
        ig_user = st.text_input("Instagram (Usuario)").lower()
        fb_user = st.text_input("Facebook (Usuario)").lower()
    with col_redes2:
        tw_user = st.text_input("X / Twitter (Usuario)").lower()
        otras_redes = st.text_input("Otras Redes (TikTok, etc.)").lower()

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

    cl_apt = st.columns(2)
    with cl_apt[0]:
        sabe_nadar = st.radio("¿Sabe Nadar?", ["SI", "NO"], horizontal=True)
    with cl_apt[1]:
        sabe_cabalgar = st.radio("¿Sabe Cabalgar?", ["SI", "NO"], horizontal=True)

# --- TAB 3: SALUD ---
with tab3:
    st.subheader("Monitor Clínico y Antecedentes Médicos")
    
    with st.expander("🩺 Síntomas y Enfermedades (Seleccione SI/NO)"):
        col_m1, col_m2, col_m3 = st.columns(3)
        lista_enf = ["Tos", "Diarreas", "Diabetes", "Tuberculosis", "Cólicos renales", "Hipertiroidismo", 
                     "Falta de aire", "Infecciones Urinarias", "Hipotiroidismo", "Enfermedades respiratorias", 
                     "Reflujo", "Intoxicaciones", "Escupir sangre", "Acidez", "Asma", "Parasitosis",
                     "Pérdida conocimiento", "Epigastralgias", "Palpitaciones", "Hepatitis", "Hernias", 
                     "Dolor pecho", "Sangre orina", "E.T.S", "Hipertensión", "Dolor cabeza", "Chagas", 
                     "Convulsiones", "Dolores óseos", "Temblores", "Lumbalgias", "Ulceras", "Insomnio"]
        dict_enf = {}
        for i, enf in enumerate(lista_enf):
            if i % 3 == 0: col = col_m1
            elif i % 3 == 1: col = col_m2
            else: col = col_m3
            dict_enf[enf] = col.selectbox(enf, ["NO", "SI"], key=f"enf_{enf}")

    with st.expander("🦴 Antecedentes Traumáticos (Zonas Afectadas)"):
        zonas = ["Cráneo", "Columna vertebral", "Tórax", "Pelvis", "Miembros Superiores", "Miembros Inferiores"]
        dict_trauma = {}
        for z in zonas:
            c_z1, c_z2 = st.columns([1, 2])
            with c_z1:
                tuvo = c_z1.selectbox(z, ["NO", "SI"], key=f"t_{z}")
            with c_z2:
                fec = c_z2.text_input(f"Fecha lesión {z}", key=f"f_{z}")
            dict_trauma[z] = f"{tuvo} ({fec})"
        relato_trauma = st.text_area("Relato del hecho de la lesión").upper()

    with st.expander("🧬 Antecedentes Familiares"):
        ant_fam_txt = st.text_area("Detalle enfermedades familiares (Padre, Madre, Abuelos, Hermanos)").upper()

    with st.expander("🚬 Hábitos y Otros"):
        hab_c1, hab_c2 = st.columns(2)
        tabaco = hab_c1.selectbox("Tabaco", ["NO", "SI"])
        alcohol = hab_c1.selectbox("Alcohol", ["NO", "SI"])
        sustancias = hab_c1.text_input("Otras sustancias").upper()
        act_fisica = hab_c2.text_input("Actividad física").upper()
        medicamentos = hab_c2.text_input("Medicamentos").upper()
        dieta = hab_c2.text_input("Dieta habitual").upper()
        internaciones = st.text_area("Internaciones previas").upper()
        condicion_especial = st.text_area("¿Condición que interfiera con la función?").upper()

# --- TAB 4: FAMILIA Y CONVIVIENTES (NUEVO REQUISITO D.G.I.I.) ---
with tab4:
    st.subheader("Datos Familiares y Grupo Conviviente")
    
    # 1. PROGENITORES (NUEVO)
    st.markdown("#### 👨‍👩‍👦 Progenitores (Padre y Madre)")
    for pariente in ["PADRE", "MADRE"]:
        with st.expander(f"Datos de la {pariente}"):
            cp1, cp2 = st.columns(2)
            with cp1:
                st.selectbox(f"¿Vive? ({pariente})", ["SI", "NO"], key=f"v_{pariente}")
                st.text_input(f"Nombre Completo ({pariente})", key=f"n_{pariente}").upper()
            with cp2:
                st.text_input(f"DNI ({pariente})", key=f"d_{pariente}")
                st.text_input(f"Celular ({pariente})", key=f"c_{pariente}")

    # 2. HERMANOS
    st.markdown("#### 👤 Hermanos (Hasta 5)")
    datos_hermanos = []
    for i in range(1, 6):
        with st.expander(f"Hermano N° {i}"):
            h_c1, h_c2 = st.columns(2)
            with h_c1:
                h_v = st.selectbox(f"¿Vive? (H{i})", ["SI", "NO"], key=f"hv_{i}")
                h_n = st.text_input(f"Nombre (H{i})", key=f"hn_{i}").upper()
                h_d = st.text_input(f"DNI (H{i})", key=f"hd_{i}")
            with h_c2:
                h_c = st.text_input(f"CUIL (H{i})", key=f"hc_{i}")
                h_f = st.date_input(f"F. Nac (H{i})", value=date(2000,1,1), key=f"hf_{i}")
                h_t = st.text_input(f"Celular (H{i})", key=f"ht_{i}")
            datos_hermanos.append(f"H{i}:{h_n}")

    # 3. GRUPO CONVIVIENTE (NUEVO)
    st.markdown("#### 🏠 Grupo Conviviente (Personas que viven con usted)")
    datos_convivientes = []
    for i in range(1, 6):
        with st.expander(f"Conviviente N° {i}"):
            cv1, cv2 = st.columns(2)
            with cv1:
                c_p = st.text_input(f"Parentesco (C{i})", key=f"cp_{i}").upper()
                c_n = st.text_input(f"Nombre (C{i})", key=f"cn_{i}").upper()
            with cv2:
                c_d = st.text_input(f"DNI (C{i})", key=f"cd_{i}")
                c_e = st.number_input(f"Edad (C{i})", 0, 100, 20, key=f"ce_{i}")
                c_t = st.text_input(f"Celular (C{i})", key=f"ct_{i}")
            datos_convivientes.append(f"C{i}:{c_n}({c_p})")

# --- TAB 5 Y 6 (FORMACIÓN Y PROFESIONAL) ---
with tab5:
    niv_alcanzado = st.selectbox("Máximo Nivel Alcanzado", ["SECUNDARIO", "TERCIARIO", "UNIVERSITARIO"])
    titulo_obt = st.text_input("Título Obtenido").upper()
    cursos_ext = st.text_area("Otros Cursos").upper()

with tab6:
    st.subheader("Situación Profesional y Armamento")
    cp_c1, cp_c2 = st.columns(2)
    otro_trabajo = cp_c1.selectbox("¿Tiene otro trabajo?", ["NO", "SI"])
    tipo_trabajo = cp_c1.text_input("¿Qué tipo?").upper()
    tuvo_accidente = cp_c2.selectbox("¿Tuvo accidente?", ["NO", "SI"])
    det_accidente = cp_c2.text_input("¿De qué tipo?").upper()
    st.markdown("---")
    jerarquia = st.selectbox("Jerarquía Actual", ["CADETE", "CABO C.", "SARGENTO C."])
    arm_prov_m = st.text_input("Arma Marca").upper()
    arm_prov_s = st.text_input("Arma Serie")

# --- BOTÓN DE CARGA Y DECLARACIÓN JURADA ---
st.markdown("---")
st.warning("⚠️ **DECLARACIÓN JURADA:** Declaro bajo juramento que los datos consignados son verídicos y me hago responsable ante cualquier inconveniente. La falsedad de lo declarado será sujeto a medidas legales pertinente.")
acepto_legales = st.checkbox("Confirmo que los datos ingresados son verídicos.")

if st.button("🚀 REGISTRAR LEGAJO COMPLETO"):
    if acepto_legales:
        if apellido and nombre and dni:
            try:
                string_enf = ", ".join([f"{k}:{v}" for k, v in dict_enf.items() if v == "SI"])
                string_trauma = ", ".join([f"{k}:{v}" for k, v in dict_trauma.items() if "SI" in v])
                
                fila = [
                    str(date.today()), apellido, nombre, dni, cuil, str(f_nac), edad, sexo, 
                    anio_cursa, ur_destino, localidad_res, domicilio_perm, cel_particular, 
                    ig_user, fb_user, tw_user, str(datos_hermanos), str(datos_convivientes),
                    string_enf, string_trauma, relato_trauma, ant_fam_txt, tabaco, alcohol, 
                    act_fisica, dieta, niv_alcanzado, titulo_obt, otro_trabajo, jerarquia, arm_prov_m
                ]
                sheet.append_row(fila)
                st.success("✅ Legajo guardado con éxito bajo juramento.")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Apellido, Nombre y DNI son obligatorios.")
    else:
        st.error("❌ Debe aceptar la declaración jurada para registrar los datos.")
