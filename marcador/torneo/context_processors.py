from .roles import rol_de


def rol_usuario(request):
    return {"rol_usuario": rol_de(request.user)}