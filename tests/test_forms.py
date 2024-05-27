# tests/test_forms.py
import unittest
from forms import UserAddForm, LoginForm, UserEditForm, BookSearchForm, ReviewForm
from flask import Flask

class FormTests(unittest.TestCase):

    def setUp(self):
        """Set up a Flask test app and context."""
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove the Flask test app context."""
        self.app_context.pop()

    def test_user_add_form(self):
        form = UserAddForm(username="testuser", password="password", email="test@example.com")
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm(username="testuser", password="password")
        self.assertTrue(form.validate())

    def test_user_edit_form(self):
        form = UserEditForm(username="testuser", email="test@example.com", password="password123")
        self.assertTrue(form.validate(), form.errors)

    def test_book_search_form(self):
        form = BookSearchForm(title="Some Book Title", keyword="keyword")
        self.assertTrue(form.validate(), form.errors)  # Print form.errors if validation fails

    def test_review_form(self):
        form = ReviewForm(rating=5, text="Great book!", comment="Nice read")
        self.assertTrue(form.validate(), form.errors)  # Print form.errors if validation fails

if __name__ == '__main__':
    unittest.main()
