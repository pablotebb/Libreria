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
  
def aviso(request):
    # Renderizamos el template 'core/aviso_legal.html'
    # Este archivo HTML contiene la estructura visual
    # de Aviso Legal.
    return render(request, 'core/aviso_legal.html')
  
def cookie(request):
    # Renderizamos el template 'core/cookie.html'
    # Este archivo HTML contiene la estructura visual
    # de Cookies.
    return render(request, 'core/cookies.html')
  
def privacidad(request):
    # Renderizamos el template 'core/privacidad.html'
    # Este archivo HTML contiene la estructura visual
    # de Privacidad.
    return render(request, 'core/privacidad.html')