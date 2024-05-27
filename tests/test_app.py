# tests/test_app.py
import unittest
from app import app
from flask import session

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        """Set up a Flask test app and context."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('JOIN US!', response.get_data(as_text=True))

    def test_login(self):
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome back.', response.get_data(as_text=True))

    def test_logout(self):
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)
            self.assertNotIn('user_id', session)

if __name__ == '__main__':
    unittest.main()
