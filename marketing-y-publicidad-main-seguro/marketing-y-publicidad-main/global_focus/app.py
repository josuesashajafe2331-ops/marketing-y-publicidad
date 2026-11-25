"""Global Focus S.A.C. - Marketing y Publicidad Corporativa Empresarial.
Ejecutar:  pip install -r requirements.txt  &&  python app.py
Abrir:     http://127.0.0.1:5000
"""
import os
import re
import secrets
import sqlite3
import time
from urllib.parse import urlparse
import servicios_info as si
from flask import Flask, render_template, request, jsonify, g, Response, redirect, url_for, session, abort, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
# Modo desarrollo SOLO en tu computadora: FLASK_DEBUG=1. En Render NO debe existir esta variable.
DEBUG = os.environ.get("FLASK_DEBUG") == "1"
DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(BASE, "global_focus.db")
)

CONFIG = {
    "empresa": "Global Focus S.A.C.",
    "telefonos": ["960 389 151", "980 688 699"],
    "whatsapp": "51 960 389 151",          # Código de país + número, sin espacios
    # Enlace del botón "¡Hola, charlemos!" (abre WhatsApp con el mensaje ya escrito)
    "whatsapp_url": "https://api.whatsapp.com/send/?phone=51960389151&text=¡Hola%21+Vengo+de+su+sitio+web+y+quisiera+más+información&type=phone_number&app_absent=0",
    "correo": "mktpublicidadcorporativo@gmail.com",  # Reemplazar por el correo oficial
    "web": "www.mkt-corporativo.com",
    "ubicacion": "Oficina 216, Jr. Carabaya 1128, Cercado de Lima, Perú",
    "dir_linea1": "Of. 216, Jr. Carabaya 1128",     # Dirección corta para el pie de página
    "dir_linea2": "Cercado de Lima, Perú",
    "mapa_lat": -12.054594126562296,               # Coordenadas del mapa
    "mapa_lng": -77.03556743975349,
    "mision": "Ayudar a las empresas a comunicar mejor lo que hacen, con diseño, publicidad y tecnología al servicio de sus resultados.",
    "vision": "Ser la agencia de marketing corporativo de referencia para las empresas de Lima y del Perú.",
    "redes": {
        "YouTube":   "https://www.youtube.com/@MKT_CORPORATIVO",
        "Instagram": "https://www.instagram.com/mkt_publicidad_corporativo/",
        "X":         "https://x.com/MKT_Corporativo",
        "TikTok":    "https://www.tiktok.com/@mkt_corporativo_?lang=es",
        "Facebook":  "https://www.facebook.com/share/1ASFnbFJ2g/",
    },
}

# Para escribirnos (formulario y chat) hay que tener cuenta: cualquier visitante puede crear la suya.
# La administración es UNA sola cuenta, la de este correo (no se puede registrar por la web).
# La clave NUNCA va en el código: se define en la variable de entorno ADMIN_CLAVE (Render > Environment).
# Al iniciar, la app crea la cuenta (o actualiza su clave) con ese valor, guardado cifrado en la base.
# Usa una clave larga (12+ caracteres). Para cambiarla: cambia ADMIN_CLAVE en Render y reinicia.
ADMIN_CORREO = os.environ.get("ADMIN_CORREO", "mktpublicidadcorporativo@gmail.com").strip().lower()
ADMIN_CLAVE = os.environ.get("ADMIN_CLAVE", "")

# Servicios agrupados por categoría (cat, [(titulo, descripcion), ...])
CATEGORIAS = [('Marketing y estrategias digitales', [('Marketing', 'Conjunto de actividades y estrategias para promocionar y comercializar productos o servicios, satisfacer las necesidades de los clientes y alcanzar objetivos comerciales.'),
    ('Branding', 'Consiste en construir y gestionar la identidad de una marca mediante su nombre, logotipo, colores, personalidad y valores para diferenciarla de la competencia.'),
    ('Estudio de mercado', 'Investiga a los clientes, competidores, tendencias y necesidades para identificar oportunidades y tomar mejores decisiones comerciales.'),
    ('Análisis situacional del mercado', 'Análisis de los competidores y comparación de sus productos, servicios, precios y estrategias para conocer la posición de una empresa en el mercado.'),
    ('Creación de contenidos', 'Consiste en elaborar artículos, imágenes, videos y otros materiales útiles para informar, promocionar y atraer al público.'),
    ('Estrategia de contenidos', 'Es el plan que establece qué contenido crear, a quién dirigirlo, dónde publicarlo y con qué frecuencia para alcanzar los objetivos de marketing.'),
    ('Grilla de contenidos', 'Es un calendario que organiza las fechas de publicación, los temas, los formatos y las plataformas donde se difundirá el contenido.'),
    ('Community Manager', 'Es la persona encargada de administrar las redes sociales, responder consultas y comentarios, moderar interacciones y mantener una buena relación con los seguidores.'),
    ('Analíticas digitales', 'Consisten en recopilar y analizar datos del tráfico web, las interacciones y las conversiones para medir resultados y mejorar las estrategias digitales.'),
    ('SEO en redes sociales', 'Optimiza los perfiles y publicaciones para mejorar su visibilidad en las búsquedas de plataformas como Instagram, TikTok, YouTube, Facebook y LinkedIn.'),
    ('Definición del target', 'Es identificar al público objetivo considerando sus características, intereses, necesidades y comportamientos para dirigir correctamente las campañas.'),
    ('Ads (publicidad)', 'Son anuncios pagados en plataformas como Google Ads, Facebook Ads e Instagram Ads para aumentar la visibilidad, atraer clientes potenciales y generar ventas.')]),
    ('Publicidad y promoción empresarial', [('Publicidad', 'Es una herramienta de comunicación que utiliza mensajes creativos y persuasivos para captar la atención, generar interés y motivar al público a comprar o participar en una causa.'),
    ('Presupuestos', 'Es la planificación del dinero disponible para realizar actividades de marketing y publicidad, controlar los gastos y distribuir los recursos eficientemente.'),
    ('Campañas impresas', 'Son estrategias publicitarias que utilizan materiales físicos como volantes, folletos, afiches y revistas para promocionar productos, servicios o eventos.'),
    ('Piezas gráficas', 'Son materiales visuales como logotipos, carteles, banners e infografías que comunican mensajes, promocionan productos y refuerzan la identidad de una marca.'),
    ('Merchandising', 'El merchandising consiste en diseñar, personalizar y distribuir artículos promocionales con la identidad de una empresa, como lapiceros, tazas, polos, llaveros, agendas, folders y banners. Su objetivo es promocionar la marca, aumentar su reconocimiento, fidelizar clientes y fortalecer la imagen corporativa.'),
    ('TV, radio y prensa', 'Son medios tradicionales de publicidad. La televisión difunde anuncios audiovisuales, la radio transmite anuncios de audio y la prensa publica anuncios en periódicos y revistas.')]),
    ('Diseño e identidad corporativa', [('Diseño digital gráfico', 'Es la creación de elementos visuales mediante imágenes, colores, tipografías y composiciones para comunicar mensajes en medios digitales e impresos.'),
    ('Identidad corporativa', 'Es el conjunto de elementos visuales y conceptuales que representan a una empresa, como su logotipo, colores, tipografía, valores y misión. Permite diferenciarla y transmitir confianza.'),
    ('Marca personal', 'Consiste en construir una identidad profesional propia que destaque las habilidades, conocimientos, experiencia, valores y reputación de una persona.'),
    ('Papelería corporativa', 'Comprende materiales impresos como tarjetas de presentación, hojas membretadas, sobres, carpetas y folletos que mantienen una imagen empresarial uniforme y profesional.'),
    ('Packaging', 'Es el diseño de envases y empaques de productos. Busca protegerlos, proporcionar información, atraer al consumidor y diferenciar la marca.')]),
    ('Producción de contenidos y medios digitales', [('Edición', 'Es el proceso de revisar, corregir y mejorar textos, fotografías, videos y audios para obtener contenidos claros, coherentes y profesionales.'),
    ('Fotografía', 'Consiste en crear y seleccionar imágenes de productos, personas, eventos y otros elementos para comunicar mensajes, captar la atención y mejorar la presentación de una marca.'),
    ('Audiovisuales', 'Son contenidos que combinan imágenes, videos, gráficos y sonidos, como anuncios, videos promocionales y presentaciones, para comunicar información y promocionar servicios.'),
    ('Diseño web', 'Consiste en planificar y desarrollar sitios web considerando su apariencia, organización, navegación y funcionalidad para ofrecer una experiencia positiva al usuario.')])]

SERVICIOS = [(t, d, "#0B4EA2", c) for c, items in CATEGORIAS for t, d in items]

EMPRESAS = [
    ("GRUPO ACADÉMICO", "Brindamos formación académica de calidad, con talleres, clases y programas especializados que impulsan el desarrollo profesional y personal.", "EDUCACIÓN", "Asesoría académica|Capacitación|Material educativo", ""),
    ("CONSULTORÍA MAGISTER SARAYA", "Ofrecemos asesoría y consultoría jurídica en derecho civil, penal, laboral, registral y administrativo, con un enfoque práctico y comprometido con cada cliente.", "DERECHO", "Derecho civil|Derecho penal|Derecho laboral|Registral", ""),
    ("INMOBILIARIA GRUPO VISIÓN", "Facilitamos la compra, venta y alquiler de inmuebles, con un servicio personalizado y seguro, orientado a tus necesidades y proyectos.", "INMOBILIARIA", "Compra y venta|Alquileres|Créditos hipotecarios", ""),
    ("SANEAMIENTO FÍSICO LEGAL", "Brindamos servicios de formalización de propiedad, planos, topografía y trámites ante registros y municipalidades, asegurando la validez legal de cada proyecto.", "SANEAMIENTO", "Formalización de la propiedad|Inmatriculación|Trato sucesivo|Sucesión intestada", ""),
]

# Equipo (cargo, nombre, descripción). El orden es el de las fotos: equipo-1, equipo-2, equipo-3, equipo-4
EQUIPO = [
    ("Gerente General / Fundador", "Mario Saraya Lopez",
     "Líder visionario con amplia experiencia en el desarrollo y gestión de proyectos inmobiliarios en Lima."),
    ("Directora de Operaciones", "Claudia Reyes Sayas",
     "Encargada de supervisar que cada proyecto se ejecute con los más altos estándares de calidad."),
    ("Gerente de Ventas", "Bianca Ybarcena Izaguirre",
     "Dedicada a encontrar la mejor oportunidad de inversión que se adapte a las necesidades de cada cliente."),
    ("Coordinadora Administrativa", "Tatiana Jiménez Calvi",
     "Asegura que todos los procesos internos y la atención al cliente fluyan de manera eficiente y transparente."),
    ("Jefe de Asesoría Legal", "Audrey Valdez Espinoza",
     "Especialista en garantizar la seguridad jurídica y el saneamiento de cada transacción inmobiliaria."),
    ("Abogada", "Nazareth Rondón Villanueva",
     "Abogada especialista en derecho publicitario, dedicada a brindar jurídicamente las campañas creativas, proteger la propiedad intelectual y asegurar el cumplimiento normativo en cada estrategia.."),

]

app = Flask(__name__)

# Render (y la mayoría de hostings) pone un proxy delante: sin esto todas las visitas "tienen la misma IP"
if os.environ.get("TRUST_PROXY", "1") == "1":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


def _clave_secreta():
    k = os.environ.get("SECRET_KEY")
    if not k:
        if DEBUG:
            return secrets.token_hex(32)      # solo desarrollo: las sesiones se reinician al reiniciar
        raise RuntimeError("Falta configurar SECRET_KEY (variable de entorno)")
    return k


app.config.update(
    SECRET_KEY=_clave_secreta(),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=not DEBUG,          # en local (http) debe ser False; en produccion (https) True
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 12,
    MAX_CONTENT_LENGTH=64 * 1024,             # ninguna petición legítima pesa más de 64 KB
)


# ---------------------------------------------------------------- seguridad
_CSP = "; ".join([
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src https://fonts.gstatic.com",
    "img-src 'self' data:",
    "media-src 'self'",
    "frame-src https://maps.google.com https://www.google.com",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])


@app.after_request
def cabeceras_seguridad(resp):
    resp.headers["Content-Security-Policy"] = _CSP
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    if request.is_secure:
        resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Las paginas con sesion / panel no se guardan en cache del navegador
    if request.path.startswith(("/admin", "/api", "/login", "/registro")):
        resp.headers["Cache-Control"] = "no-store"
    return resp


@app.before_request
def proteger_csrf():
    """Protección CSRF: una petición que modifica datos solo se acepta si viene de este mismo sitio
    (cabeceras Sec-Fetch-Site / Origin que envía el navegador). Se suma a SameSite=Lax de la cookie."""
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return None
    sitio = request.headers.get("Sec-Fetch-Site")
    if sitio is not None and sitio not in ("same-origin", "none"):
        abort(403)
    origen = request.headers.get("Origin")
    if origen and origen != "null":
        if urlparse(origen).netloc != request.host:
            abort(403)
    elif origen == "null":
        abort(403)
    return None


# Límite sencillo de velocidad por IP (en memoria; con 1 worker de gunicorn es exacto)
_ventanas = {}


def _limite(nombre, maximo, segundos):
    """True si la IP YA superó 'maximo' acciones en los últimos 'segundos'; si no, cuenta esta acción."""
    ahora = time.time()
    clave = (nombre, request.remote_addr or "?")
    marcas = [t for t in _ventanas.get(clave, []) if ahora - t < segundos]
    if len(marcas) >= maximo:
        _ventanas[clave] = marcas
        return True
    marcas.append(ahora)
    _ventanas[clave] = marcas
    if len(_ventanas) > 5000:                 # evita que el diccionario crezca sin fin
        for k in [k for k, v in _ventanas.items() if not v or ahora - v[-1] > 3600]:
            _ventanas.pop(k, None)
    return False


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS servicios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        color TEXT NOT NULL,
        orden INTEGER NOT NULL,
        categoria TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS empresas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        rubro TEXT NOT NULL,
        detalle TEXT NOT NULL DEFAULT '',
        contacto TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS equipo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo TEXT NOT NULL,
        nombre TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        clave TEXT NOT NULL,
        creado TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS mensajes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT NOT NULL,
        servicio TEXT,
        mensaje TEXT NOT NULL,
        creado TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    """)

    # Migración: descripción del integrante del equipo
    ce = [r[1] for r in db.execute("PRAGMA table_info(equipo)")]
    if "descripcion" not in ce:
        db.execute("ALTER TABLE equipo ADD COLUMN descripcion TEXT NOT NULL DEFAULT ''")

    # Migración: teléfono y empresa en los mensajes del formulario de contacto
    cm = [r[1] for r in db.execute("PRAGMA table_info(mensajes)")]
    if "telefono" not in cm:
        db.execute("ALTER TABLE mensajes ADD COLUMN telefono TEXT NOT NULL DEFAULT ''")
    if "empresa" not in cm:
        db.execute("ALTER TABLE mensajes ADD COLUMN empresa TEXT NOT NULL DEFAULT ''")

    # Cuentas: rol (las cuentas que ya existían eran del equipo -> 'admin'; las nuevas se indican al crearlas)
    cu = [r[1] for r in db.execute("PRAGMA table_info(usuarios)")]
    if "rol" not in cu:
        db.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'admin'")
    # Solo el correo de administración puede ser admin
    db.execute("UPDATE usuarios SET rol='cliente' WHERE LOWER(correo) <> LOWER(?)", (ADMIN_CORREO,))
    fila_admin = db.execute("SELECT id, clave FROM usuarios WHERE LOWER(correo)=LOWER(?)", (ADMIN_CORREO,)).fetchone()
    if not ADMIN_CLAVE:
        if fila_admin is None:
            print("AVISO: define ADMIN_CLAVE (variable de entorno) para crear la cuenta de administración.", flush=True)
    else:
        if len(ADMIN_CLAVE) < 12:
            print("AVISO: ADMIN_CLAVE es corta; usa 12 caracteres o más.", flush=True)
        if fila_admin is None:
            db.execute("INSERT INTO usuarios(nombre, correo, clave, rol) VALUES(?, ?, ?, 'admin')",
                       ("Administración", ADMIN_CORREO, generate_password_hash(ADMIN_CLAVE)))
        else:
            db.execute("UPDATE usuarios SET rol='admin' WHERE id=?", (fila_admin[0],))
            if not check_password_hash(fila_admin[1], ADMIN_CLAVE):   # rotación de clave desde Render
                db.execute("UPDATE usuarios SET clave=? WHERE id=?", (generate_password_hash(ADMIN_CLAVE), fila_admin[0]))
    # Cada consulta puede pertenecer a una cuenta (0 = visitante sin cuenta)
    if "usuario_id" not in cm:
        db.execute("ALTER TABLE mensajes ADD COLUMN usuario_id INTEGER NOT NULL DEFAULT 0")

    # Chat posterior al formulario: cada mensaje recibido abre una conversación identificada por un token
    if "token" not in cm:
        db.execute("ALTER TABLE mensajes ADD COLUMN token TEXT NOT NULL DEFAULT ''")
    if "cerrado" not in cm:
        db.execute("ALTER TABLE mensajes ADD COLUMN cerrado TEXT NOT NULL DEFAULT ''")  # '', 'cliente' o 'agente'
    db.executescript("""
    CREATE TABLE IF NOT EXISTS chat(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mensaje_id INTEGER NOT NULL,
        de TEXT NOT NULL,            -- 'cliente', 'agente' o 'auto'
        texto TEXT NOT NULL,
        creado TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    CREATE INDEX IF NOT EXISTS chat_msg ON chat(mensaje_id, id);
    """)

    # Migración: columna categoría y sincronización de servicios (los mensajes no se tocan)
    cols = [r[1] for r in db.execute("PRAGMA table_info(servicios)")]
    if "categoria" not in cols:
        db.execute("ALTER TABLE servicios ADD COLUMN categoria TEXT NOT NULL DEFAULT ''")
    actuales = [r[0] for r in db.execute("SELECT titulo FROM servicios ORDER BY orden, id")]
    if actuales != [x[0] for x in SERVICIOS]:
        db.execute("DELETE FROM servicios")
        db.executemany(
            "INSERT INTO servicios(titulo, descripcion, color, orden, categoria) VALUES(?, ?, ?, ?, ?)",
            [(t, d, c, i + 1, cat) for i, (t, d, c, cat) in enumerate(SERVICIOS)]
        )

    # Migración de columnas de empresas en caso de no existir
    columnas_empresas = [r[1] for r in db.execute("PRAGMA table_info(empresas)")]
    for col in ("detalle", "contacto"):
        if col not in columnas_empresas:
            db.execute(f"ALTER TABLE empresas ADD COLUMN {col} TEXT NOT NULL DEFAULT ''")

    if db.execute("SELECT COUNT(*) FROM empresas").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO empresas(nombre, descripcion, rubro, detalle, contacto) VALUES(?, ?, ?, ?, ?)",
            EMPRESAS
        )

    # Sincroniza el nombre de cada empresa con la lista EMPRESAS (por orden), así editar el nombre en app.py basta
    for (i,), e in zip(db.execute("SELECT id FROM empresas ORDER BY id").fetchall(), EMPRESAS):
        db.execute("UPDATE empresas SET nombre=? WHERE id=?", (e[0], i))

    for n, desc, _, _, _ in EMPRESAS:
        db.execute("UPDATE empresas SET descripcion=? WHERE nombre=?", (desc, n))

    for n, _, _, det, con in EMPRESAS:
        db.execute(
            "UPDATE empresas SET detalle=?, contacto=? WHERE nombre=? AND (detalle='' OR detalle IS NULL)",
            (det, con, n)
        )

    # El contacto de cada empresa también se sincroniza con la lista EMPRESAS
    for n, _, _, _, con in EMPRESAS:
        db.execute("UPDATE empresas SET contacto=? WHERE nombre=?", (con, n))

    # Sincroniza el equipo con la lista EQUIPO (si cambia, se vuelve a cargar)
    if [(r[0], r[1], r[2]) for r in db.execute("SELECT cargo, nombre, descripcion FROM equipo ORDER BY id")] != EQUIPO:
        db.execute("DELETE FROM equipo")
        db.executemany("INSERT INTO equipo(cargo, nombre, descripcion) VALUES(?, ?, ?)", EQUIPO)

    db.commit()
    db.close()


def _grupos():
    filas = get_db().execute("SELECT * FROM servicios ORDER BY orden ASC, id ASC").fetchall()
    grupos = {}
    for f in filas:
        grupos.setdefault(f["categoria"], []).append(f)
    return list(grupos.items())


EXT_IMG = ("jpg", "jpeg", "png", "webp")


def _buscar_img(carpeta, nombre):
    """Devuelve la ruta static/... de la primera imagen existente con ese nombre, o None."""
    for ext in EXT_IMG:
        ruta = f"{carpeta}/{nombre}.{ext}"
        if os.path.exists(os.path.join(BASE, "static", ruta)):
            return ruta
    return None


def img_servicio(n):
    # static/img/servicios/servicio-01.jpg ... servicio-27.jpg
    return _buscar_img("img/servicios", f"servicio-{int(n):02d}")


def img_equipo(n):
    # static/img/equipo/equipo-1.jpg ... (foto redonda de cada integrante, según su número)
    return _buscar_img("img/equipo", f"equipo-{int(n)}")


def img_proyecto(n):
    # static/img/proyectos/proyecto-1.jpg ... proyecto-4.jpg (una por empresa, en orden)
    return _buscar_img("img/proyectos", f"proyecto-{int(n)}")


def img_portada():
    # Foto grande de la página de servicios. Acepta cualquier imagen en static/img/ cuyo nombre
    # empiece con "servicios-portada" (jpg, jpeg, png, webp, jfif, gif, avif; mayúsculas o minúsculas).
    carpeta = os.path.join(BASE, "static", "img")
    for f in sorted(os.listdir(carpeta)):
        nombre, _, ext = f.lower().rpartition(".")
        if nombre.startswith("servicios-portada") and ext in ("jpg", "jpeg", "png", "webp", "jfif", "gif", "avif"):
            return "img/" + f
    return None


def img_categoria(n):
    # static/img/categoria-1.png ... categoria-4.png (si no existe, usa personaje2.png)
    return _buscar_img("img", f"categoria-{int(n)}") or "img/personaje2.png"


@app.context_processor
def inyectar():
    grupos = _grupos()
    return {"grupos": grupos, "categorias": [g[0] for g in grupos],
            "img_servicio": img_servicio, "img_equipo": img_equipo, "img_proyecto": img_proyecto, "img_categoria": img_categoria, "img_portada": img_portada,
            "img_contacto": lambda: _buscar_img("img", "contacto"),
            "cuenta": _usuario()}


@app.route("/")
def index():
    db = get_db()
    # Recupera los 9 servicios ordenados correlativamente del 1 al 9
    servicios = db.execute("SELECT * FROM servicios ORDER BY orden ASC, id ASC").fetchall()
    empresas = db.execute("SELECT * FROM empresas ORDER BY id ASC").fetchall()
    equipo = db.execute("SELECT * FROM equipo ORDER BY id ASC").fetchall()
    return render_template("index.html", c=CONFIG, servicios=servicios, empresas=empresas, equipo=equipo, cats=_catalogo())


@app.route("/proyectos")
def proyectos_page():
    empresas = get_db().execute("SELECT * FROM empresas ORDER BY id ASC").fetchall()
    return render_template("proyectos.html", c=CONFIG, empresas=empresas)


@app.route("/nosotros")
def nosotros_page():
    # La sección "Quiénes somos" y el equipo ahora están en la página principal
    return redirect(url_for("index") + "#nosotros", code=301)


def _catalogo():
    """Servicios en 3 niveles: categoría -> temas -> información de cada tema."""
    catalogo = []
    for i, (cat, filas) in enumerate(_grupos()):
        temas = []
        for f in filas:
            extra = si.INFO.get(f["titulo"], {})
            temas.append({
                "titulo": f["titulo"],
                "descripcion": f["descripcion"],
                "icono": si.ICONOS[si.ICONO_TEMA.get(f["titulo"], "objetivo")],
                "objetivo": extra.get("objetivo", ""),
                "caracteristicas": extra.get("caracteristicas", []),
                "beneficios": extra.get("beneficios", []),
                "aplicaciones": extra.get("aplicaciones", []),
            })
        catalogo.append({"titulo": cat, "icono": si.ICONOS[si.ICONOS_CATEGORIA[i % len(si.ICONOS_CATEGORIA)]], "temas": temas})
    return catalogo


@app.route("/servicios")
def servicios_page():
    return render_template("servicios.html", c=CONFIG, catalogo=_catalogo())


@app.post("/api/contacto")
def contacto():
    if _usuario() is None:
        return jsonify(ok=False, sesion=True, error="Inicia sesión o crea tu cuenta para enviar tu mensaje."), 401
    if _limite("contacto", 5, 600):
        return jsonify(ok=False, error="Enviaste varios mensajes seguidos. Espera unos minutos o escríbenos por WhatsApp."), 429
    d = request.get_json(silent=True) or {}
    nombre = str(d.get("nombre", "")).strip()[:100]
    correo = str(d.get("correo", "")).strip()[:120]
    telefono = str(d.get("telefono", "")).strip()[:30]
    empresa = str(d.get("empresa", "")).strip()[:100]
    servicio = str(d.get("servicio", "")).strip()[:100]
    mensaje = str(d.get("mensaje", "")).strip()[:1500]
    acepto = str(d.get("acepto", "")).strip() != ""

    if len(nombre) < 2:
        return jsonify(ok=False, error="Escribe tu nombre completo."), 400
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        return jsonify(ok=False, error="Escribe un correo electrónico válido."), 400
    if not re.fullmatch(r"[+\d][\d\s-]{6,}", telefono):
        return jsonify(ok=False, error="Escribe un teléfono válido."), 400
    if len(mensaje) < 5:
        return jsonify(ok=False, error="Cuéntanos brevemente sobre tu proyecto."), 400
    if not acepto:
        return jsonify(ok=False, error="Debes aceptar las políticas de privacidad."), 400

    db = get_db()
    token = secrets.token_urlsafe(16)
    u = _usuario()
    cur = db.execute(
        "INSERT INTO mensajes(nombre, contacto, servicio, mensaje, telefono, empresa, token, usuario_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        (nombre, correo, servicio, mensaje, telefono, empresa, token, u["id"] if u else 0)
    )
    mid = cur.lastrowid
    # El mensaje del formulario es el primero de la conversación, seguido de una respuesta automática
    db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'cliente', ?)", (mid, mensaje))
    primer = nombre.split()[0]
    db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'auto', ?)", (
        mid,
        f"¡Hola, {primer}! Recibimos tu mensaje. Un asesor de {CONFIG['empresa']} se unirá a este chat "
        "en breve. Mientras tanto, puedes seguir escribiendo aquí.",
    ))
    db.commit()
    return jsonify(ok=True, token=token, nombre=primer)


def _conversacion(token):
    """Devuelve el id de la conversación para un token válido, o None."""
    if not token or len(token) > 64:
        return None
    f = get_db().execute("SELECT id, usuario_id FROM mensajes WHERE token=?", (token,)).fetchone()
    if f is None:
        return None
    if f["usuario_id"]:
        u = _usuario()
        if u is None or u["id"] != f["usuario_id"]:
            abort(make_response(jsonify(ok=False, sesion=True), 401))   # el chat es de otra cuenta o no hay sesión
    return f["id"]


def _cerrado(mid):
    return get_db().execute("SELECT cerrado FROM mensajes WHERE id=?", (mid,)).fetchone()["cerrado"]


@app.get("/api/chat/<token>")
def chat_leer(token):
    mid = _conversacion(token)
    if mid is None:
        return jsonify(ok=False, eliminado=True), 404   # el asesor borró la conversación
    desde = request.args.get("desde", 0, type=int)
    filas = get_db().execute(
        "SELECT id, de, texto, substr(creado, 12, 5) AS hora FROM chat WHERE mensaje_id=? AND id>? ORDER BY id",
        (mid, desde)
    ).fetchall()
    return jsonify(ok=True, mensajes=[dict(f) for f in filas], cerrado=_cerrado(mid))


@app.post("/api/chat/<token>")
def chat_enviar(token):
    mid = _conversacion(token)
    if mid is None:
        return jsonify(ok=False, eliminado=True), 404
    texto = str((request.get_json(silent=True) or {}).get("texto", "")).strip()[:1000]
    if not texto:
        return jsonify(ok=False, error="Escribe un mensaje."), 400
    if _limite("chat", 30, 60):
        return jsonify(ok=False, error="Vas muy rápido. Espera un momento."), 429
    db = get_db()
    if _cerrado(mid):
        return jsonify(ok=False, error="Este chat ya fue cerrado.", cerrado=True), 409
    # Límite sencillo contra abuso: máximo 200 mensajes por conversación
    if db.execute("SELECT COUNT(*) FROM chat WHERE mensaje_id=?", (mid,)).fetchone()[0] >= 200:
        return jsonify(ok=False, error="Esta conversación alcanzó su límite. Escríbenos por WhatsApp."), 429
    db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'cliente', ?)", (mid, texto))
    db.commit()
    return jsonify(ok=True)


@app.post("/api/chat/<token>/cerrar")
def chat_cerrar(token):
    mid = _conversacion(token)
    if mid is None:
        return jsonify(ok=False), 404
    db = get_db()
    if not _cerrado(mid):
        db.execute("UPDATE mensajes SET cerrado='cliente' WHERE id=?", (mid,))
        db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'auto', 'El cliente cerró el chat.')", (mid,))
        db.commit()
    return jsonify(ok=True)


def _usuario():
    """Usuario con sesión iniciada (o None)."""
    if "u" not in g:
        uid = session.get("uid")
        g.u = get_db().execute("SELECT id, nombre, correo, rol FROM usuarios WHERE id=?", (uid,)).fetchone() if uid else None
    return g.u


def _auth_ok():
    """Solo las cuentas del equipo (rol admin) entran al panel."""
    u = _usuario()
    return u is not None and u["rol"] == "admin"


def _denegar():
    """Sin permiso: las llamadas del panel (JSON) reciben 401; las páginas pasan por el login
    (o vuelven a la web si la cuenta es de un cliente)."""
    if request.path.endswith(("/json", "/enviar")) or request.path == "/admin/estado":
        return jsonify(ok=False, error="sesion"), 401
    if _usuario() is not None:
        return redirect(url_for("index"))
    return redirect(url_for("login"))


def _destino(u_rol):
    return url_for("consultas") if u_rol == "admin" else url_for("index") + "#contacto"


def _hay_usuarios():
    return get_db().execute("SELECT 1 FROM usuarios LIMIT 1").fetchone() is not None


# Freno contra adivinar claves: 5 intentos fallidos por IP cada 5 minutos
def _bloqueado():
    ahora = time.time()
    marcas = [t for t in _ventanas.get(("login", request.remote_addr or "?"), []) if ahora - t < 300]
    return len(marcas) >= 5


def _fallo():
    _ventanas.setdefault(("login", request.remote_addr or "?"), []).append(time.time())


_HASH_FALSO = generate_password_hash(secrets.token_hex(8))


def _entrar(uid):
    session.clear()
    session["uid"] = uid
    session.permanent = True


@app.route("/login", methods=["GET", "POST"])
def login():
    u = _usuario()
    if u:
        return redirect(_destino(u["rol"]))
    error, correo = "", ""
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()[:120]
        clave = request.form.get("clave", "")[:200]
        if _bloqueado():
            error = "Demasiados intentos. Espera unos minutos e inténtalo de nuevo."
        else:
            f = get_db().execute("SELECT * FROM usuarios WHERE LOWER(correo) = LOWER(?)", (correo,)).fetchone()
            # Siempre se calcula un hash (aunque el correo no exista) para no revelar si la cuenta existe por el tiempo
            hash_ref = f["clave"] if f else _HASH_FALSO
            if check_password_hash(hash_ref, clave) and f:
                _ventanas.pop(("login", request.remote_addr or "?"), None)
                _entrar(f["id"])
                return redirect(_destino(f["rol"]))
            _fallo()
            error = "Correo o contraseña incorrectos."
    return render_template("auth.html", c=CONFIG, modo="login", error=error, correo=correo)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    u = _usuario()
    if u:
        return redirect(_destino(u["rol"]))
    db = get_db()
    error, nombre, correo = "", "", ""
    if request.method == "POST" and _limite("registro", 5, 3600):
        error = "Se crearon varias cuentas desde tu conexión. Inténtalo más tarde."
    elif request.method == "POST":
        nombre = request.form.get("nombre", "").strip()[:100]
        correo = request.form.get("correo", "").strip().lower()[:120]
        clave = request.form.get("clave", "")[:200]
        clave2 = request.form.get("clave2", "")[:200]
        if len(nombre) < 2:
            error = "Escribe tu nombre."
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            error = "Escribe un correo válido."
        elif len(clave) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        elif clave != clave2:
            error = "Las contraseñas no coinciden."
        elif correo == ADMIN_CORREO:
            error = "Ese correo es de la administración del sitio. Usa otro correo para tu cuenta."
        elif db.execute("SELECT 1 FROM usuarios WHERE correo=?", (correo,)).fetchone():
            error = "Ya existe una cuenta con ese correo."
        else:
            cur = db.execute("INSERT INTO usuarios(nombre, correo, clave, rol) VALUES(?, ?, ?, 'cliente')",
                             (nombre, correo, generate_password_hash(clave)))
            db.commit()
            _entrar(cur.lastrowid)
            return redirect(_destino("cliente"))
    return render_template("auth.html", c=CONFIG, modo="registro", error=error, nombre=nombre, correo=correo)


@app.post("/logout")
def logout():
    u = _usuario()
    admin = bool(u and u["rol"] == "admin")
    session.clear()
    return redirect(url_for("login") if admin else url_for("index"))


@app.get("/api/mis-consultas")
def mis_consultas():
    """Consultas guardadas en la cuenta del cliente (con el token para retomar cada chat)."""
    u = _usuario()
    if not u:
        return jsonify(ok=False), 401
    filas = get_db().execute(
        "SELECT m.token, m.mensaje, m.servicio, m.cerrado, substr(m.creado, 1, 16) AS creado,"
        " (SELECT COUNT(*) FROM chat WHERE mensaje_id=m.id) AS n"
        " FROM mensajes m WHERE m.usuario_id=? AND m.token<>'' ORDER BY m.id DESC LIMIT 50", (u["id"],)
    ).fetchall()
    return jsonify(ok=True, consultas=[dict(f) for f in filas])


@app.route("/admin")
def admin():
    return redirect(url_for("consultas"))


@app.route("/admin/consultas")
def consultas():
    if not _auth_ok():
        return _denegar()
    db = get_db()
    filas = db.execute(
        "SELECT m.*, (SELECT COUNT(*) FROM chat WHERE mensaje_id=m.id) AS n_chat FROM mensajes m ORDER BY m.id DESC"
    ).fetchall()
    abierto = request.args.get("chat", type=int)
    conv, sel = [], None
    if abierto:
        sel = db.execute("SELECT * FROM mensajes WHERE id=?", (abierto,)).fetchone()
        conv = db.execute("SELECT * FROM chat WHERE mensaje_id=? ORDER BY id", (abierto,)).fetchall()
    return render_template("consultas.html", filas=filas, c=CONFIG, sel=sel, conv=conv, usuario=_usuario())


@app.get("/admin/estado")
def admin_estado():
    """Huella de la actividad: cambia cuando llega un mensaje nuevo o un cliente escribe en un chat."""
    if not _auth_ok():
        return _denegar()
    db = get_db()
    return jsonify(
        mensajes=db.execute("SELECT COALESCE(MAX(id),0) FROM mensajes").fetchone()[0],
        cliente=db.execute("SELECT COALESCE(MAX(id),0) FROM chat WHERE de='cliente'").fetchone()[0],
        total=db.execute("SELECT COUNT(*) FROM mensajes").fetchone()[0],
        chats=db.execute("SELECT COUNT(*) FROM chat").fetchone()[0],
    )


@app.get("/admin/chat/<int:mid>/json")
def admin_chat_json(mid):
    """Mensajes nuevos de una conversación (el panel lo consulta solo, sin recargar la página)."""
    if not _auth_ok():
        return _denegar()
    db = get_db()
    m = db.execute("SELECT cerrado FROM mensajes WHERE id=?", (mid,)).fetchone()
    if m is None:
        return jsonify(ok=False), 404
    desde = request.args.get("desde", 0, type=int)
    filas = db.execute("SELECT id, de, texto, creado FROM chat WHERE mensaje_id=? AND id>? ORDER BY id", (mid, desde)).fetchall()
    return jsonify(ok=True, mensajes=[dict(f) for f in filas], cerrado=m["cerrado"])


@app.post("/admin/chat/<int:mid>/enviar")
def admin_chat_enviar(mid):
    if not _auth_ok():
        return _denegar()
    db = get_db()
    m = db.execute("SELECT cerrado FROM mensajes WHERE id=?", (mid,)).fetchone()
    if m is None:
        return jsonify(ok=False), 404
    if m["cerrado"]:
        return jsonify(ok=False, error="Este chat ya fue cerrado.", cerrado=m["cerrado"]), 409
    texto = str((request.get_json(silent=True) or {}).get("texto", "")).strip()[:1000]
    if not texto:
        return jsonify(ok=False, error="Escribe un mensaje."), 400
    db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'agente', ?)", (mid, texto))
    db.commit()
    return jsonify(ok=True)


def _cerrar_chat(db, mid):
    """Cierra un chat (si está abierto) y avisa en la conversación. Devuelve True si lo cerró."""
    if db.execute("SELECT 1 FROM mensajes WHERE id=? AND cerrado='' AND token<>''", (mid,)).fetchone():
        db.execute("UPDATE mensajes SET cerrado='agente' WHERE id=?", (mid,))
        db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'auto', 'El asesor cerró el chat. ¡Gracias por escribirnos!')", (mid,))
        return True
    return False


@app.post("/admin/cerrar/<int:mid>")
def admin_cerrar(mid):
    if not _auth_ok():
        return _denegar()
    db = get_db()
    _cerrar_chat(db, mid)
    db.commit()
    if request.form.get("desde") == "lista":
        return redirect(url_for("consultas"))
    return redirect(url_for("consultas", chat=mid) + "#fin")


@app.post("/admin/cerrar-todos")
def admin_cerrar_todos():
    if not _auth_ok():
        return _denegar()
    db = get_db()
    for (mid,) in db.execute("SELECT id FROM mensajes WHERE cerrado='' AND token<>''").fetchall():
        _cerrar_chat(db, mid)
    db.commit()
    return redirect(url_for("consultas"))


@app.post("/admin/borrar/<int:mid>")
def admin_borrar(mid):
    """Elimina por completo un mensaje recibido y toda su conversación de chat."""
    if not _auth_ok():
        return _denegar()
    db = get_db()
    db.execute("DELETE FROM chat WHERE mensaje_id=?", (mid,))
    db.execute("DELETE FROM mensajes WHERE id=?", (mid,))
    db.commit()
    return redirect(url_for("consultas"))


@app.post("/admin/responder/<int:mid>")
def admin_responder(mid):
    if not _auth_ok():
        return _denegar()
    texto = request.form.get("texto", "").strip()[:1000]
    fila = get_db().execute("SELECT cerrado FROM mensajes WHERE id=?", (mid,)).fetchone()
    if fila is None:
        abort(404)
    if texto and not fila["cerrado"]:
        db = get_db()
        db.execute("INSERT INTO chat(mensaje_id, de, texto) VALUES(?, 'agente', ?)", (mid, texto))
        db.commit()
    return redirect(url_for("consultas", chat=mid) + "#fin")


# Se ejecuta al importar el módulo, así funciona con "gunicorn app:app" y con "gunicorn wsgi:app"
init_db()

if __name__ == "__main__":
    app.run(debug=DEBUG)
