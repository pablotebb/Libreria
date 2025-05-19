from django import forms
from .models import Critica


# ✏️ Formulario: Formulario_critica_editar
# ────────────────────────────────────────────────
# Usado exclusivamente para editar una crítica ya existente.
# No permite cambiar el libro, solo el contenido de la crítica.

class Formulario_critica_editar(forms.ModelForm):
    class Meta:
        model = Critica
        # Solo se puede editar el contenido, no el libro asociado
        fields = ['contenido']

        widgets = {
            # ✍️ Campo de texto ampliado para edición cómoda
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }