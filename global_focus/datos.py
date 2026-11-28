"""Contenido fijo del sitio: datos de la empresa, servicios, empresas del grupo y equipo.
Para cambiar textos, teléfonos, redes o el equipo, edita SOLO este archivo.
"""

CONFIG = {
    "empresa": "Global Focus S.A.C.",
    "telefonos": ["960 389 151", "980 688 699"],
    # Enlace del botón "¡Hola, charlemos!" (abre WhatsApp con el mensaje ya escrito)
    "whatsapp_url": "https://api.whatsapp.com/send/?phone=51960389151&text=¡Hola%21+Vengo+de+su+sitio+web+y+quisiera+más+información&type=phone_number&app_absent=0",
    "correo": "mktpublicidadcorporativo@gmail.com",  # Reemplazar por el correo oficial
    "dir_linea1": "Jr. Carabaya 1128, Of. 216",     # Dirección corta para el pie de página
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
