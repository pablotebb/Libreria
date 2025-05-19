from django import forms
from .models import Libro
from django.core.exceptions import ValidationError  # Para validaciones personalizadas


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