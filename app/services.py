from .models import Book
from peewee import DoesNotExist

class BookService:
    def get_all_books(self):
        return list(Book.select())

    def create_book(self, data):
        if "title" not in data or "author" not in data:
            return None
        return Book.create(title=data["title"], author=data["author"])

    def get_book_by_id(self, book_id):
        try:
            return Book.get(Book.id == book_id)
        except DoesNotExist:
            return None

    def delete_book(self, book_id):
        try:
            book = Book.get(Book.id == book_id)
            book.delete_instance()
            return True
        except DoesNotExist:
            return False

    def borrow_book(self, book_id):
        try:
            book = Book.get(Book.id == book_id)
            if not book.available:
                return None, "Book already borrowed"
            book.available = False
            book.save()
            return book, None
        except DoesNotExist:
            return None, "Book not found"

    def return_book(self, book_id):
        try:
            book = Book.get(Book.id == book_id)
            if book.available:
                return None, "Book not borrowed"
            book.available = True
            book.save()
            return book, None
        except DoesNotExist:
            return None, "Book not found"