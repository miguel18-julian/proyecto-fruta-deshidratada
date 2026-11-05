import streamlit as st
import sqlite3
import pandas as pd
import re
import time

# ==========================================
# CONFIGURACIÓN Y ESTILOS VISUALES (ESTILO NATURAL)
# ==========================================
st.set_page_config(page_title="Fruta Deshidratada | 100% Natural", page_icon="🍃", layout="wide")

# Inyección de CSS avanzado para replicar la imagen de referencia
st.markdown("""
    <style>
    /* Ocultar el menú lateral izquierdo por completo */
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }

    /* Fondo general de la página */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Botones principales */
    .stButton>button {
        background-color: #FF7043 !important; /* Tono naranja que combina con el empaque del mango */
        color: white !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #E64A19 !important;
        transform: scale(1.02);
    }
    
    /* Títulos centrales */
    h1, h2, h3 {
        color: #2E7D32 !important; /* Verde oscuro */
        text-align: center;
        font-family: 'Arial', sans-serif;
    }

    /* Estilo del menú superior (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        background-color: #f1f8f1;
        padding: 10px;
        border-radius: 30px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #2E7D32 !important;
        font-weight: bold;
        font-size: 18px;
        padding: 10px 25px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important; /* Verde vibrante */
        color: white !important;
        border-radius: 20px;
    }

    /* === DISEÑO DE LOS CÍRCULOS VERDES INSPIRADO EN LA IMAGEN === */
    .green-wave-section {
        background-color: #61A639; /* Verde similar al de la imagen */
        padding: 60px 10px;
        border-radius: 50% 50% 0 0 / 20px 20px 0 0; /* Ligera curvatura superior */
        margin-top: 60px;
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        align-items: center;
    }
    .circle-badge {
        background-color: white;
        color: #004D26;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        line-height: 1.1;
        box-shadow: 0 10px 15px rgba(0,0,0,0.15);
    }
    .circle-badge .big-text {
        font-size: 32px;
        font-weight: 900;
        font-style: italic;
        color: #004D26;
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
# MENÚ SUPERIOR (TABS)
# ==========================================
st.title("🍃 Fruta Deshidratada Teziutlán")
st.markdown("### El snack perfecto, saludable y 100% natural.")

tab1, tab2, tab3 = st.tabs(["🛒 Productos", "💬 Burbuja IA", "📊 Panel de Ventas"])

# ==========================================
# SECCIÓN 1: TIENDA EN LÍNEA
# ==========================================
with tab1:
    # Mostramos productos en columnas (estilo catálogo de la imagen)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=800", caption="Mango Deshidratado - 100% Natural", use_container_width=True)
    
    st.divider()
    
    # Formulario de pago
    st.subheader("💳 Haz tu Pedido")
    with st.form("form_venta", clear_on_submit=True):
        col_c, col_p, col_q = st.columns([2, 2, 1])
        with col_c:
            cliente = st.text_input("👤 Tu Nombre:")
        with col_p:
            producto = st.selectbox("🍎 Producto:", 
                                    ["Mango Deshidratado (50g) - $25.00", "Manzana Deshidratada (50g) - $20.00", "Mix Frutal - $35.00"])
        with col_q:
            cantidad = st.number_input("📦 Cantidad:", min_value=1, value=1)
            
        comprar = st.form_submit_button("Añadir al Carrito y Comprar")
        
        if comprar and cliente:
            precio = float(re.search(r'\$([0-9.]+)', producto).group(1))
            total = precio * cantidad
            c = conn.cursor()
            c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                      (cliente, producto.split(" -")[0], cantidad, total))
            conn.commit()
            st.success(f"✅ ¡Gracias {cliente}! Tu pedido por ${total:.2f} MXN ha sido procesado.")

    # Recreación de los círculos verdes de la imagen usando HTML/CSS
    html_badges = """
    <div class="green-wave-section">
        <div class="circle-badge"><span class="big-text">0%</span>azúcar<br>añadida</div>
        <div class="circle-badge"><span class="big-text">100%</span>Sabor<br>natural</div>
        <div class="circle-badge"><span style="font-size:24px; font-weight:900; font-style:italic;">Libre</span>de colorantes<br>artificiales</div>
        <div class="circle-badge"><span class="big-text">Vegano</span></div>
        <div class="circle-badge">Hecho en<br><span class="big-text">México</span></div>
    </div>
    """
    st.markdown(html_badges, unsafe_allow_html=True)


# ==========================================
# SECCIÓN 2: AGENTE IA (BURBUJAS INTERACTIVAS)
# ==========================================
with tab2:
    st.subheader("🤖 Agente Experto en el Mercado de Teziutlán")
    st.write("Escríbeme cuánto gastaste, cuántas bolsas salieron de tu deshidratador y a cuánto vende la competencia.")

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "assistant", "contenido": "¡Hola! Soy tu asistente. Pásame los datos de tu lote de fruta para calcular si tienes buen margen de ganancia."}
        ]

    # Mostrar historial en burbujas de diálogo reales
    for msj in st.session_state.mensajes:
        with st.chat_message(msj["rol"]):
            st.markdown(msj["contenido"])

    # Barra de chat flotante estilo WhatsApp/ChatGPT
    if entrada := st.chat_input("Ej: Gasté $150, saqué 20 bolsas, y la competencia vende a $25"):
        with st.chat_message("user"):
            st.markdown(entrada)
        st.session_state.mensajes.append({"rol": "user", "contenido": entrada})

        with st.chat_message("assistant"):
            with st.spinner("🧠 Pensando y analizando el mercado..."):
                time.sleep(1)
                # Extraer números
                numeros = [float(n) for n in re.findall(r'\d+\.?\d*', entrada)]
                
                if len(numeros) >= 3:
                    costo_unit = numeros[0] / numeros[1]
                    precio_sug = numeros[2] * 0.85
                    margen = precio_sug - costo_unit
                    
                    resp = f"📊 **Resultados:**\n- **Costo por bolsa:** ${costo_unit:.2f} MXN.\n- **Precio sugerido:** **${precio_sug:.2f} MXN** (15% más barato que la competencia).\n"
                    
                    if margen > 0:
                        resp += f"✅ **¡Excelente!** Ganas **${margen:.2f} MXN** por cada bolsa vendida."
                    else:
                        resp += f"⚠️ **Alerta:** Pierdes ${abs(margen):.2f} MXN por bolsa. Necesitas optimizar tu deshidratador."
                else:
                    resp = "Me faltan datos. Escribe 3 números: el costo de producción, bolsas hechas y precio de la competencia."
                
                st.markdown(resp)
        st.session_state.mensajes.append({"rol": "assistant", "contenido": resp})

# ==========================================
# SECCIÓN 3: BASE DE DATOS
# ==========================================
with tab3:
    st.subheader("🗄️ Historial de Ventas")
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    if df_ventas.empty:
        st.info("Aún no tienes ventas.")
    else:
        # Métricas rápidas
        i_totales = df_ventas['total'].sum()
        b_vendidas = df_ventas['cantidad'].sum()
        
        c1, c2 = st.columns(2)
        c1.metric("Ingresos Totales", f"${i_totales:.2f} MXN")
        c2.metric("Bolsas Vendidas", f"{b_vendidas} ud")
        
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
