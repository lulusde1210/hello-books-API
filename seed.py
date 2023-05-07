

from app import create_app, db
from app.models.book import Book

my_app = create_app()
with my_app.app_context():
    db.session.add(
        Book(title="Pepper Book", description="some info about Pepper Book"))
    db.session.add(Book(title="Constance Book",
                   description="some info about Constance Book"))
    db.session.add(Book(title="Rhubarb Book",
                   description="some info about Rhubarb Book"))
    db.session.add(
        Book(title="Kiki Book", description="some info about Kiki Book"))
    db.session.commit()
