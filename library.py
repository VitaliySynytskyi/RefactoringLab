import datetime

class BookDecorator:
    """ Декоратор для розширення функціональності книг """
    def __init__(self, book):
        self._book = book

    def __getattr__(self, attr):
        return getattr(self._book, attr)

class BookWithTracking(BookDecorator):
    """ Додає можливість відстеження статусу книги """
    def check_status(self):
        return f"Книга '{self._book.title}' має статус 'на руках'"

class Library:
    """ Фасад для спрощення взаємодії з базою даних """
    def __init__(self, db):
        self.db = db

    def add_book(self, title, author):
        self.db.execute('''
            INSERT INTO books (title, author) VALUES (?, ?)
        ''', (title, author))

    def checkout_book(self, user_id, title):
        book = self.db.query('SELECT id FROM books WHERE title = ?', (title,))
        if book:
            book_id = book[0][0]
            due_date = datetime.datetime.now() + datetime.timedelta(days=14)
            self.db.execute('''
                INSERT INTO checkouts (user_id, book_id, due_date) VALUES (?, ?, ?)
            ''', (user_id, book_id, due_date))
            return f"Книга '{title}' видана користувачу {user_id} до {due_date}"
        return "Ця книга недоступна"

    def return_book(self, user_id, title):
        book = self.db.query('SELECT id FROM books WHERE title = ?', (title,))
        if book:
            book_id = book[0][0]
            checkout = self.db.query('SELECT due_date, user_id FROM checkouts WHERE book_id = ? AND user_id = ?', (book_id, user_id))
            if checkout:
                due_date = datetime.datetime.strptime(checkout[0][0], '%Y-%m-%d %H:%M:%S.%f')
                if datetime.datetime.now() > due_date:
                    days_late = (datetime.datetime.now() - due_date).days
                    fine = days_late * 5  # Наприклад, штраф 5 грн за день
                    return f"Книга повернута користувачем {checkout[0][1]} зі штрафом {fine} гривень"
                return f"Книга повернута користувачем {checkout[0][1]} вчасно"
            return "Книга не була видана цьому користувачу"
        return "Такої книги не існує"
    