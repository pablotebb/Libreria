from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class CoreViewsTest(TestCase):
  '''
  nombre: Pablo
  fecha: 18-05-2025
  OK
  '''

  def test_home_view_status_code(self):
    """Verifica que la página principal carga correctamente"""
    response = self.client.get(reverse('core:home'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'core/home.html')

  def test_home_view_content(self):
    """Verifica que el contenido de home.html se muestra correctamente"""
    response = self.client.get(reverse('core:home'))
    self.assertContains(response, "Libreria")
    self.assertContains(response, "Listado de libros")

  def test_login_logout_links_when_not_logged_in(self):
    """Verifica los enlaces de login/registro cuando el usuario no está autenticado"""
    response = self.client.get(reverse('core:home'))
    self.assertContains(response, 'Login')
    self.assertContains(response, 'Registrate')
    self.assertNotContains(response, 'Cerrar sesión')

  def test_login_logout_links_when_logged_in(self):
    """Verifica los enlaces cuando el usuario está autenticado"""
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')

    response = self.client.get(reverse('core:home'))
    self.assertContains(response, 'Hola testuser')
    self.assertContains(response, 'Cerrar sesión')
    self.assertNotContains(response, 'Login')
    self.assertNotContains(response, 'Registrate')