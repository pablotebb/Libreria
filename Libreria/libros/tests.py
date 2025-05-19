from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Libro
from .forms import Formulario_libros

class LibroModelTest(TestCase):
  '''
  nombre: Pablo
  fecha: 18-05-2025
  OK
  '''
  
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.categoria = Categoria.objects.create(nombre="Ficción")
    self.libro = Libro.objects.create(
        usuario=self.user,
        isbn="978-3-16-148410-0",
        autor="Gabriel García Márquez",
        titulo="Cien años de soledad",
        contenido="Una historia épica sobre la familia Buendía.",
        leido=True
    )
    self.libro.categoria.add(self.categoria)

  def test_crear_libro(self):
    self.assertEqual(self.libro.titulo, "Cien años de soledad")
    self.assertEqual(self.libro.autor, "Gabriel García Márquez")
    self.assertEqual(self.libro.categoria.count(), 1)

  def test_str_libro(self):
    self.assertEqual(str(self.libro), "Cien años de soledad")

  def test_str_categoria(self):
    self.assertEqual(str(self.categoria), "Ficción")


class FormularioLibrosTest(TestCase):
  '''
  nombre: Pablo
  fecha: 18-05-2025
  OK
  '''

  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.categoria = Categoria.objects.create(nombre="No ficción")

  def test_formulario_valido(self):
    form_data = {
        'isbn': '978-3-16-148410-0',
        'autor': 'Autor Test',
        'titulo': 'Título Test',
        'contenido': 'Contenido largo y detallado.',
        'categoria': [self.categoria.id],
        'leido': True
    }
    form = Formulario_libros(data=form_data)
    self.assertTrue(form.is_valid())

  def test_formulario_sin_titulo(self):
    form_data = {
      'isbn': '978-3-16-148410-0',
      'autor': 'Autor Test',
      'titulo': '',
      'contenido': 'Contenido largo y detallado.',
      'categoria': [self.categoria.id],
      'leido': True
    }
    form = Formulario_libros(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('titulo', form.errors)

  def test_formulario_isbn_invalido(self):
    form_data = {
      'isbn': 'ABC123XYZ',
      'autor': 'Autor Test',
      'titulo': 'Título Test',
      'contenido': 'Contenido largo y detallado.',
      'categoria': [self.categoria.id],
      'leido': True
    }
    form = Formulario_libros(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('isbn', form.errors)


class LibroViewTest(TestCase):
  '''
  nombre: Pablo
  fecha: 18-05-2025
  OK
  '''

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.categoria = Categoria.objects.create(nombre="Ciencia Ficción")
    self.client.login(username='testuser', password='12345')

  def test_get_libro_view(self):
    response = self.client.get(reverse('libro:libros'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'libros/libro.html')

  def test_post_libro_view(self):
    data = {
      'isbn': '978-3-16-148410-0',
      'autor': 'Isaac Asimov',
      'titulo': 'Fundación',
      'contenido': 'La primera novela de la saga Fundación.',
      'categoria': [self.categoria.id],
      'leido': True
    }
    response = self.client.post(reverse('libro:libros'), data)
    self.assertEqual(response.status_code, 302)  # Redirección tras éxito
    self.assertEqual(Libro.objects.count(), 1)
    self.assertEqual(Libro.objects.first().titulo, 'Fundación')

  def test_editar_libro(self):
    libro = Libro.objects.create(
      usuario=self.user,
      isbn="1234567890",
      autor="Autor Antiguo",
      titulo="Libro viejo",
      contenido="Contenido antiguo"
    )
    libro.categoria.add(self.categoria)

    data = {
      'isbn': '0987654321',
      'autor': 'Nuevo Autor',
      'titulo': 'Nuevo Título',
      'contenido': 'Nuevo contenido actualizado.',
      'categoria': [self.categoria.id],
      'leido': False
    }

    response = self.client.post(reverse('libro:editar_libro', args=[libro.pk]), data)
    self.assertEqual(response.status_code, 302)
    libro.refresh_from_db()
    self.assertEqual(libro.autor, 'Nuevo Autor')
    self.assertEqual(libro.contenido, 'Nuevo contenido actualizado.')

  def test_borrar_libro(self):
    libro = Libro.objects.create(
      usuario=self.user,
      isbn="1234567890",
      autor="Autor Antiguo",
      titulo="Libro viejo",
      contenido="Contenido antiguo"
    )
    self.assertEqual(Libro.objects.count(), 1)
    response = self.client.post(reverse('libro:borrar_libro', args=[libro.pk]))
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Libro.objects.count(), 0)


class LibroViewPermisosTest(TestCase):
  '''
  nombre: Pablo
  fecha: 18-05-2025
  OK
  '''

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')

  def test_acceso_no_autenticado_redirige(self):
    response = self.client.get(reverse('libro:libros'))
    
    # Verificamos que hay una redirección
    self.assertEqual(response.status_code, 302)

    # Obtenemos la URL de redirección
    redirect_url = response.url
    
    # Comprobamos que contiene lo que esperamos
    self.assertTrue(redirect_url.startswith('/autenticacion/logear'))

  def test_acceso_vista_edicion_sin_login(self):
    response = self.client.get(reverse('libro:editar_libro', args=[1]))
    
    self.assertEqual(response.status_code, 302)
    redirect_url = response.url
    self.assertTrue(redirect_url.startswith('/autenticacion/logear'))