from apiflask import APIFlask, Schema, fields, abort
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BooleanField,
    AutoField,
    DoesNotExist,
)
from flask import request, Response
import hashlib
import json

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


class BookUpdateSchema(Schema):
    title = fields.String()
    author = fields.String()


app = APIFlask(__name__, docs_ui="swagger-ui")
db.connect()


def generate_etag(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


@app.route("/books", methods=["POST"])
@app.input(BookSchema)
@app.output(BookSchema, status_code=201)
def add_book(json_data):
    book = Book.create(title=json_data["title"], author=json_data["author"])
    return book


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    try:
        book = Book.get(Book.id == book_id)
        book_data = BookSchema().dump(book)

        etag = f'"{generate_etag(book_data)}"'

        if_none_match = request.headers.get("If-None-Match")
        if if_none_match and if_none_match == etag:
            return Response(status=304)

        response_data = json.dumps(book_data)
        response = Response(response_data, mimetype="application/json", status=200)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age: 3600, must-revalidate"
        return response

    except DoesNotExist:
        abort(404, message=f"Book with id {book_id} not found")


@app.route("/books/<int:book_id>", methods=["PUT"])
@app.input(BookUpdateSchema)
def update_book(book_id, json_data):
    try:
        book = Book.get(Book.id == book_id)
        book.title = json_data.get("title", book.title)
        book.author = json_data.get("author", book.author)
        book.save()

        updated_book_data = BookSchema().dump(book)
        etag = f'"{generate_etag(updated_book_data)}"'
        response_data = json.dumps(updated_book_data)
        response = Response(response_data, mimetype="application/json", status=200)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age: 3600, must-revalidate"
        return response

    except DoesNotExist:
        abort(404, message=f"Book with id {book_id} not found")


if __name__ == "__main__":
    app.run(debug=True)
