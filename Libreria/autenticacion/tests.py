from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate

class AutenticacionTests(TestCase):
    '''
    nombre: Pablo
    fecha: 19-05-2025
    OK
    '''
    def setUp(self):
        self.client = Client()
        self.registro_url = reverse('autenticacion')  # Nombre del path en urls.py
        self.login_url = reverse('logear')            # Nombre del path en urls.py
        self.cerrar_sesion_url = reverse('cerrar_sesion')  # Nombre del path en urls.py

    def test_registro_usuario_valido(self):
        """ Test: Registro exitoso de un nuevo usuario."""
        response = self.client.post(self.registro_url, {
            'username': 'testuser',
            'password1': 'contrasena123Segura!',
            'password2': 'contrasena123Segura!'
        })

        # Verificar redirección al home
        self.assertRedirects(response, reverse('core:home'))

        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verificar que el usuario está autenticado
        user = authenticate(username='testuser', password='contrasena123Segura!')
        self.assertIsNotNone(user)

    def test_registro_formulario_invalido_password_no_coincide(self):
        """ Test: Registro fallido por contraseñas no coincidentes."""
        response = self.client.post(self.registro_url, {
            'username': 'testuser',
            'password1': 'contrasena123',
            'password2': 'contrasena456'
        })

        # Verificar que hay errores en el formulario
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        #self.assertFormError(response, 'form', None, "Las dos contraseñas no coinciden.")

    def test_registro_formulario_invalido_usuario_ya_existe(self):
        """ Test: Registro fallido por usuario ya existente."""
        # Aseguramos que no haya sesión iniciad
        self.client.logout()
        
        # Creamos un usuario previo
        User.objects.create_user(username='testuser', password='Xq9#superSecretPass2025')
        
        # Intentamos registrar el mismo usuario
        response = self.client.post(self.registro_url, {
            'username': 'testuser',
            'password1': 'Xq9#superSecretPass2025',
            'password2': 'Xq9#superSecretPass2025',
        })
        
        # Capturamos los mensajes
        messages_list = list(get_messages(response.wsgi_request))

        # Mostramos los mensajes para depurar
        print("Mensajes recibidos:", [m.message for m in messages_list])
        
        form = response.context.get('form')
        if form:
          print("Errores del formulario:", form.errors)


        # Verificamos que aparezca el mensaje correcto
        self.assertIn("Ya existe un usuario con este nombre.", form.errors['username'])
        
    def test_inicio_sesion_exitoso(self):
        """ Test: Inicio de sesión exitoso."""
        User.objects.create_user(username='testuser', password='contrasena123')

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'contrasena123'
        })

        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_inicio_sesion_contrasena_incorrecta(self):
        """ Test: Inicio de sesión fallido por contraseña incorrecta."""
        User.objects.create_user(username='testuser', password='contrasena123')

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })

        messages = list(get_messages(response.wsgi_request))
        self.assertIn("usuario no válido", [m.message for m in messages])

    def test_inicio_sesion_usuario_inexistente(self):
        """ Test: Inicio de sesión fallido por usuario inexistente."""
        response = self.client.post(self.login_url, {
            'username': 'noexisto',
            'password': 'contrasena123'
        })

        messages = list(get_messages(response.wsgi_request))
        self.assertIn("usuario no válido", [m.message for m in messages])

    def test_cerrar_sesion(self):
        """ Test: Cierre de sesión correcto."""
        user = User.objects.create_user(username='testuser', password='contrasena123')
        self.client.login(username='testuser', password='contrasena123')

        response = self.client.get(self.cerrar_sesion_url)

        self.assertRedirects(response, reverse('core:home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_csrf_proteccion_registro(self):
        """ Test: Comprobación de protección CSRF en registro."""
        response = self.client.get(self.registro_url)
        self.assertContains(response, 'csrfmiddleware')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_csrf_proteccion_login(self):
        """ Test: Comprobación de protección CSRF en login."""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'csrfmiddleware')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')