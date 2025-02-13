import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class NewsDatabase:
    def __init__(self, db_path: str = "data/news.db"):
        self.db_path = Path(db_path)

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def clear_database(self) -> bool:
        """
        Clear all data from the database tables while keeping the structure.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Clear the news table
                cursor.execute('DELETE FROM news')
                # Clear the categories table
                cursor.execute('DELETE FROM categories')
                # Reset the auto-increment counters
                cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("news", "categories")')
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False

    def save_news(self, news_data: Dict) -> bool:
        """
        Save a news article to the database
        
        Args:
            news_data (Dict): Dictionary containing news data with keys:
                - title: str
                - url: str
                - category: str
                - content: str
                - published_date: str (ISO format)
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT OR IGNORE INTO news 
                (title, url, category, content, published_date)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    news_data['title'],
                    news_data['url'],
                    news_data['category'],
                    news_data['content'],
                    news_data['published_date']
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error saving news: {e}")
            return False

    def get_news_by_category(self, category: str) -> List[Dict]:
        """
        Retrieve news articles by category
        
        Args:
            category (str): Category name
        
        Returns:
            List[Dict]: List of news articles
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, title, url, category, content, published_date, crawled_date
            FROM news
            WHERE category = ?
            ORDER BY published_date DESC
            ''', (category,))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_recent_news(self, limit: int = 10) -> List[Dict]:
        """
        Retrieve most recent news articles
        
        Args:
            limit (int): Maximum number of articles to retrieve
        
        Returns:
            List[Dict]: List of news articles
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, title, url, category, content, published_date, crawled_date
            FROM news
            ORDER BY published_date DESC
            LIMIT ?
            ''', (limit,))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def url_exists(self, url: str) -> bool:
        """
        Check if a URL already exists in the database
        
        Args:
            url (str): URL to check
        
        Returns:
            bool: True if URL exists, False otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM news WHERE url = ?', (url,))
            return cursor.fetchone() is not None 