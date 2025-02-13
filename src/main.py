import os
import schedule
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from crawler.bbc_crawler import BBCNewsCrawler
from database.db_operations import NewsDatabase
from database.init_db import init_database

# Load environment variables
load_dotenv()

def crawl_and_save():
    """
    Main function to crawl news and save to database
    """
    print(f"\nStarting crawl at {datetime.now()}")
    
    # Initialize crawler
    crawler = BBCNewsCrawler()
    
    total_found = 0
    total_saved = 0
    total_skipped = 0
    
    # Crawl category by category
    for category, url in crawler.get_category_urls().items():
        print(f"\nCrawling {category} category...")
        stats = crawler.crawl_category(category)
        
        total_found += stats['total']
        total_saved += stats['saved']
        total_skipped += stats['skipped']
    
    print(f"\nCrawl completed at {datetime.now()}")
    print(f"Total: Found {total_found} articles, Saved {total_saved} new articles, Skipped {total_skipped} articles")

def main():
    """
    Main function to run the crawler with scheduling
    """
    # Initialize database
    print("Initializing database...")
    init_database()
    print("Database initialized successfully")
    
    # Get crawl interval from environment variable (default: 10 minutes)
    crawl_interval = int(os.getenv("CRAWL_INTERVAL", 10))
    
    print(f"BBC News Crawler started. Will crawl every {crawl_interval} minutes.")
    
    # Run first crawl immediately
    print("\nStarting initial crawl...")
    crawl_and_save()
    
    # Schedule the crawling job
    schedule.every(crawl_interval).minutes.do(crawl_and_save)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 