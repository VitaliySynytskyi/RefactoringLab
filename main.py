import datetime
from collections import defaultdict

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.events = []
        self.recommendations = defaultdict(list)

    def add_book(self, title, author):
        self.books[title] = Book(title, author)

    def add_user(self, user_id, name):
        self.users[user_id] = User(user_id, name)

    def checkout_book(self, user_id, title):
        if title in self.books and self.books[title].available:
            book = self.books[title]
            book.available = False
            self.users[user_id].borrowed_books.append(book)
            due_date = datetime.datetime.now() + datetime.timedelta(days=14)
            return f"Book {title} checked out until {due_date.strftime('%Y-%m-%d')}"
        return "This book is currently unavailable"

    def return_book(self, user_id, title):
        if title in self.books:
            book = self.books[title]
            book.available = True
            self.users[user_id].borrowed_books.remove(book)
            return f"Book {title} returned successfully"
        return "This book does not exist"

    def add_event(self, event_name, date):
        self.events.append((event_name, date))

    def recommend_books(self, user_id, genre):
        # Placeholder for recommendation logic
        recommended_books = [book.title for book in self.books.values() if genre in book.title.lower()]
        self.recommendations[user_id].extend(recommended_books)

# Код застосування
library = Library()
library.add_book("Кавказ", "Тарас Шевченко")
library.add_user(1, "Олександр")
print(library.checkout_book(1, "Кавказ"))
library.add_event("Літературний вечір", "2024-12-01")
library.recommend_books(1, "Вій")
