import sqlite3

def initialize_db():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES category (id)
    )''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_name ON Category(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_item_name ON Item(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_item_category_id ON Item(category_id)')
    
    connection.commit()
    connection.close()