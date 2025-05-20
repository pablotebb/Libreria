"""
URL configuration for Libreria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/ 

Este archivo es el corazón del sistema de rutas de la aplicación.
Aquí se decide qué vista maneja cada URL, y cómo se organizan las diferentes partes del proyecto.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ┌──────────────────────────────────────────────────────┐
# │               Definición de Rutas Principales        │
# └──────────────────────────────────────────────────────┘
urlpatterns = [
    # 🔐 Panel de administración estándar de Django
    # Accesible en /admin/
    path("admin/", admin.site.urls),

    # 🏠 Página principal del sitio
    # Redirige a la app 'core' que gestiona la página de inicio
    path("", include("core.urls", namespace="core")),

    # 📝 Sección de críticas literarias
    # Todas las URLs bajo /critica/ son manejadas por la app 'critica'
    path("critica/", include("critica.urls", namespace="critica")),

    # 📚 Gestión de libros
    # Las rutas relacionadas con libros se encuentran bajo /libros/
    # y están definidas en la app 'libros', con el namespace 'libro'
    path("libros/", include("libros.urls", namespace="libro")),

    # 📋 Listados personalizados (por ejemplo: listas de lectura)
    # Incluye todas las rutas bajo /listado/
    path("listado/", include("listado.urls")),

    # 🔐 Sistema de autenticación personalizado
    # Maneja login, registro, logout, etc., bajo /autenticacion/
    path("autenticacion/", include("autenticacion.urls")),
] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)