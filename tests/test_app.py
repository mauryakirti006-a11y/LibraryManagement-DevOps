import sqlite3
import pytest

from app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_library.db")
    monkeypatch.setenv("DB_PATH", db_path)

    init_db()

    app.config["TESTING"] = True
    app.config["TEST_DB_PATH"] = db_path

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Library Management System" in response.data


def test_add_and_search_book(client):
    client.post(
        "/add",
        data={
            "title": "Python Basics",
            "author": "John Smith",
            "isbn": "ISBN-001"
        }
    )

    response = client.get("/?search=Python")

    assert response.status_code == 200
    assert b"Python Basics" in response.data
    assert b"ISBN-001" in response.data


def test_edit_and_delete_book(client):
    client.post(
        "/add",
        data={
            "title": "Old Title",
            "author": "Jane",
            "isbn": "ISBN-002"
        }
    )

    db_path = app.config["TEST_DB_PATH"]

    with sqlite3.connect(db_path) as conn:
        book_id = conn.execute(
            "SELECT id FROM books WHERE isbn = ?",
            ("ISBN-002",)
        ).fetchone()[0]

    client.post(
        f"/edit/{book_id}",
        data={
            "title": "New Title",
            "author": "Jane",
            "isbn": "ISBN-002"
        }
    )

    response = client.get("/")
    assert b"New Title" in response.data

    client.post(f"/delete/{book_id}")

    response = client.get("/")
    assert b"New Title" not in response.data
