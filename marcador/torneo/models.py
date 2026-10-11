from django.core.exceptions import ValidationError
from django.db import models


class Liga(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    temporada = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.temporada})"


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name="equipos")

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    POSICIONES = [("POR", "Portero"), ("DEF", "Defensa"), ("MED", "Mediocampista"), ("DEL", "Delantero")]
    nombre = models.CharField(max_length=100)
    numero = models.PositiveIntegerField()
    posicion = models.CharField(max_length=3, choices=POSICIONES)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="jugadores")

    def __str__(self):
        return f"{self.nombre} #{self.numero}"


class Partido(models.Model):
    ESTADOS = [("programado", "Programado"), ("en_juego", "En juego"), ("finalizado", "Finalizado")]
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name="partidos")
    local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="partidos_local")
    visita = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="partidos_visita")
    fecha = models.DateTimeField()
    estadio = models.CharField(max_length=100, blank=True)
    goles_local = models.PositiveIntegerField(default=0)
    goles_visita = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="programado")

    class Meta:
        ordering = ["fecha", "id"]

    def clean(self):
        if self.local_id and self.visita_id:
            if self.local_id == self.visita_id:
                raise ValidationError("Un equipo no puede jugar contra sí mismo.")
            if self.liga_id and (self.local.liga_id != self.liga_id or self.visita.liga_id != self.liga_id):
                raise ValidationError("Local y visita deben pertenecer a la liga del partido.")

    def __str__(self):
        return f"{self.local} vs {self.visita} ({self.fecha:%d/%m/%Y})"