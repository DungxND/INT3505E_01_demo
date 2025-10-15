from peewee import DoesNotExist
from .models import Book


class BookService:
    def get_all_books(self):
        return list(Book.select())

    def get_book_by_id(self, book_id):
        try:
            return Book.get(Book.id == book_id)
        except DoesNotExist:
            return None

    def create_book(self, data):
        if "title" not in data or "author" not in data:
            return None
        return Book.create(title=data["title"], author=data["author"])

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            book.delete_instance()
            return True
        return False
