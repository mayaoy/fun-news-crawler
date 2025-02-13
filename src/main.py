import os
import schedule
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from crawler.bbc_crawler import BBCNewsCrawler
from database.db_operations import NewsDatabase

# Load environment variables
load_dotenv()

def setup():
    """Initialize the database and create necessary directories"""
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Initialize database
    from database.init_db import init_database
    init_database()

def crawl_and_save():
    """
    Main function to crawl news and save to database
    """
    print(f"\nStarting crawl at {datetime.now()}")
    
    # Initialize crawler and database
    crawler = BBCNewsCrawler()
    db = NewsDatabase()
    
    # Crawl all categories
    articles = crawler.crawl_all_categories()
    
    # Save articles to database
    saved_count = 0
    for article in articles:
        if db.save_news(article):
            saved_count += 1
    
    print(f"Crawl completed. Saved {saved_count} new articles out of {len(articles)} found.")

def main():
    """
    Main function to run the crawler with scheduling
    """
    # Setup database and directories
    setup()
    
    # Get crawl interval from environment variable (default: 10 minutes)
    crawl_interval = int(os.getenv("CRAWL_INTERVAL", 10))
    
    print(f"BBC News Crawler started. Will crawl every {crawl_interval} minutes.")
    
    # Schedule the crawling job
    schedule.every(crawl_interval).minutes.do(crawl_and_save)
    
    # Run first crawl immediately
    crawl_and_save()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 