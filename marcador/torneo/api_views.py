from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Liga, Equipo, Jugador, Partido
from .roles import rol_de
from .serializers import (LigaSerializer, EquipoSerializer,
                          JugadorSerializer, PartidoSerializer)


def _filtro(request, qs, param, campo):
    valor = request.query_params.get(param)
    if valor and valor.isdigit():
        qs = qs.filter(**{campo: int(valor)})
    return qs


class LoginView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.username, "rol": rol_de(u)})


class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all().order_by("id")
    serializer_class = LigaSerializer

    @action(detail=True, methods=["get"], url_path="tabla")
    def tabla(self, request, pk=None):
        liga = self.get_object()   # 404 si no existe
        filas = {
            e.id: {"equipo_id": e.id, "equipo": e.nombre, "pj": 0, "pg": 0, "pe": 0,
                   "pp": 0, "gf": 0, "gc": 0, "dg": 0, "pts": 0}
            for e in Equipo.objects.filter(liga=liga)
        }
        for p in Partido.objects.filter(liga=liga, estado="finalizado"):
            for eid, gf, gc in ((p.local_id, p.goles_local, p.goles_visita),
                                (p.visita_id, p.goles_visita, p.goles_local)):
                f = filas.get(eid)
                if f is None:
                    continue
                f["pj"] += 1
                f["gf"] += gf
                f["gc"] += gc
                if gf > gc:
                    f["pg"] += 1
                    f["pts"] += 3
                elif gf == gc:
                    f["pe"] += 1
                    f["pts"] += 1
                else:
                    f["pp"] += 1
        for f in filas.values():
            f["dg"] = f["gf"] - f["gc"]
        orden = sorted(filas.values(), key=lambda f: (-f["pts"], -f["dg"], -f["gf"], f["equipo"]))
        return Response(orden)


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer

    def get_queryset(self):
        qs = Equipo.objects.select_related("liga").order_by("id")
        if self.action == "list":
            qs = _filtro(self.request, qs, "liga", "liga_id")
        return qs


class JugadorViewSet(viewsets.ModelViewSet):
    serializer_class = JugadorSerializer

    def get_queryset(self):
        qs = Jugador.objects.select_related("equipo").order_by("id")
        if self.action == "list":
            qs = _filtro(self.request, qs, "equipo", "equipo_id")
        return qs


class PartidoViewSet(viewsets.ModelViewSet):
    serializer_class = PartidoSerializer

    def get_queryset(self):
        qs = Partido.objects.select_related("liga", "local", "visita").order_by("fecha", "id")
        if self.action == "list":
            qs = _filtro(self.request, qs, "liga", "liga_id")
            estado = self.request.query_params.get("estado")
            if estado:
                qs = qs.filter(estado=estado)
        return qs