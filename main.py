from apiflask import APIFlask, Schema, fields, abort
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


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    available = fields.Boolean(dump_only=True)


app = APIFlask(__name__, docs_ui="elements")

db.connect()
db.create_tables([Book])


@app.route("/books", methods=["GET"])
@app.output(BookSchema(many=True))
def get_books():
    return list(Book.select())


@app.route("/books", methods=["POST"])
@app.input(BookSchema)
@app.output(BookSchema, status_code=201)
def add_book(json_data):
    book = Book.create(title=json_data["title"], author=json_data["author"])
    return book


@app.route("/books/<int:book_id>", methods=["GET"])
@app.output(BookSchema)
def get_book(book_id):
    try:
        return Book.get(Book.id == book_id)
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
        return book
    except DoesNotExist:
        abort(404, message="Book not found")


if __name__ == "__main__":
    app.run(debug=True)
