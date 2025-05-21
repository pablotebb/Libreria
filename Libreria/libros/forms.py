from django import forms
from .models import Libro
from PIL import Image  # Para verificar que sea una imagen válida
from django.core.exceptions import ValidationError  # Para validaciones personalizadas
import os


# ┌──────────────────────────────────────────────────────┐
# │               Formulario para crear/editar libros    │
# └──────────────────────────────────────────────────────┘
class Formulario_libros(forms.ModelForm):
    """
    Este formulario permite añadir o editar libros.
    - Excluye el campo 'usuario' para evitar manipulación desde el front-end.
    - Incluye validaciones personalizadas para datos esenciales (ISBN, título).
    - Usa widgets con clases Bootstrap para mantener consistencia visual.
    """

    class Meta:
        model = Libro
        exclude = ['usuario']  # El usuario se asigna automáticamente desde la vista

        widgets = {
            # Multiple select con estilo Bootstrap para categorías
            'categoria': forms.SelectMultiple(attrs={'class': 'form-control'}),

            # Campos básicos con estilos consistentes
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),

            # Campo de imagen con estilo adecuado para subidas de archivos
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),

            # Checkbox con estilo especial para 'leído'
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # ───── Validación personalizada para ISBN ─────
    def clean_isbn(self):
        """
        Valida que el ISBN solo contenga números y guiones.
        Elimina espacios innecesarios y verifica formato básico.
        """
        isbn = self.cleaned_data.get('isbn').strip()

        if not isbn.replace('-', '').isdigit():
            raise ValidationError("El ISBN solo debe contener números y guiones.")

        return isbn

    # ───── Validación personalizada para Título ─────
    def clean_titulo(self):
        """
        Asegura que el título tenga al menos 3 caracteres útiles.
        Evita entradas demasiado genéricas o incompletas.
        """
        titulo = self.cleaned_data.get('titulo').strip()

        if len(titulo) < 3:
            raise ValidationError("El título debe tener al menos 3 caracteres.")

        return titulo
      
    # ───── Validación personalizada para Imagen ─────
    def clean_imagen(self):
      imagen = self.cleaned_data.get('imagen')

      # Si no se subió ninguna imagen nueva, devolvemos la actual (si existe)
      if not imagen:
          # Si estamos editando y no se subió una nueva imagen, mantenemos la existente
          if 'imagen' in self.initial:
              return self.initial['imagen']
          return imagen  # Puede ser None si es creación

      # Validaciones solo si hay una imagen nueva
      try:
          img = Image.open(imagen)
          img.verify()
          if img.format not in ['JPEG', 'PNG', 'GIF', 'WEBP']:
              raise ValidationError("Formato de imagen no soportado. Usa JPG, PNG, GIF o WEBP.")
      except Exception as e:
          raise ValidationError("El archivo no es una imagen válida.")

      if imagen.size > 5 * 1024 * 1024:
          raise ValidationError("La imagen no debe superar los 5MB.")

      return imagen