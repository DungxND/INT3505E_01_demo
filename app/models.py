from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BooleanField,
    AutoField,
)

db = SqliteDatabase("books.db")

class Book(Model):
    id = AutoField()
    title = CharField()
    author = CharField()
    available = BooleanField(default=True)

    class Meta:
        database: SqliteDatabase = db

def initialize_database():
    db.connect(reuse_if_open=True)
    db.create_tables([Book])