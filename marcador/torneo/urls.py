from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="partido_list"), name="home"),
    path("partidos/", views.PartidoList.as_view(), name="partido_list"),
    path("partidos/nuevo/", views.PartidoCreate.as_view(), name="partido_create"),
    path("partidos/<int:pk>/", views.PartidoDetail.as_view(), name="partido_detail"),
    path("partidos/<int:pk>/editar/", views.PartidoUpdate.as_view(), name="partido_update"),
    path("partidos/<int:pk>/borrar/", views.PartidoDelete.as_view(), name="partido_delete"),
    path("partidos/<int:pk>/marcador/", views.MarcadorUpdate.as_view(), name="partido_marcador"),
]