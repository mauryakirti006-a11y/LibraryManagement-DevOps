import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.secret_key = "library-demo-key"

# Prometheus automatically exposes /metrics
metrics = PrometheusMetrics(app)


def get_db():
    path = os.environ.get("DB_PATH", "data/library.db")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE
            )
        """)


@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    with get_db() as conn:
        if search:
            books = conn.execute(
                """SELECT * FROM books
                   WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
                   ORDER BY id DESC""",
                (f"%{search}%", f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            books = conn.execute(
                "SELECT * FROM books ORDER BY id DESC"
            ).fetchall()
    return render_template("index.html", books=books, search=search)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()

    if not title or not author or not isbn:
        flash("Please fill in all fields.")
        return redirect(url_for("index"))

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
                (title, author, isbn)
            )
        flash("Book added successfully!")
    except sqlite3.IntegrityError:
        flash("This ISBN already exists.")

    return redirect(url_for("index"))


@app.route("/edit/<int:book_id>", methods=["POST"])
def edit_book(book_id):
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()

    if not title or not author or not isbn:
        flash("All fields are required.")
        return redirect(url_for("index"))

    try:
        with get_db() as conn:
            conn.execute(
                "UPDATE books SET title=?, author=?, isbn=? WHERE id=?",
                (title, author, isbn, book_id)
            )
        flash("Book updated successfully!")
    except sqlite3.IntegrityError:
        flash("This ISBN already exists.")

    return redirect(url_for("index"))


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    with get_db() as conn:
        conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    flash("Book deleted.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
