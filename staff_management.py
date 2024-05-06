class StaffMember:
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name

    def responsibilities(self):
        return "General duties"

class Librarian(StaffMember):
    def responsibilities(self):
        return super().responsibilities() + ", Managing book checkouts"

class Administrator(StaffMember):
    def responsibilities(self):
        return super().responsibilities() + ", Managing staff and organizing events"

class StaffObserver:
    def update(self, message):
        print(message)

class StaffManager:
    def __init__(self, db):
        self.db = db
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def create_staff_member(self, staff_id, name, type):
        if type == 'librarian':
            return Librarian(staff_id, name)
        elif type == 'administrator':
            return Administrator(staff_id, name)
        else:
            return StaffMember(staff_id, name)

    def add_staff_member(self, staff_id, name, type="general"):
        exists = self.db.query('SELECT id FROM staff WHERE id = ?', (staff_id,))
        if exists:
            self.notify_observers(f"Співробітник з ID {staff_id} вже існує.")
        else:
            staff_member = self.create_staff_member(staff_id, name, type)
            self.db.execute('''
                INSERT INTO staff (id, name, role) VALUES (?, ?, ?)
            ''', (staff_member.staff_id, staff_member.name, type))
            self.notify_observers(f"Співробітник {staff_member.name} доданий з обов'язками: {staff_member.responsibilities()}")
