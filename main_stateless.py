from apiflask import APIFlask, Schema, fields, abort
import jwt
import datetime
from functools import wraps
from flask import request

users = {}

SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


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


app = APIFlask(__name__, title="Stateless", docs_ui="elements")


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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
