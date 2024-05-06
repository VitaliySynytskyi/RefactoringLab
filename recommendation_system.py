class RecommendationStrategy:
    def recommend(self, db, user_id):
        raise NotImplementedError("Each strategy must implement the recommend method.")

class AuthorBasedStrategy(RecommendationStrategy):
    def recommend(self, db, user_id):
        authors = db.query('''
            SELECT DISTINCT author FROM books 
            INNER JOIN preferences ON books.id = preferences.book_id
            WHERE preferences.user_id = ?
        ''', (user_id,))
        recommendations = []
        for author in authors:
            books = db.query('''
                SELECT DISTINCT title FROM books WHERE author = ? AND id NOT IN (
                    SELECT book_id FROM preferences WHERE user_id = ?
                )
            ''', (author[0], user_id))
            recommendations.extend(book[0] for book in books)
        return recommendations

class RecommendationSystem:
    def __init__(self, db, strategy=None):
        self.db = db
        self.strategy = strategy if strategy else AuthorBasedStrategy()

    def set_strategy(self, strategy):
        self.strategy = strategy

    def recommend_books(self, user_id):
        return self.strategy.recommend(self.db, user_id)

    def add_preference(self, user_id, book_id):
        self.db.execute('INSERT INTO preferences (user_id, book_id) VALUES (?, ?)', (user_id, book_id))
