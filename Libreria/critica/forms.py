from django import forms
from .models import Critica


# 📝 Formulario: Formulario_critica
# ────────────────────────────────────────────────
# Sirve para crear una nueva crítica desde la interfaz web.
# Incluye selección de libro y el contenido de la crítica.

class Formulario_critica(forms.ModelForm):
    class Meta:
        model = Critica
        fields = ['id_libros', 'contenido']

        widgets = {
            # 🔍 Selección de libro: desplegable con estilo Bootstrap
            'id_libros': forms.Select(attrs={'class': 'form-control'}),

            # ✍️ Campo de texto ampliado para escribir la crítica
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }