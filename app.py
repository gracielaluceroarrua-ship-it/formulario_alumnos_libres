import requests
import streamlit as st

st.set_page_config(page_title="Orientación Examen Libre - Inglés", page_icon="🎓")

# ==============================================================================
# BLOQUEO TEMPORAL PARA PRUEBAS (Se desactiva borrando CLAVE_PRUEBA en Secrets)
# ==============================================================================
clave_esperada = str(st.secrets.get("CLAVE_PRUEBA", "")).strip()

if clave_esperada:
    if "acceso_autorizado_libre" not in st.session_state:
        st.session_state.acceso_autorizado_libre = False

    if not st.session_state.acceso_autorizado_libre:
        st.title("🔒 Acceso restringido — Modo prueba")
        st.info("Este formulario se encuentra en etapa de revisión interna por el equipo docente.")
        with st.form("form_clave_prueba_libre"):
            clave_ingresada = st.text_input("Ingresá la clave de acceso:", type="password")
            entrar = st.form_submit_button("Ingresar")

        if entrar:
            if clave_ingresada.strip() == clave_esperada:
                st.session_state.acceso_autorizado_libre = True
                st.rerun()
            else:
                st.error("Clave incorrecta.")
        st.stop()
# ==============================================================================

# ==============================================================================
# CONFIGURACIÓN DE ENLACES Y DATOS DE CÁTEDRA
# ==============================================================================
CONTACTO_CATEDRA = "inglesfmn@gmail.com"
INFO_TRAMITE_EQUIVALENCIA = (
    "Para formalizar la equivalencia directa, debés presentar una nota junto con tu "
    "certificado internacional vigente o certificado analítico (donde conste la asignatura "
    "aprobada) ante **Departamento de Alumnos / Mesa de Entradas** de la Facultad."
)

ENLACES = {
    "doc_anual": "https://docs.google.com/document/d/1jC1P9zhkL4j011B5EoMWZlRrmXwWOcmtb32_LimmrAw/edit?usp=sharing",
    "doc_ingles1_mate": "https://docs.google.com/document/d/13q0lgdrUksGRbq56cnqI1KRs0t0LKolkpBnIYYUPOCs/edit?usp=sharing",
    "doc_cuatrimestral": "https://docs.google.com/document/d/1rrQyOZxmKrBpPKNJxA-a_0iPXxJYBhMFni8y55Qs_As/edit?usp=sharing",
    "doc_ingles2_mate": "https://docs.google.com/document/d/1x7dB5FCesmA2F9y7jawb-iw68-xIcX8vQjd6kLWagjg/edit?usp=sharing",
    "mat_anual": "https://drive.google.com/drive/folders/1_6Leh5alrdQ5QsW_TUmWiPkfl1KeYkop?usp=sharing",
    "mat_cuatrimestral_ing1": "https://drive.google.com/drive/folders/1AorCtjNsx1EYtM0M59TTgbELZNKR4Qy3?usp=drive_link",
    "mat_ingles2": "https://drive.google.com/drive/folders/1OVIbO2i7onTyJxyIWcFia3juJV-NPTo4?usp=drive_link",
}

CARRERAS = {
    # --- ANUALES ---
    "Inglés para Lic. en Cs. Matemáticas (Plan 9/17)": "Anual",
    "Inglés para Profesorado en Tecnología Electrónica (Plan 05/09)": "Anual",
    "Inglés para Tecnicatura Universitaria en Electrónica (Plan 15/13)": "Anual",
    "Inglés para Tecnicatura Universitaria en Telecomunicaciones (Plan 16/13)": "Anual",
    "Inglés para Ingeniería en Electrónica con Orientación en Sistemas Digitales (Plan 13/08 - OCD-6/24)": "Anual",
    "Inglés para Tecnicatura Universitaria en Energías Renovables (Plan 05/13)": "Anual",
    "Inglés para Lic. en Física (Plan 15/06)": "Anual",
    "Inglés para Prof. en Física (Plan 16/06)": "Anual",
    "Inglés para Ingeniería en Computación (Plan 28/12)": "Anual",
    "Inglés para Ingeniería en Informática (Plan 26/12 - OCD-2/25)": "Anual",
    "Inglés para Prof. en Cs. de la Computación (Plan 35/86)": "Anual",
    "Inglés para Tecnicatura Universitaria en Redes de Computadoras (Plan 12/15)": "Anual",
    "Inglés para Tecnicatura Universitaria en Web (Plan 08/13)": "Anual",
    "Inglés para Tecnicatura Universitaria en Teledetección y Sistemas de Información Geográfica - T-SIG (OCD-13/22)": "Anual",
    # --- INGLÉS II (PROF. EN MATEMÁTICA) ---
    "Inglés II para Profesorado en Matemática": "Ingles_II_Mate",
    # --- CUATRIMESTRALES ---
    "Inglés I para Profesorado en Matemática": "Ingles_I_Mate",
    "Inglés para Lic. en Cs. Geológicas (Plan 02/22)": "Cuatrimestral",
    "Inglés para Ingeniería en Minas (Plan 11/23)": "Cuatrimestral",
    # --- VOCACIONAL (CUATRIMESTRAL ÚNICO) ---
    "Inglés Vocacional - Tecnicatura Universitaria en Minería (Plan 6/15)": "Vocacional_Cuatrimestral",
    "Inglés Vocacional - Tecnicatura Universitaria en Obras Viales (Plan 01/18 - comisión cuatrimestral 45 hs)": "Vocacional_Cuatrimestral_ObrasViales",
    # --- VOCACIONAL (ANUAL) ---
    "Inglés Vocacional - Tecnicatura Universitaria en Fotografía (Plan 15/15)": "Vocacional_Anual",
}

ETIQUETAS_MODALIDAD = {
    "Anual": "Anual",
    "Ingles_II_Mate": "Anual (Segunda parte - Inglés II Prof. Matemática)",
    "Ingles_I_Mate": "Cuatrimestral (Inglés I Prof. Matemática)",
    "Cuatrimestral": "Cuatrimestral",
    "Vocacional_Cuatrimestral": "Vocacional - Cuatrimestral (único)",
    "Vocacional_Cuatrimestral_ObrasViales": "Vocacional - Cuatrimestral (45 hs)",
    "Vocacional_Anual": "Vocacional - Anual (Fotografía)",
}


def enviar_a_sheets(payload: dict) -> bool:
    url = str(st.secrets.get("APPS_SCRIPT_URL", "")).strip()
    if not url:
        st.error("Falta configurar APPS_SCRIPT_URL en Secrets o falta reiniciar la app (Reboot).")
        return False
    try:
        resp = requests.post(url, json=payload, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") == "ok":
                    return True
                st.error(f"Apps Script devolvió un error: {data}")
                return False
            except ValueError:
                st.error("Apps Script no devolvió JSON válido. Verificá que el acceso sea 'Cualquier persona'.")
                return False
        st.error(f"Error HTTP {resp.status_code} al conectar con Google Sheets.")
        return False
    except Exception as e:
        st.error(f"Error de conexión con la planilla: {e}")
        return False


# ==============================================================================
# INTERFAZ DE USUARIO
# ==============================================================================
st.title("🎓 Orientación para Examen Libre de Inglés")
st.write(
    "Completá tus datos para conocer tu situación académica, acceder a los programas "
    "y descargar el material correspondiente."
)

nombre = st.text_input("Apellido y Nombre completos")
dni = st.text_input("DNI (sin puntos)")
email = st.text_input("Correo electrónico")
carrera = st.selectbox(
    "Seleccioná tu carrera",
    ["Seleccionar..."] + list(CARRERAS.keys()),
)

clave_mod = CARRERAS.get(carrera, "")
ruta_asignada = ""
tiene_antecedente = "No"

if carrera != "Seleccionar...":
    st.info(f"Modalidad asignada: **{ETIQUETAS_MODALIDAD[clave_mod]}**")

    tiene_antecedente = st.radio(
        "¿Poseés certificado internacional vigente (nivel A2 o superior) o Inglés aprobado en otra carrera universitaria?",
        ["No", "Sí"],
    )

    if tiene_antecedente == "Sí":
        ruta_asignada = "Equivalencia directa"
        st.success("✅ **Te corresponde tramitar Equivalencia Directa.**")
        st.markdown(INFO_TRAMITE_EQUIVALENCIA)
        st.markdown(
            f"Si necesitás orientación previa sobre la validez de tu certificado, escribinos a: "
            f"**{CONTACTO_CATEDRA}**"
        )
        st.file_uploader(
            "Podés adjuntar aquí tu certificado o constancia para pre-revisión (PDF, JPG, PNG)",
            type=["pdf", "jpg", "png"],
        )
    else:
        st.subheader("📋 Orientación y Materiales Asignados")

        if clave_mod == "Anual":
            ruta_asignada = "Libre Anual (Lectura + Comunicación; 1.ª consulta tras Actividad 1)"
            st.markdown(
                "- **Ejes evaluados:** Lectura académica y comunicación.\n"
                "- **Régimen de consultas:** La primera consulta se otorga una vez resuelta "
                "y enviada la **primera actividad** del cronograma; desde allí se pactan las siguientes."
            )
            st.link_button("📄 Programa y Orientación (Inglés Anual)", ENLACES["doc_anual"])
            st.link_button("📂 Carpeta de Material (Inglés Anual)", ENLACES["mat_anual"])

        elif clave_mod == "Ingles_II_Mate":
            ruta_asignada = "Libre Inglés II Prof. Matemática (Segunda parte curso anual; 1.ª consulta tras Actividad 1)"
            st.markdown(
                "- **Alcance:** Corresponde a la **segunda parte** del curso anual.\n"
                "- **Régimen de consultas:** La primera consulta se otorga una vez resuelta "
                "y enviada la **primera actividad** del cronograma; desde allí se pactan las siguientes."
            )
            st.link_button("📄 Programa y Orientación (Inglés II - Prof. Matemática)", ENLACES["doc_ingles2_mate"])
            st.link_button("📂 Carpeta de Material (Inglés II)", ENLACES["mat_ingles2"])

        elif clave_mod == "Ingles_I_Mate":
            ruta_asignada = "Libre Inglés I Prof. Matemática (Lectura; 1.ª consulta tras Actividad 1)"
            st.markdown(
                "- **Eje evaluado:** Lectura académica.\n"
                "- **Régimen de consultas:** La primera consulta se otorga una vez resuelta "
                "y enviada la **primera actividad** del cronograma; desde allí se pactan las siguientes."
            )
            st.link_button("📄 Programa y Orientación (Inglés I - Prof. Matemática)", ENLACES["doc_ingles1_mate"])
            st.link_button("📂 Carpeta de Material (Inglés Cuatrimestral / Inglés I)", ENLACES["mat_cuatrimestral_ing1"])

        elif clave_mod == "Cuatrimestral":
            ruta_asignada = "Libre Cuatrimestral (Lectura; 1.ª consulta tras Actividad 1)"
            st.markdown(
                "- **Eje evaluado:** Lectura académica.\n"
                "- **Régimen de consultas:** La primera consulta se otorga una vez resuelta "
                "y enviada la **primera actividad** del cronograma; desde allí se pactan las siguientes."
            )
            st.link_button("📄 Programa y Orientación (Inglés Cuatrimestral)", ENLACES["doc_cuatrimestral"])
            st.link_button("📂 Carpeta de Material (Inglés Cuatrimestral / Inglés I)", ENLACES["mat_cuatrimestral_ing1"])

        elif clave_mod == "Vocacional_Cuatrimestral":
            ruta_asignada = "Vocacional Cuatrimestral único (Sugerencia vocacional + Solo lectura)"
            st.markdown(
                "- **Recomendación:** Presentar nota solicitando incorporación como "
                "**alumno/a vocacional**.\n"
                "- **Modalidad:** Inglés cuatrimestral único (eje de lectura)."
            )
            st.link_button("📄 Programa y Orientación (Inglés Cuatrimestral)", ENLACES["doc_cuatrimestral"])
            st.link_button("📂 Carpeta de Material (Inglés Cuatrimestral / Inglés I)", ENLACES["mat_cuatrimestral_ing1"])

        elif clave_mod == "Vocacional_Cuatrimestral_ObrasViales":
            ruta_asignada = "Vocacional Cuatrimestral 45 hs - Obras Viales (Sugerencia vocacional + Solo lectura)"
            st.markdown(
                "- **Recomendación:** Presentar nota solicitando incorporación como "
                "**alumno/a vocacional**.\n"
                "- **Modalidad:** Incorporación a la comisión de inglés cuatrimestral de **45 hs** (eje de lectura)."
            )
            st.link_button("📄 Programa y Orientación (Inglés Cuatrimestral)", ENLACES["doc_cuatrimestral"])
            st.link_button("📂 Carpeta de Material (Inglés Cuatrimestral / Inglés I)", ENLACES["mat_cuatrimestral_ing1"])

        elif clave_mod == "Vocacional_Anual":
            ruta_asignada = "Vocacional Anual - Fotografía (Sugerencia vocacional + Material completo)"
            st.markdown(
                "- **Recomendación:** Presentar nota solicitando incorporación como "
                "**alumno/a vocacional**.\n"
                "- **Modalidad:** Inglés anual (material completo: lectura y comunicación)."
            )
            st.link_button("📄 Programa y Orientación (Inglés Anual / Fotografía)", ENLACES["doc_anual"])
            st.link_button("📂 Carpeta de Material (Inglés Anual)", ENLACES["mat_anual"])

        st.caption(f"Consultas administrativas o envío de actividad inicial: {CONTACTO_CATEDRA}")

st.divider()
mesa_comentarios = st.text_input("Comentario breve (opcional)")

if st.button("Registrar consulta", type="primary"):
    if carrera == "Seleccionar...":
        st.warning("Por favor, seleccioná primero tu carrera / espacio curricular.")
    elif not (nombre.strip() and dni.strip() and email.strip()):
        st.warning("Completá Apellido y Nombre, DNI y correo electrónico antes de registrar.")
    else:
        with st.spinner("Registrando en la planilla..."):
            datos = {
                "nombre": nombre.strip(),
                "dni": dni.strip(),
                "email": email.strip(),
                "carrera": carrera,
                "modalidad": ETIQUETAS_MODALIDAD[clave_mod],
                "antecedente": tiene_antecedente,
                "ruta_asignada": ruta_asignada,
                "mesa_comentarios": mesa_comentarios.strip(),
            }
            if enviar_a_sheets(datos):
                st.success("✅ ¡Consulta registrada en la planilla correctamente!")
