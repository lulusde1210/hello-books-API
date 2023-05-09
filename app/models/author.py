from app import db


# "Author is the parent table"
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    books = db.relationship("Book", back_populates="author")

    def to_dict(self):
        author_as_dict = {}
        author_as_dict["id"] = self.id
        author_as_dict["name"] = self.name

        return author_as_dict

    @classmethod
    def from_dict(cls, author_dict):
        author = cls(
            name=author_dict["title"],
            description=author_dict["description"]
        )

        return author
