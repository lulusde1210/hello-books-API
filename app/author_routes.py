from app import db
from app.models.author import Author
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request
from helper import validate_model

author_bp = Blueprint("authors", __name__, url_prefix="/authors")

# GET


@author_bp.route("", methods=["GET"])
def get_all_authors():
    all_authors = Author.query.all()

    authors_response = [author.to_dict() for author in all_authors]

    return jsonify(authors_response)


@author_bp.route("/<author_id>/books", methods=["GET"])
def get_all_books_of_author(author_id):
    author = validate_model(Author, author_id)
    books_response = []
    for book in author.books:
        books_response.append(book.to_dict())

    return jsonify(books_response)


# POST
@author_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()

    author = Author(name=request_body["name"])

    db.session.add(author)
    db.session.commit()
    return make_response(jsonify(f"Author {author.name} successfully created."), 201)


@author_bp.route("/<author_id>/books", methods=["POST"])
def create_book_for_author(author_id):

    author = validate_model(Author, author_id)

    book_data = request.get_json()
    book = Book.from_dict(book_data)
    book.author = author

    db.session.add(book)
    db.session.commit()

    return make_response(jsonify(f"Book {book.title} by {book.author.name} successfully created"), 201)
