from django.urls import path
from .views import VRegistro, cerrar_sesion, logear

# 🛣️ RUTAS DE AUTENTICACIÓN: Conectamos URLs con vistas personalizadas

urlpatterns = [
    # 🧾 Página principal de autenticación (registro)
    # Muestra el formulario de registro y maneja su envío
    path("", VRegistro.as_view(), name="autenticacion"),

    # 🔐 Cerrar sesión
    # Simplemente termina la sesión activa y redirige al home
    path("cerrar_sesion/", cerrar_sesion, name="cerrar_sesion"),

    # 🔑 Iniciar sesión
    # Muestra y procesa el formulario de login
    path("logear/", logear, name="logear"),
]