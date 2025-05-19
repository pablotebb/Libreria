from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Critica
from libros.models import Libro


@override_settings(
  LOGIN_URL="/autenticacion/logear"
)

class CriticaViewsTest(TestCase):
  '''
  nombre: Pablo
  fecha: 19-05-2025
  OK
  '''
  def setUp(self):
    # Crear usuario para login
    self.user = User.objects.create_user(username='testuser', password='12345')
    
    # Crear libro para asociar crítica
    self.libro = Libro.objects.create(
        titulo="Libro de prueba",
        leido=True,
        usuario=self.user 
    )

    # Datos básicos para formularios
    self.data = {
        'id_libros': self.libro.id,  # id
        'contenido': 'Contenido de prueba',
    }

  def login(self):
    self.client.login(username='testuser', password='12345')

    # ---------------------------
    # Pruebas de vistas protegidas
    # ---------------------------

  def test_vista_critica_requiere_login(self):
    response = self.client.get(reverse('critica:critica'))
    self.assertEqual(response.status_code, 302)  # Redirige al login

  def test_vista_editar_requiere_login(self):
    response = self.client.get(reverse('critica:editar_critica', args=[1]))
    self.assertEqual(response.status_code, 302)

  def test_vista_borrar_requiere_login(self):
    response = self.client.get(reverse('critica:borrar_critica', args=[1]))
    self.assertEqual(response.status_code, 302)

    # ---------------------------
    # Pruebas con login activo
    # ---------------------------

  def test_vista_critica_carga_correctamente(self):
    self.login()
    response = self.client.get(reverse('critica:critica'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'critica/critica.html')

  def test_guardar_critica_valida(self):
    self.login()
    response = self.client.post(reverse('critica:critica'), self.data)
    
    # # Añadimos esto para ver errores del formulario
    # if 'form' in response.context:
    #   print(response.context['form'].errors)  # Mostrar errores en consola
    
    self.assertEqual(response.status_code, 302)
    self.assertTrue(Critica.objects.filter(contenido='Contenido de prueba').exists())

  def test_no_se_guarda_critica_invalida(self):
    self.login()
    bad_data = {'contenido': ''}
    response = self.client.post(reverse('critica:critica'), bad_data)
    
    # if 'form' in response.context:
    #   print(response.context['form'].errors)
    
    self.assertEqual(response.status_code, 200)
    
    if response.context:
      form = response.context.get('form')
      self.assertIsNotNone(form)
      self.assertTrue(form.errors)
    
    self.assertFalse(Critica.objects.exists())

  def test_editar_critica(self):
    self.login()
    critica = Critica.objects.create(
      id_libros=self.libro,
      contenido="Contenido de prueba",
      usuario=self.user  # 
    )
    data = {'contenido': "Actualizado"}
    response = self.client.post(reverse('critica:editar_critica', args=[critica.pk]), data)
    self.assertEqual(response.status_code, 302)
    critica.refresh_from_db()
    self.assertEqual(critica.contenido, "Actualizado")

  def test_borrar_critica(self):
    self.login()
    critica = Critica.objects.create(
      id_libros=self.libro,
      contenido="Contenido de borrar critica",
      usuario=self.user  # 
    )
    response = self.client.post(reverse('critica:borrar_critica', args=[critica.pk]))
    self.assertEqual(response.status_code, 302)
    self.assertFalse(Critica.objects.filter(pk=critica.pk).exists())

  def test_borrar_critica_get_muestra_confirmacion(self):
    self.login()
    critica = Critica.objects.create(
      id_libros=self.libro,
      contenido="Contenido para borrar",
      usuario=self.user  # 
    )
    response = self.client.get(reverse('critica:borrar_critica', args=[critica.pk]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'critica/confirmar_borrar.html')