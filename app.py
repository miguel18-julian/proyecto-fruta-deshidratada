import streamlit as st
import sqlite3
import pandas as pd
import re
import time
from streamlit_option_menu import option_menu

# ==========================================
# CONFIGURACIÓN Y ESTILOS VISUALES (TIPO "COME VERDE")
# ==========================================
st.set_page_config(page_title="VitalFruit | Tienda Oficial", page_icon="🍃", layout="wide")

st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general tipo eCommerce orgánico */
    .stApp {
        background-color: #F8F6EE;
    }

    /* Franja superior de anuncios (como la de Amazon / Envíos) */
    .top-announcement {
        background-color: #388E3C;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        font-weight: 600;
        margin-top: -60px;
        margin-bottom: 20px;
        border-radius: 4px;
    }

    /* Barra de navegación superior corporativa verde oscuro */
    .nav-header {
        background-color: #004D26;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 8px;
        margin-bottom: 30px;
    }
    .nav-logo {
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* Títulos y tipografía */
    h1, h2, h3, h4 {
        color: #004D26 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Botones de categorías estilo píldora (como en la referencia) */
    .category-btn {
        background-color: #66BB6A;
        color: white;
        border-radius: 25px;
        padding: 8px 18px;
        text-align: center;
        font-weight: bold;
        display: inline-block;
        margin: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* Tarjeta de producto moderna y uniforme */
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #E0DCD0;
        transition: transform 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-4px);
    }

    /* Contenedor estricto para que todas las imágenes midan exactamente lo mismo */
    .product-img-box {
        width: 100%;
        height: 220px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 12px;
        background-color: #FAFAFA;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .product-img-box img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }

    /* Botón de compra principal */
    .stButton>button {
        background-color: #FF7043 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255, 112, 67, 0.3);
    }
    .stButton>button:hover {
        background-color: #E64A19 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BASE DE DATOS LOCAL / NUBE
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
# ENCABEZADO Y ANUNCIO TIPO "COME VERDE"
# ==========================================
st.markdown('<div class="top-announcement">🚚 Tu antojo saludable en casa en 24h | Disponible con envíos garantizados 🍃</div>', unsafe_allow_html=True)

# Menú superior con diseño profesional estilo pestañas
selected = option_menu(
    menu_title=None,
    options=["Catálogo y Tienda", "Asistente Inteligente (IA)", "Panel de Ventas y Base de Datos"],
    icons=["shop", "chat-dots", "graph-up-arrow"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#004D26", "border-radius": "8px"},
        "icon": {"color": "#FF7043", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "15px", "text-align": "center", "margin": "0px", "--hover-color": "#2E7D32"},
        "nav-link-selected": {"background-color": "#66BB6A", "font-weight": "bold"},
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECCIÓN 1: TIENDA Y CATÁLOGO
# ==========================================
if selected == "Catálogo y Tienda":
    st.markdown("<h1 style='text-align: center;'>Conoce todos nuestros productos</h1>", unsafe_allow_html=True)
    
    # Botones decorativos de categorías (Estilo idéntico a la barra de la página de referencia)
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <span class='category-btn'>MOSTRAR TODO</span>
            <span class='category-btn'>BOTANAS</span>
            <span class='category-btn'>FRUTA DESHIDRATADA</span>
            <span class='category-btn'>MIX ENERGÉTICO</span>
            <span class='category-btn'>INDIVIDUALES</span>
        </div>
    """, unsafe_allow_html=True)

    # Catálogo organizado en 3 columnas con imágenes perfectamente proporcionadas
    col1, col2, col3 = st.columns(3)

    catalogo = [
        {"nombre": "Mango Deshidratado", "peso": "Bolsa de 50g", "precio": 25.00, "img": "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=600"},
        {"nombre": "Manzana Orgánica", "peso": "Bolsa de 50g", "precio": 20.00, "img": "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?q=80&w=600"},
        {"nombre": "Mix Frutal Silvestre", "peso": "Bolsa de 100g", "precio": 35.00, "img": "https://images.unsplash.com/photo-1519996409144-56c88c9aa612?q=80&w=600"}
    ]

    for i, col in enumerate([col1, col2, col3]):
        item = catalogo[i]
        with col:
            st.markdown(f"""
                <div class="product-card">
                    <div class="product-img-box">
                        <img src="{item['img']}">
                    </div>
                    <h3>{item['nombre']}</h3>
                    <p style="color: #666; margin: 4px 0;">{item['peso']}</p>
                    <h4 style="color: #FF7043 !important; margin: 8px 0;">$ {item['precio']:.2f} MXN</h4>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Formulario de compra estilizado
    st.subheader("🛒 Realiza tu pedido directo")
    with st.form("form_venta", clear_on_submit=True):
        f1, f2, f3 = st.columns([2, 2, 1])
        with f1:
            cliente = st.text_input("Nombre completo:")
        with f2:
            producto = st.selectbox("Selecciona producto:", 
                                    ["Mango Deshidratado - $25.00", "Manzana Orgánica - $20.00", "Mix Frutal Silvestre - $35.00"])
        with f3:
            cantidad = st.number_input("Cantidad:", min_value=1, value=1)
            
        comprar = st.form_submit_button("Añadir al carrito y Comprar")
        
        if comprar and cliente:
            precio_unit = float(re.search(r'\$([0-9.]+)', producto).group(1))
            total = precio_unit * cantidad
            c = conn.cursor()
            c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                      (cliente, producto.split(" -")[0], cantidad, total))
            conn.commit()
            st.success(f"¡Excelente {cliente}! Tu pedido por **${total:.2f} MXN** fue registrado con éxito en la base de datos.")

    # Franja inferior institucional con círculos e insignias de calidad
    st.markdown("""
        <div style="background-color: #004D26; color: white; padding: 35px 20px; border-radius: 15px; margin-top: 40px; text-align: center;">
            <h3 style="color: white !important; margin-bottom: 20px;">Nuestros Compromisos de Calidad</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
                <div>🌱 <b>0% Azúcar Añadida</b></div>
                <div>🍃 <b>100% Sabor Natural</b></div>
                <div>✨ <b>Libre de Colorantes</b></div>
                <div>⚡ <b>Tecnología Controlada</b></div>
                <div>🇲🇽 <b>Hecho en México</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# SECCIÓN 2: ASISTENTE INTELIGENTE (IA)
# ==========================================
elif selected == "Asistente Inteligente (IA)":
    st.markdown("<h2>🤖 Asistente de Inteligencia de Negocios</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #444;'>Interactúa con el agente experto en costos de producción y precios de mercado para Teziutlán.</p>", unsafe_allow_html=True)

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "assistant", "contenido": "¡Hola! Escribe los datos de tu producción actual (ej. costo total del lote, bolsas fabricadas y precio de la competencia) para calcular tu viabilidad financiera."}
        ]

    for msj in st.session_state.mensajes:
        with st.chat_message(msj["rol"]):
            st.markdown(msj["contenido"])

    if entrada := st.chat_input("Escribe tu consulta aquí..."):
        with st.chat_message("user"):
            st.markdown(entrada)
        st.session_state.mensajes.append({"rol": "user", "contenido": entrada})

        with st.chat_message("assistant"):
            with st.spinner("Procesando análisis estratégico..."):
                time.sleep(1)
                nums = [float(n) for n in re.findall(r'\d+\.?\d*', entrada)]
                
                if len(nums) >= 3:
                    costo_unit = nums[0] / nums[1]
                    precio_sug = nums[2] * 0.85
                    margen = precio_sug - costo_unit
                    
                    respuesta = f"📊 **Análisis Estratégico Generado:**\n\n"
                    respuesta += f"- **Costo Unitario por Bolsa:** ${costo_unit:.2f} MXN\n"
                    respuesta += f"- **Precio Sugerido de Venta:** **${precio_sug:.2f} MXN**\n\n"
                    
                    if margen > 0:
                        respuesta += f"✅ **Estrategia Viable:** Tienes un margen de utilidad estimado en **${margen:.2f} MXN** por unidad."
                    else:
                        respuesta += f"⚠️ **Alerta:** Estás operando con pérdidas de ${abs(margen):.2f} MXN por bolsa. Optimiza el consumo energético."
                else:
                    respuesta = "Por favor, ingresa al menos tres valores numéricos claros: el costo total, el número de bolsas producidas y el precio de la competencia."
                
                st.markdown(respuesta)
        st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})

# ==========================================
# SECCIÓN 3: PANEL DE VENTAS Y BASE DE DATOS
# ==========================================
elif selected == "Panel de Ventas y Base de Datos":
    st.markdown("<h2>📊 Registro de Transacciones y Base de Datos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #444;'>Monitoreo general de las compras realizadas en la tienda en línea.</p>", unsafe_allow_html=True)
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    
    if df_ventas.empty:
        st.info("No hay ventas registradas todavía. Realiza una compra de prueba en la sección de la tienda.")
    else:
        ingresos = df_ventas['total'].sum()
        unidades = df_ventas['cantidad'].sum()
        ticket = ingresos / len(df_ventas)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Ingresos Totales", f"${ingresos:.2f} MXN")
        c2.metric("Unidades Vendidas", f"{unidades} bolsas")
        c3.metric("Ticket Promedio", f"${ticket:.2f} MXN")
        
        st.divider()
        st.subheader("Bitácora de Clientes")
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
