import streamlit as st
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(page_title="Sistema de Gestión - Clientes", page_icon="💼")
st.title("💼 Sistema de Gestión - Clientes")

# Conexión a Supabase usando Secrets de Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    # Limpiamos la URL de barras al final por seguridad
    url = url.rstrip('/')
    return create_client(url, key)

try:
    supabase = init_supabase()

    # Buscador en tiempo real
    busqueda = st.text_input("🔍 Ingrese nombre a buscar:")

    # Consulta a la base de datos Supabase
    if busqueda:
        respuesta = supabase.table("clientes").select("*").ilike("nombre", f"%{busqueda}%").execute()
    else:
        respuesta = supabase.table("clientes").select("*").execute()

    # Mostrar datos en pantalla
    datos = respuesta.data

    if datos:
        st.subheader(f"Lista de Clientes ({len(datos)})")
        for cliente in datos:
            st.write(f"👤 **{cliente['nombre']}** — 📞 Teléfono: {cliente.get('telefono', 'Sin teléfono')}")
    else:
        st.info("No se encontraron clientes.")

except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
