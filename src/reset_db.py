import os
import sys
from pathlib import Path
from database.db_operations import NewsDatabase
from database.init_db import init_database
from main import crawl_and_save

def reset_database(start_new_crawl: bool = False) -> None:
    """
    Reset the database and optionally start a new crawl
    
    Args:
        start_new_crawl (bool): Whether to start a new crawl after reset
    """
    print("Starting database reset...")
    
    # Initialize database connection
    db = NewsDatabase()
    
    # Clear all data
    if db.clear_database():
        print("Successfully cleared all data from database")
    else:
        print("Error clearing database")
        sys.exit(1)
    
    # Reinitialize database structure and default categories
    init_database()
    print("Database structure reinitialized")
    
    if start_new_crawl:
        print("\nStarting new crawl...")
        crawl_and_save()
    
    print("\nDatabase reset completed!")

if __name__ == "__main__":
    # Check if we should start a new crawl after reset
    start_new_crawl = "--crawl" in sys.argv
    reset_database(start_new_crawl) 