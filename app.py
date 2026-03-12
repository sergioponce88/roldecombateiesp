import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import google.generativeai as genai

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Legajo Digital IESP", layout="wide")

# Configuración IA
genai.configure(api_key="TU_API_KEY_AQUI")

# Conexión a Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
try:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("ROL DE COMBATE").sheet1
except:
    st.error("Error de conexión. Revisa los Secrets y el nombre del Excel.")

# --- TÍTULO Y ESTILO ---
st.title("📑 SISTEMA DE LEGAJO DIGITAL - I.E.S.P.")
st.markdown("---")

# --- PESTAÑAS PRINCIPALES ---
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
        convive = st.text_input("¿Con quién vive?").upper()
        alquila = st.selectbox("¿Alquila?", ["NO", "SI"])
        aviso_emerg = st.text_input("Avisar en caso de Emergencia a:").upper()
        tel_emerg = st.text_input("Teléfono de Emergencia")
    with ch2:
        conduce = st.selectbox("¿Conduce Vehículos?", ["SI", "NO"])
        que_conduce = st.text_input("¿Qué Conduce? (Auto, Moto, etc.)").upper()
        carnet = st.selectbox("¿Posee Carnet?", ["SI", "NO"])
        clase_carnet = st.text_input("Clase de Licencia (Ej: B1)").upper()

    cl_apt = st.columns(2)
    with cl_apt[0]:
        sabe_nadar = st.radio("¿Sabe Nadar?", ["SI", "NO"], horizontal=True)
    with cl_apt[1]:
        sabe_cabalgar = st.radio("¿Sabe Cabalgar?", ["SI", "NO"], horizontal=True)

# --- TAB 3: SALUD Y VISU ---
with tab3:
    st.subheader("Monitor Clínico y Antecedentes")
    cs1, cs2 = st.columns(2)
    with cs1:
        alergias = st.selectbox("¿Posee Alergias?", ["NO", "SI"])
        espec_alergia = st.text_input("Especifique Alérgeno").upper()
        enf_congenita = st.selectbox("¿Enfermedad Congénita?", ["NO", "SI"])
        usa_anteojos = st.selectbox("¿Usa Anteojos?", ["NO", "SI"])
    with cs2:
        tuvo_covid = st.selectbox("¿Tuvo COVID-19?", ["NO", "SI"])
        cant_covid = st.text_input("Cantidad de veces")
        esquema_vac = st.selectbox("Esquema de Vacunación", ["INCOMPLETO", "DOS DOSIS", "REFUERZO COMPLETADO"])

    st.markdown("##### Examen Visual (VISU)")
    cv1, cv2 = st.columns(2)
    with cv1:
        f_visu = st.date_input("Fecha último Examen Visual")
        res_visu = st.selectbox("Resultado VISU", ["APTO", "NO APTO", "PENDIENTE"])
    with cv2:
        obs_visu = st.text_area("Observaciones Médicas / Tatuajes").upper()

# --- TAB 4: GRUPO FAMILIAR ---
with tab4:
    st.subheader("Composición Familiar")
    st.warning("Complete los datos de sus familiares directos (Padres, Hijos, Cónyuge).")
    familiares_data = st.text_area("Listado de Familiares (Vínculo, Nombre, DNI, Celular)").upper()
    cargas_fam = st.number_input("Cantidad total de personas a cargo", 0, 15, 0)

# --- TAB 5: FORMACIÓN ACADÉMICA ---
with tab5:
    st.subheader("Perfil Académico")
    cf1, cf2 = st.columns(2)
    with cf1:
        niv_alcanzado = st.selectbox("Máximo Nivel Alcanzado", ["SECUNDARIO", "TERCIARIO", "UNIVERSITARIO", "POSGRADO"])
        est_academico = st.selectbox("Estado del Nivel", ["COMPLETO", "INCOMPLETO", "EN CURSO"])
    with cf2:
        titulo_obt = st.text_input("Título Obtenido / Carrera").upper()
        inst_emisora = st.text_input("Establecimiento Emisor").upper()
    
    cursos_ext = st.text_area("Otros Cursos, Talleres u Oficios").upper()

# --- TAB 6: SITUACIÓN PROFESIONAL Y ARMAMENTO ---
with tab6:
    st.subheader("Datos de Revista y Equipamiento")
    cp1, cp2 = st.columns(2)
    with cp1:
        jerarquia = st.selectbox("Jerarquía Actual", ["CADETE 1ER AÑO", "CADETE 2DO AÑO", "CADETE 3ER AÑO", "CABO CADETE", "SARGENTO CADETE"])
        f_ascenso = st.date_input("Fecha último Ascenso")
        monto_beca = st.number_input("Monto Beca/Sueldo", value=0.0)
    with cp2:
        situacion_rev = st.selectbox("Situación de Revista", ["SERVICIO EFECTIVO", "LICENCIA MÉDICA", "DISPONIBILIDAD"])
        destino_act = st.text_input("Unidad / Destino Actual", value="I.E.S.P.").upper()
        dom_laboral = st.text_input("Domicilio Laboral", value="MUÑECAS 1025 - SMT").upper()

    st.markdown("##### Armamento")
    arm1, arm2 = st.columns(2)
    with arm1:
        st.write("**Provisto**")
        arm_prov_m = st.text_input("Marca (Provisto)").upper()
        arm_prov_s = st.text_input("Nº Serie (Provisto)")
    with arm2:
        st.write("**Particular**")
        arm_part_m = st.text_input("Marca (Particular)").upper()
        arm_part_s = st.text_input("Nº Serie (Particular)")

# --- BOTÓN FINAL DE CARGA ---
st.markdown("---")
if st.button("🚀 REGISTRAR LEGAJO COMPLETO"):
    if apellido and nombre and dni:
        try:
            fila_datos = [
                str(date.today()), apellido, nombre, dni, cuil, str(f_nac), edad, sexo, est_civil, 
                legajo_lp, prontuario, anio_cursa, estatura, peso, imc, estado_imc, f"{gs} {rh}", 
                ur_destino, localidad_res, departamento, domicilio_perm, comisaria_jur, cel_particular, 
                tel_familiar, aviso_emerg, tel_emerg, movilidad, alquila, convive, sabe_nadar, 
                sabe_cabalgar, conduce, que_conduce, carnet, clase_carnet, alergias, espec_alergia, 
                enf_congenita, usa_anteojos, res_visu, esquema_vac, cargas_fam, familiares_data, 
                niv_alcanzado, titulo_obt, cursos_ext, jerarquia, situacion_rev, arm_prov_m, arm_prov_s
            ]
            sheet.append_row(fila_datos)
            st.success(f"✅ Legajo de {nombre} {apellido} registrado con éxito en la Base de Datos.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    else:
        st.warning("⚠️ Los campos de Apellido, Nombre y DNI son obligatorios.")
