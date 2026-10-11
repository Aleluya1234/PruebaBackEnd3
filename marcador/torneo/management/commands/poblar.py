from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from torneo.models import Liga, Equipo, Jugador, Partido


class Command(BaseCommand):
    help = "Crea datos de ejemplo y usuarios admin1, planillero1 y lector1 (clave: Clave12345)"

    def handle(self, *args, **opts):
        liga, _ = Liga.objects.get_or_create(nombre="Liga Demo", pais="Chile", temporada="2026")
        datos = [("Colo-Colo", "Santiago"), ("Universidad de Chile", "Santiago"),
                 ("Huachipato", "Talcahuano"), ("Cobresal", "El Salvador")]
        eqs = [Equipo.objects.get_or_create(nombre=n, ciudad=c, liga=liga)[0] for n, c in datos]
        for i, e in enumerate(eqs):
            Jugador.objects.get_or_create(nombre=f"Jugador {i+1}", numero=i + 1,
                                          posicion="DEL", equipo=e)
        Partido.objects.get_or_create(
            liga=liga, local=eqs[0], visita=eqs[1],
            defaults=dict(fecha=timezone.now(), estadio="Estadio Monumental",
                          goles_local=2, goles_visita=1, estado="finalizado"))
        Partido.objects.get_or_create(
            liga=liga, local=eqs[2], visita=eqs[3],
            defaults=dict(fecha=timezone.now(), estadio="Estadio CAP", estado="programado"))
        for username, grupo in (("admin1", "Administrador"), ("planillero1", "Planillero"), ("lector1", None)):
            u, creado = User.objects.get_or_create(username=username)
            if creado:
                u.set_password("Clave12345")
                u.save()
            if grupo:
                u.groups.add(Group.objects.get(name=grupo))
        self.stdout.write(self.style.SUCCESS("Listo"))