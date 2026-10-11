from rest_framework import serializers
from .models import Liga, Equipo, Jugador, Partido


class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ["id", "nombre", "pais", "temporada"]


class EquipoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.CharField(source="liga.nombre", read_only=True)

    class Meta:
        model = Equipo
        fields = ["id", "nombre", "ciudad", "liga", "liga_nombre"]


class JugadorSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.CharField(source="equipo.nombre", read_only=True)

    class Meta:
        model = Jugador
        fields = ["id", "nombre", "numero", "posicion", "equipo", "equipo_nombre"]


class PartidoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.CharField(source="liga.nombre", read_only=True)
    local_nombre = serializers.CharField(source="local.nombre", read_only=True)
    visita_nombre = serializers.CharField(source="visita.nombre", read_only=True)

    class Meta:
        model = Partido
        fields = ["id", "liga", "liga_nombre", "local", "local_nombre", "visita",
                  "visita_nombre", "fecha", "estadio", "goles_local", "goles_visita", "estado"]

    def validate(self, attrs):
        inst = self.instance
        liga = attrs.get("liga", getattr(inst, "liga", None))
        local = attrs.get("local", getattr(inst, "local", None))
        visita = attrs.get("visita", getattr(inst, "visita", None))
        if local and visita and local.pk == visita.pk:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo.")
        if liga and local and visita and (local.liga_id != liga.pk or visita.liga_id != liga.pk):
            raise serializers.ValidationError("Local y visita deben pertenecer a la liga del partido.")
        return attrs