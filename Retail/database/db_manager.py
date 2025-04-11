import sqlite3

class DBManager:
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                quantity INTEGER,
                sale_date TEXT
            )
        ''')
        # Create inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                product TEXT PRIMARY KEY,
                quantity INTEGER
            )
        ''')
        # Create prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                product TEXT PRIMARY KEY,
                price REAL
            )
        ''')
        # Create customer_feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                feedback TEXT,
                created_at TEXT
            )
        ''')
        self.conn.commit()

    def query(self, sql, params=None):
        params = params or ()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def execute(self, sql, params=None):
        params = params or ()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.lastrowid

if __name__ == '__main__':
    db = DBManager()
    print("Database initialized.")
