import streamlit as st
import sqlite3
import pandas as pd
import re
import time

# ==========================================
# CONFIGURACIÓN Y ESTILOS VISUALES
# ==========================================
st.set_page_config(page_title="VitalFruit | Teziutlán", page_icon="🍊", layout="wide")

# Inyección de CSS para hacer la página más atractiva
st.markdown("""
    <style>
    /* Color de botones */
    .stButton>button {
        background-color: #ff6f00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #e65c00 !important;
    }
    /* Estilo de encabezados */
    h1, h2, h3 {
        color: #ff6f00;
        font-family: 'Arial', sans-serif;
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
# NAVEGACIÓN LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1517058814526-724bbba07a75?q=80&w=500", caption="Fruta 100% Natural")
    st.title("🍊 Menú VitalFruit")
    opcion = st.radio("Navegación:", ["🛒 Tienda en Línea", "💬 Agente IA (Chat)", "📊 Base de Datos"])
    st.divider()
    st.caption("Proyecto: Inteligencia de Mercados")
    st.caption("Región: Teziutlán, Puebla")

# ==========================================
# SECCIÓN 1: TIENDA EN LÍNEA
# ==========================================
if opcion == "🛒 Tienda en Línea":
    st.title("🍊 Tienda Oficial VitalFruit")
    st.markdown("### Snack saludable, tecnología controlada por ESP32.")
    
    # Banner principal
    st.image("https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=1200&h=300&fit=crop", use_container_width=True)
    st.divider()

    # Catálogo de productos con imágenes en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?q=80&w=400", caption="Manzana Deshidratada")
        st.subheader("Manzana (50g)")
        st.write("Precio: $20.00 MXN")
    with col2:
        st.image("https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=400", caption="Mango Deshidratado")
        st.subheader("Mango (50g)")
        st.write("Precio: $25.00 MXN")
    with col3:
        st.image("https://images.unsplash.com/photo-1519996409144-56c88c9aa612?q=80&w=400", caption="Mix Frutal Energía")
        st.subheader("Mix Frutal (100g)")
        st.write("Precio: $35.00 MXN")

    st.divider()
    
    # Formulario de pago estilizado
    st.subheader("💳 Realizar Pedido")
    with st.form("form_venta", clear_on_submit=True):
        cliente = st.text_input("👤 Tu Nombre:")
        col_prod, col_cant = st.columns(2)
        with col_prod:
            producto = st.selectbox("🍎 Selecciona el producto:", 
                                    ["Manzana Deshidratada - $20.00", "Mango Deshidratado - $25.00", "Mix Frutal - $35.00"])
        with col_cant:
            cantidad = st.number_input("📦 Cantidad de bolsas:", min_value=1, value=1)
            
        comprar = st.form_submit_button("Confirmar Compra")
        
        if comprar and cliente:
            precio = float(re.search(r'\$([0-9.]+)', producto).group(1))
            total = precio * cantidad
            c = conn.cursor()
            c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                      (cliente, producto.split(" -")[0], cantidad, total))
            conn.commit()
            st.success(f"✅ ¡Gracias {cliente}! Pedido registrado por ${total:.2f} MXN.")

# ==========================================
# SECCIÓN 2: AGENTE IA (BURBUJA DE CHAT)
# ==========================================
elif opcion == "💬 Agente IA (Chat)":
    st.title("🤖 Asistente de Inteligencia de Mercados")
    st.write("Escribe los datos de tu lote en el chat para recibir un análisis en tiempo real.")

    # Inicializar el historial de chat en la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! Soy tu Agente de Mercado en Teziutlán. Dime, ¿cuánto gastaste en producir este lote, cuántas bolsas salieron y a cuánto vende la competencia?"}
        ]

    # Mostrar el historial de mensajes (burbujas)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de texto estilo ChatGPT
    if prompt := st.chat_input("Ej: Gasté $150, salieron 20 bolsas, la competencia vende a $25"):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Lógica del Sistema Experto (IA)
        with st.chat_message("assistant"):
            with st.spinner("Analizando datos del mercado en Teziutlán..."):
                time.sleep(1) # Simular tiempo de pensamiento
                
                # Extraer números del texto del usuario
                numeros = [float(n) for n in re.findall(r'\d+\.?\d*', prompt)]
                
                if len(numeros) >= 3:
                    costo_total = numeros[0]
                    bolsas = numeros[1]
                    precio_comp = numeros[2]
                    
                    costo_unit = costo_total / bolsas
                    precio_sug = precio_comp * 0.85
                    margen = precio_sug - costo_unit
                    
                    respuesta = f"📊 **Análisis Estratégico Completado:**\n\n"
                    respuesta += f"- **Costo Unitario:** ${costo_unit:.2f} MXN.\n"
                    respuesta += f"- **Precio de Competencia:** ${precio_comp:.2f} MXN.\n"
                    respuesta += f"- **Precio Sugerido (Penetración):** **${precio_sug:.2f} MXN**.\n\n"
                    
                    if margen > 0:
                        respuesta += f"✅ **Estrategia Viable:** Tienes un margen de ganancia de **${margen:.2f} MXN** por bolsa. ¡Es ideal para el mercado joven de Teziutlán!"
                    else:
                        respuesta += f"⚠️ **Alerta Financiera:** Estás perdiendo ${abs(margen):.2f} MXN por bolsa. Debes ajustar tu producción en el ESP32."
                else:
                    respuesta = "No pude detectar todos los datos. Por favor, asegúrate de escribir tres números: el costo total, las bolsas producidas y el precio de la competencia."
                
                st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# ==========================================
# SECCIÓN 3: BASE DE DATOS E HISTORIAL
# ==========================================
elif opcion == "📊 Base de Datos":
    st.title("🗄️ Panel de Control y Ventas")
    st.write("Monitorea el rendimiento comercial del proyecto.")
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    
    if df_ventas.empty:
        st.info("No hay ventas registradas actualmente.")
    else:
        # Tarjetas de métricas
        ingresos = df_ventas['total'].sum()
        bolsas = df_ventas['cantidad'].sum()
        ticket_promedio = ingresos / len(df_ventas)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Totales", f"${ingresos:.2f} MXN", "+15% vs mes anterior")
        col2.metric("Bolsas Vendidas", f"{bolsas} ud")
        col3.metric("Ticket Promedio", f"${ticket_promedio:.2f} MXN")
        
        st.divider()
        st.subheader("Registro Detallado")
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
