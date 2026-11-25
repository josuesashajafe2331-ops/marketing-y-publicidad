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

## Publicar en Render
- **Root Directory:** `global_focus`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn wsgi:app --workers 1 --threads 4`
  (1 worker porque el límite de intentos y la base SQLite funcionan en un solo proceso)
- **Environment** (ver `global_focus/.env.example`):
  - `SECRET_KEY` – texto largo aleatorio (`python -c "import secrets; print(secrets.token_hex(32))"`)
  - `ADMIN_CORREO` – correo del administrador
  - `ADMIN_CLAVE` – clave del panel (12+ caracteres). Para cambiarla, cámbiala en Render y reinicia.
  - `DB_PATH` – ruta de la base en un **disco persistente** (p. ej. `/var/data/global_focus.db`).
    Sin disco persistente, Render borra usuarios, consultas y chats en cada deploy/reinicio.

## Seguridad (qué NO subir a GitHub)
Claves, `.env`, `secret.key` y archivos `*.db` están en `.gitignore`. La base de datos se crea sola al iniciar.
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
