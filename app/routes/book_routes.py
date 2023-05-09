from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request
from helper import validate_model

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET"])
def get_all_books():
    title_query = request.args.get("title")

    if title_query:
        all_books = Book.query.filter_by(title=title_query)
    else:
        all_books = Book.query.all()

    books_resonse = [book.to_dict() for book in all_books]

    return jsonify(books_resonse)


@books_bp.route("/<id>", methods=["GET"])
def get_one_book(id):
    book = validate_model(Book, id)
    return jsonify(book.to_dict())


@books_bp.route("", methods=["POST"])
def create_a_book():
    book_data = request.get_json()

    try:
        new_book = Book.from_dict(book_data)
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)
    except KeyError as e:
        abort(make_response(jsonify(f"missing required value")), 400)


@books_bp.route("/<id>", methods=["PUT"])
def update_one_book(id):
    book_data = request.get_json()
    book = validate_model(Book, id)

    book.title = book_data["title"]
    book.description = book_data["description"]
    db.session.commit()

    return make_response(jsonify(f"Book {book.title} successfully updated"), 200)


@books_bp.route("/<id>", methods=["DELETE"])
def delete_one_book(id):
    book = validate_model(Book, id)
    db.session.delete(book)
    db.session.commit()
    return make_response(jsonify(f"Book {book.title} successfully deleted"), 200)
