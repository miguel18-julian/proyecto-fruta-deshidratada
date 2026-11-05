import base64
import re
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="VitalFruit | Tienda Oficial", page_icon="🍃",
                   layout="wide", initial_sidebar_state="collapsed")

DARK, GREEN, BEIGE, ORANGE = "#005C41", "#65B743", "#EBE8E1", "#FF7043"

# ==========================================================
# ESTILOS (pantalla completa, estilo Come Verde)
# ==========================================================
st.markdown("""
<style>
:root{--dark:#005C41;--green:#65B743;--beige:#EBE8E1;--orange:#FF7043;--blob:#DCDFD8;}
#MainMenu, footer, [data-testid="stHeader"], [data-testid="stToolbar"]{display:none !important;}
.stApp{background:var(--beige); overflow-x:hidden;}
.block-container{padding:0 3rem 0 3rem !important; max-width:100% !important;}
h1,h2,h3,h4{color:var(--dark) !important; font-family:'Segoe UI',Tahoma,sans-serif;}
.full{margin-left:-3rem; margin-right:-3rem;}
iframe[title="streamlit_option_menu.option_menu"]{margin-left:-3rem; width:calc(100% + 6rem) !important;}

/* Header */
.hdr{background:var(--dark); display:flex; align-items:center; justify-content:space-between;
     padding:22px 3rem 8px 3rem; color:white; font-size:18px;}
.hdr .logo{font-family:Georgia,'Times New Roman',serif; font-size:48px; line-height:.88;
     text-align:center; font-weight:700; letter-spacing:-1px;}
.hdr .logo small{display:block; font-size:22px; letter-spacing:0;}
.hdr .side{width:30%;} .hdr .right{text-align:right; font-size:24px;}
.hdr .right b{background:var(--orange); border-radius:50%; padding:2px 10px; font-size:16px;}

/* Franja en movimiento */
.marq{background:var(--green); color:white; font-weight:600; font-size:19px; padding:14px 0;
      overflow:hidden; white-space:nowrap;}
.marq div{display:inline-block; animation:mq 40s linear infinite;}
@keyframes mq{from{transform:translateX(0);} to{transform:translateX(-50%);}}

.ttl{text-align:center; font-size:48px !important; font-weight:700; margin:28px 0 14px 0 !important;}

/* Píldoras de categorías */
.st-key-pills button{background:var(--green) !important; color:white !important; border:none !important;
    border-radius:40px !important; padding:14px 6px !important; box-shadow:none !important;}
.st-key-pills button p{font-size:17px !important; font-weight:600;}
.st-key-pills button[data-testid="stBaseButton-primary"]{background:var(--dark) !important;}

/* Tarjetas de producto */
.circle{position:relative; width:min(100%,300px); aspect-ratio:1/1; border-radius:50%;
    margin:18px auto 14px auto; display:flex; align-items:center; justify-content:center;
    font-size:110px; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,.10); transition:transform .25s;}
.pcard:hover .circle{transform:scale(1.05);}
.photo{position:absolute; inset:0; background-size:cover; background-position:center;}
.tag{display:table; margin:0 auto 6px auto; background:var(--green); color:#fff; font-size:11px;
     font-weight:700; padding:3px 12px; border-radius:12px;}
.pname{text-align:center; color:var(--dark); font-weight:700; font-size:19px; text-transform:uppercase; margin:0;}
.ppeso{text-align:center; color:#666; font-size:14px; margin:0;}
.pprecio{text-align:center; color:var(--dark); font-weight:700; font-size:21px; margin:4px 0 8px 0;}

/* Botones */
.stButton>button, .stFormSubmitButton>button{background:var(--orange) !important; color:white !important;
    border:none !important; border-radius:30px !important; font-weight:700;}
.st-key-grid button{background:transparent !important; color:var(--dark) !important;
    border:2px solid var(--dark) !important; box-shadow:none !important;}
.st-key-grid button:hover{background:var(--dark) !important; color:white !important;}

/* Ondas + insignias + footer */
.wave-top{height:26px; background:radial-gradient(circle at 30px 0, transparent 0 17px, var(--green) 18px);
    background-size:60px 26px; margin-top:50px;}
.badges{background:var(--green); padding:30px 3rem 40px 3rem; display:flex; justify-content:center;
    flex-wrap:wrap; align-items:center;}
.blob{width:230px; height:230px; border-radius:50%; background:var(--blob); margin:0 -12px;
    display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
    color:var(--dark); font-weight:700; font-size:20px; line-height:1.15; padding:20px;}
.blob i{font-family:Georgia,serif; font-size:50px; font-weight:700;}
.blob em{font-family:Georgia,serif; font-size:20px;}
.wave-bot{height:26px; background:radial-gradient(circle at 30px 26px, var(--green) 0 17px, var(--dark) 18px);
    background-size:60px 26px;}
.foot{background:var(--dark); color:white; padding:30px 3rem 40px 3rem; display:grid;
    grid-template-columns:repeat(4,1fr); gap:20px; font-size:18px; line-height:2;}
.foot b{font-size:20px;}
.copy{background:#00402D; color:#B9D3C7; text-align:center; padding:12px; font-size:13px;}

/* Burbuja flotante del agente */
div[data-testid="stPopover"]{position:fixed; bottom:26px; right:30px; z-index:9999; width:auto !important;}
div[data-testid="stPopover"] button{width:70px; height:70px; border-radius:50% !important;
    background:var(--orange) !important; border:none !important; padding:0 !important;
    box-shadow:0 8px 24px rgba(0,0,0,.35) !important; animation:pulso 2.5s infinite;}
div[data-testid="stPopover"] button p{font-size:32px !important;}
div[data-testid="stPopover"] button svg{display:none;}
@keyframes pulso{0%{box-shadow:0 0 0 0 rgba(255,112,67,.6);}70%{box-shadow:0 0 0 18px rgba(255,112,67,0);}100%{box-shadow:0 0 0 0 rgba(255,112,67,0);}}
div[data-testid="stPopoverBody"]{width:min(430px,92vw) !important; border-radius:18px !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CATÁLOGO
# ==========================================================
CATEGORIAS = ["MOSTRAR TODO", "BOTANAS", "FRUTA DESHIDRATADA", "MIX ENERGÉTICO", "FAMILIARES", "INDIVIDUALES"]
WM = "https://commons.wikimedia.org/wiki/Special:FilePath/{}?width=700"


def P(pid, nombre, peso, precio, emoji, color, cats, tag, wiki=None):
    return {"id": pid, "nombre": nombre, "peso": peso, "precio": float(precio), "emoji": emoji,
            "color": color, "cats": cats, "tag": tag, "url": WM.format(wiki) if wiki else None}


F, B, M, FAM, IND = "FRUTA DESHIDRATADA", "BOTANAS", "MIX ENERGÉTICO", "FAMILIARES", "INDIVIDUALES"
CATALOGO = [
    P("mng-n60", "Mango natural", "60 g", 42, "🥭", "#F6D9A8", [F, IND], "MÁS VENDIDO", "Mango_and_cross_section.jpg"),
    P("mng-e60", "Mango enchilado", "60 g", 45, "🥭", "#C39F87", [F, IND], "PICOSITO", "Mango_and_cross_section.jpg"),
    P("man-50", "Manzana natural", "50 g", 30, "🍎", "#F4C7C3", [F, IND], "0% AZÚCAR", "Red_Apple.jpg"),
    P("pln-60", "Plátano natural", "60 g", 39, "🍌", "#F7E7A1", [F, IND], "NATURAL", "Banana-Single.jpg"),
    P("pin-60", "Piña deshidratada", "60 g", 42, "🍍", "#F7E7A1", [F, IND], "NUEVO", "Pineapple_and_cross_section.jpg"),
    P("fre-50", "Fresa deshidratada", "50 g", 48, "🍓", "#DBB8D0", [F, IND], "NUEVO", "PerfectStrawberry.jpg"),
    P("nar-50", "Naranja en rodajas", "50 g", 35, "🍊", "#F9D9A0", [F, IND], "VITAMINA C", "Orange-Fruit-Pieces.jpg"),
    P("kiw-50", "Kiwi deshidratado", "50 g", 50, "🥝", "#CFE5B8", [F, IND], "NUEVO", "Kiwi_aka.jpg"),
    P("pap-60", "Papaya deshidratada", "60 g", 38, "🍈", "#F9D0B0", [F, IND], "TROPICAL", "Papaya_cross_section_BNC.jpg"),
    P("mng-300", "Mango enchilado familiar", "300 g", 190, "🥭", "#C39F87", [F, FAM], "AHORRA 15%"),
    P("jic-60", "Jícama enchilada", "60 g", 40, "🌶️", "#DCCDE8", [B, IND], "BOTANA"),
    P("cmt-60", "Camote enchilado", "60 g", 40, "🍠", "#DBB8D0", [B, IND], "BOTANA"),
    P("chp-pln", "Chips de plátano sal y limón", "60 g", 38, "🍌", "#CFE5B8", [B, IND], "CRUJIENTE"),
    P("chp-man", "Chips de manzana con canela", "50 g", 36, "🍏", "#DCCDE8", [B, IND], "CRUJIENTE"),
    P("bet-60", "Chips de betabel", "60 g", 42, "🟣", "#E3C2D9", [B, IND], "NUEVO"),
    P("jic-180", "Jícama enchilada familiar", "180 g", 95, "🌶️", "#DCCDE8", [B, FAM], "FAMILIAR"),
    P("mix-sil", "Mix frutal silvestre", "100 g", 65, "🫐", "#DCCDE8", [M, IND], "ENERGÉTICO"),
    P("mix-nuez", "Mix nuez y arándano", "100 g", 72, "🥜", "#EBDDC3", [M, IND], "PROTEÍNA"),
    P("mix-trop", "Mix tropical", "100 g", 60, "🍍", "#F7E7A1", [M, IND], "TROPICAL"),
    P("mix-300", "Mix energético familiar", "300 g", 175, "🥜", "#EBDDC3", [M, FAM], "FAMILIAR"),
    P("mix-t300", "Mix tropical familiar", "300 g", 165, "🍍", "#F7E7A1", [M, FAM], "FAMILIAR"),
]
POR_ID = {p["id"]: p for p in CATALOGO}


@st.cache_data
def foto_local(pid: str):
    """Si existe imagenes/<id>.jpg|png|webp la usa (prioridad sobre las de internet)."""
    base = Path(__file__).parent / "imagenes"
    for ext, mime in (("jpg", "jpeg"), ("jpeg", "jpeg"), ("png", "png"), ("webp", "webp")):
        f = base / f"{pid}.{ext}"
        if f.exists():
            return f"data:image/{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    return None


# ==========================================================
# BASE DE DATOS Y CARRITO
# ==========================================================
@st.cache_resource
def get_conn():
    c = sqlite3.connect("ventas_fruta.db", check_same_thread=False)
    c.execute("""CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 cliente TEXT, producto TEXT, cantidad INTEGER, total REAL,
                 fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.commit()
    return c


conn = get_conn()
st.session_state.setdefault("carrito", {})
st.session_state.setdefault("categoria", "MOSTRAR TODO")
st.session_state.setdefault("mensajes", [{"rol": "assistant", "contenido":
    "¡Hola! Soy el agente de VitalFruit 🍃 Pregúntame por precios, recomendaciones, ventas, "
    "o escribe el costo de tu lote, las bolsas producidas y el precio de la competencia."}])


def agregar(pid):
    st.session_state.carrito[pid] = st.session_state.carrito.get(pid, 0) + 1
    st.toast(f"{POR_ID[pid]['nombre']} agregado al carrito 🛒")


def n_items():
    return sum(st.session_state.carrito.values())


def total_carrito():
    return sum(POR_ID[i]["precio"] * q for i, q in st.session_state.carrito.items())


# ==========================================================
# AGENTE (herramientas) — software libre: Python + SQLite
# ==========================================================
def tool_catalogo(q):
    q = q.lower()
    if "botana" in q:
        lista = [p for p in CATALOGO if B in p["cats"]]
    elif "mix" in q or "energ" in q:
        lista = [p for p in CATALOGO if M in p["cats"]]
    else:
        lista = [p for p in CATALOGO if any(w in p["nombre"].lower() for w in q.split() if len(w) > 3)]
    lista = lista or CATALOGO[:8]
    return "Esto encontré:\n\n" + "\n".join(
        f"- {p['emoji']} **{p['nombre']}** ({p['peso']}): ${p['precio']:.2f} MXN" for p in lista)


def tool_recomendar(q):
    q = q.lower()
    if any(w in q for w in ["dulce", "postre", "niño"]): pid = "fre-50"
    elif any(w in q for w in ["picante", "enchilado", "chile", "botana"]): pid = "mng-e60"
    elif any(w in q for w in ["energ", "gym", "deporte", "ejercicio"]): pid = "mix-nuez"
    elif any(w in q for w in ["familia", "compartir", "fiesta"]): pid = "mng-300"
    else: pid = "mng-n60"
    p = POR_ID[pid]
    return f"Te recomiendo {p['emoji']} **{p['nombre']}** ({p['peso']}) a **${p['precio']:.2f} MXN**."


def tool_ventas():
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    if df.empty:
        return "Aún no hay ventas registradas."
    top = df.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
    return (f"📈 **Resumen de ventas**\n\n- Registros: **{len(df)}**\n"
            f"- Ingresos: **${df['total'].sum():.2f} MXN**\n"
            f"- Más vendido: **{top.index[0]}** ({int(top.iloc[0])} uds)")


def tool_viabilidad(n):
    costo, bolsas, comp = n[:3]
    if bolsas <= 0:
        return "El número de bolsas debe ser mayor a cero."
    cu, ps = costo / bolsas, comp * 0.85
    mg = ps - cu
    txt = (f"📊 **Análisis de viabilidad**\n\n- Costo unitario: **${cu:.2f}**\n"
           f"- Precio sugerido (15% bajo la competencia): **${ps:.2f}**\n"
           f"- Margen por bolsa: **${mg:.2f}** ({mg / ps * 100:.0f}%)\n\n")
    return txt + ("✅ **Viable:** hay utilidad." if mg > 0 else "⚠️ **Alerta:** vendes con pérdida; reduce costos o sube el precio.")


def agente(msg):
    q = msg.lower()
    nums = [float(x) for x in re.findall(r"\d+\.?\d*", msg)]
    if len(nums) >= 3 and any(w in q for w in ["costo", "lote", "bolsa", "competencia", "viab"]):
        return tool_viabilidad(nums), "calcular_viabilidad"
    if any(w in q for w in ["venta", "ingreso", "vendido", "pedidos"]):
        return tool_ventas(), "consultar_base_de_datos"
    if any(w in q for w in ["recomiend", "sugier", "qué me", "que me"]):
        return tool_recomendar(msg), "recomendar_producto"
    if any(w in q for w in ["precio", "cuesta", "catálogo", "catalogo", "productos", "tienen", "botana", "mix",
                            "mango", "manzana", "plátano", "platano", "fresa", "piña", "kiwi", "papaya", "naranja"]):
        return tool_catalogo(msg), "consultar_catalogo"
    if any(w in q for w in ["envío", "envio", "entrega", "tarda"]):
        return "🚚 Entregamos en 24 h en zonas con cobertura.", "preguntas_frecuentes"
    return ("Puedo ayudarte con:\n\n- 🛍️ **Precios** (*¿cuánto cuesta el mango?*)\n"
            "- 🎯 **Recomendaciones** (*recomiéndame algo picante*)\n- 📈 **Ventas** (*¿cómo van las ventas?*)\n"
            "- 💰 **Viabilidad** (*costo del lote 600, 40 bolsas, competencia 45*)"), "ayuda"


@st.fragment
def chat_agente():
    caja = st.container(height=330)
    ejemplos = ["¿Cuánto cuesta el mango?", "Recomiéndame algo picante", "¿Cómo van las ventas?",
                "Costo del lote 600, 40 bolsas, competencia 45"]
    pregunta = None
    c1, c2 = st.columns(2)
    for i, ej in enumerate(ejemplos):
        if (c1 if i % 2 == 0 else c2).button(ej, key=f"ej{i}", use_container_width=True):
            pregunta = ej
    with st.form("form_agente", clear_on_submit=True):
        txt = st.text_input("Mensaje", placeholder="Pregúntale al agente...", label_visibility="collapsed")
        enviado = st.form_submit_button("Enviar", use_container_width=True)
    if enviado and txt.strip():
        pregunta = txt
    if pregunta:
        resp, tool = agente(pregunta)
        st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})
        st.session_state.mensajes.append({"rol": "assistant", "contenido": f"🔧 `{tool}`\n\n{resp}"})
    with caja:
        for m in st.session_state.mensajes:
            with st.chat_message(m["rol"]):
                st.markdown(m["contenido"])


# ==========================================================
# COMPONENTES DE PÁGINA
# ==========================================================
def encabezado():
    st.markdown(f"""
    <div class="full hdr">
        <div class="side">🍃 Fruta deshidratada artesanal</div>
        <div class="logo">vital<small>fruit</small></div>
        <div class="side right">🔍 &nbsp; 🛒 <b>{n_items()}</b></div>
    </div>
    <div class="full marq"><div>{"Tu antojo saludable en casa en 24h | Envíos a todo México 🚚 &nbsp;&nbsp;&nbsp;&nbsp; " * 12}</div></div>
    """, unsafe_allow_html=True)


def pie():
    st.markdown("""
    <div class="full wave-top"></div>
    <div class="full badges">
        <div class="blob"><i>0%</i>azúcar<em>añadida</em></div>
        <div class="blob"><i>100%</i>Sabor natural</div>
        <div class="blob"><i>Libre</i>de colorantes artificiales</div>
        <div class="blob"><i>Vegano</i></div>
        <div class="blob">Hecho en<i>México</i></div>
    </div>
    <div class="full wave-bot"></div>
    <div class="full foot">
        <div><b>Productos</b><br>Botanas<br>Fruta deshidratada<br>Mix energético</div>
        <div><b>VitalFruit®</b><br>Buscar<br>Contacto<br>Quiénes somos</div>
        <div><b>Soporte</b><br>Preguntas frecuentes<br>contacto@vitalfruit.mx</div>
        <div>Teziutlán, Puebla, México<br>📘 &nbsp; 📸 &nbsp; 🎵 &nbsp; ▶️ &nbsp; ✉️</div>
    </div>
    <div class="full copy">© 2026 VitalFruit® · Fruta deshidratada artesanal</div>
    """, unsafe_allow_html=True)


def tarjeta(p):
    src = foto_local(p["id"]) or p["url"]
    foto = f'<div class="photo" style="background-image:url(\'{src}\')"></div>' if src else ""
    return f"""
    <div class="pcard">
        <div class="circle" style="background:{p['color']}"><span>{p['emoji']}</span>{foto}</div>
        <div class="tag">{p['tag']}</div>
        <p class="pname">{p['nombre']}</p>
        <p class="ppeso">{p['peso']}</p>
        <p class="pprecio">$ {p['precio']:.2f} MXN</p>
    </div>"""


def vista_catalogo(titulo, cat_fija=None):
    st.markdown(f"<h1 class='ttl'>{titulo}</h1>", unsafe_allow_html=True)
    if cat_fija is None:
        with st.container(key="pills"):
            cols = st.columns([0.4] + [1] * len(CATEGORIAS) + [0.4])
            for col, c in zip(cols[1:-1], CATEGORIAS):
                col.button(c, key=f"pill_{c}", use_container_width=True,
                           type="primary" if st.session_state.categoria == c else "secondary",
                           on_click=lambda c=c: st.session_state.update(categoria=c))
        cat = st.session_state.categoria
    else:
        cat = cat_fija

    f1, _, f3 = st.columns([2, 5, 2])
    orden = f1.selectbox("Ordenar", ["Destacados", "Precio: menor a mayor", "Precio: mayor a menor", "Nombre A-Z"],
                         key=f"ord_{titulo}", label_visibility="collapsed")
    busq = f3.text_input("Buscar", placeholder="🔍 Buscar producto", key=f"q_{titulo}", label_visibility="collapsed")

    items = CATALOGO if cat == "MOSTRAR TODO" else [p for p in CATALOGO if cat in p["cats"]]
    if busq:
        items = [p for p in items if busq.lower() in p["nombre"].lower()]
    if orden == "Precio: menor a mayor": items = sorted(items, key=lambda p: p["precio"])
    elif orden == "Precio: mayor a menor": items = sorted(items, key=lambda p: -p["precio"])
    elif orden == "Nombre A-Z": items = sorted(items, key=lambda p: p["nombre"])

    if not items:
        st.info("No encontramos productos con ese filtro.")
    with st.container(key="grid"):
        for i in range(0, len(items), 4):
            for col, p in zip(st.columns(4), items[i:i + 4]):
                with col:
                    st.markdown(tarjeta(p), unsafe_allow_html=True)
                    st.button("Agregar al carrito 🛒", key=f"add_{titulo}_{p['id']}",
                              on_click=agregar, args=(p["id"],), use_container_width=True)


def vista_carrito():
    st.markdown("<h1 class='ttl'>🛒 Tu carrito</h1>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. Agrega productos desde el catálogo.")
        return
    for pid, q in list(st.session_state.carrito.items()):
        p = POR_ID[pid]
        c1, c2, c3 = st.columns([5, 3, 1])
        c1.markdown(f"### {p['emoji']} {p['nombre']} · {p['peso']}")
        c2.markdown(f"### {q} × ${p['precio']:.2f} = ${q * p['precio']:.2f}")
        if c3.button("✖", key=f"del_{pid}"):
            del st.session_state.carrito[pid]
            st.rerun()
    st.markdown(f"## Total: ${total_carrito():.2f} MXN")
    with st.form("checkout", clear_on_submit=True):
        cliente = st.text_input("Nombre completo:")
        if st.form_submit_button("Finalizar compra"):
            if not cliente.strip():
                st.error("Escribe tu nombre para registrar el pedido.")
            else:
                total = total_carrito()
                for pid, q in st.session_state.carrito.items():
                    p = POR_ID[pid]
                    conn.execute("INSERT INTO ventas (cliente, producto, cantidad, total) VALUES (?,?,?,?)",
                                 (cliente.strip(), p["nombre"], q, p["precio"] * q))
                conn.commit()
                st.session_state.carrito = {}
                st.success(f"¡Gracias {cliente}! Pedido por **${total:.2f} MXN** registrado 🎉")
                st.balloons()


def vista_nosotros():
    st.markdown("<h1 class='ttl'>Quiénes somos</h1>", unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown("""
### Fruta real, deshidratada con cuidado 🍃
En VitalFruit deshidratamos fruta y verdura fresca con tecnología controlada para conservar su sabor
y sus nutrientes, sin azúcar añadida ni colorantes artificiales. Son snacks pensados para
cualquier momento del día.
""")
    with b:
        for t, d in [("🌱 Ingredientes naturales", "Solo fruta, verdura y especias."),
                     ("⚡ Deshidratación controlada", "Temperatura y tiempo cuidados lote por lote."),
                     ("🇲🇽 Hecho en México", "Producción local en Puebla.")]:
            st.markdown(f"**{t}** — {d}")


def vista_panel():
    st.markdown("<h1 class='ttl'>📊 Panel de ventas</h1>", unsafe_allow_html=True)
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    if df.empty:
        st.info("No hay ventas todavía. Haz una compra de prueba.")
        return
    ing = df["total"].sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos totales", f"${ing:,.2f} MXN")
    c2.metric("Unidades vendidas", f"{int(df['cantidad'].sum())}")
    c3.metric("Ticket promedio", f"${ing / len(df):,.2f} MXN")
    g1, g2 = st.columns(2)
    g1.subheader("Unidades por producto")
    g1.bar_chart(df.groupby("producto")["cantidad"].sum(), color=GREEN)
    g2.subheader("Ingresos por producto")
    g2.bar_chart(df.groupby("producto")["total"].sum(), color=ORANGE)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Descargar CSV", df.to_csv(index=False).encode("utf-8"), "ventas.csv", "text/csv")


# ==========================================================
# APP
# ==========================================================
encabezado()
seleccion = option_menu(
    None, ["Productos", "Botanas", "Fruta deshidratada", "Mix energético", "Nosotros", "Carrito", "Ventas"],
    icons=["shop", "cookie", "apple", "box-seam", "info-circle", "cart3", "graph-up-arrow"],
    orientation="horizontal", key="nav",
    styles={"container": {"padding": "4px 0 14px 0", "background-color": DARK, "border-radius": "0"},
            "icon": {"color": ORANGE, "font-size": "16px"},
            "nav-link": {"color": "white", "font-size": "16px", "--hover-color": "#0A7A57"},
            "nav-link-selected": {"background-color": GREEN, "font-weight": "bold"}})

if seleccion == "Productos":
    vista_catalogo("Conoce todos nuestros productos")
elif seleccion == "Botanas":
    vista_catalogo("Botanas", B)
elif seleccion == "Fruta deshidratada":
    vista_catalogo("Fruta deshidratada", F)
elif seleccion == "Mix energético":
    vista_catalogo("Mix energético", M)
elif seleccion == "Nosotros":
    vista_nosotros()
elif seleccion == "Carrito":
    vista_carrito()
else:
    vista_panel()

if seleccion != "Ventas":
    pie()

# Burbuja flotante del agente (visible en todas las páginas)
with st.popover("💬"):
    st.markdown("#### 🤖 Agente VitalFruit")
    chat_agente()
