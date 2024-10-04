import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app, db
from models.user_model import User


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear usuario de prueba
        self.user = User(name="Test User", email="test@example.com")
        self.user.set_password("testpassword")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)

    def test_register_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)
        self.assertIn(b'Register', response.data)  # Verifica que la página contenga la palabra 'Register'

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)
        self.assertIn(b'Login', response.data)  # Verifica que la página contenga la palabra 'Login'

    def test_login_failed(self):
        response = self.client.post('/login', data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

    def test_edit_profile_unauthenticated(self):
        with self.client.session_transaction() as session:
            session.clear()

        response = self.client.get('/edit_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_delete_profile_authenticated(self):
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

        response = self.client.post('/delete_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tu cuenta ha sido eliminada.', response.data)

    def test_delete_profile_unauthenticated(self):
        with self.client.session_transaction() as session:
            session.clear()

        response = self.client.post('/delete_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)


if __name__ == '__main__':
    unittest.main()
