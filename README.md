# API REST de marcadores deportivos

Proyecto Django con un sitio web por roles y una API REST (Django REST Framework + JWT) para publicar los resultados de una liga deportiva: ligas, equipos, jugadores, partidos, marcadores y tabla de posiciones. Incluye un front externo (HTML + CSS + JS) que consume la API.

## Tecnologías

- Python 3.12 o superior
- Django
- Django REST Framework
- djangorestframework-simplejwt (autenticación JWT)
- django-cors-headers (CORS)
- SQLite

## Estructura del repositorio

```
marcador/                 <- carpeta del proyecto (aquí está manage.py)
├── manage.py
├── requirements.txt
├── SEGURIDAD.md          <- recomendaciones de seguridad y dónde se aplicaron
├── marcador/             <- configuración (settings.py, urls.py)
├── torneo/               <- app: modelos, sitio HTML, API, permisos
└── front_externo/        <- front HTML/CSS/JS que consume la API
```

## Instalación

Desde la raíz del repositorio:

```bash
cd marcador
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py poblar          # crea datos de ejemplo y usuarios de prueba
python manage.py runserver
```

El servidor queda en http://127.0.0.1:8000/

Cada vez que abras una terminal nueva, vuelve a activar el entorno virtual con `source .venv/bin/activate`.

## Usuarios de prueba

`python manage.py poblar` crea estos usuarios (clave: `Clave12345`). Son solo para demostración.

| Usuario | Rol | Qué puede hacer |
|---|---|---|
| (sin sesión) | Público | Solo ver partidos, tablas y planteles |
| `lector1` | Lector | Igual que el público |
| `planillero1` | Planillero | Además, actualizar el marcador de un partido |
| `admin1` | Administrador | CRUD completo en el sitio y en la API |

Para entrar al panel `/admin/` de Django crea un superusuario:

```bash
python manage.py createsuperuser
```

## Sitio web

| Ruta | Descripción |
|---|---|
| `/partidos/` | Lista de partidos (pública) |
| `/partidos/<id>/` | Detalle de un partido |
| `/partidos/nuevo/` | Crear partido (administrador) |
| `/partidos/<id>/editar/` | Editar partido (administrador) |
| `/partidos/<id>/borrar/` | Borrar partido (administrador) |
| `/partidos/<id>/marcador/` | Actualizar marcador (planillero o administrador) |
| `/accounts/login/` | Iniciar sesión |
| `/admin/` | Panel de administración de Django |

Sin sesión, las rutas protegidas redirigen al login. Con sesión pero sin el rol necesario, responden 403.

## API REST

Base: `http://127.0.0.1:8000/api/`

| Método | Ruta | Quién | Descripción |
|---|---|---|---|
| POST | `/api/token/` | todos | Obtiene `access` y `refresh` con `username` y `password` |
| POST | `/api/token/refresh/` | todos | Renueva el token de acceso |
| GET | `/api/me/` | con token | Devuelve `id`, `username` y `rol` |
| GET | `/api/ligas/` | todos | Lista de ligas |
| GET | `/api/ligas/<id>/tabla/` | todos | Tabla de posiciones (3 pts victoria, 1 empate) |
| GET | `/api/equipos/?liga=<id>` | todos | Equipos, filtrables por liga |
| GET | `/api/jugadores/?equipo=<id>` | todos | Jugadores, filtrables por equipo |
| GET | `/api/partidos/?liga=<id>&estado=<estado>` | todos | Partidos, filtrables por liga y estado |
| PATCH | `/api/partidos/<id>/` | planillero, administrador | Actualiza `goles_local`, `goles_visita` y `estado` |
| POST, PUT, PATCH, DELETE | `/api/{ligas,equipos,jugadores,partidos}/` | administrador | CRUD completo |

Permisos por rol: el anónimo solo lee (escribir devuelve 401); el planillero solo puede hacer PATCH de los tres campos del marcador (cualquier otra cosa devuelve 403); el administrador puede todo.

### Ejemplo de uso

```bash
# 1. Obtener un token
curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"planillero1","password":"Clave12345"}'

# 2. Consultar el rol con el token (reemplaza <ACCESS>)
curl -s http://127.0.0.1:8000/api/me/ -H "Authorization: Bearer <ACCESS>"

# 3. Ver la tabla de posiciones
curl -s http://127.0.0.1:8000/api/ligas/1/tabla/

# 4. Actualizar un marcador como planillero
curl -s -X PATCH http://127.0.0.1:8000/api/partidos/2/ \
  -H "Authorization: Bearer <ACCESS>" -H "Content-Type: application/json" \
  -d '{"goles_local":1,"goles_visita":0,"estado":"en_juego"}'
```

## Front externo

El front está en `front_externo/` y solo necesita que `config.js` apunte a la API:

```js
window.API_URL = "http://127.0.0.1:8000/api";
```

Con el servidor de Django corriendo, en otra terminal:

```bash
cd marcador/front_externo
python3 -m http.server 5500
```

Abre http://127.0.0.1:5500 . El botón **Diagnóstico de la API** comprueba que la API cumple el contrato. Para ver el flujo de sesión, inicia sesión con `planillero1` y cambia el marcador de un partido.

## Usar el proyecto en GitHub Codespaces

En Codespaces cada puerto tiene su propia URL pública, así que hay que ajustar tres cosas:

1. En la pestaña **Puertos**, pon los puertos **8000** y **5500** en **Público**.
2. En `front_externo/config.js` usa la URL del puerto 8000:
```js
   window.API_URL = "https://NOMBRE-DEL-CODESPACE-8000.app.github.dev/api";
```
   (el nombre se obtiene con `echo $CODESPACE_NAME`). Al terminar, devuélvelo a `http://127.0.0.1:8000/api`.
3. El CORS para el front del puerto 5500 se agrega solo cuando existe la variable `CODESPACE_NAME`.

## Seguridad

Las recomendaciones recibidas y dónde se aplicaron están en [`marcador/SEGURIDAD.md`](marcador/SEGURIDAD.md). Resumen:

- `SECRET_KEY` y `DEBUG` se leen de variables de entorno (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`), con valores por defecto solo para desarrollo.
- CORS restringido al origen del front (nunca `CORS_ALLOW_ALL_ORIGINS`).
- Límite de peticiones (throttling) y límite propio en el login.
- Token de acceso de vida corta (30 minutos).
- Permisos por rol con una clase propia (`RolPermiso`).

## Solución de problemas

| Problema | Solución |
|---|---|
| `No module named 'django'` | Activa el entorno: `source .venv/bin/activate` |
| Error CSRF al enviar un formulario | Recarga la página del formulario con F5 y vuelve a enviarlo (el token cambia al iniciar o cerrar sesión) |
| El front dice "Sin respuesta de la API" | Revisa que Django esté corriendo, que `config.js` apunte a la API y, en Codespaces, que los puertos estén en Público |
| Error 429 en la API | Espera un minuto: es el límite de peticiones |
