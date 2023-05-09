from app.models.book import Book
from app.models.author import Author


def test_to_dict_with_no_missing_data():
    book = Book(
        id=1,
        title="Ocean Book",
        description="watr 4evr"
    )

    result = book.to_dict()

    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"


def test_to_dict_with_missing_id():
    book = Book(
        title="Ocean Book",
        description="watr 4evr"
    )

    result = book.to_dict()

    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"


def test_to_dict_with_missing_title():
    book = Book(
        id=1,
        description="watr 4evr"
    )

    result = book.to_dict()

    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "watr 4evr"


def test_to_dict_with_missing_description():
    book = Book(
        id=1,
        title="Ocean Book",
    )

    result = book.to_dict()

    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] is None


# def test_from_dict_with_no_missing_data():
#     book_dict = {
#         "title": "Great Book",
#         "description": "This is a great book!"
#     }

#     book = Book.from_dict(book_dict)

#     assert book.title == book_dict["title"]
#     assert book.description == book_dict["description"]


# def test_from_dict_with_missing_title():
#     book_dict = {
#         "description": "This is a great book!"
#     }

#     book = Book.from_dict(book_dict)

#     assert book.title is None
#     assert book.description == book_dict["description"]
