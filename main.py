from database import Database
from library import Library
from user_management import UserManager
from event_management import EventManager
from staff_management import StaffManager
from recommendation_system import RecommendationSystem

def main():
    # Initialize the database and modules
    db = Database()

    library = Library(db)
    user_manager = UserManager(db)
    event_manager = EventManager(db)
    staff_manager = StaffManager(db)
    recommendation_system = RecommendationSystem(db)

    # Add users
    user_manager.add_user(1, "Oleksandr")
    user_manager.add_user(2, "Maria")
    user_manager.add_user(3, "Ivan")

    # Add books
    books = [
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
        ("Harry Potter and the Chamber of Secrets", "J.K. Rowling"),
        ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling"),
        ("Harry Potter and the Goblet of Fire", "J.K. Rowling"),
        ("Harry Potter and the Order of the Phoenix", "J.K. Rowling"),
        ("Harry Potter and the Half-Blood Prince", "J.K. Rowling"),
        ("Harry Potter and the Deathly Hallows", "J.K. Rowling"),
        ("The Shadow of the Wind", "Carlos Ruiz Zafón"),
        ("The Little Prince", "Antoine de Saint-Exupéry"),
        ("Sherlock Holmes", "Arthur Conan Doyle"),
        ("Three Comrades", "Erich Maria Remarque"),
        ("Hetmanshchina", "Yuriy Yanovskiy"),
        ("Do the Oxen Low When the Manger Is Full?", "Panas Myrny"),
        ("Chasing Two Hares", "Mykola Kulish"),
        ("The City", "Valeriy Shevchuk"),
        ("Voroshilovgrad", "Serhiy Zhadan"),
        ("Death of an Outsider", "Alexander Kuprin"),
        ("The Storm", "Olha Kobylianska"),
        ("On the Road to the Edge", "Ostap Vyshnya")
    ]

    for title, author in books:
        library.add_book(title, author)

    # Checkout books
    print(library.checkout_book(1, "Harry Potter and the Goblet of Fire"))
    print(library.checkout_book(3, "Voroshilovgrad"))

    # Return books
    print(library.return_book(1, "Harry Potter and the Goblet of Fire"))

    # Organize events
    event_manager.create_event("Author's Evening", "2024-06-15")
    event_manager.create_event("Lecture on American Literature", "2024-07-01")

    # Add staff members
    staff_manager.add_staff_member(101, "Viktoria")
    staff_manager.add_staff_member(102, "Maxim")

    # Add user preferences for books
    recommendation_system.add_preference(1, 5)  # User 1 prefers book with ID 5
    recommendation_system.add_preference(2, 11)  # User 2 prefers book with ID 11

    # Get recommendations for users
    print("Recommendations for User 1:", recommendation_system.recommend_books(1))
    print("Recommendations for User 2:", recommendation_system.recommend_books(2))

if __name__ == "__main__":
    main()
