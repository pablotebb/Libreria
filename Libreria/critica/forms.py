from django import forms
from .models import Critica


class Formulario_critica(forms.ModelForm):
  class Meta:
    model = Critica
    fields = ['id_libros', 'contenido']
    widgets = {
      'id_libros': forms.Select(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    }    