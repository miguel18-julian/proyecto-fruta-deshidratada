import streamlit as st
import sqlite3
import pandas as pd
import re
import time
from streamlit_option_menu import option_menu

# ==========================================
# CONFIGURACIÓN Y ESTILOS VISUALES AVANZADOS
# ==========================================
st.set_page_config(page_title="VitalFruit | Tienda Oficial", page_icon="🍊", layout="wide")

st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general estilo orgánico */
    .stApp {
        background-color: #F9F8F3;
    }

    /* Barra de navegación superior */
    .nav-container {
        background-color: #1E4620;
        padding: 5px 0;
        margin-top: -65px;
        margin-bottom: 25px;
    }

    /* Títulos y tipografía */
    h1, h2, h3, h4 {
        color: #1E4620 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Contenedor uniforme para las tarjetas de productos */
    .product-card {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #E8E5D8;
        transition: transform 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
    }

    /* FORZAR UN TAMAÑO IDÉNTICO Y PERFECTO PARA TODAS LAS IMÁGENES */
    .product-img-container {
        width: 100%;
        height: 220px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f7f7f7;
    }
    .product-img-container img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important; /* Evita deformaciones y recuadra idéntico */
    }

    /* Botones personalizados estilo e-commerce */
    .stButton>button {
        background-color: #E86A33 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 10px rgba(232, 106, 51, 0.3);
    }
    .stButton>button:hover {
        background-color: #D05522 !important;
    }

    /* Estilo de la sección de beneficios inferiores */
    .benefits-bar {
        background-color: #2D6A4F;
        color: white;
        padding: 30px 10px;
        border-radius: 20px;
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-top: 40px;
        flex-wrap: wrap;
    }
    .benefit-item {
        margin: 10px;
    }
    .benefit-title {
        font-size: 18px;
        font-weight: bold;
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
# NAVEGACIÓN SUPERIOR PROFESIONAL
# ==========================================
st.markdown('<div class="nav-container"></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Tienda y Catálogo", "Asistente Inteligente (IA)", "Panel Financiero y Ventas"],
    icons=["shop", "chat-square-text", "bar-chart-line"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1E4620", "border-radius": "0"},
        "icon": {"color": "#E86A33", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "15px", "text-align": "center", "margin": "0px", "--hover-color": "#2D6A4F"},
        "nav-link-selected": {"background-color": "#2D6A4F", "font-weight": "bold"},
    }
)

# ==========================================
# SECCIÓN 1: TIENDA Y CATÁLOGO
# ==========================================
if selected == "Tienda y Catálogo":
    st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>VitalFruit Teziutlán</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; font-size: 16px; margin-bottom: 30px;'>Fruta deshidratada con tecnología de punta, conservando el 100% de nutrientes y sabor natural.</p>", unsafe_allow_html=True)

    # Catálogo organizado en 3 columnas con tarjetas idénticas
    col1, col2, col3 = st.columns(3)

    productos_data = [
        {"nombre": "Mango Deshidratado", "peso": "Bolsa de 50g", "precio": 25.00, "img": "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=600"},
        {"nombre": "Manzana Orgánica", "peso": "Bolsa de 50g", "precio": 20.00, "img": "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?q=80&w=600"},
        {"nombre": "Mix Energético Frutal", "peso": "Bolsa de 100g", "precio": 35.00, "img": "https://images.unsplash.com/photo-1519996409144-56c88c9aa612?q=80&w=600"}
    ]

    for i, col in enumerate([col1, col2, col3]):
        p = productos_data[i]
        with col:
            st.markdown(f"""
                <div class="product-card">
                    <div class="product-img-container">
                        <img src="{p['img']}">
                    </div>
                    <h3>{p['nombre']}</h3>
                    <p style="color: #666; margin: 5px 0;">{p['peso']}</p>
                    <h4 style="color: #E86A33 !important; margin: 10px 0;">${p['precio']:.2f} MXN</h4>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Formulario de compra estilizado
    st.markdown("### 🛒 Realiza tu pedido de forma segura")
    with st.form("form_venta", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
        with f_col1:
            cliente = st.text_input("Nombre completo:")
        with f_col2:
            producto = st.selectbox("Selecciona tu producto:", 
                                    ["Mango Deshidratado - $25.00", "Manzana Orgánica - $20.00", "Mix Energético Frutal - $35.00"])
        with f_col3:
            cantidad = st.number_input("Cantidad:", min_value=1, value=1)
            
        comprar = st.form_submit_button("Confirmar Compra")
        
        if comprar and cliente:
            precio_unit = float(re.search(r'\$([0-9.]+)', producto).group(1))
            total = precio_unit * cantidad
            c = conn.cursor()
            c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                      (cliente, producto.split(" -")[0], cantidad, total))
            conn.commit()
            st.success(f"¡Excelente, {cliente}! Tu pedido por un total de **${total:.2f} MXN** ha sido guardado en la base de datos.")

    # Franja informativa inferior con beneficios
    st.markdown("""
        <div class="benefits-bar">
            <div class="benefit-item"><span class="benefit-title">🌱 0% Azúcar Añadida</span><br>Endulzado naturalmente</div>
            <div class="benefit-item"><span class="benefit-title">⚡ Deshidratación Controlada</span><br>Proceso tecnológico optimizado</div>
            <div class="benefit-item"><span class="benefit-title">🇲🇽 Orgullo Teziuteco</span><br>Hecho en México</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# SECCIÓN 2: ASISTENTE INTELIGENTE (IA)
# ==========================================
elif selected == "Asistente Inteligente (IA)":
    st.markdown("<h2>🤖 Agente de Inteligencia de Mercados</h2>", unsafe_allow_html=True)
    st.markdown("<p>Consulta estratégica en tiempo real para evaluar costos de producción, fijación de precios y rentabilidad en la región.</p>", unsafe_allow_html=True)

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "assistant", "contenido": "¡Hola! Soy tu consultor de negocios automatizado. Ingresa los datos de tu lote de producción actual (ej. costo total, bolsas producidas y precio de la competencia) para obtener un análisis financiero."}
        ]

    for msj in st.session_state.mensajes:
        with st.chat_message(msj["rol"]):
            st.markdown(msj["contenido"])

    if entrada := st.chat_input("Escribe aquí tus datos (ej: Gasté $150, saqué 20 bolsas, competencia a $25)..."):
        with st.chat_message("user"):
            st.markdown(entrada)
        st.session_state.mensajes.append({"rol": "user", "contenido": entrada})

        with st.chat_message("assistant"):
            with st.spinner("Analizando variables del mercado regional..."):
                time.sleep(1)
                nums = [float(n) for n in re.findall(r'\d+\.?\d*', entrada)]
                
                if len(nums) >= 3:
                    costo_unitario = nums[0] / nums[1]
                    precio_sugerido = nums[2] * 0.85
                    margen = precio_sugerido - costo_unitario
                    
                    respuesta = f"📊 **Reporte de Inteligencia Comercial:**\n\n"
                    respuesta += f"- **Costo de Producción por Bolsa:** ${costo_unitario:.2f} MXN\n"
                    respuesta += f"- **Precio Estratégico Sugerido:** **${precio_sugerido:.2f} MXN** (competitivo frente al mercado)\n\n"
                    
                    if margen > 0:
                        respuesta += f"✅ **Viabilidad Financiera:** Positiva. Obtienes una utilidad neta estimada de **${margen:.2f} MXN** por unidad."
                    else:
                        respuesta += f"⚠️ **Alerta Financiera:** Margen negativo. Estás perdiendo ${abs(margen):.2f} MXN por cada bolsa producida."
                else:
                    respuesta = "Por favor, proporciona al menos tres valores numéricos claros: el costo total de producción, el número de bolsas obtenidas y el precio de venta de la competencia."
                
                st.markdown(respuesta)
        st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})

# ==========================================
# SECCIÓN 3: PANEL FINANCIERO Y VENTAS
# ==========================================
elif selected == "Panel Financiero y Ventas":
    st.markdown("<h2>📊 Panel de Control y Base de Datos</h2>", unsafe_allow_html=True)
    st.markdown("<p>Monitoreo en tiempo real de transacciones comerciales y métricas clave del proyecto.</p>", unsafe_allow_html=True)
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    
    if df_ventas.empty:
        st.info("No hay registros de ventas almacenados en la base de datos actualmente. Realiza una prueba comprando en la sección de la tienda.")
    else:
        # Métricas principales superiores
        ingresos_totales = df_ventas['total'].sum()
        unidades_vendidas = df_ventas['cantidad'].sum()
        ticket_promedio = ingresos_totales / len(df_ventas)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Ingresos Totales", f"${ingresos_totales:.2f} MXN", "Crecimiento activo")
        m2.metric("Bolsas Comercializadas", f"{unidades_vendidas} unidades")
        m3.metric("Ticket Promedio", f"${ticket_promedio:.2f} MXN")
        
        st.divider()
        st.subheader("Bitácora Detallada de Transacciones")
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
