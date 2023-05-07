from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
import os
# This built-in module provides a way to read environment variables

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()
# this loads the values from our .env file so that the os module is able to see them.


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'SQLALCHEMY_DATABASE_URI')

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    from .book_routes import books_bp
    app.register_blueprint(books_bp)

    from .author_routes import author_bp
    app.register_blueprint(author_bp)

    from app.models.book import Book

    return app
