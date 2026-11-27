# Global Focus S.A.C. – Marketing y Publicidad Corporativa

Web hecha con Python (Flask). La app está en la carpeta `global_focus/`.

## Probar en tu computadora
```bash
cd global_focus
pip install -r requirements.txt
# Windows (PowerShell):  $env:FLASK_DEBUG="1"; $env:ADMIN_CLAVE="una-clave-larga"; python app.py
FLASK_DEBUG=1 ADMIN_CLAVE="una-clave-larga" python app.py
```
Abre http://127.0.0.1:5000. `FLASK_DEBUG=1` es solo para tu computadora (nunca en Render).

## Publicar en Render (gratis, con base de datos PostgreSQL)
- **Root Directory:** `global_focus`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn wsgi:app --workers 1 --threads 4`
  (1 worker porque el límite de intentos se guarda en memoria)
- **Environment** (ver `global_focus/.env.example`):
  - `SECRET_KEY` – texto largo aleatorio (`python -c "import secrets; print(secrets.token_hex(32))"`)
  - `ADMIN_CORREO` – correo del administrador
  - `ADMIN_CLAVE` – clave del panel (12+ caracteres). Para cambiarla, cámbiala en Render y reinicia.
  - `DATABASE_URL` – cadena de conexión de PostgreSQL (ver abajo).

### Base de datos gratis que no se borra: Neon
La base de datos de Render gratis **vence a los 30 días**, así que se recomienda una base externa gratuita en [Neon](https://neon.com):
1. Crea una cuenta en neon.com (sin tarjeta) y un proyecto nuevo.
2. Copia la **Connection string** (empieza con `postgresql://...`).
3. En Render > Environment crea `DATABASE_URL` con ese texto y guarda. Render reinicia solo.
Las tablas se crean solas al iniciar. Los usuarios, consultas y chats ya NO se pierden al reiniciar o redeployar.
(Neon "duerme" la base tras 5 minutos sin uso; la primera consulta tarda un instante en despertarla.)

### Probar en tu computadora
Si NO defines `DATABASE_URL`, la app usa un archivo SQLite local (`global_focus.db`, solo para pruebas; no se sube a GitHub).

## Seguridad (qué NO subir a GitHub)
Claves, `.env`, `secret.key` y archivos `*.db` están en `.gitignore` (el archivo debe llamarse exactamente `.gitignore`, con el punto). Las tablas se crean solas al iniciar. Si `global_focus.db` ya está en GitHub, bórralo del repositorio.
Si alguna vez subiste una clave al repositorio, cámbiala: el historial de Git la conserva.

## Panel de administración
Una sola cuenta: la del correo `ADMIN_CORREO`. Entra por `/login` y se abre la sección "Consultas".
Ese correo no se puede registrar desde la web.

## Cómo editar el contenido
- Teléfonos, correo, redes, misión y visión: diccionario `CONFIG` al inicio de `app.py`.
- Servicios (título y descripción): lista `CATEGORIAS` en `app.py`. Objetivo, características, beneficios, aplicaciones e íconos: `servicios_info.py`.
- Equipo: lista `EQUIPO` en `app.py` (las líneas con `"", "", ""` son tarjetas vacías).
- Imágenes: `static/img/servicios/servicio-01.jpg … servicio-27.jpg`, `static/img/equipo/equipo-1.jpg …`, `static/img/proyectos/proyecto-1.jpg … proyecto-4.jpg`, `static/img/contacto.jpg`, `static/img/servicios-portada.jpg` (jpg, png o webp).
- Video del inicio: `static/video/equipo.mp4` (reemplázalo con otro del mismo nombre). Conviene que pese menos de ~4 MB:
  `ffmpeg -i equipo.mp4 -vf scale=-2:720 -c:v libx264 -crf 28 -preset slow -an -movflags +faststart equipo_ligero.mp4`

## Pendiente (no es código)
- Página de **política de privacidad**: el formulario pide aceptarla, pero aún no hay una página con el texto (revisar con el área legal; Ley 29733 de protección de datos personales).
- Textos `alt` en las imágenes (accesibilidad y SEO).
