"""Información ampliada de cada servicio (tercer nivel de la página de Servicios).

Para cambiar un texto, edita la entrada del servicio (la clave es el título exacto).
Cada servicio tiene: objetivo, características, beneficios y aplicaciones.
El título y la descripción principal siguen viniendo de CATEGORIAS en app.py.
"""

# Íconos (contenido SVG de 24x24, trazo). Se reutilizan por tema.
ICONOS = {
    "grafico":   '<path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 15l4-4 3 3 5-6"/><path d="M16 8h4v4"/>',
    "altavoz":   '<path d="M4 10v4a1 1 0 0 0 1 1h3l7 4V5L8 9H5a1 1 0 0 0-1 1z"/><path d="M18.5 8.5a5 5 0 0 1 0 7"/>',
    "imagen":    '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    "video":     '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9.5v5l4.5-2.5z"/>',
    "objetivo":  '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "etiqueta":  '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "lupa":      '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "balanza":   '<path d="M12 3v18M7 21h10M5 7h14"/><path d="m5 7-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "pluma":     '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "brujula":   '<circle cx="12" cy="12" r="10"/><path d="m16 8-2 6-6 2 2-6z"/>',
    "calendario": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "personas":  '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "tendencia": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "numeral":   '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    "mira":      '<circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/>',
    "clic":      '<path d="m9 9 5 12 1.8-5.2L21 14z"/><path d="M7.2 2.2 8 5.1M5.1 8l-2.9-.8M14 4.1 12 6M6 12l-1.9 2"/>',
    "monedas":   '<circle cx="8" cy="8" r="6"/><path d="M18.1 10.4A6 6 0 1 1 10.4 18"/><path d="M7 6h1v4"/>',
    "impresora": '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "regalo":    '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "tv":        '<rect x="2" y="7" width="20" height="15" rx="2"/><path d="m17 2-5 5-5-5"/>',
    "paleta":    '<circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.9 0 1.7-.8 1.7-1.7 0-.4-.2-.8-.5-1.1-.3-.3-.5-.7-.5-1.1 0-.9.8-1.7 1.7-1.7H16c3.3 0 6-2.7 6-6 0-4.9-4.5-8.4-10-8.4z"/>',
    "sello":     '<path d="M12 2l2.4 2.1 3.2-.2 1 3 2.7 1.8-1 3.1 1 3.1-2.7 1.8-1 3-3.2-.2L12 22l-2.4-2.1-3.2.2-1-3-2.7-1.8 1-3.1-1-3.1 2.7-1.8 1-3 3.2.2z"/><path d="m9 12 2 2 4-4"/>',
    "usuario":   '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "documento": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8"/>',
    "caja":      '<path d="m7.5 4.3 9 5.2"/><path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "tijeras":   '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
    "camara":    '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z"/><circle cx="12" cy="13" r="3"/>',
    "pantalla":  '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
}

# Íconos de las 4 categorías (en el mismo orden que CATEGORIAS)
ICONOS_CATEGORIA = ["grafico", "altavoz", "imagen", "video"]

# Ícono de cada servicio
ICONO_TEMA = {
    "Marketing": "objetivo", "Branding": "etiqueta", "Estudio de mercado": "lupa",
    "Análisis situacional del mercado": "balanza", "Creación de contenidos": "pluma",
    "Estrategia de contenidos": "brujula", "Grilla de contenidos": "calendario",
    "Community Manager": "personas", "Analíticas digitales": "tendencia",
    "SEO en redes sociales": "numeral", "Definición del target": "mira", "Ads (publicidad)": "clic",
    "Publicidad": "altavoz", "Presupuestos": "monedas", "Campañas impresas": "impresora",
    "Piezas gráficas": "imagen", "Merchandising": "regalo", "TV, radio y prensa": "tv",
    "Diseño digital gráfico": "paleta", "Identidad corporativa": "sello", "Marca personal": "usuario",
    "Papelería corporativa": "documento", "Packaging": "caja",
    "Edición": "tijeras", "Fotografía": "camara", "Audiovisuales": "video", "Diseño web": "pantalla",
}

INFO = {
    "Marketing": {
        "objetivo": "Atraer, convencer y fidelizar clientes alineando la oferta de la empresa con las necesidades reales del mercado.",
        "caracteristicas": ["Plan de marketing con metas medibles", "Combinación de canales digitales y tradicionales", "Seguimiento constante de resultados"],
        "beneficios": ["Mayor visibilidad de la marca", "Más oportunidades comerciales", "Decisiones basadas en datos"],
        "aplicaciones": ["Lanzamiento de un producto o servicio nuevo", "Plan anual de marketing para una empresa", "Campañas por temporada o fechas clave"]},
    "Branding": {
        "objetivo": "Construir una marca reconocible, coherente y diferente de la competencia.",
        "caracteristicas": ["Nombre, logotipo, colores y tipografías", "Personalidad, valores y tono de comunicación", "Manual de marca para un uso uniforme"],
        "beneficios": ["Reconocimiento inmediato", "Imagen profesional y confiable", "Diferenciación frente a la competencia"],
        "aplicaciones": ["Creación de la marca de un negocio nuevo", "Renovación de la imagen de una empresa establecida", "Unificación de la marca en todas las áreas"]},
    "Estudio de mercado": {
        "objetivo": "Conocer a los clientes, competidores y tendencias para identificar oportunidades antes de invertir.",
        "caracteristicas": ["Investigación de clientes y su comportamiento", "Revisión de la competencia y del sector", "Informe con hallazgos y recomendaciones"],
        "beneficios": ["Menor riesgo al invertir", "Oportunidades de negocio identificadas", "Mensajes ajustados al público"],
        "aplicaciones": ["Antes de abrir una nueva línea de servicio", "Evaluar la demanda de un producto", "Elegir segmentos o zonas donde enfocarse"]},
    "Análisis situacional del mercado": {
        "objetivo": "Ubicar la posición de la empresa frente a sus competidores en productos, servicios, precios y estrategias.",
        "caracteristicas": ["Comparación con competidores directos", "Revisión de precios, ofertas y comunicación", "Fortalezas, debilidades, oportunidades y amenazas"],
        "beneficios": ["Visión clara de la situación actual", "Detección de ventajas competitivas", "Base sólida para definir la estrategia"],
        "aplicaciones": ["Diagnóstico previo a un plan de marketing", "Revisión anual de la posición en el sector", "Ajuste de precios y propuesta de valor"]},
    "Creación de contenidos": {
        "objetivo": "Producir piezas útiles y atractivas que informen, promocionen y acerquen al público a la marca.",
        "caracteristicas": ["Artículos, imágenes, videos y textos", "Contenido adaptado a cada plataforma", "Mensajes alineados con la identidad de la marca"],
        "beneficios": ["Presencia constante y profesional", "Mayor interacción con la audiencia", "Confianza al compartir contenido de valor"],
        "aplicaciones": ["Publicaciones para redes sociales", "Artículos y notas para el sitio web", "Videos explicativos de los servicios"]},
    "Estrategia de contenidos": {
        "objetivo": "Definir qué contenido crear, a quién dirigirlo, dónde publicarlo y con qué frecuencia.",
        "caracteristicas": ["Objetivos y público definidos", "Temas, formatos y canales seleccionados", "Frecuencia y tono de comunicación"],
        "beneficios": ["Contenido con propósito, sin improvisar", "Mensajes coherentes en todos los canales", "Mejor uso del tiempo y del presupuesto"],
        "aplicaciones": ["Plan trimestral de contenidos", "Posicionamiento de un especialista o una área", "Orden de la comunicación de toda la empresa"]},
    "Grilla de contenidos": {
        "objetivo": "Organizar en un calendario las fechas, temas, formatos y plataformas de cada publicación.",
        "caracteristicas": ["Calendario mensual de publicaciones", "Temas y formatos asignados por fecha", "Seguimiento de lo publicado"],
        "beneficios": ["Orden y constancia", "Anticipación a las fechas importantes", "Trabajo más eficiente del equipo"],
        "aplicaciones": ["Calendario mensual para redes sociales", "Programación de campañas por temporada", "Coordinación entre diseño, redacción y publicación"]},
    "Community Manager": {
        "objetivo": "Administrar las redes sociales y cuidar la relación con los seguidores.",
        "caracteristicas": ["Gestión y publicación en redes", "Respuesta a consultas y comentarios", "Moderación de las interacciones"],
        "beneficios": ["Atención rápida y cercana", "Comunidad activa y fiel", "Imagen cuidada ante el público"],
        "aplicaciones": ["Atención de consultas por mensaje directo", "Gestión diaria de las redes de la empresa", "Manejo de comentarios durante una campaña"]},
    "Analíticas digitales": {
        "objetivo": "Medir con datos el tráfico, las interacciones y las conversiones para mejorar las estrategias digitales.",
        "caracteristicas": ["Seguimiento del tráfico web", "Medición de interacciones y conversiones", "Informes periódicos de resultados"],
        "beneficios": ["Saber qué funciona y qué no", "Optimización de la inversión", "Decisiones respaldadas por datos"],
        "aplicaciones": ["Informe mensual de resultados", "Evaluación del rendimiento de una campaña", "Análisis del comportamiento en el sitio web"]},
    "SEO en redes sociales": {
        "objetivo": "Optimizar perfiles y publicaciones para que se encuentren con facilidad en las búsquedas de cada plataforma.",
        "caracteristicas": ["Perfiles optimizados con palabras clave", "Descripciones, etiquetas y nombres de búsqueda", "Adaptación a Instagram, TikTok, YouTube, Facebook y LinkedIn"],
        "beneficios": ["Más visibilidad sin depender solo de anuncios", "Llegada a quienes buscan lo que ofreces", "Perfiles más profesionales"],
        "aplicaciones": ["Optimización del perfil de una empresa", "Publicaciones pensadas para ser encontradas", "Posicionamiento en las búsquedas de cada plataforma"]},
    "Definición del target": {
        "objetivo": "Identificar al público objetivo para dirigir las campañas a las personas correctas.",
        "caracteristicas": ["Perfil según características e intereses", "Necesidades y comportamientos del público", "Segmentación para cada campaña"],
        "beneficios": ["Mensajes que conectan mejor", "Menos gasto en audiencias poco relevantes", "Campañas más efectivas"],
        "aplicaciones": ["Definir al cliente ideal antes de una campaña", "Segmentar anuncios por edad, zona o interés", "Ajustar el tono de comunicación"]},
    "Ads (publicidad)": {
        "objetivo": "Aumentar la visibilidad, atraer clientes potenciales y generar ventas con anuncios pagados.",
        "caracteristicas": ["Anuncios en Google Ads, Facebook Ads e Instagram Ads", "Segmentación del público y del presupuesto", "Optimización y seguimiento de resultados"],
        "beneficios": ["Resultados rápidos y medibles", "Control del presupuesto", "Alcance a un público específico"],
        "aplicaciones": ["Campaña para captar clientes potenciales", "Promoción de un servicio o de un evento", "Publicidad para impulsar ventas en fechas clave"]},
    "Publicidad": {
        "objetivo": "Captar la atención y motivar al público a comprar o participar con mensajes creativos y persuasivos.",
        "caracteristicas": ["Mensaje creativo y persuasivo", "Piezas para distintos medios", "Coherencia con la identidad de la marca"],
        "beneficios": ["Mayor recordación de la marca", "Interés y confianza del público", "Impulso a las ventas"],
        "aplicaciones": ["Campaña de lanzamiento", "Promociones y ofertas especiales", "Comunicación de un evento o de una causa"]},
    "Presupuestos": {
        "objetivo": "Planificar el dinero disponible para marketing y publicidad y distribuirlo con eficiencia.",
        "caracteristicas": ["Presupuesto por actividad y por canal", "Control de gastos", "Proyección de resultados"],
        "beneficios": ["Gasto ordenado y transparente", "Mejor retorno de la inversión", "Decisiones con información clara"],
        "aplicaciones": ["Presupuesto anual de marketing", "Costo de una campaña específica", "Comparación de alternativas antes de contratar"]},
    "Campañas impresas": {
        "objetivo": "Promocionar productos, servicios o eventos con materiales físicos que llegan de forma directa al público.",
        "caracteristicas": ["Volantes, folletos, afiches y revistas", "Diseño listo para imprimir", "Distribución en puntos estratégicos"],
        "beneficios": ["Presencia tangible de la marca", "Llegada directa a la zona deseada", "Complemento de la publicidad digital"],
        "aplicaciones": ["Volantes para una promoción local", "Folletos de servicios para ferias", "Afiches para eventos"]},
    "Piezas gráficas": {
        "objetivo": "Comunicar mensajes y reforzar la identidad de la marca con materiales visuales.",
        "caracteristicas": ["Logotipos, carteles, banners e infografías", "Diseño acorde a la identidad de la marca", "Formatos para medios digitales e impresos"],
        "beneficios": ["Imagen profesional y uniforme", "Mensajes claros y atractivos", "Material listo para usar"],
        "aplicaciones": ["Banners para redes sociales y web", "Infografías informativas", "Carteles de promociones"]},
    "Merchandising": {
        "objetivo": "Promocionar la marca, aumentar su reconocimiento, fidelizar clientes y fortalecer la imagen corporativa.",
        "caracteristicas": ["Diseño y personalización con la identidad de la empresa", "Lapiceros, tazas, polos, llaveros, agendas, folders y banners", "Producción y distribución de los artículos"],
        "beneficios": ["Recordación constante de la marca", "Clientes y colaboradores más fieles", "Imagen corporativa más sólida"],
        "aplicaciones": ["Kits de bienvenida para clientes", "Regalos corporativos de fin de año", "Material para ferias, eventos y capacitaciones"]},
    "TV, radio y prensa": {
        "objetivo": "Llegar a una audiencia amplia mediante los medios tradicionales de publicidad.",
        "caracteristicas": ["Anuncios audiovisuales en televisión", "Anuncios de audio en radio", "Avisos en periódicos y revistas"],
        "beneficios": ["Gran alcance", "Credibilidad de medios conocidos", "Refuerzo de las campañas digitales"],
        "aplicaciones": ["Spot para una campaña institucional", "Cuñas radiales promocionales", "Avisos en prensa para un evento"]},
    "Diseño digital gráfico": {
        "objetivo": "Comunicar mensajes con imágenes, colores, tipografías y composiciones atractivas.",
        "caracteristicas": ["Creación de elementos visuales", "Composición para medios digitales e impresos", "Estilo coherente con la marca"],
        "beneficios": ["Mensajes más claros y llamativos", "Imagen cuidada y profesional", "Material adaptable a varios formatos"],
        "aplicaciones": ["Diseños para publicaciones", "Presentaciones corporativas", "Material gráfico para campañas"]},
    "Identidad corporativa": {
        "objetivo": "Representar a la empresa con un conjunto visual y conceptual que la diferencie y transmita confianza.",
        "caracteristicas": ["Logotipo, colores y tipografía", "Valores y misión de la empresa", "Aplicación en todos los materiales"],
        "beneficios": ["Diferenciación clara", "Confianza y solidez", "Imagen uniforme en cada contacto"],
        "aplicaciones": ["Identidad de una empresa nueva", "Actualización de una imagen desfasada", "Uniformidad en documentos, redes y señalética"]},
    "Marca personal": {
        "objetivo": "Construir una identidad profesional propia que destaque habilidades, experiencia, valores y reputación.",
        "caracteristicas": ["Definición de la propuesta de valor personal", "Imagen y mensajes coherentes", "Presencia en redes y medios profesionales"],
        "beneficios": ["Reconocimiento como especialista", "Más oportunidades profesionales", "Reputación sólida"],
        "aplicaciones": ["Posicionamiento de un profesional independiente", "Imagen de gerentes y directivos", "Presentación de un especialista en su rubro"]},
    "Papelería corporativa": {
        "objetivo": "Mantener una imagen empresarial uniforme y profesional en los materiales impresos.",
        "caracteristicas": ["Tarjetas de presentación y hojas membretadas", "Sobres, carpetas y folletos", "Diseño alineado a la identidad corporativa"],
        "beneficios": ["Imagen profesional en cada documento", "Unidad visual", "Mayor confianza del cliente"],
        "aplicaciones": ["Papelería para una empresa nueva", "Carpetas para presentar propuestas", "Tarjetas para el equipo comercial"]},
    "Packaging": {
        "objetivo": "Proteger el producto, informar y atraer al consumidor con un empaque que diferencie la marca.",
        "caracteristicas": ["Diseño de envases y empaques", "Información clara del producto", "Materiales y formatos adecuados"],
        "beneficios": ["Producto más atractivo en el punto de venta", "Protección del contenido", "Marca más recordada"],
        "aplicaciones": ["Empaque de un producto nuevo", "Rediseño de etiquetas", "Cajas y bolsas para regalos corporativos"]},
    "Edición": {
        "objetivo": "Revisar, corregir y mejorar textos, fotografías, videos y audios para obtener contenidos claros y profesionales.",
        "caracteristicas": ["Corrección de textos", "Retoque de fotografías", "Montaje de videos y audios"],
        "beneficios": ["Contenido pulido y coherente", "Mensajes claros", "Imagen más profesional"],
        "aplicaciones": ["Edición de videos para redes", "Retoque de fotos de productos", "Revisión de textos antes de publicar"]},
    "Fotografía": {
        "objetivo": "Crear y seleccionar imágenes que comuniquen mensajes, capten la atención y mejoren la presentación de la marca.",
        "caracteristicas": ["Fotografía de productos, personas y eventos", "Selección y retoque de imágenes", "Estilo visual alineado a la marca"],
        "beneficios": ["Imagen más atractiva", "Material propio de la empresa", "Mayor impacto visual"],
        "aplicaciones": ["Fotos de productos para un catálogo", "Retratos del equipo", "Cobertura de eventos"]},
    "Audiovisuales": {
        "objetivo": "Comunicar información y promocionar servicios combinando imágenes, video, gráficos y sonido.",
        "caracteristicas": ["Anuncios y videos promocionales", "Presentaciones audiovisuales", "Gráficos y sonido integrados"],
        "beneficios": ["Mensajes más memorables", "Mayor retención de la información", "Contenido para varias plataformas"],
        "aplicaciones": ["Video institucional", "Anuncio para redes sociales", "Presentación para una reunión o un evento"]},
    "Diseño web": {
        "objetivo": "Ofrecer una experiencia positiva al usuario con un sitio web claro, atractivo y funcional.",
        "caracteristicas": ["Apariencia y organización del sitio", "Navegación sencilla", "Funcionalidad y adaptación a celulares"],
        "beneficios": ["Presencia profesional en internet", "Más clientes potenciales", "Información siempre disponible"],
        "aplicaciones": ["Sitio web institucional", "Página para una campaña específica", "Catálogo de servicios en línea"]},
}
