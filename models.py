from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()
db = SQLAlchemy()

class Book(db.Model):
    """Book model."""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    categories = db.Column(db.String(255))
    published_date = db.Column(db.String(50))
    page_count = db.Column(db.Integer)
    average_rating = db.Column(db.Float)
    ratings_count = db.Column(db.Integer)
    maturity_rating = db.Column(db.String(50))
    preview_link = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))
    google_books_id = db.Column(db.String(255), unique=True, nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='book', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Book {self.id}: {self.title}>"

class Author(db.Model):
    """Author model."""
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # Add other fields as needed

class Genre(db.Model):
    """Genre model."""
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # Add other fields as needed

class Review(db.Model):
    """Review model."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user = db.relationship('User', backref='reviews')

class Likes(db.Model):
    """Mapping user likes to books."""

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='cascade'))

    # Define back references if needed
    user = db.relationship('User', backref=db.backref('liked_books', cascade='all, delete'))
    book = db.relationship('Book', backref='liking_users', cascade='all, delete')

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    header_image_url = db.Column(db.Text, default="/static/images/warbler-hero.jpg")
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, username, email, password, image_url, header_image_url):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            header_image_url=header_image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate user."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)
