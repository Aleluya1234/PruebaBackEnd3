from django import forms
from .models import Partido

FORMATO_FECHA = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]


class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ["liga", "local", "visita", "fecha", "estadio",
                  "goles_local", "goles_visita", "estado"]
        widgets = {"fecha": forms.DateTimeInput(attrs={"type": "datetime-local"},
                                                format="%Y-%m-%dT%H:%M")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha"].input_formats = FORMATO_FECHA


class MarcadorForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ["goles_local", "goles_visita", "estado"]