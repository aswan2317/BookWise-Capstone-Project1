# BookWise

## Project Overview

BookWise is a book recommendation and review platform designed to enhance the reading experience.
Users can search for books, read detailed information about them, like and review books, and manage their profile.
A user can even view and buy a book on Google. 

## Deployed URL

[BookWise - Live Site](https://bookwise-capstone-project1.onrender.com)

## What BookWise Does

BookWise allows users to:
- Search for books using keywords.
- View detailed information about books including the author, publication date, page count, and more.
- Like and unlike books to keep track of their favorite reads.
- Write and edit reviews for books they have read.
- Manage their profile including updating their profile information and viewing their liked books and reviews.

## Features Implemented

1. **User Authentication**:
   - Users can sign up, log in, and log out.
   - Profile management including editing profile information and password confirmation for changes.
   
2. **Book Search and Details**:
   - Users can search for books by keywords.
   - Display detailed information about each book including cover image, author, publication date, and more.
   
3. **Book Likes and Reviews**:
   - Users can like and unlike books.
   - Users can write, edit, and delete reviews for books.
   
4. **User Dashboard**:
   - Display a list of liked books and reviews on the user's profile page.
   - Allow users to manage their liked books and reviews easily.

## Standard User Flow

1. **Home Page**:
   - For anonymous users: A call to action to sign up for personalized book recommendations.
   - For logged-in users: Display user profile information and lists of liked books and reviews.

2. **Sign Up**:
   - New users can sign up by providing their email, username, and password.

3. **Log In**:
   - Returning users can log in using their email and password.

4. **Search Books**:
   - Users can search for books using keywords.
   - Search results display a list of books matching the keyword.

5. **Book Details**:
   - Users can view detailed information about a book by clicking on it from the search results or their liked books list.
   - Users can like/unlike the book and add/edit reviews.

6. **Profile Management**:
   - Users can view and edit their profile information.
   - Users can view and manage their liked books and reviews from their profile page.

## API Used

BookWise utilizes the Google Books API to fetch book data. The API provides comprehensive information about books which includes:
- Book titles, authors, and cover images.
- Publication dates, page counts, and categories.
- User ratings and reviews.

### Notes on the API

The Google Books API is reliable and offers a wide range of data points for each book. It enhances the user 
experience by providing detailed and accurate information.

## Technology Stack

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap

- **Backend**:
  - Python
  - Flask
  - Jinja2 (templating engine)

- **Database**:
  - SQLite (for development)
  - SQLAlchemy (ORM)

- **APIs**:
  - Google Books API

## Additional Information

- **Responsive Design**: The site is fully responsive, ensuring a seamless experience across different devices.
- **Security**: User passwords are hashed for secure storage.
- **Error Handling**: Comprehensive error handling to manage form errors and display appropriate messages to users.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/aswan2317/bookwise.git
