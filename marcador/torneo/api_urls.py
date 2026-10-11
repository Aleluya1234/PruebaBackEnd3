from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (LoginView, MeView, LigaViewSet, EquipoViewSet,
                        JugadorViewSet, PartidoViewSet)

router = DefaultRouter()
router.register("ligas", LigaViewSet, basename="liga")
router.register("equipos", EquipoViewSet, basename="equipo")
router.register("jugadores", JugadorViewSet, basename="jugador")
router.register("partidos", PartidoViewSet, basename="partido")   # "partido" lo usa permissions.py

urlpatterns = [
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]