class EventObserver:
    """ Спостерігач за подіями. """
    def update(self, message):
        print(message)

class EventManager:
    """ Управління подіями з використанням патерну 'Фасад'. """
    def __init__(self, db):
        self.db = db
        self.observers = []

    def register_observer(self, observer):
        """ Реєстрація спостерігача. """
        self.observers.append(observer)

    def notify_observers(self, message):
        """ Повідомлення всіх спостерігачів про подію. """
        for observer in self.observers:
            observer.update(message)

    def create_event(self, event_name, event_date):
        """ Створення події із сповіщенням спостерігачів. """
        self.db.execute('''
            INSERT INTO events (name, date) VALUES (?, ?)
        ''', (event_name, event_date))
        message = f"Захід '{event_name}' заплановано на {event_date}."
        print(message)
        self.notify_observers(message)
