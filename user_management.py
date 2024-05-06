class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def privileges(self):
        return "Basic privileges"

class RegularUser(User):
    def privileges(self):
        return super().privileges() + " - Can borrow up to 2 books"

class PremiumUser(User):
    def privileges(self):
        return super().privileges() + " - Can borrow up to 5 books and access premium content"

class UserObserver:
    def update(self, message):
        print(message)

class UserManager:
    def __init__(self, db):
        self.db = db
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def create_user(self, user_id, name, type):
        if type == 'premium':
            return PremiumUser(user_id, name)
        else:
            return RegularUser(user_id, name)

    def add_user(self, user_id, name, type='regular'):
        user = self.db.query('SELECT id FROM users WHERE id = ?', (user_id,))
        if user:
            self.notify_observers(f"Користувач з ID {user_id} вже існує.")
        else:
            user = self.create_user(user_id, name, type)
            self.db.execute('''
                INSERT INTO users (id, name, type) VALUES (?, ?, ?)
            ''', (user.user_id, user.name, type))
            self.notify_observers(f"Користувач {user.name} доданий з привілеями: {user.privileges()}")
