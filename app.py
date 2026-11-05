import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Fruta Deshidratada Teziutlán", page_icon="🍎", layout="wide")

# ==========================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================
def init_db():
    conn = sqlite3.connect('ventas_fruta.db', check_same_thread=False)
    c = conn.cursor()
    # Crear tabla de ventas si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS ventas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  cliente TEXT,
                  producto TEXT,
                  cantidad INTEGER,
                  total REAL,
                  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()

# Menú de navegación lateral
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["🛒 Tienda en Línea", "🤖 Agente IA (Nube)", "📊 Base de Datos"])

# ==========================================
# 2. SECCIÓN: TIENDA EN LÍNEA (VENTAS)
# ==========================================
if opcion == "🛒 Tienda en Línea":
    st.title("🍎 Tienda de Fruta Deshidratada")
    st.write("100% natural, procesada con tecnología controlada para conservar todos sus nutrientes.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=800", caption="Mix de Frutas Deshidratadas", use_container_width=True)
    
    with col2:
        st.subheader("Realizar Pedido")
        st.write("Ideal para un estilo de vida activo en Teziutlán.")
        
        with st.form("form_venta"):
            cliente = st.text_input("Nombre del Cliente:")
            producto = st.selectbox("Selecciona tu producto:", ["Manzana Deshidratada (50g) - $20.00", "Mango Deshidratado (50g) - $25.00", "Mix Frutal (100g) - $35.00"])
            cantidad = st.number_input("Cantidad de bolsas:", min_value=1, value=1)
            
            # Extraer precio del string seleccionado
            precio_unitario = float(producto.split("$")[1])
            total = precio_unitario * cantidad
            
            st.write(f"**Total a pagar: ${total:.2f} MXN**")
            comprar = st.form_submit_button("Confirmar Compra")
            
            if comprar and cliente:
                # Guardar venta en la base de datos
                c = conn.cursor()
                c.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?, ?, ?, ?)", 
                          (cliente, producto.split(" -")[0], cantidad, total))
                conn.commit()
                st.success(f"¡Gracias por tu compra, {cliente}! Tu pedido ha sido registrado.")

# ==========================================
# 3. SECCIÓN: AGENTE IA (CLOUD)
# ==========================================
elif opcion == "🤖 Agente IA (Nube)":
    st.title("🧠 Agente de Inteligencia de Mercados")
    st.write("Este agente analiza los costos de tu deshidratador ESP32 frente al mercado de Teziutlán (28,920 clientes potenciales).")
    
    # Simulación de conexión a API de IA en la nube (ej. OpenAI / Gemini)
    api_key = st.text_input("Ingresa tu API Key (Opcional para pruebas):", type="password")
    
    with st.form("form_agente"):
        costo_produccion = st.number_input("Costo de producción del lote ($):", min_value=0.0, value=150.0)
        bolsas_generadas = st.number_input("Bolsas producidas:", min_value=1, value=20)
        precio_competencia = st.number_input("Precio promedio de la competencia ($):", min_value=0.0, value=25.0)
        
        analizar = st.form_submit_button("Generar Análisis Estratégico")
        
        if analizar:
            costo_unitario = costo_produccion / bolsas_generadas
            precio_sugerido = precio_competencia * 0.85 # Estrategia de penetración (15% más barato)
            margen = precio_sugerido - costo_unitario
            
            st.info("☁️ **Respuesta generada por el Agente en la Nube:**")
            st.write(f"> *Análisis completado para la región de Teziutlán.*")
            st.write(f"> - **Costo Unitario:** ${costo_unitario:.2f} MXN por bolsa.")
            st.write(f"> - **Estrategia de Precio:** Para competir contra los ${precio_competencia:.2f} de otras marcas y captar al público joven, el precio sugerido es de **${precio_sugerido:.2f} MXN**.")
            
            if margen > 0:
                st.success(f"> - **Viabilidad:** Excelente. Obtendrás un margen de ganancia de **${margen:.2f} MXN** por unidad vendida.")
            else:
                st.error(f"> - **Alerta:** A este precio, estás perdiendo ${abs(margen):.2f} MXN por bolsa. Necesitas optimizar el consumo de luz en el ESP32 o negociar mejor la materia prima.")

# ==========================================
# 4. SECCIÓN: BASE DE DATOS (VISUALIZACIÓN)
# ==========================================
elif opcion == "📊 Base de Datos":
    st.title("🗄️ Historial de Ventas")
    st.write("Todos los datos generados en la tienda se almacenan y consultan desde la base de datos SQLite.")
    
    df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
    
    if df_ventas.empty:
        st.info("Aún no hay ventas registradas.")
    else:
        st.dataframe(df_ventas, use_container_width=True)
        
        # Métrica rápida
        ingresos_totales = df_ventas["total"].sum()
        bolsas_vendidas = df_ventas["cantidad"].sum()
        
        col1, col2 = st.columns(2)
        col1.metric("Ingresos Totales", f"${ingresos_totales:.2f} MXN")
        col2.metric("Bolsas Vendidas", f"{bolsas_vendidas} unidades")