from app.models.book import Book
import pytest
from werkzeug.exceptions import HTTPException
from app.book_routes import validate_model
from app.models.book import Book

### GET /books test################################


def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_books_return_a_list_of_all_books(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }


def test_get_all_books_with_query_request_returns_title_book(client, two_saved_books):
    query = {"title": "Ocean Book"}
    response = client.get("/books", query_string=query)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_get_all_books_with_query_request_no_match(client, two_saved_books):
    query = {"title": "Story Book"}
    response = client.get("/books", query_string=query)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []


# GET /books/<id> tests#########################################
def test_get_one_book_returns_seeded_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["title"] == "Ocean Book"
    assert response_body["description"] == "watr 4evr"


def test_get_one_book_id_not_found(client, two_saved_books):
    # Act
    response = client.get("/books/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == "Book 100 not found"


def test_get_one_book_invalid_id(client):
    # Act
    response = client.get("/books/taco")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid Book taco"


# POST /books tests#########################################
def test_create_one_book_success(client):
    # Arrange
    expected_book = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.post("/books", json=expected_book)
    response_body = response.get_json()

    # Assert
    actual_book = Book.query.get(1)
    assert response.status_code == 201
    assert response_body == f"Book {expected_book['title']} successfully created"
    assert actual_book.title == expected_book['title']
    assert actual_book.description == expected_book['description']


def test_create_one_book_missing_title(client):
    # Arrange
    data = {"description": "The Best!"}
    response = client.post("/books", json=data)
    response_body = response.get_json()

    assert response_body == "missing required value"

    # with pytest.raises(KeyError, match="title"):
    #     response = client.post("/books", json=data)


def test_create_one_book_missing_description(client):
    # Arrange
    data = {"title": "New Book", }
    response = client.post("/books", json=data)
    response_body = response.get_json()

    assert response_body == "missing required value"

    # with pytest.raises(KeyError, match="description"):
    #     response = client.post("/books", json=data)


def test_create_one_book_with_extra_keys(client):
    # Arrange
    data = {
        "title": "New Book",
        "description": "The Best!",
        "author": "JK"
    }

    # Act
    response = client.post("/books", json=data)
    response_body = response.get_json()

    # Assert
    actual_book = Book.query.get(1)
    assert response.status_code == 201
    assert response_body == f"Book {data['title']} successfully created"
    assert actual_book.title == data['title']
    assert actual_book.description == data['description']


# PUT /books/<id> tests#########################################
def test_update_one_book_success(client, two_saved_books):
    # Arrange
    expected_book = {
        "title": "Updated Book",
        "description": "Updated info"
    }

    # Act
    response = client.put("/books/1", json=expected_book)
    response_body = response.get_json()

    # Assert
    actual_book = Book.query.get(1)
    assert response.status_code == 200
    assert response_body == f"Book {expected_book['title']} successfully updated"
    assert actual_book.title == expected_book['title']
    assert actual_book.description == expected_book['description']


def test_update_one_book_with_extra_data(client, two_saved_books):
    # Arrange
    expected_book = {
        "title": "Updated Book",
        "description": "Updated info",
        "author": "Aiden"
    }

    # Act
    response = client.put("/books/1", json=expected_book)
    response_body = response.get_json()

    # Assert
    actual_book = Book.query.get(1)
    assert response.status_code == 200
    assert response_body == f"Book {expected_book['title']} successfully updated"
    assert actual_book.title == expected_book['title']
    assert actual_book.description == expected_book['description']


def test_update_one_book_id_not_found(client, two_saved_books):
    expected_book = {
        "title": "Updated Book",
        "description": "Updated info",
    }

    # Act
    response = client.put("/books/100", json=expected_book)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == "Book 100 not found"


def test_update_one_book_invalid_id(client):
    expected_book = {
        "title": "Updated Book",
        "description": "Updated info",
    }
    # Act
    response = client.put("/books/taco", json=expected_book)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid Book taco"


# DELETE /books/<id> tests#########################################
def test_delete_one_book_success(client, two_saved_books):
    book = Book.query.get(1)

    # Act
    response = client.delete("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == f"Book {book.title} successfully deleted"


def test_delete_one_book_id_not_found(client, two_saved_books):
    response = client.delete("/books/100")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == f"Book 100 not found"


def test_delete_one_book_invalid_id(client, two_saved_books):
    response = client.delete("/books/taco")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == f"Invalid Book taco"


# validate book tests#########################################
def test_validate_book_successfully(two_saved_books):

    book = validate_model(Book, 1)

    assert book.id == 1
    assert book.title == "Ocean Book"
    assert book.description == "watr 4evr"


def test_validate_model_not_found(two_saved_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached
    with pytest.raises(HTTPException):
        book = validate_model(Book, "100")


def test_validate_book_invalid_id(two_saved_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "taco")
