import requests
from apiflask import APIFlask, Schema, fields, abort
from flask import Blueprint, request
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
        database = db

def initialize_database():
    db.connect(reuse_if_open=True)
    db.create_tables([Book])

webhooks = []

def trigger_webhook(event_type, data):
    payload = {"event": event_type, "data": data}
    for url in webhooks:
        try:
            requests.post(url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook to {url}: {e}")

class BookService:
    def create_book(self, data):
        if "title" not in data or "author" not in data:
            return None
        book = Book.create(title=data["title"], author=data["author"])
        trigger_webhook("book_created", {"id": book.id, "title": book.title})
        return book

    def get_book_by_id(self, book_id):
        try:
            return Book.get(Book.id == book_id)
        except DoesNotExist:
            return None

app = APIFlask(__name__, title="API Versioning and Webhook Demo")
book_service = BookService()

bp_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")

class BookV1Schema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    author = fields.String()

@bp_v1.route("/books/<int:book_id>", methods=["GET"])
@app.output(BookV1Schema)
def get_book_v1(book_id):
    book = book_service.get_book_by_id(book_id)
    if book is None:
        abort(404, message=f"Book with id {book_id} not found")
    return book

bp_v2 = Blueprint("api_v2", __name__, url_prefix="/v2")

class BookV2Schema(Schema):
    id = fields.Integer(dump_only=True)
    full_title = fields.String(dump_only=True)
    author = fields.String()
    is_available = fields.Boolean(attribute="available")

// Query param
@bp_v2.route("/books/<int:book_id>", methods=["GET"])
@app.output(BookV2Schema)
def get_book_v2(book_id):
    book = book_service.get_book_by_id(book_id)
    if book is None:
        abort(404, message=f"Book with id {book_id} not found")
    book.full_title = f"{book.title} by {book.author}"
    return book

class BookCreateSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)

@app.route("/books", methods=["POST"])
@app.input(BookCreateSchema)
@app.output(BookV1Schema, status_code=201)
def add_book(json_data):
    book = book_service.create_book(json_data)
    return book

class WebhookSchema(Schema):
    url = fields.URL(required=True)

@app.route("/webhooks/register", methods=["POST"])
@app.input(WebhookSchema)
@app.output({}, status_code=201)
def register_webhook(json_data):
    webhooks.append(json_data["url"])
    print(f"Webhook registered: {json_data['url']}")
    return ""

app.register_blueprint(bp_v1)
app.register_blueprint(bp_v2)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=5001)