from flask import Blueprint, render_template, redirect, url_for, flash, request, abort,  current_app
from .models import User, Book, Transaction, Feedback
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import func
from lms_app import db
from lms_app.models import Transaction
from datetime import datetime, timedelta
from slugify import slugify
import os
import time

main = Blueprint('main', __name__)

@main.after_request
def add_ngrok_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

# 🏠 Home Page
@main.route('/')
def index():
    current_time = datetime.now()
    current_year = current_time.year
    return render_template('index.html', current_time=current_time, current_year=current_year)

# 🔑 Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            if user.is_active:
                login_user(user)
                flash("Logged in successfully! ✅", "success")
                return redirect(url_for('main.admin_dashboard' if user.role == 'admin' else 'main.user_dashboard'))
            else:
                flash("Account is inactive. Please contact admin.", "warning")
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

# 📝 Register
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # ✅ Capture email
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 🔐 Simple Validation
        if not username or not email or not password:
            flash("All fields are required!", "warning")
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash("Passwords do not match!", "warning")
            return redirect(url_for('main.register'))

        # ✅ Check for existing email/username
        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "danger")
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash("Username is already taken.", "danger")
            return redirect(url_for('main.register'))

        # 🔐 Hash the password
        hashed_password = generate_password_hash(password)

        # 💾 Create new user
        new_user = User(username=username, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error during registration: {e}", "danger")
            return redirect(url_for('main.register'))

    return render_template('register.html')

# 🔓 Logout Route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out. 👋", "success")
    return redirect(url_for('main.login'))

# 👤 User Dashboard
@main.route('/user_dashboard')
@login_required
def user_dashboard():
    # 📅 Current Loans
    current_loans = Transaction.query.filter_by(user_id=current_user.id, status='Borrowed').all()

    # 🏆 Reading History
    reading_history = Transaction.query.filter_by(user_id=current_user.id, status='Returned').all()

    # 📖 Simple AI Recommendation (Based on Borrowed Genres)
    borrowed_genres = db.session.query(Book.genre, func.count(Book.id))\
        .join(Transaction, Book.id == Transaction.book_id)\
        .filter(Transaction.user_id == current_user.id)\
        .group_by(Book.genre)\
        .order_by(func.count(Book.id).desc())\
        .first()

    if borrowed_genres:
        recommended_books = Book.query.filter_by(genre=borrowed_genres[0]).limit(5).all()
    else:
        recommended_books = Book.query.limit(5).all()

    return render_template('user_dashboard.html',
                           current_loans=current_loans,
                           reading_history=reading_history,
                           recommended_books=recommended_books)


# 👑 Admin Dashboard (Protected)
@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)

    # 📈 Borrow Trends (Most Borrowed Books)
    borrow_trends = db.session.query(Book.title, func.count(Transaction.id).label('borrow_count'))\
        .join(Transaction, Book.id == Transaction.book_id)\
        .group_by(Book.title)\
        .order_by(func.count(Transaction.id).desc())\
        .limit(5).all()

    # 🏆 Get the Top Book (Most Borrowed)
    top_book = db.session.query(Book.title, func.count(Transaction.id).label('borrow_count'))\
        .join(Transaction, Book.id == Transaction.book_id)\
        .group_by(Book.title)\
        .order_by(func.count(Transaction.id).desc())\
        .first()

    # 📚 Inventory Overview
    total_books = Book.query.count()
    borrowed_books = Transaction.query.filter_by(status='Borrowed').count()
    available_books = total_books - borrowed_books

    # 👥 Active Users
    active_users = db.session.query(User.username, func.count(Transaction.id).label('books_borrowed'))\
        .join(Transaction, User.id == Transaction.user_id)\
        .group_by(User.username)\
        .order_by(func.count(Transaction.id).desc())\
        .limit(5).all()

    return render_template('admin_dashboard.html',
                           borrow_trends=borrow_trends,
                           top_book=top_book,  # 🟢 Pass top_book to Template
                           total_books=total_books,
                           borrowed_books=borrowed_books,
                           available_books=available_books,
                           active_users=active_users)


# 📖 Book Details
@main.route('/book/<slug>', methods=['GET'])
@login_required
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first_or_404()
    feedbacks = Feedback.query.filter_by(book_id=book.id).all()
    average_rating = db.session.query(func.avg(Feedback.rating)).filter_by(book_id=book.id).scalar() or 0
    return render_template('book_details.html', book=book, feedbacks=feedbacks, average_rating=round(average_rating, 1))

# 📚 Borrow Book
@main.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    due_date = datetime.utcnow() + timedelta(days=14)  # 14-day borrow window
    new_transaction = Transaction(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date
    )
    db.session.add(new_transaction)
    db.session.commit()
    flash(f"Book borrowed! Due on {due_date.strftime('%Y-%m-%d')}", 'success')
    return redirect(url_for('main.user_dashboard'))

# 📅 Return Book
@main.route('/return/<int:transaction_id>', methods=['POST'])
@login_required
def return_book(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction.return_date = datetime.utcnow()

    # 💰 Fine Calculation
    if transaction.return_date > transaction.due_date:
        days_overdue = (transaction.return_date - transaction.due_date).days
        fine_rate = 1.0  # $1 per day overdue
        transaction.fine_amount = days_overdue * fine_rate
        transaction.status = 'Overdue'
        flash(f'Book returned late. Fine: ${transaction.fine_amount:.2f}', 'warning')
    else:
        transaction.status = 'Returned'
        flash('Book returned on time. ✅', 'success')

    db.session.commit()
    return redirect(url_for('main.user_dashboard'))
    
# 🟢 Clear Fine (User/Manual)
@main.route('/clear_fine/<int:transaction_id>', methods=['POST'])
@login_required
def clear_fine(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.fine_amount > 0:
        transaction.fine_amount = 0
        db.session.commit()
        flash('Fine cleared. 💸', 'success')
    return redirect(url_for('main.user_dashboard'))

# 📨 Add Feedback Linked to Book
@main.route('/add_feedback/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_feedback(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        message = request.form.get('review_text') 
        rating = request.form.get('rating') 

        if not message:
            flash('Message is required!', 'danger')
            return render_template('feedback.html', book=book)

        feedback = Feedback(user_id=current_user.id, book_id=book.id, message=message, rating=rating)

        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted!', 'success')
            return redirect(url_for('main.book_details', slug=book.slug))
        except Exception as e:
            db.session.rollback()  # Rollback the session on error
            flash(f'Error submitting feedback: {e}', 'danger')

    feedbacks = Feedback.query.filter_by(book_id=book.id).all()  # Fetch existing feedbacks for the book
    return render_template('feedback.html', book=book, feedbacks=feedbacks)  # Pass the book and feedbacks

# 👑 Secure Admin Registration (with Secret Key in URL Params)
@main.route('/adminreg', methods=['GET', 'POST'])
def admin_register():
    secret_key = request.args.get('key')
    if secret_key != 'sinigangmix':
        abort(403)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # 🟢 Capture Email
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        # ✅ Check for Missing Fields
        if not username or not email or not password:
            flash('All fields are required!', 'warning')
            return redirect(url_for('main.admin_register', key=secret_key))

        new_admin = User(username=username, email=email, password_hash=hashed_password, role='admin')

        try:
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin registration successful! ✅ Please log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f'Error during admin registration: {e}', 'danger')


    return render_template('adminreg.html')

@main.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        description = request.form.get('description')
        quantity = request.form.get('quantity', type=int)
        cover_file = request.files.get('cover')
        cover_filename = None

        if cover_file and cover_file.filename != '':
            cover_dir = os.path.join(current_app.root_path, 'static', 'covers')
            os.makedirs(cover_dir, exist_ok=True)
            
            cover_filename = f"{slugify(title)}-{int(time.time())}.{secure_filename(cover_file.filename).split('.')[-1]}"
            cover_path = os.path.join(cover_dir, cover_filename)
            cover_file.save(cover_path)

        if not title or not author or quantity is None or quantity < 1:
            flash("Title, Author, and Quantity (must be at least 1) are required.", "warning")
            return redirect(url_for('main.add_book'))

        # Save Book
        new_book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
            quantity=quantity,
            cover=cover_filename,
            publication_year=request.form.get('publication_year'),
            isbn=request.form.get('isbn')
        )
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully! 📚", "success")
        return redirect(url_for('main.admin_dashboard'))

    return render_template('add_book.html')
   

