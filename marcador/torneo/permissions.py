from rest_framework.permissions import BasePermission, SAFE_METHODS
from .roles import rol_de

CAMPOS_MARCADOR = {"goles_local", "goles_visita", "estado"}


class RolPermiso(BasePermission):
    """Anónimo: solo GET (escritura -> 401). Planillero: GET + PATCH del marcador.
    Administrador: todo. Otro usuario autenticado: solo GET (-> 403)."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False                      # DRF responde 401
        rol = rol_de(request.user)
        if rol == "administrador":
            return True
        if rol == "planillero":
            if request.method == "PATCH" and getattr(view, "basename", "") == "partido":
                return set(request.data.keys()) <= CAMPOS_MARCADOR
        return False                          # 403