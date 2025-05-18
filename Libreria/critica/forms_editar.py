from django import forms
from .models import Critica


class Formulario_critica_editar(forms.ModelForm):
  class Meta:
    model = Critica
    fields = ['id_libros', 'contenido']
    widgets = {
      'id_libros': forms.TextInput(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    }    