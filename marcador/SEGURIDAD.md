# Seguridad de la API

## Herramienta
Claude (Anthropic) — consulta realizada en octubre de 2026.

## Prompt utilizado
"Tengo una API REST en Django REST Framework con autenticación JWT (simplejwt) y
django-cors-headers para una liga deportiva con tres roles: anónimo (solo lectura),
planillero (PATCH del marcador) y administrador (CRUD completo). Dame recomendaciones
de seguridad concretas para settings.py y la configuración de DRF."

## Recomendaciones recibidas y dónde se aplicaron

| # | Recomendación | Dónde se aplicó |
|---|---------------|-----------------|
| 1 | Leer SECRET_KEY y DEBUG desde variables de entorno (valor por defecto solo para desarrollo) | `marcador/settings.py`: `DJANGO_SECRET_KEY` y `DJANGO_DEBUG` con `os.environ.get` |
| 2 | Restringir CORS al origen del front; nunca usar CORS_ALLOW_ALL_ORIGINS | `marcador/settings.py`: `CORS_ALLOWED_ORIGINS` con `http://127.0.0.1:5500` y `http://localhost:5500` |
| 3 | Limitar la cantidad de peticiones (throttling) | `marcador/settings.py`: `DEFAULT_THROTTLE_CLASSES` y `DEFAULT_THROTTLE_RATES` (anon, user); `torneo/api_views.py`: `LoginView` con `ScopedRateThrottle` (scope `login`) |
| 4 | Access token de vida corta | `marcador/settings.py`: `SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = 30 minutos` |
| 5 | Permisos por defecto restrictivos y por rol | `torneo/permissions.py`: `RolPermiso` (BasePermission) usada como `DEFAULT_PERMISSION_CLASSES` |
| 6 | Validar las reglas de negocio en el servidor | `torneo/serializers.py`: `PartidoSerializer.validate`; `torneo/models.py`: `Partido.clean` |
| 7 | Restringir ALLOWED_HOSTS | `marcador/settings.py`: `ALLOWED_HOSTS` desde `DJANGO_ALLOWED_HOSTS` |
| 8 | Usar HTTPS, HSTS y cookies seguras en producción | No aplicado: el proyecto corre en local, solo para desarrollo y evaluación |
| 9 | Proteger formularios del sitio contra CSRF | Templates con `{% csrf_token %}`; `CsrfViewMiddleware` activo |