# tests/test_models.py
import unittest
from models import db, User, Book, Review, Author, Genre, Likes
from app import app

class ModelTests(unittest.TestCase):
    """ModelTests _summary_"""
    def setUp(self):
        """Set up a Flask test app and context, and initialize the database."""
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """test_user_creation _summary_"""
        with self.app.app_context():
            user = User(username="testuser", email="test@example.com", password="password")
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(db.session.get(User, user.id))

    def test_book_creation(self):
        """test user"""
        with self.app.app_context():
            book = Book(title="Some Book", author="Some Author", google_books_id="123456")
            db.session.add(book)
            db.session.commit()
            self.assertIsNotNone(db.session.get(Book, book.id))

    def test_review_creation(self):
        """test review"""
        with self.app.app_context():
            user = User(username="testuser", email="test@example.com", password="password")
            book = Book(title="Some Book", author="Some Author", google_books_id="123456")
            db.session.add(user)
            db.session.add(book)
            db.session.commit()
            review = Review(rating=5, text="Great book!", user_id=user.id, book_id=book.id)
            db.session.add(review)
            db.session.commit()
            self.assertIsNotNone(db.session.get(Review, review.id))

if __name__ == '__main__':
    unittest.main()
