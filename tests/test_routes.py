# tests/test_routes.py
import unittest
from app import create_app, db
from app.models import User, Task
from werkzeug.security import generate_password_hash

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        """Configura la aplicación y la base de datos de pruebas."""
        self.app = create_app(config_class='config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Limpia la base de datos después de cada prueba."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_task_creation(self):
        """Prueba la creación de una tarea."""
        # Crear un usuario
        with self.app.app_context():
            user = User(username='testuser', password=generate_password_hash('testpass', method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()

        # Iniciar sesión
        login_res = self.client.post('/auth/login', json={'username': 'testuser', 'password': 'testpass'})
        
        print("Login Response Status Code:", login_res.status_code)
        print("Login Response JSON:", login_res.get_json())
        
        # Verifica que la solicitud de inicio de sesión sea exitosa
        self.assertEqual(login_res.status_code, 200)

        json_response = login_res.get_json()
        self.assertIn('access_token', json_response)  # Verifica que 'access_token' esté en la respuesta

        token = json_response['access_token']
        
        # Crear una tarea usando el token de acceso
        response = self.client.post('/tasks', json={'title': 'Test Task'}, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Task created successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
