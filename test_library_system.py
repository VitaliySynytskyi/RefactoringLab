import unittest
from unittest.mock import MagicMock
from library import Library
from user_management import UserManager
from event_management import EventManager
from staff_management import StaffManager
from recommendation_system import RecommendationSystem

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        # Mock the database connection
        self.db = MagicMock()
        self.library = Library(self.db)
        self.user_manager = UserManager(self.db)
        self.event_manager = EventManager(self.db)
        self.staff_manager = StaffManager(self.db)
        self.recommendation_system = RecommendationSystem(self.db)

    def test_add_book(self):
        self.library.add_book("Test Book", "Test Author")
        self.db.execute.assert_called_once_with('''
            INSERT INTO books (title, author) VALUES (?, ?)
        ''', ("Test Book", "Test Author"))

    def test_checkout_book_not_found(self):
        self.db.query.return_value = []
        result = self.library.checkout_book(1, "Nonexistent Book")
        self.assertEqual(result, "Ця книга недоступна")

    def test_return_book_not_checked_out(self):
        self.db.query.side_effect = [[(1,)], []]  # First call finds the book, second finds no checkout
        result = self.library.return_book(1, "Some Book")
        self.assertEqual(result, "Книга не була видана цьому користувачу")

    def test_create_event(self):
        self.event_manager.create_event("Test Event", "2024-06-20")
        self.db.execute.assert_called_with('''
            INSERT INTO events (name, date) VALUES (?, ?)
        ''', ("Test Event", "2024-06-20"))

    def test_add_user(self):
        self.db.query.return_value = []  # Ensure the user does not exist
        self.user_manager.add_user(1, "Test User", 'regular')
        self.db.execute.assert_called()
        args, kwargs = self.db.execute.call_args
        self.assertIn('INSERT INTO users (id, name, type) VALUES', args[0])
        self.assertEqual(args[1], (1, "Test User", 'regular'))  # Corrected to access positional arguments

    def test_add_existing_user(self):
        self.db.query.return_value = [(1,)]  # User already exists
        result = self.user_manager.add_user(1, "Test User")
        self.assertEqual(result, None)

    def test_add_staff_member(self):
        self.db.query.return_value = []  # Ensure the staff does not exist
        # Specify the role explicitly if you expect 'staff'
        self.staff_manager.add_staff_member(101, "Test Staff", "staff")
        self.db.execute.assert_called()
        args, kwargs = self.db.execute.call_args
        self.assertIn('INSERT INTO staff (id, name, role) VALUES', args[0])
        self.assertEqual(args[1], (101, 'Test Staff', 'staff'))

    def test_recommend_books(self):
        self.db.query.side_effect = [
            [("Test Author",)],  # Found author
            [("Test Book",)]     # Recommend this book
        ]
        result = self.recommendation_system.recommend_books(1)
        self.assertIn("Test Book", result)

    def test_event_notification(self):
        observer = MagicMock()
        self.event_manager.register_observer(observer)
        self.event_manager.create_event("Another Event", "2025-01-01")
        observer.update.assert_called_with("Захід 'Another Event' заплановано на 2025-01-01.")

    def test_return_book_with_fine(self):
        self.db.query.side_effect = [
            [(1,)],  # First call finds the book
            [("2024-01-01 00:00:00.000000", 1)]  # Second call finds the checkout (include user_id)
        ]
        result = self.library.return_book(1, "Late Book")
        self.assertTrue("штрафом" in result)


if __name__ == '__main__':
    unittest.main()
