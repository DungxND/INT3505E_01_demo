from apiflask import APIFlask, Schema, fields, abort
from flask import request, Response, url_for
import hashlib
import json
import jwt
import datetime
from functools import wraps
from .services import BookService
from .models import initialize_database


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


class BookUpdateSchema(Schema):
    title = fields.String()
    author = fields.String()


class RegisterSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.String(dump_only=True)


class TokenSchema(Schema):
    token = fields.String()
    message = fields.String()
    user = fields.Nested(UserSchema)


class MessageSchema(Schema):
    message = fields.String()


app = APIFlask(__name__, docs_ui="swagger-ui")
initialize_database()
book_service = BookService()

users = {}
SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def generate_etag(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


def generate_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                abort(401, message="Invalid token format. Use Bearer")

        if not token:
            abort(401, message="Token missing")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            current_username = payload["username"]

            if current_username not in users:
                abort(401, message="User not found")

            current_user = users[current_username]

        except jwt.ExpiredSignatureError:
            abort(401, message="Token expired")
        except jwt.InvalidTokenError:
            abort(401, message="Invalid token")

        return f(current_user=current_user, *args, **kwargs)

    return decorated


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


@app.route("/register", methods=["POST"])
@app.input(RegisterSchema)
@app.output(MessageSchema, status_code=201)
def register(json_data):
    username = json_data["username"]
    email = json_data["email"]
    password = json_data["password"]

    if username in users:
        abort(400, message="Username already exists")

    for user in users.values():
        if user["email"] == email:
            abort(400, message="Email already exists")

    user_id = len(users) + 1
    users[username] = {
        "id": user_id,
        "username": username,
        "email": email,
        "password": password,
    }

    return {"message": f"User '{username}' registered successfully!"}


@app.route("/login", methods=["POST"])
@app.input(LoginSchema)
@app.output(TokenSchema)
def login(json_data):
    username = json_data["username"]
    password = json_data["password"]

    if username not in users:
        abort(401, message="Invalid username or password")

    user = users[username]

    if user["password"] != password:
        abort(401, message="Invalid username or password")

    token = generate_token(user["id"], user["username"])

    return {
        "token": token,
        "message": "Login successful!",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        },
    }


@app.route("/profile", methods=["GET"])
@app.output(UserSchema)
@token_required
def get_profile(current_user):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
    }


@app.route("/books", methods=["POST"])
@app.input(BookSchema)
@app.output(BookSchema, status_code=201)
def add_book(json_data):
    book = book_service.create_book(json_data)
    if book is None:
        abort(400, "Invalid: title and author are required.")
    book.links = generate_book_links(book)
    return book


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = book_service.get_book_by_id(book_id)
    if book is None:
        abort(404, message=f"Book with id {book_id} not found")

    book.links = generate_book_links(book)
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


@app.route("/books/<int:book_id>", methods=["PUT"])
@app.input(BookUpdateSchema)
def update_book(book_id, json_data):
    book = book_service.get_book_by_id(book_id)
    if book is None:
        abort(404, message=f"Book with id {book_id} not found")

    book.title = json_data.get("title", book.title)
    book.author = json_data.get("author", book.author)
    book.save()

    book.links = generate_book_links(book)
    updated_book_data = BookSchema().dump(book)
    etag = f'"{generate_etag(updated_book_data)}"'
    response_data = json.dumps(updated_book_data)
    response = Response(response_data, mimetype="application/json", status=200)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age: 3600, must-revalidate"
    return response


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    success = book_service.delete_book(book_id)
    if not success:
        abort(404, message=f"Book {book_id} not found")
    return "", 204


@app.route("/books/<int:book_id>/borrow", methods=["POST"])
@app.output(BookSchema)
def borrow_book(book_id):
    book, error = book_service.borrow_book(book_id)
    if error:
        abort(400, message=error)
    book.links = generate_book_links(book)
    return book


@app.route("/books/<int:book_id>/return", methods=["POST"])
@app.output(BookSchema)
def return_book(book_id):
    book, error = book_service.return_book(book_id)
    if error:
        abort(400, message=error)
    book.links = generate_book_links(book)
    return book


if __name__ == "__main__":
    app.run(debug=True)
