from django.contrib.auth.mixins import UserPassesTestMixin


def es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Administrador").exists()
    )


def es_planillero(user):
    return user.is_authenticated and user.groups.filter(name="Planillero").exists()


def rol_de(user):
    if es_administrador(user):
        return "administrador"
    if es_planillero(user):
        return "planillero"
    return "lector"


# Anónimo -> redirige al login. Con sesión pero sin rol -> 403.
class AdministradorMixin(UserPassesTestMixin):
    def test_func(self):
        return es_administrador(self.request.user)


class PlanilleroMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return es_administrador(u) or es_planillero(u)