from django.shortcuts import render

# ┌──────────────────────────────────────────────┐
# │           Vista Principal: home              │
# └──────────────────────────────────────────────┘
# La función `home` es la encargada de mostrar la 
# página de inicio de nuestra aplicación web.
# Recibe una solicitud (request) y responde 
# devolviendo un template HTML procesado.

def home(request):
    # Renderizamos el template 'core/home.html'
    # Este archivo HTML contiene la estructura visual
    # de nuestra página principal.
    return render(request, 'core/home.html')