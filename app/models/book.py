from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author = db.relationship("Author", back_populates="books")
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))

    @classmethod
    def from_dict(cls, book_dict):
        book = cls(
            title=book_dict["title"],
            description=book_dict["description"]
        )

        return book

    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description
        book_as_dict["author_id"] = self.author_id

        return book_as_dict
