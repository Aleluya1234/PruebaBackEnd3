from django.contrib import admin
from .models import Liga, Equipo, Jugador, Partido


@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais", "temporada")
    search_fields = ("nombre", "pais")
    list_filter = ("temporada",)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "liga")
    list_filter = ("liga",)
    search_fields = ("nombre", "ciudad")


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "numero", "posicion", "equipo")
    list_filter = ("posicion", "equipo")
    search_fields = ("nombre",)


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("local", "visita", "liga", "fecha", "goles_local", "goles_visita", "estado")
    list_filter = ("liga", "estado")
    search_fields = ("local__nombre", "visita__nombre", "estadio")