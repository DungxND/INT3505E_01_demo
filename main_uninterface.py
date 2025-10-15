from apiflask import APIFlask, Schema, fields, abort
from flask import url_for
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BooleanField,
    AutoField,
    DoesNotExist,
)

db = SqliteDatabase("books.db")


class Book(Model):
    id = AutoField()
    title = CharField()
    author = CharField()
    available = BooleanField(default=True)

    class Meta:
        database: SqliteDatabase = db


class LinkSchema(Schema):
    href = fields.URL()
    rel = fields.String()
    method = fields.String()


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    available = fields.Boolean(dump_only=True)
    links = fields.List(fields.Nested(LinkSchema), dump_only=True)


app = APIFlask(__name__, docs_ui="elements")

db.connect()
db.create_tables([Book])


def generate_book_links(book):
    links = [
        {
            "href": url_for("get_book", book_id=book.id, _external=True),
            "rel": "self",
            "method": "GET",
        },
        {
            "href": url_for("delete_book", book_id=book.id, _external=True),
            "rel": "delete",
            "method": "DELETE",
        },
    ]
    if book.available:
        links.append(
            {
                "href": url_for("borrow_book", book_id=book.id, _external=True),
                "rel": "borrow",
                "method": "POST",
            }
        )
    else:
        links.append(
            {
                "href": url_for("return_book", book_id=book.id, _external=True),
                "rel": "return",
                "method": "POST",
            }
        )
    return links


@app.route("/books", methods=["GET"])
@app.output(BookSchema(many=True))
def get_books():
    books = list(Book.select())
    for book in books:
        book.links = generate_book_links(book)
    return books


@app.route("/books", methods=["POST"])
@app.input(BookSchema)
@app.output(BookSchema, status_code=201)
def add_book(json_data):
    book = Book.create(title=json_data["title"], author=json_data["author"])
    book.links = generate_book_links(book)
    return book


@app.route("/books/<int:book_id>", methods=["GET"])
@app.output(BookSchema)
def get_book(book_id):
    try:
        book = Book.get(Book.id == book_id)
        book.links = generate_book_links(book)
        return book
    except DoesNotExist:
        abort(404, message="Book not found")


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book = Book.get(Book.id == book_id)
        book.delete_instance()
        return "", 204
    except DoesNotExist:
        abort(404, message="Book not found")


@app.route("/books/<int:book_id>/borrow", methods=["POST"])
@app.output(BookSchema)
def borrow_book(book_id):
    try:
        book = Book.get(Book.id == book_id)
        if not book.available:
            abort(400, message="Book already borrowed")
        book.available = False
        book.save()
        book.links = generate_book_links(book)
        return book
    except DoesNotExist:
        abort(404, message="Book not found")


@app.route("/books/<int:book_id>/return", methods=["POST"])
@app.output(BookSchema)
def return_book(book_id):
    try:
        book = Book.get(Book.id == book_id)
        if book.available:
            abort(400, message="Book not borrowed")
        book.available = True
        book.save()
        book.links = generate_book_links(book)
        return book
    except DoesNotExist:
        abort(404, message="Book not found")


if __name__ == "__main__":
    app.run(debug=True)
