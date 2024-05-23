"""Main Application
"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
import requests
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from forms import UserAddForm, LoginForm, UserEditForm, BookSearchForm, ReviewForm
from models import db, connect_db, User, Book, Review, Author, Genre, Likes
from functools import wraps

CURR_USER_KEY = 'curr_user'

# Configure and Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///bookwise'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "Sunnyday24.")
app.config['API_KEY'] = 'AIzaSyC2be_H14--bzjwo578LlDj1Ab8iFBPYpE'

connect_db(app)

##############################################################################
# User login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    print(f"User {user.username} logged in.")


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        print(f"User {g.user.username} logged out.")
        del session[CURR_USER_KEY]

    """Handles auth if not logged in."""
def redirect_if_missing(func):
    """Handles auth if not logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper

##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage:
    - anon users: no messages
    - logged in: 100 most recent reviews
    """

    if g.user:
        reviews = (Review
                    .query
                    .filter(Review.user_id == g.user.id)
                    .order_by(Review.id.desc())
                    .limit(100)
                    .all())

        return render_template('home.html', reviews=reviews)

    else:
        return render_template('home-anon.html')
####################################################################
# User Signup route..

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserAddForm()

    if form.is_submitted() and form.validate():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                header_image_url=form.header_image_url.data or User.header_image_url.default.arg,
            )
            db.session.commit()
            print(f"User {user.username} signed up successfully.")
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)

########################################################################### User Login route...
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.is_submitted() and form.validate():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

########################################################################### User Logout route...
@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logged out", "success")
    return redirect('/login')


##################################Users Profile
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    reviews = (Review
                .query
                .filter(Review.user_id == user_id)
                .order_by(Review.id.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, reviews=reviews)


@app.route('/users/profile', methods=["GET", "POST"])
@redirect_if_missing
def profile():
    """Update profile for current user."""

    form = UserEditForm(obj=g.user)
    if form.is_submitted() and form.validate():
        user = User.authenticate(g.user.username, form.password.data)
        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.header_image_url = form.header_image_url.data
            db.session.add(user)
            db.session.commit()
            print(f"User {user.username} profile updated successfully.")
            return redirect(f"/users/{user.id}")
        flash('Incorrect password.', "danger")
        return redirect('/')
    return render_template('users/edit.html',form=form)

@app.route('/users/delete', methods=["POST"])
@redirect_if_missing
def delete_user():
    """Delete user."""

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash(f"{g.user.username} has been deleted.", "success")
    return redirect("/signup")

##################### Route for book search...
@app.route('/search', methods=['GET', 'POST'])
def search_books():
    """Search for books using the Google Books API."""
    form = BookSearchForm()
    books = []
    if form.validate_on_submit():
        keyword = form.keyword.data
        url = f"https://www.googleapis.com/books/v1/volumes?q={keyword}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])
            for item in items:
                volume_info = item['volumeInfo']
                book = Book(
                    title=volume_info['title'],
                    author=', '.join(volume_info.get('authors', [])),
                    google_books_id=item['id'],
                    # Add other fields as necessary
                )
                db.session.add(book)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()  # Handle duplicate google_books_id
            return render_template('search_results.html', books=items, curr_user=g.user)
        except requests.exceptions.Timeout as e:
            flash(f"Request timed out: {e}", "warning")
            return render_template('search.html', form=form)
        except requests.exceptions.RequestException as e:
            flash(f"Failed to fetch book data: {e}", "danger")
            return render_template('search.html', form=form)

    return render_template('search.html', form=form)


@app.route('/search_results')
def search_results():
    """Display search results."""
    books = []  # Define the "books" variable as an empty list
    return render_template('search_results.html', books=books, curr_user=g.user)


#################################################### Route for displaying book details...
@app.route('/book/<book_id>')
def book_details(book_id):
    """Display details of a book."""
    book = Book.query.get_or_404(book_id)
    print(f"Displaying details for book: {book.title}")
    return render_template('book_details.html', book=book)

######################################################## Route for liking and unliking book...

@app.route('/like/<book_id>', methods=['POST'])
@redirect_if_missing
def like_book(book_id):
    """Like a book."""
    try:
        book = Book.query.filter_by(google_books_id=book_id).first_or_404()
        if book:
            like = Likes(user_id=g.user.id, book_id=book.id)
            db.session.add(like)
            db.session.commit()
            flash(f"You liked '{book.title}'.", "success")
            print(f"User {g.user.username} liked the book: {book.title}")
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback any changes made to the database session
        flash("An error occurred while liking the book. Please try again later.", "error")
        app.logger.error(f"Error liking book: {e}")  # Log the error for debugging purposes
    return redirect(request.referrer or '/')


@app.route('/unlike/<book_id>', methods=['POST'])
@redirect_if_missing
def unlike_book(book_id):
    """Unlike a book."""
    like = Likes.query.filter_by(user_id=g.user.id, book_id=book_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash("You unliked the book.", "success")
        print(f"User {g.user.username} unliked the book with ID {book_id}")
    return redirect(request.referrer or '/')


############################################ Route for adding a review...
@app.route('/review/<book_id>', methods=['GET', 'POST'])
@redirect_if_missing
def add_review(book_id):
    """Add a review for a book."""
    book = Book.query.get_or_404(book_id)
    print(f"Adding review for book: {book.title}")
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            text=form.comment.data,  # Update to match your ReviewForm
            user_id=g.user.id,
            book_id=book.id
        )
        db.session.add(review)
        db.session.commit()
        flash("Your review has been added.", "success")
        return redirect(url_for('book_details', book_id=book_id))

    return render_template('review.html', form=form, book=book)

if __name__ == "__main__":
    app.run()
