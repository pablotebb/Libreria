from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# ██████████████████████████████████████████████████████████████████████
# ███ VISTAS DE AUTENTICACIÓN: Registro, inicio de sesión y cierre     ███
# ██████████████████████████████████████████████████████████████████████

class VRegistro(View):
    """
    🧑‍💻 Vista basada en clase para manejar el registro de nuevos usuarios.
    
    Se encarga de mostrar el formulario de registro y procesar los datos cuando alguien decide crear una cuenta nueva. Usa Django's UserCreationForm.
    """

    def get(self, request):
        """
        📄 GET: Muestra el formulario vacío de registro.
        
        Cuando un usuario entra por primera vez a la página de registro,
        le devolvemos el formulario listo para llenar.
        """
        form = UserCreationForm()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):
        """
        ✅ POST: Procesa los datos del formulario de registro.
        
        Si todo está bien, guarda al nuevo usuario y lo loguea automáticamente. Si hay errores, mostramos mensajes claros y volvemos a mostrar el formulario.
        """
        form = UserCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save()         # Guardamos al nuevo usuario
            login(request, usuario)       # Lo logueamos automáticamente
            return redirect("core:home")  # Y lo llevamos al home
        else:
            # Mostramos todos los errores del formulario
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    """
    🔐 Función para cerrar sesión.
    
    Simplemente llama a logout() y redirige al home. Todo muy limpio y directo.
    """
    logout(request)
    return redirect("core:home")


def logear(request):
    """
    🔑 Vista para iniciar sesión.
    
    Maneja el formulario de login, verifica las credenciales y redirige si es válido. Si algo falla, muestra mensajes de error amigables.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)

            if usuario is not None:
                login(request, usuario)
                return redirect("core:home")
            else:
                messages.error(request, "usuario no válido")

        else:
            messages.error(request, "usuario no válido")

    # Si no es POST o si falló, mostramos el formulario vacío
    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})