from apiflask import APIFlask, Schema, fields, abort

from .models import initialize_database
from .services import BookService


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    available = fields.Boolean(dump_only=True)


app = APIFlask(__name__, docs_ui="elements")

book_service = BookService()

initialize_database()


@app.route("/books", methods=["GET"])
@app.output(BookSchema(many=True))
def get_books():
    books = book_service.get_all_books()
    return books


@app.route("/books", methods=["POST"])
@app.input(BookSchema)
@app.output(BookSchema, status_code=201)
def add_book(json_data):
    book = book_service.create_book(json_data)
    if book is None:
        abort(400, "Invalid: title and author are required.")
    return book


@app.route("/books/<int:book_id>", methods=["GET"])
@app.output(BookSchema)
def get_book(book_id):
    book = book_service.get_book_by_id(book_id)
    if book is None:
        abort(404, message=f"Book {book_id} not found")
    return book


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    success = book_service.delete_book(book_id)
    if not success:
        abort(404, message=f"Book {book_id} not found")
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
