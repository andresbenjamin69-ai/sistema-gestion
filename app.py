import streamlit as st
from supabase import create_client

# Configuración de la ventana
st.set_page_config(page_title="Sistema de Gestión", layout="centered")
st.title("💼 Sistema de Gestión - Clientes")

# Conexión ultra segura utilizando credenciales ocultas
@st.cache_resource
def conectar_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = conectar_supabase()

# Interfaz del Buscador
st.subheader("Buscador de Clientes")
busqueda = st.text_input("Ingrese nombre a buscar:")

# Consulta a la base de datos Supabase
if busqueda:
    respuesta = supabase.table("clientes").select("*").ilike("nombre", f"%{busqueda}%").execute()
else:
    respuesta = supabase.table("clientes").select("*").execute()

# Mostrar datos en pantalla
datos = respuesta.data
if datos:
    for cliente in datos:
        st.write(f"👤 **{cliente['nombre']}** — 📞 Teléfono: {cliente['telefono']}")
else:
    st.info("No se encontraron clientes.")
