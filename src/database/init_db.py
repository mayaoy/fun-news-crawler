import sqlite3
import os
from pathlib import Path

def init_database():
    # Create database directory if it doesn't exist
    db_dir = Path("data")
    db_dir.mkdir(exist_ok=True)
    
    # Connect to SQLite database (creates it if it doesn't exist)
    db_path = db_dir / "news.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create news table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL,
        category TEXT,
        content TEXT,
        published_date DATETIME,
        crawled_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create categories table for future use
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        url_path TEXT NOT NULL,
        category_type TEXT NOT NULL  -- 'main' or 'news'
    )
    ''')

    # Insert default categories
    main_categories = [
        ('Home', '/', 'main'),
        ('News', '/news', 'main'),
        ('Sport', '/sport', 'main'),
        ('Business', '/business', 'main'),
        ('Innovation', '/innovation', 'main'),
        ('Culture', '/culture', 'main'),
        ('Travel', '/travel', 'main'),
        ('Earth', '/future-planet', 'main')
    ]
    
    news_categories = [
        ('Israel-Gaza War', '/news/topics/c2vdnvdg6xxt', 'news'),
        ('War in Ukraine', '/news/war-in-ukraine', 'news'),
        ('US & Canada', '/news/us-canada', 'news'),
        ('UK', '/news/uk', 'news'),
        ('Africa', '/news/world/africa', 'news'),
        ('Asia', '/news/world/asia', 'news'),
        ('Australia', '/news/world/australia', 'news'),
        ('Europe', '/news/world/europe', 'news'),
        ('Latin America', '/news/world/latin_america', 'news'),
        ('Middle East', '/news/world/middle_east', 'news'),
        ('BBC InDepth', '/news/bbcindepth', 'news'),
        ('BBC Verify', '/news/bbcverify', 'news')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO categories (name, url_path, category_type) VALUES (?, ?, ?)',
        main_categories + news_categories
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!") 