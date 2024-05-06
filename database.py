import sqlite3
import logging

class Database:
    def __init__(self, db_file='library.db'):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.connection.row_factory = sqlite3.Row  # Optional: This enables column access by name
        self.cursor = self.connection.cursor()
        self.setup()

    def setup(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL DEFAULT 'regular'
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (book_id) REFERENCES books (id)
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS checkouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    due_date DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS staff (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'staff'
                );
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"An error occurred during table setup: {e}")

    def query(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Failed to execute query: {sql}, error: {e}")
            return []

    def execute(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            logging.error(f"Failed to execute command: {sql}, error: {e}")

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            logging.error(f"Failed to close the database connection: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
