from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PartidoForm, MarcadorForm
from .models import Partido
from .roles import AdministradorMixin, PlanilleroMixin


class PartidoList(ListView):
    model = Partido
    template_name = "torneo/partido_list.html"
    context_object_name = "partidos"
    queryset = Partido.objects.select_related("liga", "local", "visita")


class PartidoDetail(DetailView):
    model = Partido
    template_name = "torneo/partido_detail.html"
    context_object_name = "partido"


class PartidoCreate(AdministradorMixin, CreateView):
    model = Partido
    form_class = PartidoForm
    template_name = "torneo/form.html"
    success_url = reverse_lazy("partido_list")
    extra_context = {"titulo": "Nuevo partido"}


class PartidoUpdate(AdministradorMixin, UpdateView):
    model = Partido
    form_class = PartidoForm
    template_name = "torneo/form.html"
    success_url = reverse_lazy("partido_list")
    extra_context = {"titulo": "Editar partido"}


class PartidoDelete(AdministradorMixin, DeleteView):
    model = Partido
    template_name = "torneo/confirmar_borrar.html"
    success_url = reverse_lazy("partido_list")


class MarcadorUpdate(PlanilleroMixin, UpdateView):
    model = Partido
    form_class = MarcadorForm
    template_name = "torneo/marcador_form.html"
    context_object_name = "partido"

    def get_success_url(self):
        return reverse("partido_detail", args=[self.object.pk])