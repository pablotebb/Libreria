from django import forms
from .models import Libro
from django.core.exceptions import ValidationError

class Formulario_libros(forms.ModelForm):
  class Meta:
    model = Libro
    exclude = ['usuario']  # Excluimos el campo del formulario
    widgets = {
      'categoria': forms.SelectMultiple(attrs={'class': 'form-control'}),
      'isbn': forms.TextInput(attrs={'class': 'form-control'}),
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'autor': forms.TextInput(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
      'imagen': forms.FileInput(attrs={'class': 'form-control'}),
      'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
    
  def clean_isbn(self):
    isbn = self.cleaned_data.get('isbn').strip()
    if not isbn.replace('-', '').isdigit():
        raise ValidationError("El ISBN solo debe contener números y guiones.")
    return isbn

  def clean_titulo(self):
    titulo = self.cleaned_data.get('titulo').strip()
    if len(titulo) < 3:
        raise ValidationError("El título debe tener al menos 3 caracteres.")
    return titulo
  

    