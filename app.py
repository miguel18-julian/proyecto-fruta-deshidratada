import streamlit as st
import sqlite3
import pandas as pd
import re
import time
from streamlit_option_menu import option_menu

# ==========================================
# CONFIGURACIÓN Y ESTILOS VISUALES
# ==========================================
st.set_page_config(page_title="VitalFruit | 100% Natural", page_icon="🍃", layout="wide")

# Inyección de CSS para simular el diseño de "come verde"
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general */
    .stApp {
        background-color: #F4F1E1; /* Beige claro de fondo */
    }

    /* Estilo del navbar (simulado con color de fondo) */
    .nav-container {
        background-color: #005A32; /* Verde oscuro */
        padding: 10px 0;
        margin-top: -60px; /* Ajuste para subir el nav */
        margin-bottom: 20px;
    }

    /* Títulos y textos generales */
    h1, h2, h3, p {
        color: #005A32 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Botones estilo "Mostrar Todo" */
    .stButton>button {
        background-color: #81C784 !important; /* Verde claro */
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #66BB6A !important;
    }

    /* Ajuste de imágenes para que se parezcan a los empaques */
    img {
        border-radius: 15px;
    }
    
    /* Contenedor del Chat (Burbuja IA) */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BASE DE DATOS
# ==========================================
def init_db():
    conn = sqlite3.connect('ventas_fruta.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ventas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  cliente TEXT, producto TEXT, cantidad INTEGER, total REAL,
                  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()

# ==========================================
# MENÚ DE NAVEGACIÓN SUPERIOR
# ==========================================
# Creamos un contenedor verde oscuro en la parte superior
st.markdown('<div class="nav-container"></div>', unsafe_allow_html=True)

# Usamos streamlit_option_menu para un navbar más estético
selected = option_menu(
    menu_title=None,
    options=["Productos", "Burbuja IA", "Panel de Ventas"],
    icons=["bag", "chat-dots", "graph-up"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#005A32", "border-radius": "0"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#004020"},
        "nav-link-selected": {"background-color": "#81C784"},
    }
)

# Título principal de la página
st.markdown("<h2 style='text-align: center;'>Conoce todos nuestros productos</h2>", unsafe_allow_html=True)

# ==========================================
# SECCIÓN 1: TIENDA (Productos)
# ==========================================
if selected == "Productos":
    # Fila de botones simulados (como filtros)
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1,1,2,1,1])
    with col_f3:
        st.markdown("<div style='text-align: center;'><button style='background-color:#81C784; border:none; border-radius:20px; color:white; padding:5px 15px; margin:5px;'>MOSTRAR TODO</button><button style='background-color:#81C784; border:none; border-radius:20px; color:white; padding:5px 15px; margin:5px;'>FRUTA DESHIDRATADA</button></div>", unsafe_allow_html=True)

    st.write("") # Espacio

    # Productos (Imágenes de ejemplo similares a empaques)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=400", caption="Mango Deshidratado")
        st.markdown("<p style='text-align:center;'>$25.00 MXN</p>", unsafe_allow_html=True)
    with col2:
         st.image("https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?q=80&w=400", caption="Manzana Deshidratada")
         st.markdown("<p style='text-align:center;'>$20.00 MXN</p>", unsafe_allow_html=True)
    with col3:
        st.image("https://images.unsplash.com/photo-1519996409144-56c88c9aa612?q=80&w=400", caption="Mix Frutal")
        st.markdown("<p style='text-align:center;'>$35.00 MXN</p>", unsafe_allow_html=True)

    st.divider()
    
    # Formulario de compra
    st.subheader("🛒 Realizar Compra")
    with st.form("form_venta", clear_on_submit=True):
        col_c, col_p, col_q = st.columns([2, 2, 1])
        with col_c:
            cliente = st.text_input("Nombre:")
        with col_p:
            producto = st.selectbox("Producto:", 
                                    ["Mango Deshidratado - $25.00", "Manzana Deshidratada - $20.00", "Mix Frutal - $35.00"])
        with col_q:
            cantidad = st.number_input("Cantidad:", min_value=1, value=1)
            
        comprar = st.form_submit_button("Comprar")
        
        if comprar and cliente:
            precio = float(re.search(r'\$([0-9.]+)', producto).group(1))
            total = precio * cantidad
            c = conn.cursor()
            c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                      (cliente, producto.split(" -")[0], cantidad, total))
            conn.commit()
            st.success(f"¡Pedido procesado para {cliente} por ${total:.2f} MXN!")

# ==========================================
# SECCIÓN 2: BURBUJA IA
# ==========================================
elif selected == "Burbuja IA":
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.subheader("🤖 Asistente de Mercado")
    st.write("Ingresa los datos de producción de tu deshidratador.")

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "assistant", "contenido": "Hola. Dime el costo total del lote, bolsas obtenidas y precio de competencia."}
        ]

    for msj in st.session_state.mensajes:
        with st.chat_message(msj["rol"]):
            st.markdown(msj["contenido"])

    if entrada := st.chat_input("Ej: Costo $150, bolsas 20, competencia $25"):
        with st.chat_message("user"):
            st.markdown(entrada)
        st.session_state.mensajes.append({"rol": "user", "contenido": entrada})

        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                time.sleep(1)
                numeros = [float(n) for n in re.findall(r'\d+\.?\d*', entrada)]
                
                if len(numeros) >= 3:
                    costo_unit = numeros[0] / numeros[1]
                    precio_sug = numeros[2] * 0.85
                    margen = precio_sug - costo_unit
                    
                    resp = f"**Análisis:**\n- Costo Unitario: ${costo_unit:.2f}\n- Precio Sugerido: **${precio_sug:.2f}**\n"
                    if margen > 0:
                        resp += f"✅ Margen de ganancia: **${margen:.2f}** por bolsa."
                    else:
                        resp += f"⚠️ Pérdida de ${abs(margen):.2f} por bolsa."
                else:
                    resp = "Faltan datos. Necesito: costo, número de bolsas y precio de competencia."
                
                st.markdown(resp)
        st.session_state.mensajes.append({"rol": "assistant", "contenido": resp})
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SECCIÓN 3: PANEL DE VENTAS
# ==========================================
elif selected == "Panel de Ventas":
    st.subheader("📊 Datos de Ventas")
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    if df_ventas.empty:
        st.info("Sin datos.")
    else:
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
