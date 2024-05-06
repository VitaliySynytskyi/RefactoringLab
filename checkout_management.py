class CheckoutObserver:
    """ Спостерігач за процесом видачі та повернення книг. """
    def update(self, message):
        print(message)

class CheckoutManager:
    """ Управління видачею та поверненням книг з використанням 'Фасаду'. """
    def __init__(self, db):
        self.db = db
        self.observers = []

    def register_observer(self, observer):
        """ Реєстрація спостерігача. """
        self.observers.append(observer)

    def notify_observers(self, message):
        """ Повідомлення спостерігачів про подію. """
        for observer in self.observers:
            observer.update(message)

    def return_book(self, user_id, title):
        """ Повернення книги з повідомленням спостерігачам. """
        book_id = self.db.query('SELECT id FROM books WHERE title = ?', (title,))
        if book_id:
            book_id = book_id[0][0]
            checkout = self.db.query('SELECT due_date FROM checkouts WHERE user_id = ? AND book_id = ?', (user_id, book_id))
            if checkout:
                due_date = checkout[0][0]
                self.db.execute('DELETE FROM checkouts WHERE user_id = ? AND book_id = ?', (user_id, book_id))
                self.notify_observers(f"Книга '{title}' повернута користувачем {user_id}.")
                return "Книга повернута."
            self.notify_observers(f"Спроба повернути книгу '{title}', яка не була видана користувачу {user_id}.")
            return "Книга не була видана цьому користувачу"
        self.notify_observers(f"Спроба повернути неіснуючу книгу '{title}'.")
        return "Книга не знайдена."
