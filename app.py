import re
import sqlite3
import time

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
st.set_page_config(page_title="VitalFruit | Tienda Oficial", page_icon="🍃", layout="wide")

VERDE_OSCURO = "#004D26"
VERDE = "#388E3C"
VERDE_CLARO = "#66BB6A"
NARANJA = "#FF7043"

st.markdown(
    f"""
<style>
#MainMenu, footer, header {{visibility: hidden;}}
.stApp {{background-color: #F8F6EE;}}
.block-container {{padding-top: 0.5rem; max-width: 1200px;}}

h1, h2, h3, h4 {{color: {VERDE_OSCURO} !important;
    font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;}}

/* Franja de anuncios con texto en movimiento (como Come Verde) */
.top-announcement {{background: {VERDE}; color: white; padding: 8px 0;
    font-size: 14px; font-weight: 600; border-radius: 6px; overflow: hidden;
    white-space: nowrap; margin-bottom: 14px;}}
.top-announcement span {{display: inline-block; padding-left: 100%;
    animation: marquee 22s linear infinite;}}
@keyframes marquee {{0% {{transform: translateX(0);}} 100% {{transform: translateX(-100%);}}}}

/* Logo */
.logo {{text-align: center; font-size: 34px; font-weight: 800; color: {VERDE_OSCURO};
    letter-spacing: 1px; margin: 6px 0 12px 0;}}
.logo small {{display:block; font-size: 12px; font-weight: 600; color: {VERDE};
    letter-spacing: 3px;}}

/* Tarjeta de producto */
.product-img {{height: 190px; border-radius: 12px; display: flex; align-items: center;
    justify-content: center; font-size: 84px; margin-bottom: 10px;}}
.badge {{display: inline-block; background: {VERDE_CLARO}; color: white; font-size: 11px;
    font-weight: 700; padding: 2px 10px; border-radius: 12px; margin-bottom: 6px;}}
.p-name {{color: {VERDE_OSCURO}; font-weight: 700; font-size: 17px; text-align: center;
    margin: 4px 0 0 0; text-transform: uppercase;}}
.p-peso {{color: #777; text-align: center; font-size: 13px; margin: 0;}}
.p-precio {{color: {NARANJA}; text-align: center; font-weight: 800; font-size: 20px;
    margin: 6px 0 10px 0;}}

/* Contenedores con borde (tarjetas) */
div[data-testid="stVerticalBlockBorderWrapper"] {{background: white; border-radius: 16px;
    border: 1px solid #E0DCD0; box-shadow: 0 4px 15px rgba(0,0,0,0.05);}}

/* Botones */
.stButton > button, .stFormSubmitButton > button {{
    background-color: {NARANJA} !important; color: white !important;
    border-radius: 25px !important; border: none !important; font-weight: 700;
    width: 100%; box-shadow: 0 4px 10px rgba(255,112,67,.3);}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background-color: #E64A19 !important;}}

/* Compromisos */
.compromisos {{background: {VERDE_OSCURO}; color: white; padding: 30px 20px;
    border-radius: 15px; margin-top: 40px; text-align: center;}}
.compromisos h3 {{color: white !important;}}
.compromisos .fila {{display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;}}

/* Footer */
.footer {{background: {VERDE_OSCURO}; color: #DDE8DD; padding: 25px; border-radius: 15px;
    margin-top: 30px; font-size: 14px; text-align: center;}}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# CATÁLOGO
# ==========================================================
CATEGORIAS = ["MOSTRAR TODO", "FRUTA DESHIDRATADA", "BOTANAS", "MIX ENERGÉTICO", "INDIVIDUALES", "FAMILIARES"]

CATALOGO = [
    {"id": "mng-60", "nombre": "Mango Enchilado", "peso": "60 g", "precio": 45.0, "emoji": "🥭", "color": "#FFE9A8", "cats": ["FRUTA DESHIDRATADA", "INDIVIDUALES"], "tag": "MÁS VENDIDO"},
    {"id": "man-50", "nombre": "Manzana Natural", "peso": "50 g", "precio": 30.0, "emoji": "🍎", "color": "#FFD6D6", "cats": ["FRUTA DESHIDRATADA", "INDIVIDUALES"], "tag": "0% AZÚCAR"},
    {"id": "pln-60", "nombre": "Plátano Natural", "peso": "60 g", "precio": 39.0, "emoji": "🍌", "color": "#FFF3B0", "cats": ["FRUTA DESHIDRATADA", "INDIVIDUALES"], "tag": "NATURAL"},
    {"id": "pin-60", "nombre": "Piña Deshidratada", "peso": "60 g", "precio": 42.0, "emoji": "🍍", "color": "#FFF0B3", "cats": ["FRUTA DESHIDRATADA", "INDIVIDUALES"], "tag": "NUEVO"},
    {"id": "fre-50", "nombre": "Fresa Deshidratada", "peso": "50 g", "precio": 48.0, "emoji": "🍓", "color": "#FFD1DC", "cats": ["FRUTA DESHIDRATADA", "INDIVIDUALES"], "tag": "NUEVO"},
    {"id": "jic-60", "nombre": "Jícama Enchilada", "peso": "60 g", "precio": 40.0, "emoji": "🌶️", "color": "#FFE0D0", "cats": ["BOTANAS", "INDIVIDUALES"], "tag": "BOTANA"},
    {"id": "mix-100", "nombre": "Mix Frutal Silvestre", "peso": "100 g", "precio": 65.0, "emoji": "🫐", "color": "#E1D5F5", "cats": ["MIX ENERGÉTICO", "INDIVIDUALES"], "tag": "ENERGÉTICO"},
    {"id": "mng-300", "nombre": "Mango Enchilado Familiar", "peso": "300 g", "precio": 190.0, "emoji": "🥭", "color": "#FFE9A8", "cats": ["FRUTA DESHIDRATADA", "FAMILIARES"], "tag": "AHORRA 15%"},
    {"id": "mix-300", "nombre": "Mix Energético Familiar", "peso": "300 g", "precio": 175.0, "emoji": "🥜", "color": "#EBDDC3", "cats": ["MIX ENERGÉTICO", "FAMILIARES"], "tag": "FAMILIAR"},
]
PRECIOS = {p["nombre"]: p["precio"] for p in CATALOGO}
POR_ID = {p["id"]: p for p in CATALOGO}


# ==========================================================
# BASE DE DATOS
# ==========================================================
@st.cache_resource
def get_conn():
    conn = sqlite3.connect("ventas_fruta.db", check_same_thread=False)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT, producto TEXT, cantidad INTEGER, total REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    )
    conn.commit()
    return conn


conn = get_conn()

if "carrito" not in st.session_state:
    st.session_state.carrito = {}  # {id: cantidad}
if "categoria" not in st.session_state:
    st.session_state.categoria = "MOSTRAR TODO"


def agregar(pid):
    st.session_state.carrito[pid] = st.session_state.carrito.get(pid, 0) + 1
    st.toast(f"{POR_ID[pid]['nombre']} agregado al carrito 🛒")


def total_carrito():
    return sum(POR_ID[i]["precio"] * q for i, q in st.session_state.carrito.items())


def n_items():
    return sum(st.session_state.carrito.values())


# ==========================================================
# AGENTE (herramientas + razonamiento por intención)
# Tecnología libre: Python + Streamlit + SQLite, sin API de pago.
# ==========================================================
def tool_catalogo(consulta: str) -> str:
    q = consulta.lower()
    encontrados = [p for p in CATALOGO if any(w in p["nombre"].lower() for w in q.split() if len(w) > 3)]
    lista = encontrados or CATALOGO
    filas = "\n".join(f"- {p['emoji']} **{p['nombre']}** ({p['peso']}): ${p['precio']:.2f} MXN" for p in lista)
    return "Estos son los productos que encontré:\n\n" + filas


def tool_recomendar(consulta: str) -> str:
    q = consulta.lower()
    if any(w in q for w in ["dulce", "postre", "niño", "niños"]):
        p = POR_ID["fre-50"]
    elif any(w in q for w in ["picante", "enchilado", "chile", "botana"]):
        p = POR_ID["mng-60"]
    elif any(w in q for w in ["energ", "gym", "deporte", "ejercicio"]):
        p = POR_ID["mix-100"]
    elif any(w in q for w in ["familia", "compartir", "fiesta"]):
        p = POR_ID["mng-300"]
    else:
        p = POR_ID["mng-60"]
    return f"Te recomiendo {p['emoji']} **{p['nombre']}** ({p['peso']}) a **${p['precio']:.2f} MXN**. ¡Es de los favoritos!"


def tool_ventas() -> str:
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    if df.empty:
        return "Aún no hay ventas registradas en la base de datos."
    top = df.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
    return (
        f"📈 **Resumen de ventas**\n\n- Pedidos registrados: **{len(df)}**\n"
        f"- Ingresos totales: **${df['total'].sum():.2f} MXN**\n"
        f"- Producto más vendido: **{top.index[0]}** ({int(top.iloc[0])} uds)"
    )


def tool_viabilidad(nums: list) -> str:
    costo_total, bolsas, precio_comp = nums[0], nums[1], nums[2]
    if bolsas <= 0:
        return "El número de bolsas debe ser mayor a cero."
    costo_unit = costo_total / bolsas
    precio_sug = precio_comp * 0.85
    margen = precio_sug - costo_unit
    pct = (margen / precio_sug * 100) if precio_sug else 0
    txt = (
        "📊 **Análisis de viabilidad**\n\n"
        f"- Costo unitario por bolsa: **${costo_unit:.2f} MXN**\n"
        f"- Precio sugerido (15% bajo la competencia): **${precio_sug:.2f} MXN**\n"
        f"- Margen por bolsa: **${margen:.2f} MXN** ({pct:.0f}%)\n\n"
    )
    if margen > 0:
        txt += "✅ **Viable:** con ese precio obtienes utilidad."
    else:
        txt += "⚠️ **Alerta:** vendes con pérdida. Reduce costos (energía del deshidratador, merma) o sube el precio."
    return txt


def agente(mensaje: str):
    """Devuelve (respuesta, herramienta_usada)."""
    q = mensaje.lower()
    nums = [float(n) for n in re.findall(r"\d+\.?\d*", mensaje)]

    if len(nums) >= 3 and any(w in q for w in ["costo", "lote", "bolsa", "competencia", "precio", "viab"]):
        return tool_viabilidad(nums), "calcular_viabilidad"
    if any(w in q for w in ["venta", "ingreso", "vendido", "pedidos"]):
        return tool_ventas(), "consultar_base_de_datos"
    if any(w in q for w in ["recomienda", "recomiend", "sugier", "qué me", "que me"]):
        return tool_recomendar(mensaje), "recomendar_producto"
    if any(w in q for w in ["precio", "cuesta", "catálogo", "catalogo", "productos", "tienen", "mango", "manzana", "plátano", "platano", "fresa", "piña", "mix"]):
        return tool_catalogo(mensaje), "consultar_catalogo"
    if any(w in q for w in ["envío", "envio", "entrega", "tarda"]):
        return "🚚 Hacemos envíos en 24 h en zonas con cobertura. El pedido se confirma al registrarlo en la tienda.", "preguntas_frecuentes"
    return (
        "Puedo ayudarte con:\n\n"
        "- 🛍️ **Precios y catálogo** (ej. *¿cuánto cuesta el mango?*)\n"
        "- 🎯 **Recomendaciones** (ej. *recomiéndame algo picante*)\n"
        "- 📈 **Ventas** (ej. *¿cómo van las ventas?*)\n"
        "- 💰 **Viabilidad**: escribe costo del lote, bolsas producidas y precio de la competencia "
        "(ej. *costo del lote 600, 40 bolsas, competencia 45*)"
    ), "ayuda"


# ==========================================================
# ENCABEZADO
# ==========================================================
anuncio = "🚚 Tu antojo saludable en casa en 24h &nbsp;|&nbsp; Envíos garantizados 🍃 &nbsp;|&nbsp; 0% azúcar añadida &nbsp;|&nbsp; Hecho en México 🇲🇽"
st.markdown(f'<div class="top-announcement"><span>{anuncio}</span></div>', unsafe_allow_html=True)
st.markdown('<div class="logo">🍃 VitalFruit<small>FRUTA DESHIDRATADA</small></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Tienda", "Asistente (Agente IA)", "Panel de Ventas"],
    icons=["shop", "robot", "graph-up-arrow"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": VERDE_OSCURO, "border-radius": "8px"},
        "icon": {"color": NARANJA, "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "15px", "text-align": "center", "--hover-color": "#2E7D32"},
        "nav-link-selected": {"background-color": VERDE_CLARO, "font-weight": "bold"},
    },
)
st.write("")

# ==========================================================
# TIENDA
# ==========================================================
if selected == "Tienda":
    st.markdown("<h1 style='text-align:center;'>Conoce todos nuestros productos</h1>", unsafe_allow_html=True)

    # Filtros por categoría (funcionales)
    cols = st.columns(len(CATEGORIAS))
    for col, cat in zip(cols, CATEGORIAS):
        with col:
            if st.button(cat, key=f"cat_{cat}"):
                st.session_state.categoria = cat
    st.caption(f"Mostrando: **{st.session_state.categoria}**")

    cat = st.session_state.categoria
    visibles = CATALOGO if cat == "MOSTRAR TODO" else [p for p in CATALOGO if cat in p["cats"]]

    # Cuadrícula de 3 columnas
    for fila in range(0, len(visibles), 3):
        cols = st.columns(3)
        for col, p in zip(cols, visibles[fila:fila + 3]):
            with col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="product-img" style="background:{p['color']};">{p['emoji']}</div>
                        <div style="text-align:center;"><span class="badge">{p['tag']}</span></div>
                        <p class="p-name">{p['nombre']}</p>
                        <p class="p-peso">{p['peso']}</p>
                        <p class="p-precio">$ {p['precio']:.2f} MXN</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.button("Agregar al carrito 🛒", key=f"add_{p['id']}", on_click=agregar, args=(p["id"],))

    # Carrito y checkout
    st.divider()
    st.subheader(f"🛒 Tu carrito ({n_items()})")
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. Agrega productos desde el catálogo.")
    else:
        for pid, q in list(st.session_state.carrito.items()):
            p = POR_ID[pid]
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"{p['emoji']} **{p['nombre']}** ({p['peso']})")
            c2.write(f"{q} × ${p['precio']:.2f} = **${q * p['precio']:.2f}**")
            if c3.button("✖", key=f"del_{pid}"):
                del st.session_state.carrito[pid]
                st.rerun()
        st.markdown(f"### Total: ${total_carrito():.2f} MXN")

        with st.form("checkout", clear_on_submit=True):
            cliente = st.text_input("Nombre completo:")
            confirmar = st.form_submit_button("Finalizar compra")
            if confirmar:
                if not cliente.strip():
                    st.error("Escribe tu nombre para registrar el pedido.")
                else:
                    total = total_carrito()
                    for pid, q in st.session_state.carrito.items():
                        p = POR_ID[pid]
                        conn.execute(
                            "INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?,?,?,?)",
                            (cliente.strip(), p["nombre"], q, p["precio"] * q),
                        )
                    conn.commit()
                    st.session_state.carrito = {}
                    st.success(f"¡Gracias {cliente}! Tu pedido por **${total:.2f} MXN** fue registrado. 🎉")
                    st.balloons()

    st.markdown(
        """
        <div class="compromisos">
            <h3>Nuestros Compromisos de Calidad</h3>
            <div class="fila">
                <div>🌱 <b>0% Azúcar Añadida</b></div>
                <div>🍃 <b>100% Sabor Natural</b></div>
                <div>✨ <b>Libre de Colorantes</b></div>
                <div>⚡ <b>Deshidratación Controlada</b></div>
                <div>🇲🇽 <b>Hecho en México</b></div>
            </div>
        </div>
        <div class="footer">VitalFruit © 2026 · Fruta deshidratada artesanal · Teziutlán, Puebla</div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# AGENTE
# ==========================================================
elif selected == "Asistente (Agente IA)":
    st.markdown("<h2>🤖 Agente VitalFruit</h2>", unsafe_allow_html=True)
    st.markdown(
        "Agente con **herramientas**: consulta el catálogo, recomienda productos, "
        "lee la base de datos de ventas y calcula la viabilidad de tu producción."
    )

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "assistant", "contenido": "¡Hola! Soy el agente de VitalFruit 🍃 Pregúntame por precios, recomendaciones, ventas, o escribe el costo de tu lote, las bolsas producidas y el precio de la competencia."}
        ]

    # Preguntas rápidas para la demo en video
    st.caption("Prueba rápida:")
    ejemplos = ["¿Cuánto cuesta el mango?", "Recomiéndame algo picante", "¿Cómo van las ventas?", "Costo del lote 600, 40 bolsas, competencia 45"]
    cols = st.columns(len(ejemplos))
    pregunta_rapida = None
    for col, ej in zip(cols, ejemplos):
        if col.button(ej, key=f"ej_{ej}"):
            pregunta_rapida = ej

    for m in st.session_state.mensajes:
        with st.chat_message(m["rol"]):
            st.markdown(m["contenido"])

    entrada = st.chat_input("Escribe tu consulta aquí...") or pregunta_rapida
    if entrada:
        with st.chat_message("user"):
            st.markdown(entrada)
        st.session_state.mensajes.append({"rol": "user", "contenido": entrada})

        with st.chat_message("assistant"):
            with st.spinner("Pensando y eligiendo herramienta..."):
                time.sleep(0.8)
                respuesta, herramienta = agente(entrada)
            st.caption(f"🔧 Herramienta usada: `{herramienta}`")
            st.markdown(respuesta)
        st.session_state.mensajes.append({"rol": "assistant", "contenido": f"🔧 `{herramienta}`\n\n{respuesta}"})

# ==========================================================
# PANEL DE VENTAS
# ==========================================================
elif selected == "Panel de Ventas":
    st.markdown("<h2>📊 Panel de Ventas</h2>", unsafe_allow_html=True)
    df = pd.read_sql_query("SELECT * FROM ventas", conn)

    if df.empty:
        st.info("No hay ventas registradas todavía. Haz una compra de prueba en la Tienda.")
    else:
        ingresos = df["total"].sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Ingresos Totales", f"${ingresos:,.2f} MXN")
        c2.metric("Unidades Vendidas", f"{int(df['cantidad'].sum())} bolsas")
        c3.metric("Ticket Promedio", f"${ingresos / len(df):,.2f} MXN")

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Unidades por producto")
            st.bar_chart(df.groupby("producto")["cantidad"].sum(), color=VERDE_CLARO)
        with g2:
            st.subheader("Ingresos por producto")
            st.bar_chart(df.groupby("producto")["total"].sum(), color=NARANJA)

        st.subheader("Bitácora de clientes")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Descargar CSV", df.to_csv(index=False).encode("utf-8"), "ventas.csv", "text/csv")
