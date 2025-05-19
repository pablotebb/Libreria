from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from libros.models import Libro


class HomeViewTest(TestCase):
  '''
  nombre: Pablo
  fecha: 19-05-2025
  OK
  '''

  def setUp(self):
    # Crear un usuario de prueba
    self.user = User.objects.create_user(username='testuser', password='12345')
    
    # Crear algunos libros de prueba
    Libro.objects.create(titulo="Libro 1", autor="Autor 1", leido=True, usuario=self.user)
    Libro.objects.create(titulo="Libro 2", autor="Autor 2", leido=False, usuario=self.user)

  def test_home_view_authenticated_user(self):
    # Iniciar sesión
    self.client.login(username='testuser', password='12345')

    response = self.client.get(reverse('listado'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'listado/home.html')
    self.assertIn('listado', response.context)

    # Verificar que se pasan todos los libros
    libros = response.context['listado']
    self.assertEqual(len(libros), 2)

  def test_home_view_unauthenticated_user_redirect(self):
    response = self.client.get(reverse('listado'))
    self.assertEqual(response.status_code, 302)  # Redirección
    login_url = reverse('logear')  
    
    redirect_url = f'{login_url}?next={reverse("listado")}'
    self.assertRedirects(
      response, 
      redirect_url, 
      status_code=302, 
      target_status_code=200,
      fetch_redirect_response=True 
    )

  def test_home_view_displays_correct_data(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('listado'))
    self.assertEqual(response.status_code, 200)

    # Simular renderizado manualmente (opcional, para más control)
    content = response.content.decode()

    self.assertIn("Libro 1", content)
    self.assertIn("Autor 1", content)
    self.assertIn("Sí", content)  # Leído == True

    self.assertIn("Libro 2", content)
    self.assertIn("Autor 2", content)
    self.assertIn("No", content)  # Leído == False