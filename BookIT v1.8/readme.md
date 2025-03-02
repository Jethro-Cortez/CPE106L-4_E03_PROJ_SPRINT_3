# BookIT

BookIT is a modern, open-source library management system built with Python and Flask. It allows users to manage their library, borrow books, leave reviews, and track their reading history. The application features an intuitive user interface and provides analytics for both users and administrators.

## Features

- User registration and authentication
- Book borrowing and returning functionality
- Admin dashboard for managing books and users
- User dashboard for tracking borrowed books and reading history
- Feedback and rating system for books
- Search functionality for books
- Responsive design with dark mode support

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- HTML/CSS/JavaScript
- Bootstrap
- Plotly for analytics visualization

### Issues

1. User authentication issues (e.g., password resets, login failures)
2. Database connection errors
3. Data validation errors (e.g., invalid inputs)
4. Book availability issues (e.g., borrowing unavailable books)
5. Feedback submission problems (e.g., empty messages, invalid ratings)
6. Performance issues with large datasets
7. Security vulnerabilities (e.g., SQL injection, XSS)
8. User interface (UI) issues (e.g., non-intuitive design, responsiveness)
9. Error handling and logging problems
10. Deployment challenges (e.g., configuration mismatches)
11. Backup and data recovery issues
12. User role management problems (e.g., incorrect permissions)
13. Analytics and reporting inaccuracies
14. Integration issues with external services
15. User feedback and feature request management

## Installation

To get started with BookIT, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jethro-Cortez/CPE106L-4_E03_PROJ_SPRINT_3/edit/CAPULI-backup/BookIT%20v1.8.git
   cd BookIT
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   flask run
   ```

7. **Access the application:** Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

- **User Registration:** Users can create an account to start borrowing books.
- **Book Management:** Admins can add, edit, and delete books from the library.
- **Borrowing Books:** Users can borrow books for a specified period and return them.
- **Feedback System:** Users can leave reviews and ratings for books they have read.
