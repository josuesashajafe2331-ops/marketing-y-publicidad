(() => {
  const anio = document.getElementById('anio'); if (anio) anio.textContent = new Date().getFullYear();

  // Cabecera más compacta al bajar.
  const top = document.getElementById('top');
  const onScroll = () => top.classList.toggle('sc', scrollY > 40);
  addEventListener('scroll', onScroll, {passive: true}); onScroll();

  // Los bloques aparecen al entrar en pantalla.
  const items = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); }
    }), {threshold: .15});
    items.forEach(el => io.observe(el));
  } else items.forEach(el => el.classList.add('vis'));

  // "Consultar por..." deja un mensaje inicial en el formulario.
  document.querySelectorAll('[data-servicio]').forEach(a => a.addEventListener('click', () => {
    const msg = document.querySelector('textarea[name=mensaje]');
    if (msg && !msg.value) msg.value = 'Hola, quiero información de marketing para ' + a.dataset.servicio + '.';
  }));

  // Llegar desde "Conocer servicios..." (?consulta=Empresa) deja el mensaje listo.
  const consulta = new URLSearchParams(location.search).get('consulta');
  const msg0 = document.querySelector('textarea[name=mensaje]');
  if (consulta && msg0 && !msg0.value) msg0.value = 'Hola, quiero información de marketing para ' + consulta + '.';

  // Video del inicio: en bucle y sin sonido; reintenta si el navegador lo pausa.
  const vid = document.querySelector('.hero2-video video');
  if (vid) { vid.muted = true; const p = vid.play(); if (p && p.catch) p.catch(() => {}); }

  // Círculo "Nuestros servicios": se expande y entra a la otra página.
  const circ = document.getElementById('irServicios');
  const trans = document.getElementById('trans');
  if (circ && trans && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    circ.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      const r = circ.getBoundingClientRect();
      trans.style.left = (r.left + r.width / 2) + 'px';
      trans.style.top = (r.top + r.height / 2) + 'px';
      trans.classList.add('go');
      setTimeout(() => { location.href = circ.href; }, 600);
    });
  }

  // Servicios: navegación por niveles (tarjetas -> temas -> información del tema).
  const dataEl = document.getElementById('sv-data');
  if (dataEl) {
    const cats = JSON.parse(dataEl.textContent);
    const modal = document.getElementById('svm');
    const cuerpo = document.getElementById('svm-cuerpo');
    const volver = document.getElementById('svm-volver');
    const ruta = document.getElementById('svm-ruta');
    const equis = document.getElementById('svm-x');
    const reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let ci = -1, ti = -1, origen = null, cerrando = null;

    const esc = s => String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
    const ico = (p, cl) => '<svg class="' + cl + '" viewBox="0 0 24 24" aria-hidden="true">' + p + '</svg>';
    const lis = a => '<ul>' + a.map(x => '<li>' + esc(x) + '</li>').join('') + '</ul>';
    const bloque = (t, html) => html ? '<section class="svm-bloque"><h4>' + t + '</h4>' + html + '</section>' : '';

    // Muestra una vista en la ventana (con animación) y actualiza ruta y botón "Volver".
    function pintar(html, atras, texto, conVolver) {
      cuerpo.innerHTML = '<div class="svm-vista' + (atras ? ' atras' : '') + '">' + html + '</div>';
      cuerpo.scrollTop = 0;
      ruta.textContent = texto;
      volver.hidden = !conVolver;
      const h = cuerpo.querySelector('#svm-titulo');
      if (h) h.focus({preventScroll: true});
    }

    // SEGUNDO NIVEL: todos los temas de una categoría.
    function verTemas(i, atras) {
      const c = cats[i]; ci = i; ti = -1;
      const tarjetas = c.temas.map((t, j) =>
        '<button class="svm-tema" type="button" data-j="' + j + '">' +
          '<span class="svm-ibox">' + ico(t.icono, 'svm-ic') + '</span>' +
          '<span class="svm-tt">' + esc(t.titulo) + '</span>' +
          '<span class="svm-td">' + esc(t.descripcion) + '</span>' +
          '<span class="svm-ver">Ver información <i aria-hidden="true">→</i></span>' +
        '</button>').join('');
      pintar(
        '<div class="svm-cab"><span class="svm-ibox grande">' + ico(c.icono, 'svm-ic') + '</span>' +
        '<div><p class="svm-peq">Servicio ' + (i + 1) + ' de ' + cats.length + '</p>' +
        '<h3 id="svm-titulo" tabindex="-1">' + esc(c.titulo) + '</h3>' +
        '<p class="svm-sub">' + c.temas.length + ' temas. Elige uno para conocer su información.</p></div></div>' +
        '<div class="svm-temas">' + tarjetas + '</div>',
        atras, 'Servicios  /  ' + c.titulo, false);
    }

    // TERCER NIVEL: información completa de un tema.
    function verTema(i, j, atras) {
      const c = cats[i], t = c.temas[j]; ci = i; ti = j;
      const ant = c.temas[j - 1], sig = c.temas[j + 1];
      pintar(
        '<div class="svm-cab det"><span class="svm-ibox grande">' + ico(t.icono, 'svm-ic') + '</span>' +
        '<div><p class="svm-peq">' + esc(c.titulo) + '</p><h3 id="svm-titulo" tabindex="-1">' + esc(t.titulo) + '</h3></div></div>' +
        '<p class="svm-desc">' + esc(t.descripcion) + '</p>' +
        '<div class="svm-info">' +
          bloque('Objetivo', t.objetivo ? '<p>' + esc(t.objetivo) + '</p>' : '') +
          bloque('Características principales', t.caracteristicas.length ? lis(t.caracteristicas) : '') +
          bloque('Beneficios', t.beneficios.length ? lis(t.beneficios) : '') +
          bloque('Aplicaciones y ejemplos empresariales', t.aplicaciones.length ? lis(t.aplicaciones) : '') +
        '</div>' +
        '<div class="svm-pie">' +
          '<div class="svm-nav">' +
            (ant ? '<button type="button" class="svm-btn" data-ir="' + (j - 1) + '"><span aria-hidden="true">←</span> ' + esc(ant.titulo) + '</button>' : '') +
            (sig ? '<button type="button" class="svm-btn" data-ir="' + (j + 1) + '">' + esc(sig.titulo) + ' <span aria-hidden="true">→</span></button>' : '') +
          '</div>' +
          '<a class="svm-pedir" href="/?consulta=' + encodeURIComponent(t.titulo) + '#contacto">Solicitar información</a>' +
        '</div>',
        atras, 'Servicios  /  ' + c.titulo + '  /  ' + t.titulo, true);
    }

    function abrir(i, desde) {
      clearTimeout(cerrando);
      origen = desde || null;
      verTemas(i, false);
      modal.classList.add('abierto');
      modal.setAttribute('aria-hidden', 'false');
      document.documentElement.classList.add('svm-bloq');
      history.replaceState(null, '', '#cat' + (i + 1));
    }

    function cerrar() {
      if (!modal.classList.contains('abierto')) return;
      modal.classList.remove('abierto');
      modal.setAttribute('aria-hidden', 'true');
      document.documentElement.classList.remove('svm-bloq');
      history.replaceState(null, '', location.pathname + location.search);
      cerrando = setTimeout(() => { cuerpo.innerHTML = ''; }, reducido ? 0 : 350);
      if (origen) origen.focus({preventScroll: true});
    }

    document.querySelectorAll('.sv-tab').forEach(b => b.addEventListener('click', () => abrir(+b.dataset.i, b)));
    cuerpo.addEventListener('click', e => {
      const tema = e.target.closest('.svm-tema');
      if (tema) return verTema(ci, +tema.dataset.j, false);
      const ir = e.target.closest('[data-ir]');
      if (ir) verTema(ci, +ir.dataset.ir, false);
    });
    volver.addEventListener('click', () => verTemas(ci, true));
    equis.addEventListener('click', cerrar);
    modal.addEventListener('mousedown', e => { if (e.target === modal) cerrar(); });

    // ESC cierra; Tab se mantiene dentro de la ventana.
    document.addEventListener('keydown', e => {
      if (!modal.classList.contains('abierto')) return;
      if (e.key === 'Escape') { e.preventDefault(); cerrar(); return; }
      if (e.key !== 'Tab') return;
      const f = [...modal.querySelectorAll('button:not([hidden]), a[href], [tabindex="-1"]#svm-titulo')].filter(x => x.offsetParent !== null);
      if (!f.length) return;
      const primero = f[0], ultimo = f[f.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    });

    // Enlaces directos: servicios#cat1 ... #cat4 abren esa categoría (al cargar y al hacer clic en un enlace del pie).
    const porHash = () => {
      const h = location.hash.match(/^#cat([1-9])$/);
      if (h && cats[h[1] - 1]) abrir(h[1] - 1, document.querySelector('.sv-tab[data-i="' + (h[1] - 1) + '"]'));
    };
    porHash();
    addEventListener('hashchange', porHash);
  }

  const form = document.getElementById('form');
  const estado = document.getElementById('estado');
  if (!form) return;
  const show = (t, cls) => { estado.textContent = t; estado.className = cls; };
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('button');
    btn.disabled = true; show('Enviando...', '');
    try {
      const r = await fetch('/api/contacto', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(Object.fromEntries(new FormData(form)))
      });
      const d = await r.json().catch(() => null);      // si el servidor devolvió HTML (error), d queda en null
      if (r.status === 401 && d && d.sesion) { show(d.error, 'err'); setTimeout(() => location.reload(), 1800); btn.disabled = false; return; }
      if (d && d.ok && d.token) { form.reset(); show('', ''); abrirChat(d.token); }
      else show((d && d.error) || 'El servidor no pudo guardar tu consulta (error ' + r.status + '). Inténtalo de nuevo.', 'err');
    } catch { show('Sin conexión. Revisa tu internet e inténtalo de nuevo.', 'err'); }
    btn.disabled = false;
  });

  // ---- Chat que aparece después de enviar el formulario ----
  const chat = document.getElementById('chat');
  const log = document.getElementById('cc-log');
  const cform = document.getElementById('cc-form');
  const ctxt = document.getElementById('cc-txt');
  const rapidas = document.getElementById('cc-rapidas');
  let token = null, ultimo = 0, timer = null, vistos = new Set();

  function burbuja(m) {
    if (vistos.has(m.id)) return;
    vistos.add(m.id);
    const b = document.createElement('div');
    b.className = 'cc-m ' + (m.de === 'cliente' ? 'yo' : 'ellos');
    const t = document.createElement('p'); t.textContent = m.texto;
    const h = document.createElement('small');
    h.textContent = (m.de === 'agente' ? 'Asesor · ' : m.de === 'auto' ? 'Global Focus · ' : '') + m.hora;
    b.append(t, h);
    log.appendChild(b);
    ultimo = Math.max(ultimo, m.id);
  }

  async function traer() {
    if (!token) return;
    try {
      const r = await fetch('/api/chat/' + token + '?desde=' + ultimo);
      if (r.status === 404) return eliminado();
      if (r.status === 401) { try { sessionStorage.removeItem('gf_chat'); } catch {} return location.reload(); }
      if (!r.ok) return;
      const d = await r.json();
      if (d.cerrado) marcarCerrado(d.cerrado);
      if (d.mensajes && d.mensajes.length) {
        const abajo = log.scrollHeight - log.scrollTop - log.clientHeight < 60;
        d.mensajes.forEach(burbuja);
        if (abajo) log.scrollTop = log.scrollHeight;
      }
    } catch {}
  }

  const mis = document.getElementById('mis');           // solo existe si hay una cuenta de cliente
  const misLista = document.getElementById('mis-lista');
  const atras = document.getElementById('cc-atras');
  // Muestra una sola de las tres vistas de la tarjeta: formulario, chat o lista de consultas guardadas.
  function vista(v) {
    form.hidden = v !== 'form'; chat.hidden = v !== 'chat'; if (mis) mis.hidden = v !== 'mis';
  }
  const fecha = s => { const [d, h] = s.split(' '), [y, m, dd] = d.split('-'); return dd + '/' + m + '/' + y + ' ' + h; };
  async function verMis() {
    if (!mis) return;
    clearInterval(timer); token = null;
    vista('mis');
    misLista.textContent = 'Cargando…';
    try {
      const r = await fetch('/api/mis-consultas', {cache: 'no-store'});
      if (!r.ok) throw 0;
      const d = await r.json();
      misLista.textContent = '';
      if (!d.consultas.length) { const p = document.createElement('p'); p.className = 'mis-vacia'; p.textContent = 'Aún no tienes consultas. Cuando envíes una, aparecerá aquí con su chat.'; misLista.appendChild(p); }
      d.consultas.forEach(c => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'mis-item'; b.setAttribute('role', 'listitem');
        const t = document.createElement('span'); t.className = 'mis-t'; t.textContent = c.mensaje;
        const m = document.createElement('small'); m.textContent = fecha(c.creado) + (c.servicio ? ' · ' + c.servicio : '');
        const e = document.createElement('i'); e.className = c.cerrado ? 'cerrada' : 'abierta'; e.textContent = c.cerrado ? 'Cerrada' : 'Abierta';
        b.append(t, m, e); b.addEventListener('click', () => abrirChat(c.token)); misLista.appendChild(b);
      });
    } catch { misLista.textContent = 'No se pudieron cargar tus consultas. Inténtalo de nuevo.'; }
  }

  const cerrarBtn = document.getElementById('cc-cerrar');
  const est = document.getElementById('cc-est');

  // Chat cerrado (por el cliente o por el asesor): ya no se puede escribir; el botón pasa a "Nueva consulta".
  function marcarCerrado(quien) {
    clearInterval(timer);
    ctxt.disabled = true; cform.querySelector('button').disabled = true; rapidas.hidden = true;
    ctxt.placeholder = 'Este chat está cerrado';
    est.textContent = quien === 'agente' ? 'Chat cerrado por el asesor' : 'Chat cerrado';
    cerrarBtn.textContent = 'Nueva consulta'; cerrarBtn.dataset.fin = '1';
  }

  // El asesor borró la conversación: se vuelve a la pantalla de inicio (formulario) con un aviso.
  const AVISO_BORRADO = 'El asesor eliminó tu chat. Vuelve a completar tus datos para iniciar una nueva consulta.';
  function eliminado() {
    if (!token) return;
    volverAlInicio();
    show(AVISO_BORRADO, 'err');
  }

  // Vuelve al formulario inicial.
  function volverAlInicio() {
    clearInterval(timer); token = null;
    try { sessionStorage.removeItem('gf_chat'); } catch {}
    vista('form'); show('', '');
    ctxt.disabled = false; ctxt.value = ''; ctxt.placeholder = 'Escribe tu mensaje…';
    cform.querySelector('button').disabled = false; rapidas.hidden = false;
    cerrarBtn.textContent = 'Cerrar chat'; delete cerrarBtn.dataset.fin;
    est.textContent = 'Tu mensaje fue enviado · conversemos';
    form.querySelector('input').focus({preventScroll: true});
  }

  async function abrirChat(t) {
    token = t; ultimo = 0; vistos = new Set(); log.innerHTML = '';
    ctxt.disabled = false; cform.querySelector('button').disabled = false; rapidas.hidden = false;
    ctxt.placeholder = 'Escribe tu mensaje…'; cerrarBtn.textContent = 'Cerrar chat'; delete cerrarBtn.dataset.fin;
    est.textContent = 'Tu mensaje fue enviado · conversemos';
    try { sessionStorage.setItem('gf_chat', t); } catch {}
    vista('chat');
    await traer();
    log.scrollTop = log.scrollHeight;
    clearInterval(timer);
    timer = setInterval(() => { if (!document.hidden) traer(); }, 2000);
    ctxt.focus({preventScroll: true});
  }

  async function mandar(texto) {
    texto = texto.trim();
    if (!texto || !token) return;
    ctxt.value = ''; rapidas.hidden = true;
    try {
      const r = await fetch('/api/chat/' + token, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({texto})
      });
      if (!r.ok) { const d = await r.json().catch(() => ({})); if (r.status === 404) eliminado(); else if (r.status === 401) location.reload(); else if (d.cerrado) { await traer(); } else alert(d.error || 'No se pudo enviar.'); return; }
      await traer(); log.scrollTop = log.scrollHeight;
    } catch { alert('Sin conexión. Inténtalo de nuevo.'); }
  }

  if (chat) {
    document.addEventListener('visibilitychange', () => { if (!document.hidden && token) traer(); });
    cform.addEventListener('submit', e => { e.preventDefault(); mandar(ctxt.value); });
    if (atras) atras.addEventListener('click', verMis);
    const verMisBtn = document.getElementById('ver-mis'); if (verMisBtn) verMisBtn.addEventListener('click', verMis);
    const nuevaBtn = document.getElementById('mis-nueva'); if (nuevaBtn) nuevaBtn.addEventListener('click', volverAlInicio);
    if (mis && new URLSearchParams(location.search).get('mis')) verMis();
    cerrarBtn.addEventListener('click', async () => {
      if (cerrarBtn.dataset.fin) return volverAlInicio();
      if (token) { try { await fetch('/api/chat/' + token + '/cerrar', {method: 'POST'}); } catch {} }
      volverAlInicio();
    });
    rapidas.addEventListener('click', e => { const b = e.target.closest('[data-q]'); if (b) mandar(b.dataset.q); });
    // Si recarga la página, retoma la conversación
    try { const t = sessionStorage.getItem('gf_chat'); if (t && !(mis && new URLSearchParams(location.search).get('mis'))) fetch('/api/chat/' + t + '?desde=0').then(r => { if (r.ok) abrirChat(t); else if (r.status === 404) { sessionStorage.removeItem('gf_chat'); show(AVISO_BORRADO, 'err'); } else if (r.status === 401) sessionStorage.removeItem('gf_chat'); }); } catch {}
  }
})();

// Menú de la cuenta (encabezado): se cierra al hacer clic fuera.
document.addEventListener('click', e => {
  const m = document.getElementById('cuenta-menu');
  if (m && m.open && !m.contains(e.target)) m.open = false;
});

// Al cerrar sesión, esta pestaña olvida el chat que tenía abierto (no queda a la vista de quien use el equipo después).
document.querySelectorAll('.cuenta-menu form').forEach(f => f.addEventListener('submit', () => {
  try { sessionStorage.removeItem('gf_chat'); } catch {}
}));
